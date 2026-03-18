# Tech Steering

## Language and runtime
- Java 11+ (LTS preferred: 11, 17, or 21)
- OpenJDK distribution (Temurin, Corretto, or vendor-provided)
- Target: Linux containers or bare-metal Linux servers

## Frameworks
- Web: JSF 2.x / Servlet-based (legacy) — new endpoints may use JAX-RS or Spring MVC
- Persistence: JPA/Hibernate — prefer JPQL over native queries unless performance requires it
- DI: CDI or Spring — follow whichever the project already uses, don't mix
- Validation: Bean Validation (JSR 380)

## Database
- PostgreSQL 12+ (prefer 15+)
- Migrations managed by Flyway (preferred) or Liquibase
- Connection pool: HikariCP
- All DDL changes go through migration scripts, never manual ALTER in production

## Build and packaging
- Maven 3.8+ (or Gradle if project already uses it — don't switch mid-project)
- Artifact: WAR (legacy) or fat JAR (Spring Boot)
- Docker image for deployment when possible
- CI builds must be reproducible — pin all plugin and dependency versions

## Key dependencies
- Logging: SLF4J + Logback (never `System.out.println` or `java.util.logging` directly)
- JSON: Jackson (prefer over Gson for consistency)
- HTTP client: Java 11 HttpClient or OkHttp (avoid Apache HttpClient in new code)
- Testing: JUnit 5 + Mockito + Testcontainers for integration tests
- Utilities: avoid adding Guava/Apache Commons for things Java 11+ stdlib handles

## Infrastructure
- Application server: Tomcat, WildFly, or embedded (Spring Boot)
- Reverse proxy: Nginx or cloud load balancer
- Secrets: environment variables or vault — never in source code or property files committed to git

## Deployment
- CI/CD pipeline (GitHub Actions, Jenkins, or GitLab CI)
- Environments: dev → staging → production
- Database migrations run automatically on startup (Flyway) or as a pre-deploy step
- Rollback strategy: previous artifact + rollback migration script

## Monitoring
- Structured logging (JSON format) with correlation IDs
- Health check endpoint (`/health` or `/actuator/health`)
- Metrics: Micrometer → Prometheus/Grafana or CloudWatch
- Alerting on: error rate spikes, response time P95, database connection pool exhaustion
