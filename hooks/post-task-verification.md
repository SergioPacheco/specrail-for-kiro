# Hook: Post-Task Verification

## Trigger
After a task from a spec is marked as complete.

## What it checks

1. **Expected files changed** — Compare the files listed in the task with the files actually modified.

2. **Done criteria met** — Review each done criterion and check if it's satisfied.

3. **Tests exist** — If the task changed behavior, verify a test covers it.

4. **State files updated** — Check that CHANGELOG_AI.md has an entry for this task.

5. **No unintended changes** — Flag files that were modified but not listed in the task.

## Actions

- If expected files weren't changed, warn the user.
- If tests are missing for behavioral changes, block completion.
- If state files weren't updated, remind the user.
- If unintended files were changed, ask for justification.

## Output

```
## Post-Task Check: [task title]

### Verdict: PASS | NEEDS ATTENTION

### Files
- Expected: [list]
- Changed: [list]
- Unexpected: [list or "none"]

### Done criteria
- [x] or [ ] for each criterion

### State
- [ ] CHANGELOG_AI.md updated
- [ ] Other state files updated (if applicable)

### Issues
- [list or "none"]
```
