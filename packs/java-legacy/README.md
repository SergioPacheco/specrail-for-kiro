# Java Legacy Pack

## What this pack is for

Brownfield Java applications: 50k+ lines of code, layered architecture (controller/service/repository), JPA/Hibernate, PostgreSQL, Maven. Systems that are in production, have real users, and can't be rewritten from scratch.

## What gets installed

### Steering files
| File | What it provides |
|------|-----------------|
| `product.md` | Enterprise defaults: BigDecimal for money, soft-delete, audit trail, UTC dates |
| `tech.md` | Java 11+, PostgreSQL, Flyway, Maven, JUnit 5, Testcontainers, SLF4J |
| `structure.md` | Layered layout with strict dependency rules and file placement guide |
| `coding-standards.md` | Atomic commits, null safety, error handling, logging rules |
| `testing.md` | Testcontainers over H2, characterization tests for legacy code, regression-first bugfixes |
| `security.md` | Java-specific: bcrypt, XXE prevention, deserialization safety, OWASP dependency-check |
| `brownfield-java.md` | Migration rules, refactoring safety, legacy pattern preservation, review checklist |

### Agents
| Agent | Role |
|-------|------|
| `planner.md` | Clarify → risks → tasks, reads CODEBASE.md for existing patterns |
| `verifier.md` | Checks delivery against spec criteria, tests, state files |
| `bugfix-investigator.md` | Reproduce → root cause → regression test → fix |
| `codebase-mapper.md` | Scans existing code, produces structural map |
| `quick-change.md` | Lightweight path for small changes (≤ 3 files) |

### Hooks
| Hook | Trigger |
|------|---------|
| `on-spec-created.md` | Validates spec completeness on save |
| `pre-task-quality.md` | Checks preconditions before task execution |
| `post-task-verification.md` | Verifies task completion |
| `on-file-save-guardrails.md` | Checks migrations, security, models, config |

## When to use this pack

- Java 11+ applications with existing codebase
- Layered architecture (MVC, service/repository pattern)
- PostgreSQL database with migration scripts
- Teams that need to add features and fix bugs safely in legacy code
- Projects where "move fast and break things" is not acceptable

## When NOT to use this pack

- Greenfield projects (use `spring-boot` pack instead)
- Microservices with Spring Cloud (different patterns needed)
- Non-Java projects
- Projects with no database
