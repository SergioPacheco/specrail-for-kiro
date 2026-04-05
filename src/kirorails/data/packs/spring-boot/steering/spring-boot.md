---
inclusion: fileMatch
fileMatchPattern: ["**/*.java", "**/pom.xml", "**/build.gradle", "**/application*.yml", "**/application*.properties"]
description: Spring Boot 3.x specific patterns and conventions
---

# Spring Boot Overlay

## Stack
- Java 17+, Spring Boot 3.x, Spring Data JPA, Spring Security
- Embedded Tomcat, Actuator for health/metrics
- Flyway for migrations, HikariCP for connection pool

## Conventions
- Constructor injection only — never `@Autowired` on fields
- `@ConfigurationProperties` with `@Validated` for typed config — avoid raw `@Value`
- `ResponseEntity` from controllers for explicit status codes
- `@Transactional(readOnly = true)` for read-only service methods
- `ProblemDetail` (RFC 7807) for error responses
- Central `@ControllerAdvice` for all exception handling

## Testing
- `@WebMvcTest` for controller tests (mocked service)
- `@DataJpaTest` for repository tests (Testcontainers, not H2)
- `@SpringBootTest(webEnvironment = RANDOM_PORT)` for full integration
- Never use H2 — it hides PostgreSQL-specific behavior

## Feedback loops
```bash
mvn compile
mvn test
mvn checkstyle:check
```

## Security
- `SecurityFilterChain` bean config (not `WebSecurityConfigurerAdapter`)
- JWT: `spring-boot-starter-oauth2-resource-server`
- CORS: configure in `SecurityConfig`, never `@CrossOrigin` everywhere
- Disable Actuator sensitive endpoints in production or secure behind auth
