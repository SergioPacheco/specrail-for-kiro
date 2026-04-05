# Sprint Management

## Backlog

Track requirements in `.kiro/specs/backlog.md`:

```markdown
| ID  | Requirement | Sprint | Status |
|-----|-------------|--------|--------|
| R01 | description | sprint-1 | ✅ Done |
| R02 | description | — | 🔲 Todo |
```

Status: 🔲 Todo, 🔄 In Progress, ✅ Done, ❌ Blocked, ⏭️ Deferred

## Sprints

Each sprint is a directory under `.kiro/specs/` with a `tasks.md` file.

```bash
kirorails sprint init                     # create backlog.md
kirorails sprint new sprint-1-foundation  # create sprint
kirorails sprint list                     # show progress
```

## Quick tasks

Skip the full planning flow for small, well-understood changes:

```bash
kirorails quick "Add CRUD for Product"
kirorails quick "Fix date format" --sprint sprint-2
```

## Progress

```bash
kirorails status    # consolidated dashboard
```
