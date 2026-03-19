---
description: Tech stack — language, frameworks, database, build, deployment
inclusion: always
---

# Tech Steering

## Language and runtime
<!-- e.g., Java 17+, Python 3.12+, TypeScript 5.x -->

## Frameworks
<!-- e.g., Spring Boot 3.x, FastAPI, Next.js -->

## Database
<!-- e.g., PostgreSQL 15+, MySQL 8+, MongoDB -->
- Migrations managed by a versioned tool (Flyway, Alembic, Prisma)
- All DDL changes go through migration scripts, never manual ALTER in production

## Build and packaging
<!-- e.g., Maven, Gradle, npm, uv -->
- Pin all dependency versions explicitly
- CI builds must be reproducible

## Deployment
- CI/CD pipeline with environments: dev → staging → production
- Rollback strategy documented for every release
- Health check endpoint available

## Monitoring
- Structured logging with correlation IDs
- Health check endpoint
- Alerting on error rate spikes and latency degradation
