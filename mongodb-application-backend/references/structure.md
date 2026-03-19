---
title: Project Structure
impact: CRITICAL
tags: fastapi, python, folder-structure, organization
---

# Project Structure

Use a modular FastAPI layout. Each domain concern gets its own directory. Never put all code in a single file.

## Canonical Layout

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app factory, lifespan, middleware
│   ├── config.py              # Settings via pydantic-settings / dotenv
│   ├── database.py            # MongoDB client, connection, db reference
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py           # /api/users routes
│   │   ├── documents.py       # /api/documents routes
│   │   └── health.py          # /health, /readiness endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # Pydantic models: UserCreate, UserResponse, UserDB
│   │   └── document.py        # Pydantic models for documents
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py    # Business logic for users
│   │   └── document_service.py
│   ├── dependencies.py        # Shared FastAPI dependencies (get_db, get_current_user)
│   └── exceptions.py          # Custom exception classes and handlers
├── scripts/
│   └── seed.py                # Database seed script (see database.md)
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures: test client, test db
│   ├── test_users.py
│   └── test_documents.py
├── .env                       # Local environment variables (git-ignored)
├── .env.example               # Template with placeholder values (committed)
├── requirements.txt           # or pyproject.toml
└── README.md
```

## Key Rules

### One Router Per Resource

Each domain entity has its own file under `app/routers/`. Never mix user routes and document routes in one file.

```python
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/")
async def list_users(): ...

@router.post("/")
async def create_user(): ...
```

Register routers in `main.py`:

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users, documents, health

app = FastAPI(title="My MongoDB App")
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(health.router)
```

### Separate Models from Routes

Pydantic models live in `app/models/`. Use distinct models for creation, response, and database shapes:

```python
# app/models/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: str = Field(default="user", pattern="^(admin|user|viewer)$")

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime

class UserDB(UserCreate):
    """Shape stored in MongoDB — includes server-generated fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Services for Business Logic

Keep route handlers thin — move database queries and business rules to `app/services/`.

```python
# app/routers/users.py
from app.services.user_service import UserService

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db=Depends(get_db)):
    return await UserService(db).create(user)
```

### `app/main.py` — App Factory Pattern

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import connect_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(title="My MongoDB App", lifespan=lifespan)
```

### Health Check Endpoint

Always include a health route that verifies the MongoDB connection:

```python
# app/routers/health.py
from fastapi import APIRouter, Depends
from app.dependencies import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health(db=Depends(get_db)):
    await db.command("ping")
    return {"status": "ok"}
```

Reference: https://fastapi.tiangolo.com/tutorial/bigger-applications/

