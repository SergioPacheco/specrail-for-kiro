# Security Steering

## Authentication and authorization
- Use Spring Security with `SecurityFilterChain` bean configuration (not `WebSecurityConfigurerAdapter`)
- JWT validation: `spring-boot-starter-oauth2-resource-server` with `jwt` decoder
- Method-level security: `@PreAuthorize("hasRole('ADMIN')")` where needed
- CORS: configure explicitly in `SecurityConfig`, never `@CrossOrigin` on every controller

## Input validation
- `@Valid` on all `@RequestBody` parameters — Bean Validation catches malformed input before it reaches service layer
- Custom validators for complex business rules (`@Constraint` + `ConstraintValidator`)
- Reject unknown fields: `spring.jackson.deserialization.fail-on-unknown-properties=true`
- File uploads: validate MIME type, enforce size limits via `spring.servlet.multipart.max-file-size`

## SQL injection prevention
- Spring Data JPA parameterized queries by default — safe
- `@Query` with `:param` placeholders — safe
- String concatenation in native queries — critical bug, fix immediately

## Secrets management
- Never commit secrets to git
- Use environment variables: `${DB_PASSWORD}` in `application.yml`
- For complex setups: Spring Cloud Config + Vault or AWS Secrets Manager
- If a secret was committed: rotate immediately, don't just remove the commit

## Dependency security
- Run `mvn dependency-check:check` (OWASP) in CI
- Spring Boot manages most dependency versions via BOM — keep Boot version current
- Critical CVEs: patch within 7 days
- Subscribe to Spring Security advisories

## API security
- Rate limiting on public endpoints (use Spring Cloud Gateway or a reverse proxy)
- HTTPS only — redirect HTTP to HTTPS
- Security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`
- Disable Spring Boot Actuator sensitive endpoints in production or secure them behind auth
