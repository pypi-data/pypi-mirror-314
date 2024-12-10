# Resolution on VERSES Factor Graph (VFG) format for representing factor graphs for Genius beta parity release

- Status: proposed
- Deciders: 
    - [Prasaanth Sridharan](https://github.com/prasaanth-verses)
    - [Lior Saar](https://github.com/lior-saar)
    - [Coop Williams](https://github.com/coopwilliams)
    - [Sylvan Pronovost](https://github.com/doctorsylvainpronovost)
    - [Shohei Wakayama](https://github.com/shoheiw94)
    - [Alex Kiefer](https://github.com/alex-kiefer)
    - [Ryan Zaki](https://github.com/ryan-z)    

- Date: 2024-08-13

Technical Story: https://verses.atlassian.net/jira/software/c/projects/GPIL/boards/144?selectedIssue=GPIL-18

## Context and Problem Statement

We require a representation of the kinds of models that Genius can run inference, learning, and planning on, that is general, lightweight, independent of any particular programming language, and user-friendly.

## Decision Drivers

- Human legibility of representation
- Generality of representation (model classes it can represent)
- Storage size

## Considered Options

- Bayesian Interchange Format (BIF) file
- HSML
- VFG (VERSES Factor Graph)

## Decision Matrix

To systematically evaluate the considered options, we have created a decision matrix. This matrix lists each option in a row and each decision driver in a column. Each cell in the matrix contains a rating that reflects how well the option meets the corresponding decision driver. The rating scale is as follows:

- -5: Extremely Poor
- -3: Poor
- -1: Slightly Negative
- 0: Neutral
- 1: Slightly Positive
- 3: Good
- 5: Excellent

### Decision Matrix

| Option \ Driver | Legibility | Generality | Size | Total Score |
| --------------- | ---------- | ---------- | ---- | ----------- |
| BIF             | 3          | 0          | 4    | 7           |
| HSML            | 1          | 2          | -1   | 2           |
| VFG             | 4          | 2          | 4    | 10          |

## Decision Outcome

Chosen option: "VFG", because it best meets all requirements of the considered options.

### Positive Consequences

- We have a representation that can encode any of the models covered in the beta release of Genius (discrete Bayesian networks and Markov random fields)
- We have a format that is intuitive and easy for humans to parse and construct

### Negative Consequences

- The format is not yet fully general (does not include continuous factors or factors with arbitrary functions)
- The format is not already in wider use (e.g. outside VERSES)

## Pros and Cons of the Options

### Option 1: BIF

Definition: https://www.cs.washington.edu/dm/vfml/appendixes/bif.htm

Example: https://github.com/VersesTech/genius-samples/blob/main/data/processed/sprinkler.bif

#### BIF is good, because

- It can represent any discrete Bayesian network
- It is quite human-readable
- It can be stored as a plain text file
- It can be parsed by several Bayesian inference libraries

#### BIF is bad, because

- It is limited to representing Bayesian networks which are only one class of problem we wish to solve
- The rules defining the format are somewhat complex, and not as standardized as JSON
- The representation contains some redundancies

### Option 2: HSML

JSON schema(s): https://github.com/VersesTech/alexandria/tree/main/crates/kortex_types_and_utils/src/static_schema

Example: https://github.com/VersesTech/genius-samples/blob/main/data/hsql_ready/sprinkler_factor_graph_hsml.json

#### HSML is good, because

- It is a general-purpose format for representing anything (in principle)
- It is independently under development by VERSES and the Spatial Web Foundation
- It leverages JSON + JSON schemas
- It is the format used natively by the beta implementation of Genius, so no translation is required to perform runtime operations on factor graphs

#### HSML is bad, because

- It is a general-purpose format designed for use with the Spatial Web, so it is not optimized for representing probabilistic models
- It contains many fields not necessary for the purposes of Bayesian inference
- Its representation is not compact, in that edges in a represented graph are explicitly defined where they could be deduced from node properties
- Because of the above, file sizes are significantly larger than for the alternative formats considered
- It is difficult to read and reason about factor graphs represented in HSML at a glance, even for smaller models

### Option 3: VFG

JSON schema: [latest version](../api/schema/vfg_schema_0_1_0.json)

Example: [sprinkler graph](../models/sprinkler/sprinkler_vfg_0_1_0.json)

#### VFG is good, because

- It is a general-purpose format for representing discrete factor graphs
- It is user-readable and can be created by users with sufficient knowledge of factor graphs
- It leverages JSON + JSON schemas
- It successfully facilitated creation of new models by a variety of users during the Genius beta release

#### VFG is bad, because

- In its current version it is limited to discrete factor graphs
- It is not in use outside VERSES and so not natively supported by existing frameworks
