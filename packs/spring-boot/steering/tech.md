# Tech Steering

## Language and runtime
- Java 17+ (LTS: 17 or 21)
- Spring Boot 3.x (Spring Framework 6.x)
- OpenJDK (Temurin, Corretto, or GraalVM for native image)

## Core dependencies
- Web: `spring-boot-starter-web` (embedded Tomcat)
- Persistence: `spring-boot-starter-data-jpa` + Hibernate
- Validation: `spring-boot-starter-validation` (Jakarta Bean Validation)
- Security: `spring-boot-starter-security` + `spring-boot-starter-oauth2-resource-server` for JWT
- Configuration: `spring-boot-starter-actuator` for health/metrics

## Database
- PostgreSQL 15+ (or MySQL 8+ if project requires)
- Migrations: Flyway (`spring-boot-starter-flyway`)
- Connection pool: HikariCP (Spring Boot default)
- All schema changes via migration scripts — never manual DDL

## Build and packaging
- Maven 3.9+ or Gradle 8+
- Artifact: executable JAR (`spring-boot-maven-plugin`)
- Docker: multi-stage build, distroless or Eclipse Temurin base image
- Pin all dependency versions via Spring Boot BOM

## Key libraries
- Logging: SLF4J + Logback (Spring Boot default)
- JSON: Jackson (auto-configured by Spring Boot)
- HTTP client: `RestClient` (Spring 6.1+) or `WebClient` for reactive
- Testing: JUnit 5 + Mockito + Testcontainers + MockMvc
- Mapping: MapStruct (preferred) or manual mappers
- API docs: SpringDoc OpenAPI (`springdoc-openapi-starter-webmvc-ui`)

## Configuration
- `application.yml` for defaults, `application-{profile}.yml` for environment overrides
- Secrets via environment variables or Spring Cloud Config/Vault
- Use `@ConfigurationProperties` with `@Validated` for typed config — avoid raw `@Value`

## Deployment
- Container-based: Docker → Kubernetes or ECS
- Health: `/actuator/health` (liveness), `/actuator/health/readiness` (readiness)
- Graceful shutdown enabled (`server.shutdown=graceful`)
- Metrics: Micrometer → Prometheus or CloudWatch
