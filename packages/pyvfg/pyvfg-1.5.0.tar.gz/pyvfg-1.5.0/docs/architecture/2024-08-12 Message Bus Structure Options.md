# Message Bus Message structure - Factor Graph Store

* Status: Proposed
* Deciders: GP-FGS team, GP-IFL team, GP-AI team, Darin Bunker, Lori Pike, Peter Provst
* Date: 2024-09-06

Technical Story: https://verses.atlassian.net/browse/GPFGS-16

## Context and Problem Statement

Identify a consistent message bus pattern for interacting with the Factor Graph Store

The Factor Graph Store will have to support numerous operations.   There are a few options for leveraging the message bus, this document is to identify a pattern which will work for consumers of the Factor Graph Store.

## Decision Drivers <!-- optional -->

* User Friendly
* Performance
* Potential for Error

## Considered Options

* [option 1] One topic per command.  A topic for get_graph, a separate topic for get_subgraph, etc
    * Responses written back to a topic specified by the caller.
* [option 2] One topic that suppports all commands.  Structure is "command, parameters".  
    * Responses written back to a topic specified by the caller.

## Decision Outcome

Chosen option: "[option 1]".  Provides the cleanest implementation, especially when working with binding tooling.  With the limited number of commands expected, this will be the easiest to implement.  Will re-evaluate if the number of commands becomes unruly.  


## Pros and Cons of the Options <!-- optional -->

### Option 1: [option 1]

Separate topics for each command. 

#### [option 1] is good, because
* Provides a clear separation of topics and commands
* Allows for each topic/command to have clearly defined parameters
* Allows for binding tooling to generate clear stubs 


#### [option 1] is bad, because
* Creates a larger amount of topics to listen to
* Creates a larger amount of maintenance ensuring the listen pattern is implemented consistently
* Requires a "thicker" layer over the Factor Graph Store core implementations

### Option 2: [option 2]

One topic that supports all commands. Writes back to a different topic upon response

#### [option 2] is good, because
* Minimal number of topics (2)
* Smaller code footprint for all command implementations

#### [option 2] is bad, because
* Not as clearly defined parameters.  Some parameters will need to be polymorphic
* Binding tooling difficult to use with polymorphic parameters
* Available "commands" and necessary "parameters" will need to be maintained outside of binding toolset

