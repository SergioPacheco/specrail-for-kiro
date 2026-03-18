# Coding Standards Steering

## Spring Boot idioms
- Use constructor injection, never field injection (`@Autowired` on fields)
- Use `@ConfigurationProperties` for grouped config, not scattered `@Value`
- Return `ResponseEntity` from controllers for explicit status codes
- Use `@Transactional(readOnly = true)` for read-only service methods
- Prefer `Optional` returns from repositories over null checks

## Error handling
- Central `@ControllerAdvice` with `@ExceptionHandler` for all error responses
- Custom exceptions extend a base `ApplicationException` with error code
- Never return stack traces in API responses — log them, return a clean error body
- Use `ProblemDetail` (RFC 7807) for error responses in Spring Boot 3.x

## REST conventions
- Use HTTP methods correctly: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE
- Return 201 + Location header for resource creation
- Return 204 for successful delete
- Pagination: `?page=0&size=20&sort=createdAt,desc` using Spring Data `Pageable`
- Filter/search: query parameters, not request body on GET

## Feedback loops

Never commit without running feedback loops.

### Required loops (run after every task)
```bash
mvn compile                    # Compilation
mvn test                       # Unit + integration tests
mvn checkstyle:check           # Style (if configured)
mvn spring-boot:run &          # Smoke test: does it start?
curl -s localhost:8080/actuator/health && kill %1
```

### Rules
- Do NOT commit if any feedback loop fails
- Run loops after each task, not at the end of a batch
- If tests are slow, run `mvn test -pl :module` for the affected module

## Explicit quality

This is production code. Follow Spring Boot conventions. Use auto-configuration where possible — don't fight the framework. The codebase patterns win over your preferences.

## Atomic commits

One task = one commit. Format: `type(scope): description`

Types: feat, fix, refactor, test, docs, chore, migration

### Clean state rule
Every commit must leave the app startable and tests passing. No broken builds between iterations.

### Markdown tampering protection
- Do NOT edit tasks.md except to mark checkboxes as `[x]`
- State files (PROGRESS.md, CHANGELOG_AI.md) are append-only
