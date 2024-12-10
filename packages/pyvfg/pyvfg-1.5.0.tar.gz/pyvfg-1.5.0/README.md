# Genius Agent Factor Graph (pyVFG)

This crate is the main import and export library for the Genius Agent Factor Graph (VFG) format. It defines persistence,
storage, and other features required to work with VFGs in Rust and Python. It also contains import procedures for VFG,
and storage specifications for VFG.B.

## Supported Operating Systems
### Tested and supported:
- Linux (pure-VM, hosted VM, AWS, GCP, k8s, Docker)
- OSX
### Will fail:
- Windows
- WSL, WSL2

## VFG Version Support
Output graphs will always be in the latest version. This is currently **0.3.0**.
The following table shows the input support for each version:

| Version | Input Support |
|---------|---------------|
| 0.0.1   | ❌             |
| 0.1.0   | ❌             |
| 0.2.0   | ✅︎            |
| 0.3.0   | ✅︎            |
| 2.0.0   | ❌             |
| 2.1.0   | ❌             |
| 2.2.0   | ❌             |

This also contains validation functions for VFG formats.

## Features
With no features, the types will exist, but will have no import or export conversions. This is non-ideal.

- `json`: the ability to ingest and output a `vfg` json file
- `python`: conversion of types to and from python via `pyo3` and `numpy`

## Rust Usage
Full usage is in the `usage.rs` example file.

1. Include as crate with features desired.
2. Use the included importer to convert from what you have (disk, json, network) to the internal format.
    - See tests in `lib.rs` as examples.
3. Use the included exporter to convert from the internal format to what you need (disk, json, network).
    - See tests in `lib.rs` as examples.
4. Persistence is available through the `FactorGraph` class. Use the following example:

```rust
use genius_agent_factor_graph::FactorGraphStore;

fn example() {
    let store = FactorGraphStore::new("storage/");
    let vfg = store.get_graph();
    // do operations
    store.set_graph(vfg);
}
```

### Running Examples
The `examples/` directory contains useful example programs to illustrate the library’s usage. To run an example:
```bash
cargo run --example <EXAMPLE_NAME>
```
For instance, to run the `usage` example:

```bash
cargo run --example usage --features json
#To pass input the conents of a JSON file
cargo run --example usage --features json -- -i path/to/your_file.json

#To observe the tracing output
RUST_LOG=info cargo run --example usage --features json 
#To pass input the conents of a JSON file
RUST_LOG=info cargo run --example usage --features json -- -i path/to/your_file.json
`
## Python Usage
1. Import as `pyVFG`.
2. Exposed types are `FactorGraphStore`, and `VFG` (and its contents).
3. Conversion to and from JSON are available, using the module-level `vfg_to_json`, `vfg_from_json`, `vfg_to_proto`, and `vfg_from_proto` functions.
4. Persistence is available with the following example:

```python
import pyvfg
vfg = pyvfg.get_graph()
# do operations
pyvfg.set_graph(vfg)
```

## Rust Testing
1. Ensure `cargo-all-features` is installed to your machine: `cargo install cargo-all-features`
2. Run tests with `cargo test-all-features`

### Rust Testing Notes
LMDB, our backing database (exposed via the `heed` crate), uses sparse files for storage. This means several files that
are marked as having sizes of 1TB will be allocated and deleted during the test case. Total data written per test is less
than 400KiB. However, this may cause problems on NTFS under WSL, which treats sparse files as having their true extents for
file creation purposes.

**NTFS is not a supported filesystem. Windows is not a supported operating system.**

## Python Testing
1. Set up a venv
2. Build `pyvfg` using `maturin build --release`
3. In the venv, install python bindings using: `pip install --force-reinstall './target/wheels/<GENERATED_WHEEL>.whl'`
4. In the venv, install pytest using `python -m pip install pytest`
5. In the same venv, run `pytest -rP`

## Updating VFG Schema
1. Create a new schema submission in `docs/schemas/vfg/{VERSION}` with the new schema version
2. Create a new Rust implementation, copied from previous implementations, in `src/types/{VERSION}`
3. If this requires a new database change, set up a database migration
   1. A new verison of 
   2. Insert the new format in the `handle_db_migration` function in `src/loader/arena/migrations.rs`
   3. Update the `Arena` struct in `src/loader/arena/mod.rs` to handle the new format
4. Create a migration for this version in `src/types/migrations.rs`
5. Update the `VFG` enum in `src/types/mod.rs` to include the new version
6. Update the pyi file manually (???)
7. Update `python/pyvfg/pydantic.py`
   1. upload the new schema to s3 (TODO Automate!!)
   2. update the `__get_pydantic_json_schema__` method to point to the new schema

## Maintainers
Code:
- [Jasmine Moore](mailto:jasmine.moore@verses.ai)

Format:
- [Alex Kiefer](mailto:alex.kiefer@verses.ai)


## Prerequisites
- [buf](https://buf.build/docs/installation)
