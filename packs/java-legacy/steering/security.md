# Security Steering

## Authentication and authorization
- All endpoints require authentication unless explicitly annotated as public (`@PermitAll`, `@Public`)
- Use role-based access control (RBAC) at the endpoint level — `@RolesAllowed("ADMIN")`
- Never trust client-side authorization checks alone — always enforce server-side
- Session management: use HTTP-only, Secure cookies. Set reasonable timeout (30 min idle).
- Password storage: bcrypt with cost factor ≥ 12. Never MD5, SHA-1, or plain text.

## Input validation
- Validate all inputs at the controller/API boundary using Bean Validation (`@NotNull`, `@Size`, `@Pattern`)
- Reject unexpected fields — use DTOs with explicit fields, never bind directly to entities
- Sanitize any input that will be rendered in HTML (XSS prevention)
- File uploads: validate MIME type, enforce size limits, never trust the filename

## SQL injection prevention
- Use JPA/Hibernate parameterized queries exclusively
- Native queries: always use `?` or `:param` placeholders, never string concatenation
- If you see `"SELECT * FROM users WHERE id = " + userId` — that's a critical bug, fix immediately

## Secrets management
- Never commit secrets, tokens, API keys, or credentials to git
- Use environment variables or a secrets manager (Vault, AWS Secrets Manager)
- Database credentials: environment variables, never in `application.properties` committed to repo
- If a secret was accidentally committed: rotate it immediately, don't just delete the commit

## Dependency security
- Run `mvn dependency-check:check` (OWASP Dependency-Check) in CI
- Critical CVEs: patch within 7 days
- High CVEs: patch within 30 days
- Don't add dependencies without checking their maintenance status and known vulnerabilities

## Logging and audit
- Log: authentication events, authorization failures, data access to sensitive entities
- Never log: passwords, tokens, credit card numbers, PII (names, emails, CPF/SSN)
- Use structured logging with correlation IDs for request tracing
- Audit trail: who changed what, when, from which IP — for sensitive entities

## Common Java-specific pitfalls
- `@Transactional` on private methods does nothing — Spring proxies only intercept public methods
- Deserialization of untrusted data (Jackson `@JsonTypeInfo` with `enableDefaultTyping`) is a known RCE vector
- XML parsing: disable external entity processing (XXE) — `setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
- Random number generation for security: use `SecureRandom`, never `Math.random()` or `Random`
