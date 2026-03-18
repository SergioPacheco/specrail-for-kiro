# Testing Steering

## Test strategy
- Unit tests: service layer with mocked repositories
- Integration tests: full request cycle via `httpx.AsyncClient` + Testcontainers
- Migration tests: Alembic upgrade/downgrade against real PostgreSQL

## Coverage expectations
- New service functions: 80%+ branch coverage
- Bug fixes: regression test that fails without the fix
- Refactoring: existing tests pass without modification
- New endpoints: at least one happy path + one error case

## Test structure
```python
# tests/test_users.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_returns_201(client: AsyncClient):
    response = await client.post("/api/v1/users", json={
        "email": "<email>",
        "name": "<name>",
    })
    assert response.status_code == 201
    assert response.json()["email"] == "<email>"

@pytest.mark.asyncio
async def test_create_user_rejects_invalid_email(client: AsyncClient):
    response = await client.post("/api/v1/users", json={
        "email": "not-an-email",
        "name": "<name>",
    })
    assert response.status_code == 422
```

## Fixtures
```python
# tests/conftest.py
@pytest.fixture
async def client(app, db_session):
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
```

## Database tests
- Use Testcontainers with same PostgreSQL version as production
- Alembic migrations run in test setup
- Each test gets a clean transaction (rollback after test)

## What NOT to test
- FastAPI/Pydantic validation internals
- SQLAlchemy ORM behavior (cascade, lazy loading)
- Third-party library internals
