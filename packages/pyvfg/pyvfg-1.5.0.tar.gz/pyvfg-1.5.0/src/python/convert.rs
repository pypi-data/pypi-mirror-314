use pyo3::create_exception;
use pyo3::exceptions::{PyIOError, PyException, PyValueError};
use crate::types::{load_vfg_from_reader, VFG};
use pyo3::prelude::*;
use crate::error::FactorGraphStoreError;

create_exception!(module, FileManipulationError, PyIOError);
create_exception!(module, DatabaseError, PyIOError);
create_exception!(module, RkyvDeserializationError, PyException);
create_exception!(module, JsonSerializationError, PyValueError);
create_exception!(module, ValidationError, PyValueError);
create_exception!(module, InvalidVersionSpecification, PyValueError);

#[cfg(feature = "python")]
impl From<FactorGraphStoreError> for PyErr {
    fn from(err: FactorGraphStoreError) -> Self {
        match err {
            FactorGraphStoreError::FileManipulationError(e) => FileManipulationError::new_err(e.to_string()),
            FactorGraphStoreError::DatabaseError(e) => DatabaseError::new_err(e.to_string()),
            FactorGraphStoreError::RkyvDeserializationError(e) => RkyvDeserializationError::new_err(e.to_string()),
            FactorGraphStoreError::JsonSerializationError(e) => JsonSerializationError::new_err(e.to_string()),
            FactorGraphStoreError::ValidationError(e) => ValidationError::new_err(e.to_string()),
            FactorGraphStoreError::InvalidVersionSpecification => InvalidVersionSpecification::new_err("invalid version specification"),
        }
    }
}

#[cfg(feature = "json")]
#[pyfunction]
pub(crate) fn vfg_to_json(vfg: &VFG) -> PyResult<String> {
    Ok(serde_json::to_string(vfg).map_err(|e| -> FactorGraphStoreError {
        e.into()
    })?)
}

#[cfg(feature = "json")]
#[pyfunction]
pub(crate) fn vfg_from_json(json: &str) -> PyResult<VFG> {
    Ok(load_vfg_from_reader(std::io::Cursor::new(json.as_bytes()))
        .map_err(|e| -> FactorGraphStoreError {
            e.into()
        })?)
}

#[cfg(all(test, feature = "json"))]
mod py_json_tests {
    use crate::test_util::{generate_test_vfg, init_py_test, sprinkler_graph_as_json_value_0_2_0};
    use pyo3::{py_run, IntoPy, Python};

    #[test]
    fn test_from_json() {
        init_py_test();
        // todo check with py.eval_bound()
        let json = sprinkler_graph_as_json_value_0_2_0().to_string();
        Python::with_gil(|py| {
            py_run!(py, json, r#"
            vfg = vfg_from_json(json)
            assert vfg.version == "0.3.0"
            "#)
        })
    }

    #[test]
    fn test_to_json() {
        init_py_test();
        // todo check with py.eval_bound()
        Python::with_gil(|py| {
            let vfg = generate_test_vfg().into_py(py);
            py_run!(py, vfg, r#"
                vfg = VFG()
                json = vfg_to_json(vfg)
                assert json == '{"version":"0.1.0","factors":[{"variables":["rain","cloudy"],"distribution":"categorical_conditional"}]}'
            "#)
        })
    }
}
