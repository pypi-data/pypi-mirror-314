use thiserror::Error;
use crate::types::ProbabilityDistribution;

#[derive(Error, Clone, Debug)]
pub enum ValidationError {
    #[error("Uncategorized validation error")]
    ValidationError,
    #[error("Invalid variable name: {0}")]
    InvalidVariableName(String),
    #[error("Variable '{0}' must have at least 1 value.")]
    InvalidVariableItemCount(String),
    #[error("A factor must have at least one variable.")]
    MissingVariable,
    #[error("A factor must have at least one probability value.")]
    MissingProbability,
    #[error("Factor variable '{0}' is not defined in variables.")]
    VariableMissingInVariableList(String),
    #[error("Factor variables {0:?} have incorrect number of probability values. Expected {1}, found {2}.")]
    IncorrectProbabilityLength(Vec<String>, usize, usize),
    #[error("Factor values for each category must sum to 1.0 for {0:?} distributions. Found sum of {1} for {2:?}.")]
    StrideMustSumToOneError(ProbabilityDistribution, f32, Vec<String>),
    #[error("Invalid shape. Found strides {0:?} for Values {1:?}; product of strides must equal length of elements.")]
    InvalidShapeError(Vec<usize>, Vec<f32>),
}
