---
title: Code Quality
impact: MEDIUM
tags: python, typing, naming, logging, environment, testing
---

# Code Quality

Naming, typing, environment variables, logging, and testing conventions.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | snake_case | `user_service.py`, `database.py` |
| Classes | PascalCase | `UserService`, `UserCreate` |
| Functions / methods | snake_case | `get_by_id()`, `create_user()` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE`, `DEFAULT_ROLE` |
| Variables | snake_case | `user_count`, `db_client` |
| Pydantic models | PascalCase + suffix | `UserCreate`, `UserResponse`, `UserDB` |
| Routers | resource name | `users.py`, `documents.py` |
| Services | resource + `_service` | `user_service.py` |

## Type Hints — Required Everywhere

All functions must have full type annotations. Never use `Any`.

```python
# BAD
def get_user(user_id):
    ...

# GOOD
async def get_user(user_id: str) -> UserResponse | None:
    ...
```

Use Pydantic models for all structured data. Raw `dict` types are only acceptable for low-level MongoDB operations.

```python
# BAD — returns untyped dict
async def create_user(data: dict) -> dict: ...

# GOOD — Pydantic in, Pydantic out
async def create_user(data: UserCreate) -> UserResponse: ...
```

## Environment Variables

Use `pydantic-settings` for config. Never hardcode secrets, URIs, or database names.

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "myapp"
    API_KEY: str = ""              # no default for secrets
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

Rules:
- Commit `.env.example` with placeholder values — never commit `.env`
- Prefix public values with descriptive names
- No secrets in default values

## Logging

Use Python's `logging` module, never `print()` in production code.

```python
import logging

logger = logging.getLogger(__name__)

async def create_user(data: UserCreate) -> UserResponse:
    logger.info("Creating user: %s", data.email)
    try:
        result = await db.users.insert_one(data.model_dump())
        logger.info("User created: %s", result.inserted_id)
    except Exception:
        logger.exception("Failed to create user: %s", data.email)
        raise
```

Configure logging level via environment:

```python
import logging
logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
```

## Testing

Use `pytest` + `pytest-asyncio` + `httpx` for async test support:

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

```python
# tests/test_users.py
import pytest

@pytest.mark.anyio
async def test_list_users(client):
    response = await client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Rules:
- One test file per router/service
- Use a separate test database (set `DATABASE_NAME` to `myapp_test`)
- Clean up test data in fixtures

## Import Order

Follow the standard Python convention:

```python
# 1. Standard library
import logging
from datetime import datetime

# 2. Third-party
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# 3. Local application
from app.config import settings
from app.models.user import UserCreate
```

Reference: https://fastapi.tiangolo.com/tutorial/ | https://docs.python.org/3/library/logging.html

