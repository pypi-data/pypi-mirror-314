pub(crate) mod node_arena;
pub(crate) mod migration;

pub(crate) use node_arena::*;

// DO NOT CHANGE THESE. NOT EVEN FOR A REFACTOR. They are ESSENTIAL to finding items.
/// filename for the version
pub(super) const VERSION_FN: &str = "version";
/// singular key in that datastore for the current version
pub(super) const VERSION_KEY: &[u8] = b"cur_version";
/// filename for the variable metadata
pub(crate) const VARIABLES_FN: &str = "variables";
/// filename for the variable mapping
pub(crate) const FACTORS_FN: &str = "factors";

/// These represent the STORAGE format version. These do not exactly align with the VFG version;
/// only certain VFG changes necessitate a change in th storage format.
#[allow(non_camel_case_types)] // it's nicer this way, honestly.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Default, PartialEq, Debug)]
#[repr(u8)]
pub(crate) enum Version {
    /// Format 0 stores VFGv0.1.0 through 0.2.0
    #[default]
    Format0 = 0,
    /// Format 0 stores VFGv0.3.0
    Format1 = 1,
}

impl TryFrom<String> for Version {
    type Error = crate::error::FactorGraphStoreError;
    fn try_from(s: String) -> Result<Self, Self::Error> {
        match s.as_ref() {
            "0.2.0" => Ok(Version::Format0),
            "0.3.0" => Ok(Version::Format1),
            _ => Err(crate::FactorGraphStoreError::InvalidVersionSpecification),
        }
    }
}
