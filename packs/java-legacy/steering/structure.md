# Structure Steering

## Project layout
```
src/
├── main/
│   ├── java/com/company/project/
│   │   ├── controller/    ← REST endpoints, JSF backing beans
│   │   ├── service/       ← Business logic (transactional boundary)
│   │   ├── repository/    ← Database access (JPA repositories, DAOs)
│   │   ├── model/         ← JPA entities
│   │   ├── dto/           ← Data transfer objects (API input/output)
│   │   ├── mapper/        ← Entity ↔ DTO conversion
│   │   ├── config/        ← Framework configuration, beans
│   │   ├── exception/     ← Custom exceptions and error handlers
│   │   ├── util/          ← Stateless utility classes (keep minimal)
│   │   └── integration/   ← External service clients
│   ├── resources/
│   │   ├── db/migration/  ← Flyway migration scripts
│   │   ├── application.yml or application.properties
│   │   └── META-INF/
│   └── webapp/            ← JSF pages, static assets (if WAR)
└── test/
    ├── java/              ← Mirrors main structure
    └── resources/         ← Test configs, fixtures
```

## Module boundaries
- Controllers depend on services. Never on repositories directly.
- Services depend on repositories and other services. Never on controllers.
- Repositories depend only on models. Never on services or controllers.
- DTOs are separate from entities. Never expose JPA entities in API responses.
- Mappers are the only place where entity ↔ DTO conversion happens.
- Utility classes must be stateless. If it needs state, it's a service.

## Naming conventions
- Classes: `PascalCase` — `UserService`, `OrderRepository`, `PaymentDto`
- Methods/variables: `camelCase` — `findByEmail`, `isActive`
- Constants: `UPPER_SNAKE_CASE` — `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`
- Packages: `lowercase` — `com.company.project.service`
- Database tables: `snake_case` — `user_accounts`, `order_items`
- REST endpoints: `kebab-case` — `/api/v1/user-accounts`
- Migration files: `V{number}__{description}.sql` — `V015__add_email_index.sql`

## File placement rules
- New REST endpoint → `controller/` + corresponding `service/` method
- New business rule → `service/` (never in controller or repository)
- New database query → `repository/` (custom query in `@Query` or named query)
- New external API call → `integration/` with its own DTO and error handling
- New table or column → `model/` entity + `db/migration/` script
- New API input/output shape → `dto/` + `mapper/`
- Configuration class → `config/`
- Shared stateless helper → `util/` (but prefer putting logic in the service that uses it)
