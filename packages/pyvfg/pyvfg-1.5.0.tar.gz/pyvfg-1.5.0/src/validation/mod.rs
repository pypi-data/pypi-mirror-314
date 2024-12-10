pub mod error;

pub use error::*;

use crate::types::VFG;
use crate::validation::ValidationError;

fn is_valid_variable_name(name: &str) -> bool {
    !name.is_empty()
        && name
            .find(|c: char| !c.is_ascii_alphanumeric() && c != '-' && c != '_' && c != '.')
            .is_none()
}

fn validate_variable_name(vfg: &VFG) -> Result<(), ValidationError> {
    for (name, values) in &vfg.variables {
        if !is_valid_variable_name(name) {
            return Err(ValidationError::InvalidVariableName(name.clone()));
        }
        if values.count() < 1 {
            return Err(ValidationError::InvalidVariableItemCount(name.clone()));
        }
    }

    Ok(())
}

fn validate_factors(vfg: &VFG) -> Result<(), ValidationError> {
    for factor in &vfg.factors {
        if factor.variables.is_empty() {
            return Err(ValidationError::MissingVariable);
        }
        if factor.values.strides.is_empty() || factor.values.values.is_empty() {
            return Err(ValidationError::MissingProbability);
        }

        // validate that all factor variables exist in the variables list
        for var in &factor.variables {
            if !vfg.variables.contains_key(var) {
                return Err(ValidationError::VariableMissingInVariableList(var.clone()));
            }
        }

        /*
           TODO: test for convergence, once we have a utility that can build and traverse the graph
           in the meantime we will implement a simple variable count check
        */
        // expected number of values is the count of each
        let mut expected_value_count = 1;
        for x in &factor.variables {
            expected_value_count *= vfg.variables[x].count()
        }

        // get the number of variables provided
        let actual_value_count = &factor.values.values.len();

        if actual_value_count != &expected_value_count {
            return Err(ValidationError::IncorrectProbabilityLength(
                factor.variables.clone(),
                expected_value_count,
                *actual_value_count,
            ));
        }

        // always sum over Axis(0), or the outermost axis; this is the categorical distribution.
        // every conditional combination, if any, generates a new categorical in the outermost axis.
        // so categoricals without a conditional only have an Axis(0), one conditional gets an Axis(1), two conditionals get an Axis(1) and an Axis(2), and so on -- but the actual categorical distribution is always the outermost!
        // this results in the Values structure, where { shape: [2, 2], values: [0.5, 0.9, 0.5, 0.1] } should sum to [1.0, 1.0]
        // we convert it to an ndarray for parallelism with numpy; it's also much easier to reason about this way.
        let vec = factor.values.values.clone();
        let _matrix =
            ndarray::Array::from_shape_vec(factor.values.strides.clone(), vec).map_err(|_| {
                ValidationError::InvalidShapeError(
                    factor.values.strides.clone(),
                    factor.values.values.clone(),
                )
            })?;

        // This validation rule is disabled for now, as our factor graph representation doesn't currently
        // distinguish between tensors that directly represent categorical distributions (using probability
        // values which must sum to 1) and those that represent alpha parameters for Dirichlet distributions,
        // which needn't sum to 1.
        // We should revisit this once we have a more expressive factor graph representation (https://verses.atlassian.net/browse/GPIL-217).

        // if factor.distribution == ProbabilityDistribution::CategoricalConditional {
        //     // sum_axis: keep it SIMD!
        //     for sum in matrix.sum_axis(Axis(0)) {
        //         if f32::abs(sum - 1.0) > f32::EPSILON {
        //             return Err(ValidationError::StrideMustSumToOneError(factor.distribution, sum, factor.variables.clone()));
        //         }
        //     }
        // } else if factor.distribution == ProbabilityDistribution::Categorical {
        //     let sum = matrix.sum();
        //     if f32::abs(sum - 1.0) > f32::EPSILON {
        //         return Err(ValidationError::StrideMustSumToOneError(factor.distribution, sum, factor.variables.clone()));
        //     }
        // }
    }

    Ok(())
}

pub fn validate_vfg(vfg: &VFG) -> Result<(), ValidationError> {
    // validate variables
    validate_variable_name(vfg)?;

    // validate factors
    validate_factors(vfg)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_util::generate_test_vfg;
    use crate::types::{Values, Variable};
    use std::collections::HashMap;

    /// Description: Test of the `validate_vfg` method's success case (happy path)
    /// Objectives: 1. `validate_vfg` is called without error;
    ///             2. a correct and valid vfg results in an `Ok` response from the method
    #[test]
    fn test_validation_success() {
        let result = validate_vfg(&generate_test_vfg());

        // this is a happy path test, so the below should _not_ print, this is just for debugging purposes if the VFG validation starts failing
        if let Err(e) = &result {
            println!("VFG format is invalid: {:?}", e)
        }

        assert!(result.is_ok());
    }

    #[test]
    fn test_is_valid_variable_name() {
        assert!(is_valid_variable_name("valid_name123"));
        assert!(is_valid_variable_name("valid.name-123"));
        assert!(!is_valid_variable_name("invalid name!"));
        assert!(!is_valid_variable_name(""));
    }

    /// Description: Test that a variable name which contains invalid characters is rejected
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the variable name was invalid
    #[test]
    fn test_invalid_variable_name() {
        let mut test_vfg: VFG = generate_test_vfg();

        // manipulate the test VFG to contain a variable name with an invalid character, &
        let mut variables: HashMap<String, Variable> = HashMap::new();
        variables.insert(
            "rain&".to_string(),
            vec!["yes".to_string(), "no".to_string()].into(),
        );
        variables.insert(
            "cloudy".to_string(),
            vec!["yes".to_string(), "no".to_string()].into(),
        );

        test_vfg.variables = variables;
        test_vfg.factors[0].variables = vec!["rain&".to_string(), "cloudy".to_string()];

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(error_message, "Invalid variable name: rain&");
    }

    /// Description: Test that a variable with one or no values is rejected
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the variable list was invalid
    #[test]
    fn test_variable_must_have_at_least_one_value() {
        let mut test_vfg: VFG = generate_test_vfg();

        // manipulate the test VFG to have a variable which contains only a single value
        let mut variables: HashMap<String, Variable> = HashMap::new();
        variables.insert("rain".to_string(), vec![].into());
        variables.insert(
            "cloudy".to_string(),
            vec!["yes".to_string(), "no".to_string()].into(),
        );

        test_vfg.variables = variables;

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(error_message, "Variable 'rain' must have at least 1 value.");
    }

    /// Description: Test that a factor with no variables specified is rejected
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the factor variables were invalid
    #[test]
    fn test_factor_must_have_at_least_one_variable() {
        let mut test_vfg: VFG = generate_test_vfg();
        test_vfg.factors[0].variables = vec![];

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(error_message, "A factor must have at least one variable.");
    }

    /// Description: Test that a factor with no probability values is rejected
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the factor probability list was invalid
    #[test]
    fn test_factor_must_have_at_least_one_prob_value() {
        let mut test_vfg: VFG = generate_test_vfg();
        test_vfg.factors[0].values.values = vec![];

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(
            error_message,
            "A factor must have at least one probability value."
        );
    }

    /// Description: Test that a factor with a variable which does not appear in the list of variables is rejected
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the factor variable was invalid
    #[test]
    fn test_factor_variable_not_defined_in_variables() {
        let mut test_vfg: VFG = generate_test_vfg();
        test_vfg.factors[0].variables = vec!["non_existent".to_string()];

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(
            error_message,
            "Factor variable 'non_existent' is not defined in variables."
        );
    }

    /// Description: Test that factor variables with an incorrect number of probability values are rejected
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the number of probability values were  invalid
    #[test]
    fn test_factor_variables_incorrect_num_prob_values() {
        let mut test_vfg: VFG = generate_test_vfg();
        test_vfg.factors[0].values.values = vec![0.1, 0.2, 0.3];

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(error_message, "Factor variables [\"rain\", \"cloudy\"] have incorrect number of probability values. Expected 4, found 3.");
    }

    /// Description: Test that factor values must sum up to 1.0 per stride (i.e. matrix row)
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the factor values were invalid
    #[ignore]
    // This test is disabled because the validation rule is not being enforced in this version of the software
    #[test]
    fn test_factor_strides_must_sum_to_one_conditional_probability() {
        let mut test_vfg: VFG = generate_test_vfg();
        test_vfg.factors[1].values.values = vec![0.5, 0.6];

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        assert_eq!(error_message, "Factor values for each category must sum to 1.0 for Categorical distributions. Found sum of 1.1 for [\"cloudy\"].");
    }

    /// Description: We want to validate that the validation actually sums the correct items in the stride.
    /// Objectives: For a multi-stride factor, we can actually change the values and they still validate.
    #[ignore]
    // This test is disabled because the validation rule is not being enforced in this version of the software
    #[test]
    fn test_factor_strides_must_sum_to_one_conditional_probability_multiple_stride() {
        let mut test_vfg = generate_test_vfg();
        test_vfg.factors[2].values = Values {
            strides: vec![2, 2],
            values: vec![0.4, 0.9, 0.6, 0.1], // good, proper, correct
        };

        let result = validate_vfg(&test_vfg);
        assert!(result.is_ok(), "ensuring success on accurate values");

        test_vfg.factors[2].values.values = vec![0.4, 0.6, 0.4, 0.6]; // this was transposed
        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok(), "ensuring failure on transposed values");
    }

    /// Description: Test that factor values must sum up to 1.0 for CategoricalConditional distributions
    /// Objectives: 1. `validate_vfg` is called without error (it may return Err to indicate an invalid VFG, but should not panic);
    ///             2. `validate_vfg` returns an `Err` and the resulting error message indicates the factor values were invalid
    //#[test]
    //#[ignore] // This test is disabled because the validation rule is not being enforced in this version of the software
    //fn test_factor_strides_must_sum_to_one_joint_probability() {
    //    let mut test_vfg: VFG = generate_test_vfg();
    //    test_vfg.factors[1].distribution = ProbabilityDistribution::CategoricalConditional;
    //    test_vfg.factors[1].values.values = vec![0.5, 0.6];

    //    let result = validate_vfg(&test_vfg);
    //    assert!(!result.is_ok());

    //    let error_message = result.err().unwrap().to_string();
    //    assert_eq!(error_message, "Factor values for each category must sum to 1.0 for CategoricalConditional distributions. Found sum of 1.1 for [\"cloudy\"].");
    //}

    //#[ignore]
    // This test is disabled because the validation rule is not being enforced in this version of the software
    //#[test]
    //fn test_factor_must_sum_to_one_categorical_multiple_stride() {
    //    let mut test_vfg: VFG = generate_test_vfg();
    //    test_vfg.factors[1].variables = vec!["sprinkler".to_string(), "cloudy".to_string()];
    //    test_vfg.factors[1].distribution = ProbabilityDistribution::Categorical;
    //    test_vfg.factors[1].values = Values {
    //        strides: vec![2, 2],
    //        values: vec![0.2, 0.3, 0.1, 0.4],
    //    };

    //    let result = validate_vfg(&test_vfg);
    //    assert!(result.is_ok(), "ensuring categorical values can be strided");
    //}

    #[test]
    fn test_factor_zero_stride() {
        let mut test_vfg: VFG = generate_test_vfg();
        test_vfg.factors[0].values.strides = vec![0]; // Set stride to zero

        let result = validate_vfg(&test_vfg);
        assert!(!result.is_ok());

        let error_message = result.err().unwrap().to_string();
        println!("{}", error_message);
        assert_eq!(
            error_message, "Invalid shape. Found strides [0] for Values [0.8, 0.2, 0.2, 0.8]; product of strides must equal length of elements."
        );
    }
}
