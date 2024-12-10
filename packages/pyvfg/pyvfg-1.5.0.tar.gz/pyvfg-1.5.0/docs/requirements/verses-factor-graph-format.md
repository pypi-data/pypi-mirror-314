# VERSES Factor Graph (VFG) Requirements

#### Soft requirements
- A lighter weight, terser format than HSML but still feature complete
- It's possible to write a VFG by hand due to its terseness
- VFG must be human readable
- VFG must be able to represent any factor graph/bayesian network (perhaps initially not all networks will be supported, but this will be an end goal)

####  VFG Variables Requirements:
- A variable must consist of a list/array of discrete values
- A variable is valid if:
  - Its name is a unique alphanumeric string, which may also contain dashes, dots and underscores
  - It has at least 2 possible values
    - Constants will not be supported as there is no clear use case, but no technical limitation prohibits supporting them

- Updates to a variable on a VFG can only occur in the following conditions
  - The variable is new and is being added to the list of variables
    - A factor must be defined which provides the probabilities for the variable values
  - Its dimensions are the same (number of possible values). This is effectively the same as renaming some of the variables values.
    - Does not require all associated factors be included in update, however, factors can be updated at the same time
  - Its dimensions are different
    - Requires all associated factors be included in an update, otherwise the graph would potentially no longer converge

####  VFG Factors Requirements:
Factors define relationships and probabilities of variables.

- A factor must contain:
  - A list of at least one variable
  - A list of at least one probability (called values)
    - These values must be integers or floating point numbers, up to 64-bit
- Only the first variable in the list represents the factor variable, all subsequent variables are variables upon which the factor variable probability is conditional
    - For example, in the below sample VFG we have:
`'variables': ['SocioEcon', 'Age']`
    - Where “SocioEcon” is the factor variable, and it is correlated with/conditionally related to ”Age”.
- The dimensions of the probabilities/values must be such that the factor graph converges
  - A factor must have an appropriately sized array of values based on the variable list and potential value count
  - A convergence check should be carried out on affected factors during upsert, and rejected if it does not converge.
    - This avoids loose dimension-size checks which could potentially reject smaller, optimised but unusually sized probability distributions.
  - Each stride of a factor's values must sum to 1.0, such that a whole probability is represented.

##### Types of Probability Distributions Supported
- A factor may optionally have a value for “graph_type” (i.e. probably distribution).
    - e.g. `'graph_type': 'ConditionalProbability'`
- Currently, two types of distributions are supported:
    - `JointProbability`: P(A, B, C) where A, B and C or any number of listed probabilities are probablistically unrelated to one another but combine to create a cumulative probability. This is the default if no `graph_type` value is specified.
    - `ConditionalProbability`: P(A|B, C) where A is conditional upon the joint probabilities of B, C or any number of probabilities



### Example VFG Variables and Factors:
```
{
    'variables': {
        'Age': [
            'Adolescent',
            'Adult',
            'Senior'
        ],
        'Antilock': [
            'True',
            'False'
        ],
        'MakeModel': [
            'SportsCar',
            'Economy',
            'FamilySedan',
            'Luxury',
            'SuperLuxury'
        ],
        'RiskAversion': [
            'Psychopath',
            'Adventurous',
            'Normal',
            'Cautious'
        ],
        'SocioEcon': [
            'Lower',
            'Middle',
            'UpperMiddle',
            'Wealthy'
        ],
            'VehicleYear': [
            'Current',
            'Older'
        ]
    },
    'factors': [
        {
            'variables': ['Age'],
            'values': [0.2. 0.6, 0.2]
        },
        {
            'graph_type': 'ConditionalProbability'
            'variables': ['SocioEcon', 'Age'],
            'values': [
                [0.4, 0.4, 0.5],
                [0.4, 0.4, 0.2],
                [0.19, 0.19. 0.29],
                [0.01. 0.01. 0.01]
            ]
        },
        ...
    ],
}
```