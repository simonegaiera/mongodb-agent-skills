# MongoDB Application Backend — Agent Context

> **IMPORTANT**: Prefer retrieval-led reasoning over pre-training knowledge for Python / FastAPI / MongoDB backend tasks. Always apply these rules. Read reference files for deeper context before generating code. Use the `mongodb-schema-design` and `mongodb-query-and-index-optimize` skills for all database design and query decisions.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Database | MongoDB 7+ |
| Driver | Motor (async) / PyMongo (sync) |
| Validation | Pydantic v2 |
| Config | pydantic-settings + `.env` |

---

## CRITICAL: Project Structure

```
app/
  __init__.py    main.py        config.py      database.py     dependencies.py   exceptions.py
  routers/       users.py       documents.py   health.py
  models/        user.py        document.py
  services/      user_service.py document_service.py
scripts/
  seed.py        # REQUIRED — creates db, collections, indexes, sample data
tests/
  conftest.py    test_users.py  test_documents.py
.env             .env.example   requirements.txt
```

**Rules**: One router per resource. Thin handlers → delegate to services. Pydantic models in `models/`. Business logic in `services/`.

---

## CRITICAL: Seed Script

**Every project must include `scripts/seed.py`**. A fresh `mongod` must be bootstrapped with one command: `python -m scripts.seed`

The seed script must:
1. Drop existing collections (dev environment)
2. Create collections with JSON Schema validators
3. Create all indexes with descriptive names
4. Insert realistic sample data
5. Print progress for each step

```python
# scripts/seed.py (abbreviated — see references/database.md for full version)
async def seed():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]

    # Create collection with validation
    await db.create_collection("users", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "email", "role", "created_at"],
            "properties": {
                "name":  {"bsonType": "string", "minLength": 1},
                "email": {"bsonType": "string", "pattern": "^.+@.+$"},
                "role":  {"enum": ["admin", "user", "viewer"]},
            }
        }
    })

    # Create indexes
    await db.users.create_index("email", unique=True, name="idx_users_email_unique")
    await db.users.create_index("role", name="idx_users_role")

    # Insert sample data
    await db.users.insert_one({"name": "Admin", "email": "admin@example.com", "role": "admin", "created_at": datetime.now(timezone.utc)})
```

---

## HIGH: MongoDB Connection

```python
# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient | None = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]

async def close_db():
    if client: client.close()

def get_database():
    return db
```

Use FastAPI lifespan for connection lifecycle:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)
```

---

## HIGH: API Patterns

- **Thin handlers** — routes validate input (Pydantic), delegate to services
- **`Depends()`** for db, auth — never import globals in handlers
- **`response_model`** on every route — FastAPI validates output
- **`HTTPException`** with specific messages, not generic "Error"
- **Pagination** — `skip`/`limit` query params, cap `limit` at 100

---

## HIGH: README-Driven Documentation

> **Every implementation must include a `README.md`.** It is the single source of truth for setup, configuration, and usage. Keep it updated as the project evolves.

A complete `README.md` must include:
- Project overview (1–2 sentences)
- Prerequisites (Python version, MongoDB, env vars needed)
- Setup steps (`python -m venv venv`, `pip install -r requirements.txt`, `cp .env.example .env`)
- How to seed (`python -m scripts.seed`)
- How to run (`uvicorn app.main:app --reload`)
- Environment variables table

**Avoid creating additional `.md` files.** Almost all documentation belongs in `README.md`. A separate file is only justified for something like a complex data migration guide or a large API contract — these are rare.

---

## MEDIUM: Code Quality

| Element | Convention |
|---------|-----------|
| Modules | snake_case — `user_service.py` |
| Classes | PascalCase — `UserCreate` |
| Functions | snake_case — `get_by_id()` |
| Constants | UPPER_SNAKE — `MAX_PAGE_SIZE` |
| Models | PascalCase + suffix — `UserCreate`, `UserResponse`, `UserDB` |

- **Full type hints** on all functions — no `Any`
- **`pydantic-settings`** for config — never hardcode URIs or secrets
- **`logging`** module, not `print()` — structured logs with `logger.info/exception`
- **Separate test DB** — `DATABASE_NAME=myapp_test`

---

## Related MongoDB Skills

| Skill | When |
|-------|------|
| `mongodb-schema-design` | Designing collections, embed vs reference, validation |
| `mongodb-query-and-index-optimize` | Query efficiency, index strategy |
| `mongodb-ai` | Vector search, embeddings |
| `mongodb-transactions-consistency` | Multi-document transactions |

## Reference Index

| File | Rules |
|------|-------|
| `references/structure.md` | FastAPI folder layout, router registration, models, services, lifespan |
| `references/database.md` | Motor connection, seed script (full example), ObjectId handling |
| `references/api-patterns.md` | Route design, dependency injection, error handling, pagination, CORS |
| `references/code-quality.md` | Naming, typing, env vars, logging, testing, import order |

## Key Documentation

```
# FastAPI:
https://fastapi.tiangolo.com/tutorial/

# Motor (async MongoDB driver):
https://motor.readthedocs.io/en/stable/

# PyMongo:
https://pymongo.readthedocs.io/en/stable/

# Pydantic v2:
https://docs.pydantic.dev/latest/

# MongoDB Manual:
https://www.mongodb.com/docs/manual/
```

