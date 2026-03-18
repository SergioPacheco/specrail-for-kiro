# Hook: On File Save Guardrails

## Trigger
When a file is saved that matches critical paths (configurable per project).

## Critical paths (defaults)
- `**/migration/**`, `**/db/**` — database migrations
- `**/config/**`, `**/application*.yml`, `**/application*.properties` — configuration
- `**/security/**`, `**/auth/**` — security-related code
- `**/model/**`, `**/entity/**` — domain models

## What it checks

1. **Coding standards** — Does the saved file follow `.kiro/steering/coding-standards.md`?
   - No magic numbers
   - No swallowed exceptions
   - Proper logging

2. **Security rules** — For security-critical files:
   - No hardcoded credentials
   - Input validation present
   - Parameterized queries used

3. **Migration safety** — For database migration files:
   - Rollback script exists or is documented
   - No destructive operations without confirmation
   - `CONCURRENTLY` used for index creation on large tables

4. **Breaking change detection** — For public API or shared code:
   - Method signature changes flagged
   - Removed public methods flagged
   - Changed return types flagged

## Actions

- Display warnings inline for violations.
- For critical violations (hardcoded secrets, destructive migrations), block and require acknowledgment.

## Output

```
## File Save Check: [file path]

### Status: OK | WARNING | BLOCKED

### Checks
- [x] or [ ] Coding standards
- [x] or [ ] Security rules
- [x] or [ ] Migration safety (if applicable)
- [x] or [ ] Breaking changes (if applicable)

### Issues
- [list or "none"]
```
