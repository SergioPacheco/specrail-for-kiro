# Product Steering

## Description
Application with PostgreSQL as the primary data store. Data integrity and migration safety are top priorities.

## Core constraints
- Zero data loss — all schema changes must be reversible or have a rollback plan
- No downtime migrations — prefer backward-compatible changes that work with old and new code simultaneously
- All schema changes go through migration scripts — never manual DDL in production
- Data migrations (backfills) are separate from schema migrations
- Foreign keys and constraints are enforced at the database level, not just in application code

## Business rules
- Monetary values: `NUMERIC(19,4)`, never `FLOAT` or `DOUBLE PRECISION`
- Soft-delete: `deleted_at TIMESTAMP` column, never `DELETE FROM` for user-facing entities
- Audit columns on every table: `created_at`, `updated_at`, `created_by`, `updated_by`
- Timestamps stored as `TIMESTAMPTZ` (with timezone), always UTC
- UUIDs for public-facing IDs, sequences for internal PKs
