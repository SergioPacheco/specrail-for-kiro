# PostgreSQL Steering

## Migration tool
<!-- e.g., Flyway, Liquibase -->

## Migration rules
- Every schema change is a versioned migration file
- Every migration must have a corresponding rollback script
- Never use `DROP` without confirming the rollback path
- Migrations run in a transaction when possible
- Test migrations against a copy of production data before deploying

## Naming conventions
- Tables: `snake_case`, plural (e.g., `user_accounts`)
- Columns: `snake_case` (e.g., `created_at`)
- Indexes: `idx_<table>_<columns>` (e.g., `idx_user_accounts_email`)
- Foreign keys: `fk_<table>_<referenced_table>` (e.g., `fk_orders_user_accounts`)
- Migration files: `V<number>__<description>.sql` (e.g., `V012__add_email_to_users.sql`)

## Query safety
- Always use parameterized queries
- Avoid `SELECT *` — list columns explicitly
- Add `LIMIT` to queries that could return unbounded results
- Use `EXPLAIN ANALYZE` on new queries touching large tables

## Schema change risks
- Adding a NOT NULL column without a default locks the table on large datasets
- Renaming columns breaks existing queries — prefer add + migrate + drop
- Index creation on large tables should use `CONCURRENTLY`

## Backup and recovery
- Document the backup strategy for the database
- Test restore procedures periodically
- Migration rollback scripts must be tested before deployment

## Performance
- Index columns used in WHERE, JOIN, and ORDER BY clauses
- Monitor slow query logs
- Avoid N+1 query patterns — use joins or batch fetching
