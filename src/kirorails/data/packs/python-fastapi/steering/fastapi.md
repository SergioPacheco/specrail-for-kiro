---
inclusion: fileMatch
fileMatchPattern: ["**/*.py", "**/pyproject.toml", "**/requirements*.txt"]
description: Python FastAPI specific patterns and conventions
---

# FastAPI Overlay

## Stack
- Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x async, Alembic
- uvicorn for ASGI, httpx for HTTP client, structlog for logging

## Conventions
- Type hints on all function signatures — no `Any` unless truly necessary
- `str | None` not `Optional[str]` (Python 3.10+ syntax)
- `async def` for I/O-bound handlers, `def` for CPU-bound
- `Depends()` for dependency injection — never instantiate services in handlers
- Separate Pydantic schemas for request and response: `CreateUserRequest`, `UserResponse`
- `pydantic-settings` for typed environment config

## Testing
- `pytest` + `pytest-asyncio` + `httpx.AsyncClient` for API tests
- Testcontainers for database tests (same PostgreSQL version as production)
- Alembic migrations run in test setup

## Feedback loops
```bash
mypy src/
pytest
ruff check src/
ruff format --check src/
```

## Security
- `Depends()` for auth injection — never check auth inside handler body
- CORS: configure in `main.py`, never `allow_origins=["*"]` in production
- Disable `/docs` and `/redoc` in production or secure behind auth
