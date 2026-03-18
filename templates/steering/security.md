# Security Steering

## Authentication and authorization
- All endpoints require authentication unless explicitly marked as public
- Use role-based access control (RBAC) at the endpoint level
- Never trust client-side authorization checks alone

## Input validation
- Validate all inputs at the API boundary
- Use allowlists over denylists
- Sanitize inputs that will be rendered in HTML or used in queries

## Secrets management
- Never hardcode secrets, tokens, or credentials in source code
- Use environment variables or a secrets manager
- Rotate secrets on a defined schedule

## SQL injection prevention
- Use parameterized queries or ORM-generated queries exclusively
- Never concatenate user input into SQL strings

## Dependency security
- Run dependency vulnerability scans in CI
- Update vulnerable dependencies within 7 days for critical CVEs

## Logging and audit
- Log authentication events (login, logout, failed attempts)
- Log authorization failures
- Never log passwords, tokens, or PII

## HTTPS and transport
- All external communication over HTTPS
- Internal service communication encrypted when crossing network boundaries
