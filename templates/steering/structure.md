# Structure Steering

## Project layout
<!-- Describe the top-level directory structure -->
```
src/
├── main/
│   ├── java/
│   │   └── com/example/project/
│   │       ├── controller/
│   │       ├── service/
│   │       ├── repository/
│   │       ├── model/
│   │       ├── dto/
│   │       └── config/
│   └── resources/
└── test/
```

## Module boundaries
<!-- Which packages/modules can depend on which -->
- Controllers depend on services, never on repositories directly
- Services depend on repositories and other services
- Models are plain objects with no framework annotations in the domain layer

## Naming conventions
- Classes: `PascalCase`
- Methods/variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Database tables: `snake_case`
- REST endpoints: `kebab-case`

## File placement rules
- New endpoints go in `controller/`
- Business logic goes in `service/`
- Database queries go in `repository/`
- DTOs are separate from domain models
