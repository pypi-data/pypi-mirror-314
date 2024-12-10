use genius_agent_factor_graph::types::load_vfg_from_reader;
use genius_agent_factor_graph::{types::VFG, FactorGraphStore};
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;

fn main() -> Result<(), Box<dyn Error>> {
    // Default JSON file path
    let mut file_path = "./test_data/small/grid_world.json".to_string();
    // let mut file_path = "./test_data/small/random_field_example_vfg_v1.json".to_string();
    // let mut file_path = "./test_data/small/sprinkler_factor_graph_vfg.json".to_string();
    // let mut file_path = "./test_data/medium/insurance_vfg_v1.json".to_string(); // Error replacing graph: ValidationError(ValidationError { code: StrideMustSumToOneError, message: "Factor values must sum up to 1.0 per stride (i.e. matrix row) for CategoricalConditional distributions. Found sum of 0.1 for [\"GoodStudent\", \"SocioEcon\", \"Age\"]." })
    
    // Manually parse command-line arguments for "-i" flag
    let args: Vec<String> = env::args().collect();
    if let Some(pos) = args.iter().position(|arg| arg == "-i") {
        if pos + 1 < args.len() {
            file_path = args[pos + 1].clone();
        } else {
            eprintln!("Error: No file path provided after -i flag");
            return Err("Missing file path argument after -i".into());
        }
    }

    let mut factor_graph_store = FactorGraphStore::new("storage")?;

    // Open the specified JSON file and pass it to load_vfg_from_reader
    let file = File::open(&file_path)?;
    let reader = BufReader::new(file);
    let graph_to_store: VFG = load_vfg_from_reader(reader)?;

    // println!("VFG JSON String:\n{:?}", &graph_to_store);

    let validate_graph_result = factor_graph_store.validate_graph(graph_to_store.clone());
    match validate_graph_result {
        Ok(_) => println!("Graph validated successfully"),
        Err(e) => println!("Error validating graph: {:?}", e),
    }

    let replace_graph_result = factor_graph_store.replace_graph(graph_to_store);
    match replace_graph_result {
        Ok(_) => println!("Graph replaced successfully"),
        Err(e) => println!("Error replacing graph: {:?}", e),
    }

    let stored_graph_result = factor_graph_store.get_graph();
    match stored_graph_result {
        Ok(Some(stored_graph)) => {
            println!("Graph loaded successfully");
            println!("{:?}", stored_graph);
        },
        Ok(None) => println!("No graph found in storage"),
        Err(e) => println!("Error retrieving graph: {:?}", e),
    }

    Ok(())
}
