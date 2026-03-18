# Tech Steering

## Database
- PostgreSQL 15+ (prefer latest stable)
- Extensions: `uuid-ossp` or `pgcrypto` for UUID generation, `pg_stat_statements` for query analysis
- Connection pool: HikariCP (Java), asyncpg (Python), pgBouncer for connection multiplexing at scale

## Migration tooling
- Flyway (Java projects) or Alembic (Python projects)
- Migrations run automatically on deploy or as a pre-deploy step
- Every migration has a corresponding rollback script or is designed to be backward-compatible

## Monitoring
- `pg_stat_statements` enabled for slow query identification
- `pg_stat_user_tables` for table bloat and dead tuple monitoring
- Connection pool metrics exposed to Prometheus/Grafana
- Alerting on: replication lag, connection pool exhaustion, long-running transactions, table bloat

## Backup and recovery
- Automated daily backups with point-in-time recovery (PITR)
- WAL archiving enabled for continuous backup
- Test restore procedure quarterly — untested backups are not backups
