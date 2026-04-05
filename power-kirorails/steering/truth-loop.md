# Truth Loop — Verification

## After every task, verify:

1. **Feedback loops** — compile, test, lint must all pass (via `.kiro/hooks-exec/post-task.sh`)
2. **Done criteria** — each criterion in tasks.md must be objectively satisfied
3. **Regressions** — no unintended changes to files not listed in the task
4. **State files** — CHANGELOG_AI.md, DECISIONS.md updated if applicable
5. **Steering compliance** — changes follow coding-standards.md, testing.md, security.md
6. **Phantom detection** — verify tasks marked [x] have real implementation:
   - Check `git diff` for actually modified files
   - Compare against files listed in the task
   - Verify tests exist for changed behavior

## Phantom completion verdicts

| Verdict | Meaning |
|---------|---------|
| ✅ Real | Files changed, tests present, done criteria verifiable |
| ⚠️ Suspicious | Files changed but no tests, or trivial changes only |
| 👻 Phantom | Marked done but no corresponding code changes found |

A single 👻 Phantom = automatic FAIL.

## Atomic commits

One task = one commit. Format: `type(scope): description`

Types: feat, fix, refactor, test, docs, chore, migration

Every commit must leave the codebase in a mergeable state.
