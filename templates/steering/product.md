# Product Steering

## Product name
<!-- Replace with your product name -->

## Description
Enterprise Java application with established user base. Brownfield system under active maintenance and gradual modernization.

## Key users
- Internal business users (back-office operations)
- External customers via web interface (JSF/Servlet-based)
- System integrations via REST/SOAP APIs

## Core constraints
- Zero tolerance for data loss — all operations must be transactional
- No breaking changes to existing API contracts without versioning
- Must maintain backward compatibility with current client integrations
- Downtime windows are limited — prefer rolling deployments
- Regulatory/compliance requirements may restrict data handling

## Business rules
- All monetary values stored as `BigDecimal`, never `float` or `double`
- User deletion is always soft-delete (`active = false`, never `DELETE FROM`)
- Audit trail required for all state-changing operations on sensitive entities
- Date/time always stored as UTC, converted to user timezone only at presentation layer
- Business logic lives in the service layer, never in controllers or repositories

## Out of scope
- Full rewrite of the application
- Migration to a different language or framework in a single effort
- Greenfield microservices architecture (incremental extraction only)
