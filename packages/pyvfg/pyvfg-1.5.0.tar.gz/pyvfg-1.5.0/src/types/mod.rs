pub(crate) mod v0_2_0;
pub(crate) mod v0_3_0;
mod migrations;

pub use v0_3_0::*;

#[cfg(feature = "json")]
#[derive(serde::Serialize, serde::Deserialize)]
#[serde(tag = "version")]
#[non_exhaustive]
pub enum VFGMeta {
    #[serde(rename = "0.2.0")]
    VFGv0_2_0(v0_2_0::VFG),
    #[serde(rename = "0.3.0")]
    VFGv0_3_0(VFG),
}

#[cfg(feature = "json")]
pub fn load_vfg_from_reader(json: impl std::io::Read) -> Result<VFG, serde_json::Error> {
    let meta: VFGMeta = serde_json::from_reader(json)?;
    match meta {
        VFGMeta::VFGv0_2_0(vfg) => Ok(vfg.into()),
        VFGMeta::VFGv0_3_0(vfg) => Ok(vfg),
    }
}

#[cfg(all(test, feature = "json"))]
mod json_migration_test {
    use crate::test_util::generate_test_vfg_v0_2_0;
    use super::*;

    #[test]
    fn test_v2_to_v3_json() {
        let v2 = generate_test_vfg_v0_2_0();
        let str = serde_json::to_string(&v2).expect("can convert v2 to string");
        let mut reader = std::io::Cursor::new(str);
        let v3 = load_vfg_from_reader(&mut reader).expect("can load v2 from reader");
        assert_eq!(v3, v2.into());
    }
}
