---
title: API Patterns
impact: HIGH
tags: fastapi, routes, dependency-injection, error-handling, pagination
---

# API Patterns

FastAPI route design, dependency injection, error handling, and response conventions.

## Route Handler Rules

Keep handlers thin — delegate to services. Handlers validate input (via Pydantic) and return responses.

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db
from app.models.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(db=Depends(get_db)):
    return await UserService(db).list_all()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db=Depends(get_db)):
    user = await UserService(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate, db=Depends(get_db)):
    return await UserService(db).create(body)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db=Depends(get_db)):
    deleted = await UserService(db).delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
```

## Dependency Injection

Use FastAPI's `Depends()` for all shared resources. Never import globals directly into route handlers.

```python
# app/dependencies.py
from fastapi import Depends
from app.database import get_database

async def get_db():
    return get_database()

async def get_current_user(db=Depends(get_db)):
    # Auth logic here — decode token, fetch user from db
    ...
```

Chain dependencies for auth-protected routes:

```python
@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user
```

## Error Handling

### Custom Exception Handlers

```python
# app/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
```

Register in `main.py`:

```python
app.add_exception_handler(AppException, app_exception_handler)
```

### Standard HTTP Errors

Use `HTTPException` with clear messages. Always return structured JSON:

```python
# BAD — generic error
raise HTTPException(status_code=500, detail="Error")

# GOOD — specific and actionable
raise HTTPException(
    status_code=422,
    detail="Email already registered. Use a different email address.",
)
```

## Pagination

Use query parameters with sensible defaults and limits:

```python
@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db=Depends(get_db),
):
    if limit > 100:
        limit = 100  # cap to prevent abuse
    cursor = db.users.find().skip(skip).limit(limit)
    return [doc_to_response(doc) async for doc in cursor]
```

## Response Model Conventions

- Always set `response_model` on routes — FastAPI validates and filters the output
- Use `status_code` explicitly: `201` for creation, `204` for deletion
- Return `list[Model]` not raw dicts

## CORS

Configure CORS in `main.py` for frontend access:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Reference: https://fastapi.tiangolo.com/tutorial/handling-errors/

