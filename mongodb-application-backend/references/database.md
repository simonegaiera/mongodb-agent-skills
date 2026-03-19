---
title: Database & Seed
impact: CRITICAL
tags: mongodb, pymongo, motor, seed, collections, indexes, connection
---

# Database & Seed

MongoDB connection management, collection setup, and the mandatory seed script.

## Connection Setup (Motor — Async)

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
    # Verify connection
    await client.admin.command("ping")
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")

async def close_db():
    global client
    if client:
        client.close()

def get_database():
    """Dependency for route handlers."""
    return db
```

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "myapp"

    class Config:
        env_file = ".env"

settings = Settings()
```

## Dependency Injection

```python
# app/dependencies.py
from fastapi import Depends
from app.database import get_database

async def get_db():
    return get_database()
```

Use in routes:

```python
@router.get("/")
async def list_users(db=Depends(get_db)):
    cursor = db.users.find({}, {"_id": 0})
    return await cursor.to_list(length=100)
```

## Seed Script (REQUIRED)

**Every project must include `scripts/seed.py`**. It creates the database, collections, indexes, and inserts sample data. A fresh `mongod` should be fully bootstrapped by running this file.

```python
#!/usr/bin/env python3
"""
Seed script — creates database, collections, indexes, and sample data.
Run: python -m scripts.seed
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def seed():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]

    # ── 1. Drop existing data (dev only) ──────────────────────
    existing = await db.list_collection_names()
    for coll in existing:
        await db.drop_collection(coll)
    print(f"Cleared database: {settings.DATABASE_NAME}")

    # ── 2. Create collections with JSON Schema validation ─────
    await db.create_collection("users", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "email", "role", "created_at"],
            "properties": {
                "name":       {"bsonType": "string", "minLength": 1},
                "email":      {"bsonType": "string", "pattern": "^.+@.+$"},
                "role":       {"enum": ["admin", "user", "viewer"]},
                "created_at": {"bsonType": "date"}
            }
        }
    })
    print("Created collection: users")

    await db.create_collection("documents", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "owner_id", "created_at"],
            "properties": {
                "title":      {"bsonType": "string", "minLength": 1},
                "owner_id":   {"bsonType": "objectId"},
                "status":     {"enum": ["draft", "published", "archived"]},
                "created_at": {"bsonType": "date"}
            }
        }
    })
    print("Created collection: documents")

    # ── 3. Create indexes ─────────────────────────────────────
    await db.users.create_index("email", unique=True, name="idx_users_email_unique")
    await db.users.create_index("role", name="idx_users_role")

    await db.documents.create_index("owner_id", name="idx_documents_owner")
    await db.documents.create_index(
        [("status", 1), ("created_at", -1)],
        name="idx_documents_status_date"
    )
    print("Created indexes")

    # ── 4. Insert sample data ─────────────────────────────────
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)

    admin_result = await db.users.insert_one({
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin",
        "created_at": now,
    })

    await db.users.insert_one({
        "name": "Regular User",
        "email": "user@example.com",
        "role": "user",
        "created_at": now,
    })

    await db.documents.insert_one({
        "title": "Getting Started",
        "owner_id": admin_result.inserted_id,
        "status": "published",
        "content": "Welcome to the application.",
        "created_at": now,
    })
    print("Inserted sample data")

    # ── 5. Verify ─────────────────────────────────────────────
    user_count = await db.users.count_documents({})
    doc_count = await db.documents.count_documents({})
    print(f"Seed complete: {user_count} users, {doc_count} documents")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
```

## Seed Script Rules

1. **Idempotent** — safe to run multiple times (drops and recreates)
2. **Creates collections explicitly** with JSON Schema validators (use `mongodb-schema-design` skill)
3. **Creates all indexes** with descriptive names (use `mongodb-query-and-index-optimize` skill)
4. **Inserts realistic sample data** — enough to test queries and UI rendering
5. **Prints progress** — each step logs what it did
6. **Runnable standalone** — `python -m scripts.seed` from project root

## ObjectId Handling

Convert `_id` to string in responses. Never expose raw `ObjectId` to API consumers:

```python
from bson import ObjectId

def doc_to_response(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc
```

Reference: https://pymongo.readthedocs.io/en/stable/ | https://motor.readthedocs.io/en/stable/

