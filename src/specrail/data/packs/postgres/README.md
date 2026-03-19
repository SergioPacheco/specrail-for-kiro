# PostgreSQL Pack

Stack: PostgreSQL 15+, Flyway migrations, query optimization, schema safety

This is a supplementary pack — use it alongside a language pack (java-legacy, spring-boot, python-fastapi). It adds database-specific steering for teams working heavily with PostgreSQL.

Includes opinionated steering for:
- Product: data integrity, migration discipline, zero-downtime schema changes
- Tech: PostgreSQL ecosystem, extensions, tooling
- Structure: migration file layout, naming, rollback conventions
- Coding standards: query patterns, indexing rules, transaction discipline
- Testing: database test strategy with Testcontainers
- Security: access control, encryption, audit logging
- Postgres-specific: advanced patterns, performance, operational rules
