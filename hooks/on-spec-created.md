# Hook: On Spec Created

## Trigger
When a new spec is created or a spec file is saved in `.kiro/specs/`.

## What it checks

1. **Required sections present** — Verify the spec has all required sections from the template:
   - For features: summary, acceptance criteria, constraints
   - For bugfixes: reproduction steps, expected behavior, actual behavior, root cause

2. **Acceptance criteria are testable** — Each criterion should be specific and verifiable, not vague ("works correctly" is not acceptable).

3. **Risks identified** — If the spec touches database, shared code, or public APIs, a risks section must be present.

4. **Rollback strategy** — If the spec involves migrations or breaking changes, a rollback strategy must be documented.

## Actions

- If sections are missing, list them and suggest what to add.
- If acceptance criteria are vague, suggest more specific alternatives.
- If risks are missing for high-impact changes, warn the user.

## Output

```
## Spec Review: [spec name]

### Completeness
- [x] or [ ] for each required section

### Suggestions
- [list of improvements]

### Warnings
- [list of risks or missing elements]
```
