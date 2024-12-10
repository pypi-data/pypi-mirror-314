---
status: proposed
deciders: [Lori Pike](mailto:lori.pike@verses.ai), [Richard Petty](mailto:richard.petty@veses.ai)
date: 2024-10-13
---
# Consolidation of Genius Agent Components

* Status: proposed
* Deciders: [Lori Pike](mailto:lori.pike@verses.ai), [Richard Petty](mailto:richard.petty@veses.ai)
* Date: 2024-10-13

Technical Story: [SPIKE: Recommend simplification strategy for combining existing components](https://verses.atlassian.net/browse/GPAI-93)

## Context and Problem Statement

We have a lot of components and a lot of complexity for what should be a fairly straightforward process.

## Decision Drivers

* Needs swappable models
  * This means that a given VFG might need to be swapped out
* Needs swappable python implementations of models
  * This means the actual python code should be modifiable in as easy or easier than currently
  * Both user agents and Verses-supplied inference components are expected to be written in python
    * Julia is outside of requirements, but can be considered for "bonus points"
* Minimal disruption to the GPDE platform
  * Their work is KEY to user acceptance so we want to disrupt as little as possible
* Tracing capability preserved
* Agent explainability preserved
* Visualization capability preserved
* Remote graph editing capability preserved
* Reduce calling overhead for GPIL to ensure inference is fast

## Considered Options

* "Five-container" option: Do not combine. Run each component in its own container.
* "Two-container" option: Combine everything not in GPIL into a single container, running multiprocess
* "One-container" option: Combine everything, including GPIL, into a single container, running multiprocess
* "One-process" option: Combine everything into a single process.

## Decision Outcome

Proposed option: One-process option.

## Pros and Cons of the Options

### Option 1: Five-container

This would keep everything as it is now, with each component running in its own container.

#### Five-container is good, because
* Least amount of development work
* We're very close to done

#### Five-container is bad, because
* The factor graph has to be transmitted across a message bus, several times per call
* Orchestration pain
* Communication complexity is high

### Option 2: Two-container

This would combine all existing containers that are not GPIL into one container, and have GPIL run as a second container.

#### Two-container is good, because
* It keeps most of our existing code
* It allows for a swap of the GPIL container

#### Two-container is bad, because
* The factor graph has to be transmitted across a message bus, several times per call
* Communication complexity is high
* Orchestration pain is *just as high* as five-container

### Option 3: One-container

This would combine all containers into a single container.

#### One-container is good, because
* It keeps most of our existing code
* Lower orchestration pain than five-container

#### One-container is bad, because
* It does not allow for a swap of the GPIL container -- agent builder needs this
* The factor graph has to be transmitted across a message bus, several times per call
* Communication complexity is high, and unsolved

### Option 4: One-process

This would form the GPAI portion of the Genius Agent Framework as a python library, which would be useful here.
We would need to move the rust code to a python library, which would take about a day of work, and then two days
to ensure that our HTTP endpoints are compatible with the remainder of components.

Components in rust would remain in rust, with a python library wrapper to expose them to Python, as user inference components
and Verses-supplied GPIL modules will both be in python. Please see the [migration strategy](../migrations/2024-10-11%20Single-Process%20Migration%20Strategy.md) for more information.

#### One-process is good, because
* In-memory transmission of VFG is much more efficient
* Communication complexity is very low
* Orchestration pain is very low
* Significantly less code to maintain

#### One-process is bad, because
* In order to expose python code changes, we would need to make the library available
* This is a significant rewrite, touching on GPIL again
* We would be exposing HTTP directly from the python IL code; if the IL code does not load our library, we do not properly respond to requests.

## Links
- [Miro board](https://miro.com/app/board/uXjVLTpLzmY=/?share_link_id=127612028335)
- [Migration Strategy](../migrations/2024-10-11%20Single-Process%20Migration%20Strategy.md)
