# Tasks — [Bug Title]

## Task list

### Task 1: Write regression test
- **Description:** Create a test that reproduces the bug and currently fails
- **Files:**
- **Done criteria:**
  - [ ] Test fails with the current bug present
  - [ ] Test clearly documents the expected behavior
- **Commit:** <!-- e.g., test(module): add regression test for #123 -->

### Task 2: Implement fix
- **Description:** Apply the minimal fix for the root cause
- **Files:**
- **Done criteria:**
  - [ ] Regression test now passes
  - [ ] All existing tests still pass
  - [ ] No unrelated changes included
- **Commit:** <!-- e.g., fix(module): resolve null pointer in user lookup -->

### Task 3: Verify and update state
- **Done criteria:**
  - [ ] CHANGELOG_AI.md updated
  - [ ] DECISIONS.md updated if architectural choice was made
  - [ ] RISKS.md updated if new risk was identified
- **Commit:** <!-- e.g., docs(state): update changelog for bugfix #123 -->

## Execution order
1. Task 1 — regression test first
2. Task 2 — fix
3. Task 3 — state update

## Notes
- Each task = one atomic commit
