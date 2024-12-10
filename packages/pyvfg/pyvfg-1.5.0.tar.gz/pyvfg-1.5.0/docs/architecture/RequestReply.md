# NATS Calling Convention

* Status: proposed
* Deciders: [Jasmine Moore](mailto:jasmine.moore@verses.ai), [Richard Petty](mailto:richard.petty@verses.ai), [Lior Saar](mailto:lior.saar@verses.ai)
* Consultation: [Ben Fu](ben.fu@verses.ai), [Alex Kiefer](alex.kiefer@verses.ai)
* Date: 2024-10-08

Technical Story:
NATS is an asynchronous, one-way message bus. What is the best way to associate requests with responses?

## Context and Problem Statement

In order to very strongly decouple components across programming language boundaries, provide discovery, and allow for
variable cardinality of endpoints without the necessity of bespoke proxies per endpoint, it was decided to use a message
bus. On technical merits, NATS was the message bus chosen.

Many of our calls, however, are equivalent to remote procedure call invocations. As such, we need to associate requests
with the given reply. As NATS is as an asynchronous, one-way message bus, a HTTP invocation cannot be used here. What
is the best method?

## Decision Drivers

* Uses NATS
* Can receive responses
  * (ex: `get_graph` needs to get the graph!)
* Simple to implement
* Allow for indefinite runtimes

## Considered Options

1. Implement manually in client library
2. Use a correlation ID, managed in a request map for each client (similar to a NAT lookup table)
3. Use publish-with-reply, a NATS feature where each request has an associated reply topic that is manually-ephemeral
4. Use a request-reply pattern, where each request has an associated reply topic that is automatically-ephemeral from the caller's side

## Decision Outcome

We are going to use option 4, the request-reply pattern, because it is simplest to implement.

### Positive Consequences

* Using an in-built NATS feature reduces the maintenance burden
* Automatically ephemeral topics simplify the implementation of the client library
* Callees can use standard request-with-reply, so do not need significant modification

### Negative Consequences <!-- optional -->

* If we need a tracing header later for MLOps features, we'll need to implement it
  * But doing it as a header instead of part of dispatch simplifies the path of critical functionality.
  * Code should be able to ignore a tracing header; it would not be able to ignore a correlation ID

## Pros and Cons of the Options <!-- optional -->

### Option 1: Implement manually in client library

#### Manual implementation is good, because
* We have maximal control

#### Manual implementation is bad, because
* Code maintenance burden
* Code writing burden
* Need for testing

### Option 2: Correlation ID

This would have a dedicated "request" and "reply" channel pair per API, and responses would be differentiated by client ID.

#### Correlation ID is good, because
* It allows other components to "snoop" on a response, not just a request
* It allows for a "reply to all" feature

#### Correlation ID is bad, because
* It complicates the server library
* It greatly complicates the client library
* Increases the complexity of schemata and schema packaging
  * In some cases, it requires nested schemas and nested deserialization

### Option 3: Publish-With-Reply

NATS messages can have an optional reply topic, visible to called code. This is a NATS feature.

#### Publish-with-reply is good, because
* In-built NATS feature reduces code burden and testing burden
* Free-form reply topic allows for more complex interactions

#### Publish-with-reply is bad, because
* It complicates the client library by needing to set up and subscribe to a reply topic
* Cleanup of reply topics is necessary to avoid NATS resource exhaustion

### Option 4: Request-reply

Request-reply is a NATS client feature that automatically creates an ephemeral reply topic for each request.
It will create a reply topic, wait for a single response, delete the reply topic, then return the Result to the caller.
This is the same pattern as HTTP, but async over NATS.

#### Request-reply is good, because
* Very simple client library
* Server code is identical to option 3, so callers can use option 3 if needed

#### Request-reply is bad, because
* Single reply topic per request means that a single request can only have one reply

## Links

* [NATS Request-Reply](https://docs.nats.io/nats-concepts/core-nats/reqreply)
* [Example request-reply code in Rust](https://natsbyexample.com/examples/messaging/request-reply/rust)
* [Example conversion of Option 3 to Option 4](https://github.com/VersesTech/genius-agent-factor-graph/pull/34)
