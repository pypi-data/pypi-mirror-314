use thiserror::Error;

#[derive(Error, Debug)]
pub enum FactorGraphStoreError {
    #[error("file manipulation error")]
    FileManipulationError(#[from] std::io::Error),
    #[error("database error")]
    DatabaseError(#[from] heed::Error),
    #[error("rkyv deserialization error: {}", .0)]
    RkyvDeserializationError(#[from] rkyv::rancor::Error),
    #[cfg(feature = "json")]
    #[error("json serialization error: {}", .0)]
    JsonSerializationError(#[from] serde_json::Error),
    #[error("validation error: {:?}", .0)]
    ValidationError(#[from] crate::validation::error::ValidationError),
    #[error("invalid version specification")]
    InvalidVersionSpecification,
}
