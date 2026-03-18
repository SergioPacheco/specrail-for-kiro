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

## Feedback loops

Never commit without running feedback loops. The more loops you give the AI, the higher quality code it produces.

### Required loops (run after every task)
```bash
# Compilation / type checking — catches type errors, missing imports
mvn compile                 # Java
npm run typecheck           # TypeScript

# Tests — catches broken logic, regressions
mvn test                    # Java
npm test                    # Node.js

# Linting — catches style violations, potential bugs
mvn checkstyle:check        # Java
npm run lint                # TypeScript/JavaScript
```

### Rules
- Do NOT commit if any feedback loop fails. Fix issues first.
- Run loops after each task, not at the end of a batch
- If a loop is slow (>2 min), consider running a focused subset during development and full suite before commit
- Pre-commit hooks are the last line of defense — configure them to block bad commits

### Why this matters
AI agents amplify what they see. If feedback loops catch errors early, the agent learns to avoid them. If errors slip through, the agent copies the broken patterns. Tight feedback loops = higher quality code.

## Explicit quality

Tell the AI what kind of codebase this is. Without explicit guidance, it will default to prototype-quality code.

### For production code
This codebase is production software with real users. Every shortcut becomes someone else's burden. Every hack compounds into technical debt. Follow existing patterns. Add tests. Handle errors. Log meaningfully.

### The repo wins
Your instructions compete with your codebase. When the AI explores your repo, it sees two sources of truth: what you told it to do and what you actually did. The codebase always wins. Keep your codebase clean before letting the AI loose — it will amplify whatever patterns it finds.

## Atomic commits

Each task in a spec maps to exactly one git commit. This keeps history clean, enables `git bisect`, and makes each change independently revertable.

### Clean state rule

Every commit must leave the codebase in a mergeable state. No half-implemented features, no broken builds, no failing tests. If you can't finish a task cleanly, revert and document why in PROGRESS.md.

Think of it as shift work: the next agent starts with zero memory. If you leave a mess, they'll waste their entire context window cleaning up instead of making progress.

### Markdown tampering protection

AI agents are more likely to inappropriately edit Markdown files than structured formats. To prevent this:

- Do NOT edit `tasks.md` except to mark done criteria checkboxes as `[x]`
- Do NOT remove, reorder, or rewrite tasks — the planner owns the task list
- Do NOT edit `requirements.md` or `design.md` during execution — those are the spec
- State files (PROGRESS.md, CHANGELOG_AI.md) are append-only during execution

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
