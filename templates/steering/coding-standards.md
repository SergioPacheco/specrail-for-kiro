# Coding Standards Steering

## General rules
- No unused imports
- No commented-out code in production
- No magic numbers — use named constants
- Methods should do one thing and be under 30 lines when possible
- Prefer composition over inheritance

## Error handling
- Never swallow exceptions silently
- Use specific exception types, not generic `Exception`
- Log errors with context (what was being done, with what input)
- Return meaningful error responses to callers

## Null safety
- Avoid returning `null` — use `Optional`, empty collections, or domain-specific defaults
- Validate inputs at boundaries (controllers, public APIs)

## Logging
- Use structured logging (key-value pairs)
- Log at appropriate levels: ERROR for failures, WARN for recoverable issues, INFO for business events, DEBUG for troubleshooting
- Never log sensitive data (passwords, tokens, PII)

## Dependencies
- Pin dependency versions explicitly
- Avoid adding new dependencies without justification
- Prefer standard library solutions over third-party when equivalent

## Code review expectations
- Every change should be reviewable in under 15 minutes
- If a PR is too large, split it
- Include context in commit messages: what changed and why

## Atomic commits

Each task in a spec maps to exactly one git commit. This keeps history clean, enables `git bisect`, and makes each change independently revertable.

### Commit message format

```
type(scope): description
```

### Types
- `feat` — new feature or capability
- `fix` — bug fix
- `refactor` — code change that neither fixes a bug nor adds a feature
- `test` — adding or updating tests
- `docs` — documentation changes
- `chore` — build, config, tooling changes
- `migration` — database migration

### Rules
- One task = one commit
- Refactoring commits are separate from behavior-change commits
- Never mix unrelated changes in a single commit
- Commit message should be understandable without reading the diff
- Reference the spec or task when relevant: `feat(auth): add login endpoint [spec:user-auth/task-1]`
