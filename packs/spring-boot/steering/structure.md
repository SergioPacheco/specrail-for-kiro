# Structure Steering

## Project layout
```
src/
├── main/
│   ├── java/com/company/project/
│   │   ├── config/          ← @Configuration, security config, CORS, OpenAPI
│   │   ├── controller/      ← @RestController endpoints
│   │   ├── service/         ← @Service business logic
│   │   ├── repository/      ← Spring Data JPA interfaces
│   │   ├── model/           ← @Entity JPA entities
│   │   ├── dto/             ← Request/response DTOs
│   │   ├── mapper/          ← Entity ↔ DTO (MapStruct or manual)
│   │   ├── exception/       ← Custom exceptions + @ControllerAdvice handler
│   │   └── client/          ← External service clients (RestClient wrappers)
│   └── resources/
│       ├── db/migration/    ← Flyway scripts
│       ├── application.yml
│       └── application-{profile}.yml
└── test/
    ├── java/                ← Mirrors main structure
    └── resources/
        └── application-test.yml
```

## Module boundaries
- Controllers: receive HTTP, validate input, delegate to service, return DTO. No business logic.
- Services: business logic, transaction boundaries (`@Transactional`). May call other services.
- Repositories: data access only. Custom queries via `@Query` or specifications.
- DTOs separate from entities — never expose `@Entity` in API responses.
- Exception handler (`@ControllerAdvice`) maps exceptions to HTTP responses centrally.

## Naming conventions
- Controllers: `UserController`, endpoints return `UserResponse`
- Services: `UserService`, methods describe business action (`createUser`, `deactivateAccount`)
- Repositories: `UserRepository extends JpaRepository<User, Long>`
- DTOs: `CreateUserRequest`, `UserResponse`, `UserSummary`
- Config: `SecurityConfig`, `CorsConfig`, `OpenApiConfig`
- Migrations: `V001__create_users_table.sql`
