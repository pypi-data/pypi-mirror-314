use std::collections::HashSet;

use crate::error::FactorGraphStoreError;
use crate::loader::arena::{NodeArena, FACTORS_FN, VARIABLES_FN, VERSION_KEY};
use crate::types::{Factor, Variable, VFG};
use itertools::Itertools;
use persist::Persist;
use rkyv::api::low::deserialize;

pub(crate) mod arena;
pub(crate) mod persist;

const VARIABLE_SEPARATOR: &str = "\x1F";
pub(crate) const VFG_VERSION: &str = "0.3.0";

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Default, Debug, PartialEq)]
pub(crate) struct GraphNode<F> {
    input: Vec<String>,
    contents: F,
}

/// This LOADS a graph INTO the datastore
pub(crate) fn load_graph(source: VFG, path: &str) -> Result<NodeArena, FactorGraphStoreError> {
    // set version
    let version = Persist::new(path, "version")?;
    let mut transaction = version.open_write()?;
    debug_assert!(
        source.version.as_str() == "0.3.0",
        "check that version matches expected"
    );
    version.insert(&mut transaction, VERSION_KEY, source.version.try_into()?)?;
    drop(transaction);

    // create variables
    let variables = Persist::new(path, VARIABLES_FN)?;
    let mut transaction = variables.open_write()?;
    for var in source.variables.into_iter() {
        variables.insert(&mut transaction, var.0.as_bytes(), var.1)?;
    }
    drop(transaction);

    let factors = Persist::new(path, FACTORS_FN)?;
    let mut transaction = factors.open_write()?;
    for factor in source.factors.into_iter() {
        let index_var = factor.variables.iter().join(VARIABLE_SEPARATOR);
        let inputs = factor.variables.to_vec();
        let tgt_node = GraphNode {
            input: inputs,
            contents: factor,
        };
        factors.insert(&mut transaction, index_var.as_bytes(), tgt_node)?;
    }
    drop(transaction);

    Ok(NodeArena::new(
        path.to_string().into_boxed_str(),
        version,
        factors,
        variables,
    ))
}

fn variable_mapping(
    arena: &NodeArena,
) -> Result<std::collections::HashMap<String, Variable>, FactorGraphStoreError> {
    let var_vals_transaction = arena.variables.open_read()?;
    arena
        .variables
        .iter(&var_vals_transaction)
        .map(|(k, v)| {
            let k = String::from_utf8(k.to_vec()).unwrap();
            let vals = deserialize::<Variable, rkyv::rancor::Error>(v)?;
            Ok((k, vals))
        })
        .collect()
}

fn variable_mapping_for(
    arena: &NodeArena,
    vars: &[String],
) -> Result<std::collections::HashMap<String, Variable>, FactorGraphStoreError> {
    let variable_mapping_transaction = arena.factors.open_read()?;
    let var_vals_transaction = arena.variables.open_read()?;
    arena
        .factors
        .iter(&variable_mapping_transaction)
        .filter_map(|(k, _)| {
            String::from_utf8(k.to_vec())
                .ok()
                .filter(|k| vars.iter().any(|part| k.contains(part)))
        })
        .flat_map(|k| {
            k.split(VARIABLE_SEPARATOR)
                .map(|s| s.to_string())
                .collect::<Vec<String>>()
        })
        .map(|k| {
            let vals = arena.variables.get(&var_vals_transaction, k.as_bytes());
            match vals {
                Some(vals) => {
                    let vals = deserialize::<Variable, rkyv::rancor::Error>(vals)?;
                    Ok((k, vals))
                }
                None => Ok((k, Variable::default())),
            }
        })
        .collect()
}

/// Finds all factor keys in the arena that contain the given variable
fn find_factor_keys_for_var(arena: &NodeArena, var: &str) -> Result<Vec<String>, FactorGraphStoreError> {
    {
        let transaction = arena.factors.open_read()?;

        let vec = arena
            .factors
            .iter(&transaction)
            .filter_map(|(key, _)| {
                String::from_utf8(key.to_vec())
                    .ok()
                    .filter(|k| k.split(VARIABLE_SEPARATOR).any(|part| part == var))
            })
            .collect();
        Ok(vec)
    }
}

/// Loads the entire graph from the arena
/// Returns a VFG containing the entire graph.
/// Returns an error if there is an error retrieving the graph.
pub(crate) fn retrieve_graph(arena: &NodeArena) -> Result<Option<VFG>, FactorGraphStoreError> {
    let mut factors = Vec::new();
    let transaction = arena.factors.open_read()?;

    for (_, node) in arena.factors.iter(&transaction) {
        factors.push(
            rkyv::deserialize::<GraphNode<Factor>, rkyv::rancor::Error>(node)
                .unwrap()
                .contents,
        );
    }

    let variables = variable_mapping(arena)?;

    Ok(Some(VFG {
        version: VFG_VERSION.to_string(),
        factors,
        variables,
    }))
}

/// Loads the subgraph that produces the output for a given variable
/// Returns an Option<VFG> where the VFG is the subgraph that produces the output for the given variable,
/// or None if the variable is not found in the graph.
/// Returns an error if there is an error retrieving the graph.
pub(crate) fn retrieve_subgraph(
    arena: &NodeArena,
    vars: &[String],
) -> Result<Option<VFG>, FactorGraphStoreError> {
    // convert from user variable to internal variable
    let mut stack = vars.to_vec();
    // tree traversal
    let mut visited = HashSet::new();
    let mut factors = Vec::new();
    let transaction = arena.factors.open_read()?;
    while let Some(var_ref) = stack.pop() {
        let factor_keys = find_factor_keys_for_var(arena, &var_ref)?;
        for key in factor_keys {
            if visited.contains(&key) {
                continue;
            }
            visited.insert(key.clone());
            if let Some(node) = arena.factors.get(&transaction, key.as_bytes()) {
                factors.push(
                    rkyv::deserialize::<GraphNode<Factor>, rkyv::rancor::Error>(node)
                        .unwrap()
                        .contents,
                );
                stack.extend(
                    node.input
                        .iter()
                        .map(|s| rkyv::deserialize::<String, rkyv::rancor::Error>(s).unwrap()),
                );
            } else {
                return Ok(None);
            }
        }
    }

    let variables = variable_mapping_for(arena, vars)?;

    if variables.is_empty() && factors.is_empty() {
        return Ok(None);
    }

    Ok(Some(VFG {
        version: VFG_VERSION.to_string(),
        factors,
        variables,
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_util::generate_test_vfg;

    /// Description: Tests if we can oad a graph into the NodeArena
    /// Objectives: Loading a graph from the "wire" format results in a change to the
    /// factor graph store
    #[test]
    fn test_load_graph() {
        let wire_graph = generate_test_vfg();
        let arena = load_graph(wire_graph, "factor_graph_data/test_load_graph").expect("can load graph");
        let variable_mapping_transaction = arena.factors.open_read().unwrap();
        let var_vals_transaction = arena.variables.open_read().unwrap();
        assert_eq!(arena.factors.len(&variable_mapping_transaction).unwrap(), 3);
        assert_eq!(arena.variables.len(&var_vals_transaction).unwrap(), 3);
        drop(var_vals_transaction);
        drop(variable_mapping_transaction);
        drop(arena);
        std::fs::remove_dir_all("factor_graph_data/test_load_graph").unwrap();
    }

    /// Description: Tests if we can load a graph with empty values
    /// Objectives: Loading a graph with empty values should not result in an error
    /// Regression test for GPAI-155.
    #[test]
    #[cfg(feature = "json")]
    fn test_load_graph_var_empty_values() {
        let wire_graph = serde_json::from_value(serde_json::json!({
            "factors": [
              {
                "distribution": "categorical",
                "values": [],
                "variables": [
                  "cloudy"
                ]
              }
            ],
            "variables": {
              "cloudy": {
                "elements": [
                  "no",
                  "yes"
                ]
              }
            },
            "version": "0.3.0"
        })).unwrap();
        let test_fn = format!("factor_graph_data/test_{}", nanoid::nanoid!());
        {
            let arena = load_graph(wire_graph, &test_fn).expect("can load graph");
            let variable_mapping_transaction = arena.factors.open_read().unwrap();
            let var_vals_transaction = arena.variables.open_read().unwrap();
            assert_eq!(arena.factors.len(&variable_mapping_transaction).unwrap(), 1);
            assert_eq!(arena.variables.len(&var_vals_transaction).unwrap(), 1);
            let vfg = retrieve_graph(&arena).unwrap().unwrap();
            assert_eq!(vfg.variables.len(), 1);
            assert_eq!(vfg.factors.len(), 1);
            let _json = serde_json::to_value(vfg).expect("Can reserialize");
        }

        std::fs::remove_dir_all(&test_fn).unwrap();
    }

    /// Description: Tests if we can fetch a subgraph from the arena
    /// Objectives: We can retrieve a subgraph from the arena
    #[test]
    fn test_retrieve_subgraph() {
        let wire_graph = generate_test_vfg();
        let arena = load_graph(wire_graph, "factor_graph_data/test_retrieve_subgraph").expect("can load graph");
        let deps = retrieve_subgraph(&arena, &["rain".to_string()]).expect("can retrieve subgraph");
        assert!(deps.is_some());
        drop(arena);
        std::fs::remove_dir_all("factor_graph_data/test_retrieve_subgraph").unwrap();
    }

    #[test]
    fn test_retrieve_subgraph_multiple() {
        let wire_graph = generate_test_vfg();
        let arena =
            load_graph(wire_graph, "factor_graph_data/test_retrieve_subgraph_multiple").expect("can load graph");
        let deps = retrieve_subgraph(&arena, &["rain".to_string(), "cloudy".to_string()])
            .expect("can retrieve subgraph");
        assert!(deps.is_some());
        drop(arena);
        std::fs::remove_dir_all("factor_graph_data/test_retrieve_subgraph_multiple").unwrap();
    }
}
