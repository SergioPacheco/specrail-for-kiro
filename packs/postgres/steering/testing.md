# Testing Steering

## Database test strategy
- Use Testcontainers with the same PostgreSQL major version as production
- Flyway/Alembic migrations run in test setup — validates migration scripts against real PG
- Never use H2 or SQLite as a test substitute — they hide PostgreSQL-specific behavior

## What to test
- Migration scripts: apply forward, verify schema, apply rollback, verify rollback
- Repository queries: test against real PostgreSQL with representative data
- Constraints: verify that invalid data is rejected at the DB level
- Indexes: `EXPLAIN ANALYZE` on critical queries to verify index usage
- Edge cases: NULL handling, empty strings, timezone conversions, numeric precision

## Test data
- Use factories/builders to create test data — never shared seed scripts between tests
- Each test class gets a clean database (Testcontainers per class or `@Transactional` rollback)
- For performance tests: generate realistic data volumes (10k+ rows)

## What NOT to test
- PostgreSQL internal behavior (CASCADE, trigger execution order)
- Flyway/Alembic framework behavior
- Connection pool configuration (test in staging, not unit tests)
