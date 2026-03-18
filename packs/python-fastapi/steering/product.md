# Product Steering

## Description
Python REST API application built with FastAPI. Async-ready, type-safe, and designed for production.

## Key users
- Frontend clients (SPA, mobile) consuming REST APIs
- Other backend services via internal APIs
- DevOps teams managing deployment and monitoring

## Core constraints
- API contracts versioned via URL prefix (`/api/v1/`, `/api/v2/`)
- All responses use consistent Pydantic models — no raw dicts in responses
- Backward compatibility for at least one major version
- Health endpoint always available at `/health`
- Configuration via environment variables — no hardcoded values

## Business rules
- Monetary values: `Decimal`, never `float`
- Soft-delete for user-facing entities (`deleted_at: datetime | None`)
- Audit trail for state-changing operations
- Dates stored as UTC, returned as ISO 8601
- Business logic in service layer, never in route handlers

## Out of scope
- Django migration — this is a FastAPI project
- Synchronous-only patterns — embrace async where it makes sense
