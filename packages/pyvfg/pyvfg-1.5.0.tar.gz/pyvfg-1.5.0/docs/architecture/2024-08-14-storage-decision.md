# Identify technology to use for persistent storage of the Factor Graph

* Status: proposed
* Deciders: gpfgs team, Darin Bunker, Lori Pike, Peter Probst
* Date: 2024-08-14

Technical Story: Identify technology to be used to persist the Factor Graph to permanent storage

## Context and Problem Statement

The Factor Graph will need to persist to permanent storage to survive process restarts.  The mechanism used to persist the factor graph should only have a minimal impact on performance. In addition, it should introduce as few dependencies as possible

## Decision Drivers <!-- optional -->

Hard requirements:
* Lightweight dependency (smallness)
* Performance 
* Zero copy (perf)
* Only needs key/value store (smallness)
* Lock free reads (perf)
* Disk persistence
* Embeddable
* Plays well with rust
* Established and stable

Nice to haves:
* Hashmap based (perf)
* Lock free writes (perf)

## Considered Options

* RocksDB
* LMDB
* Badger
* Sled
* Rust Hashmaps (Home grown)
* LevelDB
* redis
* dashmap

## Decision Outcome

LMDB is the best option for now, but we might want to consider writing our own key value store in the future
LMDB doesn't do lock free writes and doesn't do hashmaps, but it's the best option for now, I recommend we use LMDB only for persistent storage of data and use something like dashmap for indices (that we would rebuild on startup)


## Pros and Cons of the Options <!-- optional -->

### Option 1: RockDB

[RocksDB] (https://rocksdb.org/)
RocksDB was the underlying database for Genius Core. 

#### [option 1] is good, because
* We know it very well
* It plays well with Rust

#### [option 1] is bad, because
* Too slow for our purposes, tested to be 80x slower than lmdb on alexandria [branch] (https://github.com/VersesTech/alexandria/pull/339)
* Large dependency that takes a long time to compile and creates oversized executables

### Option 2: LMDB

[LMDB](https://dbdb.io/db/lmdb)
LMDB (Lightning Memory-Mapped Database) is a embedded database for key-value data based on B+trees. It is fully ACID transactional. The key features of LMDB are that it uses a single-level store based on memory-map files, which means that the OS is responsible for managing the pages (like caching frequently uses pages). It uses shared memory copy-on-write semantics with a single writer; readers do not block writers, writers do not block readers, and readers do not block readers. The system allows as many versions of data at any time as there are transactions (many read, one write). It also maintains a free list of pages to track and reuse pages instead of allocating memory each time.

We should be mindful of a few footguns that are easy to avoid with proper usage:
https://blogs.kolabnow.com/2018/06/07/a-short-guide-to-lmdb
we especially should consider a mechanism for shrinking the database

#### [option 2] is good, because
* Fits all our requirements

#### [option 2] is bad, because
* Doesn't have our nice to haves[argument a]

### Option 3: [option 3]

[BadgerDB](https://github.com/dgraph-io/badger)
BadgerDB is an embeddable, persistent and fast key-value (KV) database written in pure Go. It is the underlying database for Dgraph, a fast, distributed graph database. It's meant to be a performant alternative to non-Go-based key-value stores like RocksDB.

#### [option 3] is good, because
* It's being used to serve large datasets
* Checks most of the boxes

#### [option 3] is bad, because
* Doesn't play well with Rust



### Option 4: [option 4]

[SLED](https://github.com/spacejam/sled)


#### [option 4] is good, because
* Embeddable
* Key Value based

#### [option 4] is bad, because
* Not actively supported (last commit was over a year ago)
* Doesn't support many of the key features like zero copy


### Option 5: [option 5]

Rust Hashmaps (Home grown)
We can write our own Memory Mapped file and leverage Rust's built in Hashmap functions

#### [option 5] is good, because
* We own all the code
* We can directly tune for performance

#### [option 5] is bad, because
* We own ALL the code
* We have to figure out transactions, zero copy, lock free reads, etc. 


### Option 6: [option 6]

[LevelDB](https://dbdb.io/db/leveldb)
LevelDB is a key/value store built by Google. It can support an ordered mapping from string keys to string values. The core storage architecture of LevelDB is a log-structured merge tree (LSM), which is a write-optimized B-tree variant. It is optimized for large sequential writes as opposed to small random writes.)
We can write our own Memory Mapped file and leverage Rust's built in Hashmap functions

#### [option 6] is good, because
* Stable, well supported key value database
* Checks most of the boxes for requirements

#### [option 6] is bad, because
* Performance is a concern 
* Does not appear to support concurent reads


### Option 7: [option 7]

[Redis](https://redis.io/)

#### [option 7] is good, because
* Well known and stable Key Value database

#### [option 7] is bad, because
* Not embeddable


### Option 8: [option 8]

[DashMap](https://github.com/xacrimon/dashmap)
DashMap is an implementation of a concurrent associative array/hashmap in Rust.

#### [option 8] is good, because
* Potentially the fastest option
* Could be leveraged to build indexes upon chosen solution

#### [option 8] is bad, because
* Doesn't have disk persistence. 

