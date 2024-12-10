use crate::error::FactorGraphStoreError;
use crate::loader::arena::{Version, FACTORS_FN, VARIABLES_FN, VERSION_FN, VERSION_KEY};
use crate::loader::persist::Persist;
use crate::loader::GraphNode;
use crate::types::Variable;

const V0_FACTORS_FN: &str = "variable_mapping";
const V0_VARIABLES_FN: &str = "var_vals";
const V1_FACTORS_FN: &str = FACTORS_FN;
const V1_VARIABLES_FN: &str = VARIABLES_FN;

pub(crate) fn handle_db_migration(path: &str) -> Result<Persist<Version>, FactorGraphStoreError> {
    let version = Persist::new(path, VERSION_FN)?;
    let mut transaction = version.open_write()?;

    // match here for later, additional versions we care about
    match version.get(&transaction, VERSION_KEY).map(|x| {
        rkyv::deserialize::<Version, rkyv::rancor::Error>(x)
    }).transpose() {
        Err(e) => return Err(e.into()),
        Ok(None) | Ok(Some(Version::Format0)) => {
            convert_v0_to_v1(path)?
        },
        Ok(Some(Version::Format1)) => {},
    }
    // update to the current version
    version.insert(&mut transaction, VERSION_KEY, Version::Format1)?;
    drop(transaction);
    Ok(version)
}

/// Version writing is handled by the caller. If this is confusing, feel free to move it here.
fn convert_v0_to_v1(path: &str) -> Result<(), FactorGraphStoreError> {
    use crate::types::v0_2_0::Factor as FactorV2;
    use crate::types::v0_3_0::Factor as FactorV3;

    // update the variable mapping
    let factors: Persist<GraphNode<FactorV2>> = Persist::new(path, V0_FACTORS_FN)?;
    let otx = factors.open_read()?;
    let converted_factors: Vec<(&[u8], GraphNode<FactorV3>)> = factors.iter(&otx).map(|(k, v)| -> Result<(&[u8], GraphNode<FactorV3>), rkyv::rancor::Error> {
        let old_factor = rkyv::deserialize::<GraphNode<FactorV2>, rkyv::rancor::Error>(v)?;
        Ok((k, GraphNode {
            input: old_factor.input,
            contents: old_factor.contents.into(),
        }))
    }).collect::<Result<Vec<(&[u8], GraphNode<FactorV3>)>, rkyv::rancor::Error>>()?;

    let new_factors: Persist<GraphNode<FactorV3>> = Persist::new(path, V1_FACTORS_FN)?;
    let mut tx = new_factors.open_write()?;
    for (key, value) in converted_factors {
        new_factors.insert(&mut tx, key, value)?;
    }
    drop(tx);

    // only delete AFTER new version has been written back!
    drop(otx);
    factors.delete()?;

    // update the variable metadata
    let old_variables: Persist<Vec<String>> = Persist::new(path, V0_VARIABLES_FN)?;
    let otx = old_variables.open_write()?;
    let converted_variables = old_variables.iter(&otx).map(|(k, v)| {
        let old_var = rkyv::deserialize::<Vec<String>, rkyv::rancor::Error>(v)?;
        Ok((k, old_var.into()))
    }).collect::<Result<Vec<(&[u8], Variable)>, rkyv::rancor::Error>>()?;

    let new_factors: Persist<Variable> = Persist::new(path, V1_VARIABLES_FN)?;
    let mut tx = new_factors.open_write()?;
    for (key, value) in converted_variables {
        new_factors.insert(&mut tx, key, value)?;
    }
    drop(tx);
    // only delete AFTER new version has been written back!
    drop(otx);
    old_variables.delete()?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::error::FactorGraphStoreError;
    use crate::loader::arena::{Version, VERSION_FN, VERSION_KEY};
    use crate::loader::arena::migration::{V0_VARIABLES_FN, V0_FACTORS_FN};
    use crate::loader::persist::Persist;

    #[test]
    fn test_migration_from_empty() {
        let path = format!("factor_graph_data/test_db_{}", nanoid::nanoid!());
        let version = super::handle_db_migration(&path).expect("can migrate database");

        // manual drop to allow deletion on windows
        drop(version);
        std::fs::remove_dir_all(path).expect("can clean up");
    }


    fn create_v0_database() -> Result<String, FactorGraphStoreError> {
        use crate::types::v0_2_0::Factor as FactorV2;
        use crate::types::v0_2_0::ProbabilityDistribution as ProbabilityDistributionV2;
        use crate::types::v0_2_0::Values as ValuesV2;

        let path = format!("factor_graph_data/test_db_{}", nanoid::nanoid!());

        // set up variables...
        let variables = Persist::new(&path, V0_VARIABLES_FN)?;
        let mut vtx = variables.open_write()?;
        variables.insert(&mut vtx, "rain".as_bytes(), vec!["yes".to_string(), "no".to_string()])?;
        drop(vtx);

        // nodes...
        let nodes = Persist::new(&path, V0_FACTORS_FN)?;
        let mut ntx = nodes.open_write()?;
        nodes.insert(&mut ntx, "rain".as_bytes(), crate::loader::GraphNode {
            input: vec!["rain".into()],
            contents: FactorV2 {
                distribution: ProbabilityDistributionV2::Categorical,
                variables: vec!["rain".into()],
                values: ValuesV2 {
                    strides: vec![2],
                    values: vec![0.2, 0.8],
                },
                role: None,
            },
        })?;
        drop(ntx);

        // and version.
        let version = Persist::new(&path, VERSION_FN)?;
        let mut vtx = version.open_write()?;
        version.insert(&mut vtx, VERSION_KEY, Version::Format0)?;
        drop(vtx);

        Ok(path)
    }

    #[test]
    fn test_migration() {
        let path = create_v0_database().expect("can create test database");
        let version = super::handle_db_migration(&path).expect("can migrate database");
        let rtx = version.open_read().expect("can open read transaction");
        let new_version_archived = version.get(&rtx, VERSION_KEY).expect("can read version");
        let new_version = rkyv::deserialize::<Version, rkyv::rancor::Error>(new_version_archived).expect("can deserialize version");
        assert_eq!(new_version, Version::Format1, "version moved to format 1");

        // manual drop to allow deletion on windows
        drop(rtx);
        version.delete().expect("Can delete backing file");
        std::fs::remove_dir_all(path).expect("can clean up");
    }
}
