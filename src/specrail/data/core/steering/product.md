---
description: Product context — what this project is, who uses it, business rules
inclusion: always
---

# Product Steering

## Product name
<!-- Replace with your product name -->

## Description
<!-- What does this product do? Who is it for? -->

## Key users
<!-- List the main user types and how they interact with the system -->

## Core constraints
- Zero tolerance for data loss — all operations must be transactional
- No breaking changes to existing API contracts without versioning
- Backward compatibility required for at least one major version

## Business rules
- All monetary values stored as `BigDecimal` / `Decimal`, never floating point
- Soft-delete for user-facing entities unless domain requires hard delete
- Audit trail for state-changing operations on sensitive entities
- Dates stored as UTC, converted to user timezone only at presentation layer
- Business logic lives in the service layer, never in controllers or repositories

## Out of scope
<!-- What this project is NOT doing -->
