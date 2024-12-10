use crate::types::VariableRole;

type RoleV2 = crate::types::v0_2_0::Role;
type RoleV3 = crate::types::v0_3_0::FactorRole;

impl From<crate::types::v0_2_0::VFG> for crate::types::v0_3_0::VFG {
    fn from(val: crate::types::v0_2_0::VFG) -> Self {
        crate::types::v0_3_0::VFG {
            version: "0.3.0".to_string(),
            factors: val.factors.into_iter().map(|f| f.into()).collect(),
            variables: val.variables.into_iter().map(|(k, v)| (k, v.into())).collect(),
        }
    }
}

impl From<crate::types::v0_2_0::Factor> for crate::types::v0_3_0::Factor {
    fn from(val: crate::types::v0_2_0::Factor) -> crate::types::v0_3_0::Factor {
        crate::types::v0_3_0::Factor {
            variables: val.variables,
            distribution: val.distribution.into(),
            values: val.values.into(),
            role: val.role.into(),
        }
    }
}

impl From<crate::types::v0_2_0::ProbabilityDistribution> for crate::types::v0_3_0::ProbabilityDistribution {
    fn from(value: crate::types::v0_2_0::ProbabilityDistribution) -> crate::types::v0_3_0::ProbabilityDistribution {
        match value {
            crate::types::v0_2_0::ProbabilityDistribution::Categorical => crate::types::v0_3_0::ProbabilityDistribution::Categorical,
            crate::types::v0_2_0::ProbabilityDistribution::CategoricalConditional => crate::types::v0_3_0::ProbabilityDistribution::CategoricalConditional,
        }
    }
}

impl From<crate::types::v0_2_0::Values> for crate::types::v0_3_0::Values {
    fn from(value: crate::types::v0_2_0::Values) -> crate::types::v0_3_0::Values {
        crate::types::v0_3_0::Values {
            strides: value.strides.into_iter().map(|x| x as usize).collect(),
            values: value.values,
        }
    }
}

impl From<Vec<String>> for crate::types::v0_3_0::Variable {
    fn from(value: Vec<String>) -> crate::types::v0_3_0::Variable {
        crate::types::v0_3_0::Variable::DiscreteVariableNamedElements(crate::types::v0_3_0::DiscreteVariableNamedElements {
            elements: value,
            role: VariableRole::default(),
        })
    }
}

impl From<Option<RoleV2>> for RoleV3 {
    fn from(value: Option<RoleV2>) -> RoleV3 {
        match value {
            None | Some(RoleV2::None) => crate::types::v0_3_0::FactorRole::NoRole,
            Some(RoleV2::Transition) => crate::types::v0_3_0::FactorRole::Transition,
            Some(RoleV2::Preference) => crate::types::v0_3_0::FactorRole::Preference,
            Some(RoleV2::Likelihood) => crate::types::v0_3_0::FactorRole::Likelihood,
        }
    }
}
