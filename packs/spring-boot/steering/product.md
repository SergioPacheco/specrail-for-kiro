# Product Steering

## Description
Spring Boot REST API application. May be a standalone service or part of a larger system.

## Key users
- Frontend clients (SPA, mobile apps) consuming REST APIs
- Other backend services via internal APIs
- DevOps teams managing deployment and monitoring

## Core constraints
- API contracts are versioned — breaking changes require a new version (`/api/v2/`)
- All responses follow a consistent envelope or use standard HTTP semantics
- Backward compatibility is mandatory for at least one major version
- Health and readiness endpoints must always be available
- Configuration is externalized — no environment-specific values in code

## Business rules
- All monetary values use `BigDecimal`, never floating point
- Soft-delete for user-facing entities unless domain requires hard delete
- Audit trail for state-changing operations on sensitive resources
- Dates stored as UTC, returned as ISO 8601 with timezone offset
- Business logic in service layer, never in controllers or repositories

## Out of scope
- Monolith-to-microservices migration in a single effort
- Custom framework abstractions over Spring — use Spring idioms directly
