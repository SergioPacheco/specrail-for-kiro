# 🐛 Bugfix — [Title]

## Bug Report

| Field | Value |
|-------|-------|
| Reported | <!-- YYYY-MM-DD --> |
| Severity | <!-- 🔴 Critical / 🟡 High / 🟢 Medium / ⚪ Low --> |
| Status | <!-- 🔄 Investigating / 🔧 Fixing / ✅ Fixed --> |

## Reproduction

**Steps:**
1. <!-- step -->
2. <!-- step -->

**Expected:** <!-- what should happen -->

**Actual:** <!-- what happens instead -->

**Environment:** <!-- OS, version, config that matters -->

## Root Cause

<!-- WHY it happens, not just WHERE. Trace the code path. -->

## Impact Assessment

- **Who is affected:** <!-- users, modules, other features -->
- **Data impact:** <!-- any corrupted data? -->
- **Workaround:** <!-- temporary fix available? -->

## Fix

- **Approach:** <!-- minimal change that fixes root cause -->
- **Files:** <!-- files to modify -->
- **Regression test:** <!-- test that fails without fix, passes with fix -->
- **Rollback:** <!-- how to revert if fix causes issues -->

## Tasks

### [ ] Task 1: Write regression test
- **Files:** <!-- test file -->
- **Done:** Test fails (reproduces the bug)
- **Commit:** `test(scope): add regression test for [bug]`

### [ ] Task 2: Implement fix
- **Files:** <!-- source files -->
- **Done:** Regression test passes, all existing tests pass
- **Commit:** `fix(scope): [description]`

## Feedback Loops

```bash
# Commands configured in .kiro/kirorails.conf
.kiro/hooks-exec/post-task.sh
```
