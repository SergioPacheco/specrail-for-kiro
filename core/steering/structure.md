---
description: Project structure — directory layout, module boundaries, naming conventions
inclusion: always
---

# Structure Steering

## Project layout
<!-- Document your project's directory structure here -->

## Module boundaries
- Controllers/routes depend on services. Never on repositories directly.
- Services contain business logic. May call other services.
- Repositories handle data access only.
- DTOs/schemas are separate from domain models.

## Naming conventions
- Classes/types: `PascalCase`
- Functions/methods/variables: `camelCase` or `snake_case` (follow language convention)
- Constants: `UPPER_SNAKE_CASE`
- Database tables: `snake_case`
- REST endpoints: `kebab-case`
- Migration files: versioned with description

## File placement rules
- New endpoint → controller + service method
- New business rule → service layer (never in controller or repository)
- New database query → repository
- New external API call → dedicated client with its own error handling
- New table/column → model + migration script
