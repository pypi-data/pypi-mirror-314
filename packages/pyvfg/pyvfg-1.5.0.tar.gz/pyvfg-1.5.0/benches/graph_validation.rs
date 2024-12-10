use genius_agent_factor_graph::FactorGraphStore;
use genius_agent_factor_graph::test_util::*;

fn main() {
    let graph = generate_test_vfg();
    let db_path = format!("factor_graph_data/bench_{}", nanoid::nanoid!());
    let fg = FactorGraphStore::new(&db_path).unwrap();

    let options = microbench::Options::default();
    microbench::bench(&options, "validate_graph", || fg.validate_graph(graph.clone()).unwrap());

    std::fs::remove_dir_all(db_path).unwrap()
}
