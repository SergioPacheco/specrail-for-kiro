# Brownfield Patterns

## Before touching legacy code

1. Map the codebase first — understand existing patterns, dependencies, and test coverage
2. Read `.kiro/state/CODEBASE.md` if it exists
3. Check `.kiro/skills/` for patterns the team has already documented

## Rules for brownfield work

- **Respect existing patterns** — match the style already in the codebase, even if you'd do it differently
- **Characterization tests first** — before modifying legacy code, add tests that capture current behavior
- **Small blast radius** — prefer many small changes over one big refactor
- **Flag shared code** — anything used by multiple modules gets higher risk score
- **Migration safety** — database changes must be backward-compatible and have rollback plans
- **No big-bang rewrites** — incremental improvement, one task at a time

## Risk scoring for brownfield

| Factor | +1 point each |
|--------|---------------|
| Touches shared/core code | Code used by multiple modules |
| Database changes | Schema migration, data migration |
| External integration | API calls, message queues, third-party services |
| No existing tests | Area has low or no test coverage |
| >3 files modified | Larger blast radius |

Score 4-5 = HITL recommended. Score 1-2 = safe for autonomous execution.
