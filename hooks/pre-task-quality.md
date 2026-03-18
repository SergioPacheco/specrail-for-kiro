# Hook: Pre-Task Quality

## Trigger
Before starting execution of a task from a spec.

## What it checks

1. **Task has done criteria** — The task must have at least one specific, verifiable done criterion.

2. **Dependencies are met** — If the task depends on other tasks, verify those are marked complete.

3. **Risks are acknowledged** — If the task is flagged as risky in the spec, confirm the user is aware.

4. **Preconditions exist** — If the task requires a migration, config change, or external setup, verify it's in place.

## Actions

- If done criteria are missing, block and ask the user to define them.
- If dependencies are not met, warn and list what's pending.
- If risks exist, display them before proceeding.

## Output

```
## Pre-Task Check: [task title]

### Ready: YES | NO

### Checklist
- [x] or [ ] Done criteria defined
- [x] or [ ] Dependencies met
- [x] or [ ] Risks acknowledged
- [x] or [ ] Preconditions in place

### Blockers
- [list or "none"]
```
