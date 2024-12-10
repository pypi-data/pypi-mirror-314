## "Unit" tests for database migrations

`migration.rs` contains unit tests for database migrations. These are run as part of the standard test suite, but will
create and delete directories. Every new directory is a new database, and while it *tries* to clean up, test failures
may cause this to be abnormally terminated. Please be sure to manually clean up your test databases, prefixed with
`test_db_` followed by a nanoid, every so often to preserve disk space.
