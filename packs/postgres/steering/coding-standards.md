# Coding Standards Steering

## Query patterns
- Use parameterized queries exclusively — never string concatenation
- Prefer specific column lists over `SELECT *`
- Use `EXISTS` instead of `COUNT(*) > 0` for existence checks
- Use `RETURNING` clause on INSERT/UPDATE/DELETE to avoid extra SELECT
- Limit result sets — always use `LIMIT` or pagination for user-facing queries
- Use CTEs (`WITH`) for readability, but be aware they're optimization fences in older PG versions

## Indexing rules
- Every foreign key column gets an index
- Columns used in `WHERE`, `JOIN`, `ORDER BY` frequently → index candidate
- Composite indexes: put the most selective column first
- Use partial indexes for filtered queries: `CREATE INDEX idx_active_users ON users(email) WHERE is_active = true`
- Don't over-index — each index slows writes. Justify every index with a query pattern.
- Use `EXPLAIN ANALYZE` to verify index usage before and after

## Transaction discipline
- Keep transactions short — long transactions hold locks and block vacuum
- Read-only operations: use `SET TRANSACTION READ ONLY` or `@Transactional(readOnly = true)`
- Avoid `SELECT ... FOR UPDATE` unless you truly need pessimistic locking
- Use advisory locks for application-level coordination, not table locks

## Migration safety
- Every migration must be backward-compatible with the currently deployed code
- Add columns as `NULL` first, backfill, then add `NOT NULL` constraint in a separate migration
- Never rename columns in a single migration — add new, migrate data, drop old (3 steps)
- Never drop columns that the current code still references
- Large data migrations: batch in chunks, don't lock the entire table
- Always test migrations against a copy of production data volume

## Feedback loops
```bash
# Run migrations against test database
flyway migrate -url=jdbc:postgresql://localhost:5432/testdb

# Validate migration checksums
flyway validate

# Run application tests (includes DB integration tests)
mvn test
```

### Rules
- Do NOT commit if migrations fail to apply cleanly
- Test rollback scripts before committing the forward migration
- Run `EXPLAIN ANALYZE` on new queries touching tables with >100k rows

## Atomic commits
One migration = one commit. Never bundle unrelated schema changes.

Format: `migration(scope): description` — e.g., `migration(users): add email uniqueness constraint`
