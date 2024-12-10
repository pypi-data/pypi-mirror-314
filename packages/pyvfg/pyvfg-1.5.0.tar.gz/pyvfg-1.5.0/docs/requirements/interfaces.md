# Interfaces and Functions

## Structures

This includes the structures that will be part of the request/response for the functions below. 



### Variable

A Varaible consists of a name (String) and an array of possible values ([String])
Example:
```json
{
    "temperature": [
        "cold",
        "moderate",
        "hot"
    ]
}
```

### Variables
```rust
struct Variables {
      variables:  HashMap<String, Vec<String>>
}
```

```json
{ "variables" : {
    "temperature" : ["cold","moderate","hot"],
    "cloudy" : ["yes","no"]
    } 
}
```


### Factor
Fields:
* variables - An array of variables which uniquely identifies this factor
    * Order Matters
    * The first value is the probability of A
    * The remaining values can be read as "given B and C"
* CPD - conditional probablily distribution
* values - an array of matrices sized by the number of potential values in the variables

```rust
struct Factor {
    variables: Vec<String>,
    CPD: bool,
    values: Vec<Vec<f32>>
}
```


### Graph
A factor graph consists of Variables and Factors

```rust
struct Graph {
    variables : Variables,
    factors: Vec<Factor>
}
```


## Functions Overview


* [set_graph(graph)](#set_graphgraph) - Creates or replaces the entire graph with the one provided.
* [get_graph()](#get_graph) - returns the whole graph
* [get_subgraph([variable names])](#get_subgraphvariable-names--string) - returns any factor that uses any of the associated variables, and all variables needed by those factors
* [get_variables(Option([variable names]))](#get_variablesoptionvariable-names) - returns either the variables requested in the array, or all of the variables in the graph if Option is none
* [get_factor([array of variable names])](#get_factorarray-of-variable-names--) - returns a single factor as a mini factor graph (factor, variables)
* [get_factor_names()](#get_factor_names--) - returns all factors in the graph as an array [] of factor names: example [["wet","sprinkler","rain"],["sprinkler","rain"]]
* [get_variable_names()](#get_variable_names) - returns all variables in the graph as an array of variable names
* [add_variable([variable])](#add_variablevariable) - Adds a new variable to the graph
* [add_factor([factor])](#add_factorfactor) - Adds a new factor to the graph. 
* [delete_variable([variable name])](#delete_variablevariable-name) - This will fail if there's still a factor in the graph which uses the variable.  Delete factors first
* [delete_factor([factor name])](#delete_factorfactor-name) - Removes a factor from the graph.
* [update_variable([variable])](#update_variablevariable) - updates variables in the graph.  If the number of possible values has changed, will fail.   Use update_subgraph instead.
* [update_factor([factor])](#update_factorfactor--) - updates factors in the graph.
* [update_subgraph(subgraph)](#update_subgraphsubgraph) - Updates a portion of the graph, includes factors and associated variables

These have been removed for now
* ~[get_hyperparams()](#get_hyperparams--needs-more-understanding-warning)- needs more understanding :warning:~
* ~[update_hyperparams()](#update_hyperparams---needs-more-understanding-warning) - needs more understanding :warning:~

### set_graph(Graph)
Creates or replaces the entire graph with the one provided

#### Input: Graph structure

#### Potential Responses: 
* Success 
* Error
    * Validation Error
    * Invalid Parameters
    * Internal Error

#### General Processing Steps:
* Validate the input graph meets all factor graph rules
    * Return Validation Error if graph is not valid
* Write Lock Current Graph - Return Internal Error if unable to get lock
* Replace Current Graph - Return Internal Error if unable to replace current graph
* Unlock Current Graph - Return Internal Error if unable to release lock
* Return OK

#### Key Testing Scenarios
* Pass an incomplete graph (Error)
* Pass in a structure that is not a graph at all (Invalid Parameters)
* Pass a complete graph
* Pass in much larger graph than is currently in place (Memory allocation rises)
* Pass in a much smaller graph than is currently in place (Memory allocation drops)
* Benchmarking for loading, validating, etc.


### get_graph()
Returns the whole graph

#### Input : None

#### Potential Responses
* Success: Graph structure which contains the entire graph
* Error:
    * Not Found - No Graph has been loaded yet
    * Internal Error
        * Out of Memory?
        * Unable to get read lock?

#### General Processing steps
* Establish read lock on graph
* Create in memory copy of entire graph
* release read lock on graph
* return result

#### Key Testing Scenarios
* Call with existing graph in memory and verify results match expected
* Call with no graph loaded and verify error message
* See if we can produce an out of memory error

        
### get_subgraph([variable names : string]) 
Returns any factor that uses any of the associated variables, and all variables needed by those factors as a Graph

### Input : Array of variable names ([string])

#### Potential Responses
* Success: Graph structure which contains the subgraph
* Error: 
    * Not Found - one or more variables doesn't exist
    * Internal Error
        * Out of memory?
        * Unable to get read lock?

#### General processing steps:
* Establish read lock on graph
* Identify all factors that contain each variable in the string array passed in
* For each factor:
    * add all variables to a "variables" structure (only once!)
    * add all factors to a "factor" array
* Consolidate the variables and factors into a single factor graph response
* Release read lock on graph
* Return result


#### Key Testing Scenarios
* Call with existing graph in memory with a variety of values:
    * no variables
    * one variable
    * multiple variables
    * One of multiple variables doesn't exist
* Benchmark performance with large factor graphs


### get_variables(Option([variable names]))  
Returns either the variables requested in the array, or all of the variables in the graph if Option is none

### Input : Optional : Array of variable names ([string])

#### Potential Responses
* Success: A Variables structure with all requested variable (if included in the request)
* Success: A Variables structure with all variables in the graph
* Error:  
    * Not Found if a variable is not in the graph but was included in the list
    * Not Found if the graph is empty
    * Internal Error?
        * Out of Memory?
        * Unable to get read lock on graph

#### General Processing Steps

* Get a read lock on the graph
* If list of variables is in the request:
    * For each variable in the request, build a Variables structure with each variable from the graph
    * Release read lock on graph
    * Return newly created Variable structure
* If no list of variables in the request:
    * Release read lock on graph
    * Return Variable structure from main graph

#### Testing Scenarios
* Get all variables
* Get all variables when the graph is empty
* Input data is not an array 
* Input data is not strings
* Get variables with a list
    * Small list
    * Large list
    * List with some invalid variables



### get_factor([array of variable names]) - 
Returns a single factor as a mini factor graph (factor, variables)   

#### Input: Factor_Name (Array of variable names) 

#### Potential Responses
* Success: A Graph structure with the requested factor
* Error:
    * Not Found
    * Internal Error?
        * Out of Memory?
        * Unable to get read lock on graph

#### General Processing Steps
* Get a read lock on the graph
* Locate factor on graph by factor_name
* Create variables structure
* For each variable in the factor graph
    * Add variable from graph's variable list to new variables structure
* Consolidate the variable and factor into a single factor graph response
* Release read lock on graph
* Return result

#### Testing Scenarios
* Get Factor (Found)
* Get Factor (Not Found)
* Ensure all factors returned are valid (well formed matrices and existing variables)
* Benchmark with large graph


### get_factor_names() - 
Returns all Factor Names in the graph as an array [] of factor names: example [["wet","sprinkler","rain"],["sprinkler","rain"]]

#### Input: None

#### Potential Responses
* Success - An array of factor names
* Error
    * Not found if factor graph is empty
    * Internal Error?
    * Internal Error?
        * Out of Memory?
        * Unable to get read lock on graph

#### General Processing Steps
* Get read lock on graph
* Create empty response
* For each factor in the factors array:
    * Add "variables" array to new response
* Release read lock on graph
* Return result

 #### Testing Scenarios
* Get Factor Names (Found)
* Get Factor Names (Empty graph = Not Found)
* Benchmark with large graph


### get_variable_names()
Returns all variables in the graph as an array of variable names

#### Input: None

#### Potential Responses
* Success - An array of variable names
* Error
    * Not found if factor graph is empty
    * Internal Error?
        * Out of Memory?
        * Unable to get read lock on graph

#### General Processing Steps
* Get read lock on graph
* Create empty response
* For each variable  in the variables structure:
    * Add variable name to new response
* Release read lock on graph
* Return result

 #### Testing Scenarios
* Get Variable Names (Found)
* Get Variable Names (Empty graph = Not Found)
* Benchmark with large graph

#### add_variable([Variable])  
Adds a new variable(s) to the graph

#### Input: Array of Variable structures

#### Potential Responses
* Success - Variable added, no content in the response
* Error
    * Variable Already Exists - If any variable in the list already exists, add no variables and return error
        * Potentially specify which of the variables already exists?
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* For each variable, verify variable name does not exist in current "variables" structure
    * Return Duplicate Value Error if already found
* Write Lock Current Graph - Return Internal Error if unable to get lock
* Add each new variable to "variables" structure
* Unlock Current Graph - Return Internal Error if unable to release lock
* Return OK

#### Testing Scenarios
* All variables are new (OK)
* Some variables are new (Error- Duplicate Value)
* Benchmark with large graph

### add_factor([factor]) 
Adds new factor(s) to the graph. 


#### Input : Array of Factor structures

#### Potential Responses
* Success - No content in response
* Error
    * Validation - Add no factor and return error response
        * Factor already exists (include list of existing factors?)
        * Missing Variable (include list of missing variables?)
        * Invalid Matrice
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* Verify Factor(s) - For Each Factor
    * Factor does not already exist
    * Variables exist in "variables" structure
    * Matrice structure is well formed for the Factor
* Obtain Write lock on Graph
* For each factor:
    * Add factor to "factors" array
* Release Write lock on graph
* Return Success

#### Testing Scenarios
* Happy Path:  Factors don't already exist, all variables exist, and Matrice structure well formed
* Unhappy Path: 
    * Factor already exists
    * Missing Variables
    * Matrice not well formed
    * Overflow available space?
* Tests should include one, two, or more variations of potential unhappy path scenarios


### delete_variable([variable name]) 
Remove variable from graph This will fail if there's still a factor in the graph which uses the variable.  Delete factors first

#### Input  - Array of Variable Names (String)

#### Potential Responses
* Success - All variables removed from graph, no response content
* Error
    * Validation Error
        * Factors still exist which use this variable (Variable still in use Error)
        * Not Found - Variable does not exist
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* For each variable name:
    * Verify variable name exists in "variables" structure
    * Verify no other factors exist which use this variable
* Obtain write lock on graph    
* Remove variable structure from "variables"
* Release write lock on graph
* Return Success

#### Testing Scenarios
* Happy Path - No other factors use this variable
* Unhappy Path
    * variable name doesn't exist
    * variable is still in use by another factor
    * null values
* Testing should contain single variable names, and multiple variable names with different situations (doesn't exist, still in use, etc.)


### delete_factor([factor name]) 
Removes factor(s) from the graph.

#### Input: Array of Factor Names 

#### Potential Responses
* Success - All factors removed.  No content in respose
* Error
    * Validation Error
        * Factor Not Found
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* For each Factor Name in input:
    * Verify Factor exists in graph
* Get Write lock on graph
* For each Factor Name in input:
    * Remove the factor from the factors array
* Release write lock on the graph

#### Testing Scenarios
* Happy Path: All factors exist
* Unhappy Path
    * Factor does not exist
    * One of many factors does not exist
    * Factor graph is empty


### update_variable([variable])  
Updates variables in the graph.  If the number of possible values has changed, will fail.   Use update_subgraph instead.

#### Input: Array of Variable structures

#### Potential Responses
* Success - Variable updated, no content in the response
* Error
    * Variable signature changed - If any variable in the list has changed the count of possible values, update no variables and return an error
        * Potentially specify which of the variables has a count mismatch?
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* For each variable, verify variable name exists in current "variables" structure
    * Return Not found error if it doesn't exist
    * Return Variable Signature Mismatch Error if count of possible options is different 
* Write Lock Current Graph - Return Internal Error if unable to get lock
* Update each variable on "variables" structure
* Unlock Current Graph - Return Internal Error if unable to release lock
* Return OK

#### Testing Scenarios
* All variables are able to be updated
* Variable(s) don't exist
* Some variables are new (Error- Not Found)
* Some variables change count of possible options (Variable Signature Mismatch)
* Multiple combinations of the above 2 testing scenarios to ensure quality
* Benchmark with large graph




### update_factor([factor]) - 
Updates factors in the graph.

#### Input : Array of Factor structures

#### Potential Responses
* Success - No content in response
* Error
    * Validation - update no factor and return error response
        * Factor doesn't already exists (include list of missing factors?)
        * Missing Variable (include list of missing variables?)
        * Invalid Matrice
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* Verify Factor(s) - For Each Factor
    * Factor exists
    * Variables exist in "variables" structure
    * Matrice structure is well formed for the Factor
* Obtain Write lock on Graph
* For each factor:
    * find the factor by matching "variables" array
    * update the factor with the new values
* Release Write lock on graph
* Return Success

#### Testing Scenarios
* Happy Path:  Factors already exist, all variables exist, and Matrice structure well formed
* Unhappy Path: 
    * Factor missing from graph
    * Missing Variables
    * Matrice not well formed
    * Graph has been reset (whole graph missing)
* Tests should include one, two, or more variations of potential unhappy path scenarios

### update_subgraph(subgraph)
Updates a portion of the graph, includes factors and associated variables.  Will add/update variables and factors as long as the end result creates a valid factor graph

#### Input - Graph structure to update

#### Potential Responses
* Success - No response content
* Error
    * Validation
        * Missing Variable(s)
        * Variable changes do not include all Factors (if number of values is changing)
        * Factor matrices not well formed
    * Internal Error?
        * Out of Memory?
        * Unable to get write lock on graph

#### General Processing Steps
* Validate incoming graph
* Get write lock on current graph
* Take copy of existing graph
* Merge incoming variables to copy of existing "variables" structure
* Merge incoming factors to copy of existing factors
    * add new factors if factor does not already exist
* Validate new copy of factor graph
* If valid:  
    * Replace existing graph with copied graph
    * Release lock on graph
* If invalid:  
    * Release lock on graph (no changes)
    * Return error "Merge would create invalid graph" (and pass back associated validation errors)

#### Testing Scenarios
* Invalid Input
    * Invalid Factor Graph (all defined validation testing scenarios)
        * Not a factor graph
        * Missing variables
        * Poorly formed matricies
    * variable changes (size of options)
        * all changed factors not in new graph
* Valid/Invalid merged graph (all defined validation testing scenarios)


