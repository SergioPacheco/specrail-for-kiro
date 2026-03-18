# Security Steering

## Access control
- Application connects with a dedicated database user, not `postgres` superuser
- Principle of least privilege: app user gets `SELECT, INSERT, UPDATE, DELETE` on app tables only
- Migration user is separate from app user — has `CREATE, ALTER, DROP` permissions
- Never grant `SUPERUSER` or `CREATEDB` to application accounts

## Data protection
- Encrypt sensitive columns at the application level (not just TLS in transit)
- Use `pgcrypto` for database-level encryption when needed
- PII columns: consider column-level encryption or tokenization
- Enable SSL/TLS for all database connections (`sslmode=verify-full`)

## SQL injection prevention
- Parameterized queries only — enforced by ORM and code review
- Native queries: always use bind parameters (`:param` or `$1`)
- If you see string concatenation in a query — that's a critical security bug

## Audit logging
- Enable `pgaudit` extension for DDL and sensitive DML logging
- Application-level audit: `created_by`, `updated_by` columns on sensitive tables
- Log all schema changes with who, when, and why (migration commit messages)

## Backup security
- Encrypt backups at rest
- Restrict access to backup storage (S3 bucket policy, IAM roles)
- Audit access to production database and backups
