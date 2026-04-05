# 📋 Tasks — [Feature Name]

## Progress Dashboard

| Metric | Value |
|--------|-------|
| Total Tasks | <!-- N --> |
| Completed | <!-- 0/N --> |
| Verification | <!-- ✅ All passed / ⚠️ Pending / ❌ Has failures --> |
| Risk Level | <!-- 🟢 Low / 🟡 Medium / 🔴 High --> |
| Execution Mode | <!-- HITL / AFK --> |

## Feedback Loops

Run after every task. Do NOT commit if any fail.

```bash
# Run after every task. Do NOT commit if any fail.
# Commands are configured in .kiro/kirorails.conf
.kiro/hooks-exec/post-task.sh
```

## Task List

<!-- Status key:
  [✅] — Done + verified (Truth Loop passed)
  [⚠️] — Done, pending verification
  [❌] — Verification failed
  [🔄] — In progress
  [ ]  — Not started
-->

### [ ] Task 1: [Title]
- **Risk:** <!-- 1-5 (1=low, 5=high) → reason -->
- **Description:** <!-- What to do — one thing only -->
- **Files:** <!-- Expected files to create/modify -->
- **Done criteria:**
  - [ ] <!-- e.g., Unit test passes -->
  - [ ] <!-- e.g., Migration runs without error -->
  - [ ] Feedback loops pass
- **Commit:** `<!-- e.g., feat(auth): add login endpoint -->`
- **Dependencies:** <!-- Other tasks that must be done first, or "none" -->

### [ ] Task 2: [Title]
- **Risk:** <!-- 1-5 → reason -->
- **Description:**
- **Files:**
- **Done criteria:**
  - [ ]
  - [ ] Feedback loops pass
- **Commit:** `<!-- -->`
- **Dependencies:**

<!-- Add more tasks as needed -->

## Execution Order

Tasks ordered by risk (highest first):

1. Task 1 — <!-- why first: architectural decision / integration point / spike -->
2. Task 2 — <!-- reason -->

## Verification Summary

<!-- Filled by the Truth Loop after verification -->

| Task | Status | Notes |
|------|--------|-------|
| Task 1 | <!-- ✅ / ⚠️ / ❌ --> | <!-- --> |
| Task 2 | <!-- ✅ / ⚠️ / ❌ --> | <!-- --> |

## Notes

- Each task = one Ralph iteration = one atomic commit
- If a task touches > 5 files, split it
- Never outrun your feedback loops
