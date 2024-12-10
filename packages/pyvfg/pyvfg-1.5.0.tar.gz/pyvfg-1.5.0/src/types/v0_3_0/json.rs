use crate::types::v0_3_0::Values;
use itertools::Itertools;
use serde::{Deserialize, Deserializer, Serialize, Serializer};

pub fn vfg_schema_version() -> String {
    "0.3.0".to_string()
}

/// Returns true if the factor role is none.
pub fn factor_role_is_none(role: &super::FactorRole) -> bool {
    *role == super::FactorRole::NoRole
}

/// Returns true if the variable role is none.
pub fn variable_role_is_none(role: &super::VariableRole) -> bool {
    *role == super::VariableRole::NoRole
}

pub(crate) mod graph_type {
    use crate::types::ProbabilityDistribution;
    use serde::{Deserializer, Serializer};

    #[allow(unused)] // used by serde
    impl<'de> serde::Deserialize<'de> for ProbabilityDistribution {
        fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
        where
            D: Deserializer<'de>,
        {
            let value = serde_json::Value::deserialize(deserializer)?;
            match value.as_str() {
                Some(value_str) => match value_str.to_lowercase().as_str() {
                    "categorical" => Ok(ProbabilityDistribution::Categorical),
                    "categorical_conditional" => {
                        Ok(ProbabilityDistribution::CategoricalConditional)
                    }
                    _ => Err(serde::de::Error::custom("Invalid distribution")),
                },
                None => Err(serde::de::Error::custom("Invalid distribution")),
            }
        }
    }

    #[allow(unused)] // used by serde
    impl serde::Serialize for ProbabilityDistribution {
        fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
        where
            S: Serializer,
        {
            if self == &ProbabilityDistribution::Categorical {
                serializer.serialize_str("categorical")
            } else if self == &ProbabilityDistribution::CategoricalConditional {
                serializer.serialize_str("categorical_conditional")
            } else {
                // unreachable
                serializer.serialize_none()
            }
        }
    }

    #[allow(unused)] // used by serde
    pub(crate) fn deserialize<'de, D>(data: D) -> Result<ProbabilityDistribution, D::Error>
    where
        D: Deserializer<'de>,
    {
        use serde::de::Deserialize;

        let value = serde_json::Value::deserialize(data)?;
        match value.as_str() {
            Some(value_str) => match value_str {
                "categorical" => Ok(ProbabilityDistribution::Categorical),
                "categorical_conditional" => Ok(ProbabilityDistribution::CategoricalConditional),
                _ => Err(serde::de::Error::custom("Invalid distribution")),
            },
            None => Err(serde::de::Error::custom("Invalid distribution")),
        }
    }

    #[allow(unused)] // used by serde
    pub(crate) fn serialize<S>(val: &ProbabilityDistribution, ser: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        if val == &ProbabilityDistribution::Categorical {
            ser.serialize_str("categorical")
        } else if val == &ProbabilityDistribution::CategoricalConditional {
            ser.serialize_str("categorical_conditional")
        } else {
            // unreachable
            ser.serialize_none()
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(untagged)]
#[cfg_attr(test, derive(PartialEq))]
enum ValueTypeExpanded {
    ValueList(Vec<ValueTypeExpanded>),
    Value(f32),
}

impl IntoIterator for ValueTypeExpanded {
    type Item = ValueTypeExpanded;
    type IntoIter = std::vec::IntoIter<Self::Item>;

    fn into_iter(self) -> Self::IntoIter {
        match self {
            Self::Value(_) => vec![self].into_iter(),
            Self::ValueList(vec) => vec.into_iter(),
        }
    }
}

impl FromIterator<ValueTypeExpanded> for ValueTypeExpanded {
    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = ValueTypeExpanded>,
    {
        ValueTypeExpanded::ValueList(iter.into_iter().collect())
    }
}

impl<'de> serde::Deserialize<'de> for Values {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let vte = ValueTypeExpanded::deserialize(deserializer)?;
        Ok(vte.into())
    }
}

impl serde::Serialize for Values {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        ValueTypeExpanded::from(self).serialize(serializer)
    }
}

impl From<ValueTypeExpanded> for Values {
    fn from(vte: ValueTypeExpanded) -> Self {
        // todo use ndarray here, and internally.
        use ValueTypeExpanded::*;
        match vte {
            // general case
            ValueList(vtes) => {
                if vtes.iter().any(|vte| matches!(vte, ValueList(_))) {
                    // if there are any sublists, we want to recurse
                    let len = vtes.len();
                    let mut values = vtes
                        .into_iter()
                        .map_into()
                        .reduce(|mut acc: Values, cur: Values| {
                            acc.values.extend(&cur.values);
                            acc
                        })
                        .unwrap_or_default();
                    values.strides.insert(0, len);
                    values
                } else {
                    // otherwise, we handle it simpler
                    let values: Vec<f32> = vtes
                        .into_iter()
                        .map(|x| match x {
                            ValueList(_) => panic!("not possible"),
                            Value(x) => x,
                        })
                        .collect();
                    let strides = vec![values.len()];
                    Values { values, strides }
                }
            }
            // handle the base case
            Value(num) => Values {
                strides: vec![1],
                values: vec![num],
            },
        }
    }
}

impl From<&Values> for ValueTypeExpanded {
    fn from(v: &Values) -> Self {
        if v.values.is_empty() {
            return Self::default();
        }
        // handle single stride special
        if v.strides.len() == 1 && v.strides[0] == 1 {
            return ValueTypeExpanded::Value(v.values[0]);
        }
        // re-nest the structure
        fn chunk_to_list<C: IntoIterator<Item = ValueTypeExpanded>>(chunk: C) -> ValueTypeExpanded {
            let chunk_vec = chunk.into_iter().collect::<Vec<ValueTypeExpanded>>();
            ValueTypeExpanded::ValueList(chunk_vec)
        }

        let mut stride_iter = v.strides.iter().rev();
        if let Some(first) = stride_iter.next() {
            let mut vte_raw: Vec<ValueTypeExpanded> = v
                .values
                .iter()
                .copied()
                .map(ValueTypeExpanded::Value)
                .chunks(*first)
                .into_iter()
                .map(chunk_to_list)
                .collect();

            for next_stride in stride_iter {
                vte_raw = vte_raw
                    .into_iter()
                    .chunks(*next_stride)
                    .into_iter()
                    .map(chunk_to_list)
                    .collect();
            }

            // sorry we shouldn't have to do this, i'm a little sick so I'm kinda dumb today
            // Unwrap the outer ValueList to remove one level of nesting
            match vte_raw.into_iter().next() {
                Some(ValueTypeExpanded::ValueList(inner)) => ValueTypeExpanded::ValueList(inner),
                Some(other) => other,
                None => Self::default(),
            }
        } else {
            Self::default()
        }
    }
}

impl Default for ValueTypeExpanded {
    fn default() -> Self {
        ValueTypeExpanded::Value(0.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Description: Tests conversion from a ValueTypeExpanded::ValueList to a Values
    /// Outcomes: A ValueList of two Values converts to a single value array containing the two elements, and a strides array of a single element with value two
    #[test]
    fn test_value_from_value_type_expanded() {
        let vte = ValueTypeExpanded::ValueList(vec![
            ValueTypeExpanded::Value(1.0),
            ValueTypeExpanded::Value(2.0),
        ]);
        let vt: Values = vte.into();
        assert_eq!(vt.values.len(), 2, "checking we still have two elements");
        assert_eq!(
            vt.strides,
            vec![2],
            "checking we have one stride of two elements"
        );
    }

    /// Description: Tests conversion from `[[3, 5], [7, 9]]` to the corresponding values
    /// Outcomes: Stride of `[2, 2]` with values `[3, 5, 7, 9]`
    #[test]
    fn test_value_from_value_type_expanded_2() {
        use ValueTypeExpanded::*;
        let vte = ValueList(vec![
            ValueList(vec![Value(3.0), Value(4.0)]),
            ValueList(vec![Value(5.0), Value(6.0)]),
        ]);
        let vt: Values = vte.into();
        assert_eq!(vt.values.len(), 4, "checking we still have two elements");
        assert_eq!(
            vt.strides,
            vec![2, 2],
            "checking we have two stride of two elements each"
        );
    }

    /// Description: Tests conversion from a Values to a ValueTypeExpanded
    /// Outcomes: A single value array containing the two elements, and a strides array of a single element with value two converts to a ValueList of two Values
    #[test]
    fn test_value_type_expanded_from_value_2() {
        let vt = Values {
            strides: vec![2],
            values: vec![0.2, 0.8],
        };
        let vte: ValueTypeExpanded = (&vt).into();
        let expected_vte = ValueTypeExpanded::ValueList(vec![
            ValueTypeExpanded::Value(0.2),
            ValueTypeExpanded::Value(0.8),
        ]);
        assert_eq!(
            vte, expected_vte,
            "checking that one stride of two elements expands into a value list"
        )
    }

    /// Description: Tests conversion from a Values to a ValueTypeExpanded
    /// Outcomes: A single value array containing the two elements, and a strides array of [1,2] converts to a ValueList of a ValueList of two Values
    #[test]
    fn test_value_type_expanded_from_value_3() {
        let vt = Values {
            strides: vec![1, 2],
            values: vec![0.2, 0.8],
        };
        let vte: ValueTypeExpanded = (&vt).into();
        let expected_vte = ValueTypeExpanded::ValueList(vec![ValueTypeExpanded::ValueList(vec![
            ValueTypeExpanded::Value(0.2),
            ValueTypeExpanded::Value(0.8),
        ])]);
        assert_eq!(
            vte, expected_vte,
            "checking that one stride of two elements expands into a value list"
        )
    }
}
