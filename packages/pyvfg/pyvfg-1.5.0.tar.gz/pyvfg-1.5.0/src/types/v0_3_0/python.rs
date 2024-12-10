use crate::types::v0_3_0::{DiscreteVariableNamedElements, Factor, Values, VariableRole, VFG};
use crate::types::{DiscreteVariableAnonymousElements, FactorRole, ProbabilityDistribution, VariableID};
use ndarray::{Array, IntoDimension};
use numpy::{IntoPyArray};
use pyo3::prelude::PyAnyMethods;
use pyo3::types::PyDict;
use pyo3::{pymethods, Bound, IntoPy, PyAny, PyObject, Python};

impl IntoPy<PyObject> for Values {
    fn into_py(self, py: Python) -> PyObject {
        let strides = self
            .strides
            .into_iter()
            .map(|x| x as usize)
            .collect::<Vec<usize>>();
        let arr = Array::from_shape_vec(strides.into_dimension(), self.values)
            .expect("can create ndarray");
        arr.into_pyarray_bound(py).into()
    }
}

impl IntoPy<PyObject> for super::Variable {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            super::Variable::DiscreteVariableNamedElements(dvne) => dvne.into_py(py),
            super::Variable::DiscreteVariableAnonymousElements(dvae) => dvae.into_py(py),
        }
    }
}

#[pymethods]
impl VFG {
    #[new]
    fn new(factors: Vec<Factor>, variables: Bound<PyDict>) -> Self {
        let variables = variables
            .into_iter()
            .map(|(key, any)| {
                let key = key.extract::<String>().unwrap();
                let var = match any.extract::<DiscreteVariableNamedElements>() {
                    Ok(var) => super::Variable::DiscreteVariableNamedElements(var),
                    Err(_) => {
                        let var = any.extract::<DiscreteVariableAnonymousElements>().unwrap();
                        super::Variable::DiscreteVariableAnonymousElements(var)
                    }
                };
                (key, var)
            })
            .collect();
        VFG { version: crate::loader::VFG_VERSION.to_string(), factors, variables }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        VFG::default()
    }
}

#[pymethods]
impl Factor {
    #[new]
    #[pyo3(signature = (variables, distribution, role = None))]
    fn new(variables: Vec<VariableID>, distribution: ProbabilityDistribution, role: Option<FactorRole>) -> Self {
        let role = role.unwrap_or(FactorRole::NoRole);
        Factor {
            variables,
            distribution,
            values: Values::default(), // todo fix!!
            role,
        }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        Factor::default()
    }
}

#[pymethods]
impl DiscreteVariableNamedElements {
    #[new]
    #[pyo3(signature = (elements, role = None))]
    fn new(elements: Vec<String>, role: Option<VariableRole>) -> Self {
        let role = role.unwrap_or(VariableRole::NoRole);
        DiscreteVariableNamedElements { elements, role }
    }
}

#[pymethods]
impl DiscreteVariableAnonymousElements {
    #[new]
    #[pyo3(signature = (cardinality, role = None))]
    fn new(cardinality: u32, role: Option<VariableRole>) -> Self {
        let role = role.unwrap_or(VariableRole::NoRole);
        DiscreteVariableAnonymousElements { cardinality, role }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pyo3::py_run;

    fn init_py_test() {
        pyo3::prepare_freethreaded_python();
    }

    #[test]
    fn test_into_py() {
        init_py_test();
        let values = Values {
            values: vec![1.0, 2.0, 3.0],
            strides: vec![1, 3],
        };
        Python::with_gil(|py| {
            let py_obj = values.into_py(py);
            py_run!(
                py,
                py_obj,
                r#"
                assert py_obj.shape == (1, 3)
                assert py_obj[0, 0] == 1.0
                assert py_obj[0, 1] == 2.0
                assert py_obj[0, 2] == 3.0
            "#
            );
        });
    }
}
