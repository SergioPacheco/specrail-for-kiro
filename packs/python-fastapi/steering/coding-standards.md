# Coding Standards Steering

## Python idioms
- Type hints on all function signatures — no `Any` unless truly necessary
- Use `|` union syntax (Python 3.10+): `str | None` not `Optional[str]`
- Use `async def` for I/O-bound route handlers, `def` for CPU-bound
- Use `Depends()` for dependency injection — never instantiate services in route handlers
- Use `Enum` for fixed value sets, not magic strings

## Error handling
- Custom exception classes that map to HTTP status codes
- Central exception handler registered via `app.exception_handler()`
- Never return raw tracebacks in API responses — log them, return clean error body
- Use FastAPI's `HTTPException` for simple cases, custom exceptions for domain errors

## Pydantic patterns
- Separate request and response schemas: `CreateUserRequest`, `UserResponse`
- Use `model_validator` for cross-field validation
- Use `Field(...)` with descriptions for auto-generated API docs
- Never use `dict` as a response model — always a Pydantic schema

## Async patterns
- Use `async/await` for database queries (SQLAlchemy async session)
- Use `httpx.AsyncClient` for external HTTP calls
- Never use `time.sleep()` in async code — use `asyncio.sleep()`
- CPU-bound work: offload to thread pool via `asyncio.to_thread()` or task queue

## Feedback loops

Never commit without running feedback loops.

### Required loops (run after every task)
```bash
mypy src/                      # Type checking
pytest                         # Tests
ruff check src/                # Linting
ruff format --check src/       # Formatting
```

### Rules
- Do NOT commit if any feedback loop fails
- Run loops after each task, not at the end of a batch

## Explicit quality

This is production code. Follow FastAPI conventions. Use type hints everywhere. The codebase patterns win over your preferences.

## Atomic commits

One task = one commit. Format: `type(scope): description`

Types: feat, fix, refactor, test, docs, chore, migration

### Clean state rule
Every commit must leave the app startable and tests passing.

### Markdown tampering protection
- Do NOT edit tasks.md except to mark checkboxes as `[x]`
- State files (PROGRESS.md, CHANGELOG_AI.md) are append-only
