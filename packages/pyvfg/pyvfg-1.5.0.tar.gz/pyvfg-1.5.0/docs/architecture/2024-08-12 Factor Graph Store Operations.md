# [short title of solved problem and solution]

* Status: Proposed
* Deciders: GP-FGS team, GP-IFL team, Darin Bunker, Lori Pike, Peter Provst
* Date: 2024-08-12

Technical Story: https://verses.atlassian.net/browse/GPFGS-5

## Context and Problem Statement

As a Factor Graph consumer, I need to interact with the Factor Graph Store in a number of ways.   The below operations are the "commands" that will be available to me when I'm building out my application and need to consume Factor Graphs.  


## Decision Drivers 

* Developer ease of use
* Avoid Redundant Operations
* 


## Decision Outcome

Behaviors to be allowed by this interface are:


* Full-graph operations
    * set_graph(graph) - Creates or replaces the entire graph with the one provided.
    * get_graph() - returns the whole graph

* Partial-graph operations
    * get_subgraph([variable names]) - returns any factor that uses any of the associated variables, and all variables needed by those factors
    * update_subgraph(subgraph) - Updates a portion of the graph, includes factors and associated variables

* Variable operations
    * get_variable_names() - returns all variables in the graph as na array of variable names
    * add_variable([variable]) - Adds a new variable to the graph
    * get_variables(Option([variable names])) - returns either the variables requested in the array, or all of the variables in the graph if Option is none
    * update_variable([variable]) - updates variables in the graph.  If the number of possible values has changed, will fail.   Use update_subgraph instead.
    * delete_variable([variable name]) - This will fail if there's still a factor in the graph which uses the variable.  Delete factors first

* Factor Operations
    * get_factor_names() - returns all factors in the graph as an array [] of factor names: example [["wet","sprinkler","rain"],["sprinkler","rain"]]
    * add_factor([factor]) - Adds a new factor to the graph. 
    * get_factor([array of variable names]) - returns a single factor as a mini factor graph (factor, variables)
    * update_factor([factor]) - updates factors in the graph.
    * delete_factor([factor name]) - Removes a factor from the graph.

Removed for now
* ~Metadata operations~
    * ~get_hyperparams()- needs more understanding :warning:~
    * ~update_hyperparams() - needs more understanding :warning:~

