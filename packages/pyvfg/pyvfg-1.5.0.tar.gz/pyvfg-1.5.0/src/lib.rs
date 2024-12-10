use std::sync::{Arc, OnceState};
use std::sync::Once;
use telemetry_rust::trace::init_tracer;
use tracing::{error, info, instrument};
use tracing_subscriber::layer::SubscriberExt;
use tracing_subscriber::Layer;
use tracing_subscriber::{EnvFilter, Registry};

pub mod error;
pub(crate) mod loader;
#[cfg(feature = "python")]
pub mod python;
#[cfg(any(test, feature = "bench"))]
pub mod test_util;
pub mod types;
pub mod validation;

use crate::error::FactorGraphStoreError;
use crate::loader::arena::{FACTORS_FN, VARIABLES_FN};
use crate::loader::persist::Persist;
use crate::types::VFG;
use loader::arena::NodeArena;

static INIT: Once = Once::new();

pub struct FactorGraphStore {
    arena: NodeArena,
    #[allow(dead_code)]
    rt: Arc<tokio::runtime::Runtime>,
}

impl FactorGraphStore {
    #[instrument(name = "new")]
    pub fn new(path: &str) -> Result<Self, FactorGraphStoreError> {
        info!("Creating FactorGraphStore at path: {}", path);
        let path_owned = path.to_string().into_boxed_str();

        let version = loader::arena::migration::handle_db_migration(path)?;

        // Initialize tracing for the factor graph store
        let rt = tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .build()
            .unwrap();
        rt.spawn(async {
            FactorGraphStore::init_tracing();
        });

        Ok(FactorGraphStore {
            arena: NodeArena {
                path: path_owned,
                version,
                factors: Persist::new(path, FACTORS_FN)?,
                variables: Persist::new(path, VARIABLES_FN)?,
            },
            rt: Arc::new(rt),
        })
    }

    /**
     * public interface begins here
     */
    #[instrument(name = "get_subgraph_from", skip(self))]
    pub fn get_subgraph_from(
        &self,
        variable_name: &[String],
    ) -> Result<Option<VFG>, FactorGraphStoreError> {
        info!("Retrieving subgraph for variables: {:?}", variable_name);
        loader::retrieve_subgraph(&self.arena, variable_name).map_err(|err| {
            error!("Error retrieving subgraph: {:?}", err);
            err
        })
    }

    #[instrument(name = "get_graph", skip(self))]
    pub fn get_graph(&self) -> Result<Option<VFG>, FactorGraphStoreError> {
        info!("Retrieving the entire graph.");
        loader::retrieve_graph(&self.arena).map_err(|err| {
            error!("Error retrieving graph: {:?}", err);
            err
        })
    }

    #[instrument(name = "validate_graph", skip(self))]
    pub fn validate_graph(&self, vfg: VFG) -> Result<(), FactorGraphStoreError> {
        info!("Validating the entire graph.");
        validation::validate_vfg(&vfg).map_err(|err| {
            error!("Error validating graph: {:?}", err);
            FactorGraphStoreError::ValidationError(err)
        })
    }

    #[instrument(name = "replace_graph", skip(self))]
    pub fn replace_graph(&mut self, new_graph: VFG) -> Result<(), FactorGraphStoreError> {
        info!("checking graph for validation");
        self.validate_graph(new_graph.clone())?;
        info!("Replacing graph with new data.");
        let mut transaction = self.arena.factors.open_write()?;
        self.arena.factors.clear(&mut transaction)?;
        drop(transaction);
        let mut transaction = self.arena.variables.open_write()?;
        self.arena.variables.clear(&mut transaction)?;
        drop(transaction);
        let new_graph = loader::load_graph(new_graph, self.arena.path())?;
        self.arena = new_graph;
        Ok(())
    }

    // Initialize the tracing subscriber to collect log information.
    pub fn init_tracing() {
        // Set the RUST_LOG, if it hasn't been explicitly defined
        if std::env::var_os("RUST_LOG").is_none() {
            std::env::set_var("RUST_LOG", "genius-agent-factor-graph=debug")
        }

        INIT.call_once_force(|os: &OnceState| {
            fn init_telemetry() -> Result<(), Box<dyn std::error::Error>> {
                let stdout = tracing_subscriber::fmt::layer()
                    .with_writer(std::io::stdout)
                    .json()
                    .with_filter(EnvFilter::from_default_env());

                let tracer =
                    init_tracer("genius-agent-factor-graph")?;
                let telemetry = tracing_opentelemetry::layer()
                    .with_tracer(tracer)
                    .with_filter(EnvFilter::from_default_env());
                let subscriber = Registry::default().with(stdout).with(telemetry);
                tracing::subscriber::set_global_default(subscriber)?;
                Ok(())
            }

            let result = init_telemetry();
            match result {
                Ok(_) if os.is_poisoned() => {
                    error!("Initialization of telemetry failed AT LEAST ONCE due to poisoning! continue to examine");
                }
                Ok(_) => info!("Initialized telemetry"),
                Err(e) => println!("Initialization of telemetry failed: {:?}", e),
            }
        });
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    use crate::test_util::generate_test_vfg;
    use crate::types::Values;

    /// Description: End-to-end test of the `replace_graph` API function
    /// Objectives: Replace graph is called without error.
    ///
    /// This is the foundational test, used in other tests. Failures here
    /// will also cause failures elsewhere!
    #[test]
    fn test_replace_graph() {
        let mut fg = FactorGraphStore::new("factor_graph_data/test_replace_graph").unwrap();
        let new_graph = generate_test_vfg();
        assert!(fg.replace_graph(new_graph).is_ok());
        drop(fg);
        std::fs::remove_dir_all("factor_graph_data/test_replace_graph")
            .expect("can clean up after tests");
    }

    /// Description: End-to-end test of the `replace_graph` API function
    /// Objectives: Replace graph is called twice without error.
    /// Regression tests for GPFGS-52
    #[test]
    fn test_replace_graph_twice() {
        let mut fg = FactorGraphStore::new("factor_graph_data/test_replace_graph_twice").unwrap();
        let new_graph = generate_test_vfg();
        assert!(fg.replace_graph(new_graph).is_ok());

        let a_second_graph = generate_test_vfg();
        assert!(fg.replace_graph(a_second_graph).is_ok());

        drop(fg);
        std::fs::remove_dir_all("factor_graph_data/test_replace_graph_twice")
            .expect("can clean up after tests");
    }

    /// Description: Happy path test of the `validate_graph` API function
    /// Objectives: Validate graph is called without error.
    #[test]
    fn test_validate_graph() {
        let fg = FactorGraphStore::new("factor_graph_data/test_validate_graph").unwrap();
        let new_graph = generate_test_vfg();
        assert!(fg.validate_graph(new_graph).is_ok());
        drop(fg);
        std::fs::remove_dir_all("factor_graph_data/test_validate_graph")
            .expect("can clean up after tests");
    }

    #[test]
    fn test_validate_graph_failure() {
        let fg = FactorGraphStore::new("factor_graph_data/test_validate_graph_failure").unwrap();
        let mut new_graph = generate_test_vfg();
        new_graph.factors[0].values = Values {
            strides: vec![2, 3],  // change this to be a shape mismatch because normalization test is disabled
            values: vec![0.9, 0.2, 0.8, 0.1], // do some value flippy, for funsies
        };
        assert!(fg.validate_graph(new_graph).is_err());
        drop(fg);
        std::fs::remove_dir_all("factor_graph_data/test_validate_graph_failure")
            .expect("can clean up after tests");
    }

    /// Description: End-to-end test of the `get_graph` API function
    /// Objectives: `get_graph` is called without error; `get_graph` returns the replaced graph,
    ///             instead of the original graph
    #[test]
    fn test_get_graph() {
        let mut fg = FactorGraphStore::new("factor_graph_data/test_get_graph").unwrap();
        let new_graph = generate_test_vfg();
        fg.replace_graph(new_graph).expect("Can replace graph");
        let graph = fg.get_graph().expect("can load graph");
        assert!(graph.is_some());
        assert_eq!(graph.unwrap(), generate_test_vfg());
        drop(fg);
        std::fs::remove_dir_all("factor_graph_data/test_get_graph")
            .expect("can clean up after tests");
    }

    /// Description: End-to-end test of the `get_subgraph_from` function
    /// Objectives:
    ///  - We can get the subgraph from a single variable
    ///  - We can get the subgraph from a list of variables
    ///  - The subgraph returns all dependant nodes
    ///  - Subgraph retrieval retrieves a subgraph, not the entire graph
    ///  - Non-extant variables are ignored
    ///  - A query that contains only non-extant variables returns None
    #[test]
    fn test_get_subgraph_from() {
        let mut fg = FactorGraphStore::new("factor_graph_data/test_get_subgraph_from").unwrap();
        let new_graph = generate_test_vfg();
        fg.replace_graph(new_graph).expect("Can replace graph");

        let test_vfg = Some(generate_test_vfg());

        let subgraph = fg
            .get_subgraph_from(&["rain".into(), "cloudy".into()])
            .expect("cannot fail to get subgraph");
        assert_eq!(test_vfg, subgraph, "explicitly asked for all variables");

        let subgraph = fg
            .get_subgraph_from(&["sun".into()])
            .expect("cannot fail to get subgraph");
        assert!(subgraph.is_none(), "Unknown variable must return None");

        drop(fg);
        std::fs::remove_dir_all("factor_graph_data/test_get_subgraph_from").unwrap();
    }
}
