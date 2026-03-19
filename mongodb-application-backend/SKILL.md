---
name: mongodb-application-backend
description: Backend application standards for MongoDB projects using Python, FastAPI, and PyMongo/Motor. Use when creating API endpoints, database models, seed scripts, or backend project structure. Triggers on "backend", "FastAPI", "Python", "API route", "seed", "PyMongo", "Motor", "database setup", "collections".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.0.0"
---

# MongoDB Application Backend

Standards for building backend applications with **Python**, **FastAPI**, and **MongoDB** (via PyMongo / Motor). Covers project structure, database connection patterns, seed scripts, API design, and code quality.

## When to Use

- Creating a new FastAPI backend for a MongoDB-backed application
- Setting up MongoDB connections, collections, and indexes
- Writing seed scripts to bootstrap databases
- Building or reviewing API endpoints and route handlers
- Organizing Python project structure for a FastAPI app

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Database | MongoDB 7+ |
| Driver | PyMongo (sync) / Motor (async) |
| Validation | Pydantic v2 |
| Environment | python-dotenv |

## Related MongoDB Skills

Apply these companion skills when working on the database layer:

| Skill | When to Use |
|-------|-------------|
| `mongodb-schema-design` | Designing collections, choosing embed vs reference, schema validation |
| `mongodb-query-and-index-optimize` | Writing queries, creating indexes, optimizing performance |
| `mongodb-ai` | Adding vector search, embeddings, or AI features |
| `mongodb-transactions-consistency` | Multi-document transactions and data consistency |

## Rule Categories

| Priority | Category | Impact | Reference |
|----------|----------|--------|-----------|
| 1 | Project Structure | CRITICAL | `references/structure.md` |
| 2 | Database & Seed | CRITICAL | `references/database.md` |
| 3 | API Patterns | HIGH | `references/api-patterns.md` |
| 4 | Code Quality | MEDIUM | `references/code-quality.md` |

## Key Principles

> **Seed everything** — Every project includes a seed script that creates the database, collections, indexes, and sample data. The app should be runnable from a fresh `mongod` with one command.

> **Schema at two levels** — Pydantic models validate at the API layer; MongoDB JSON Schema validation enforces at the database layer. Use the `mongodb-schema-design` skill for schema decisions.

> **Async by default** — Use Motor (async PyMongo) with FastAPI's async routes. Fall back to PyMongo only when async is not needed.

> **Type everything** — Full type hints on all functions, Pydantic models for all request/response shapes, no `Any`.

> **One router per resource** — Each domain entity gets its own router file under `app/routers/`.

## Instructions

When building backend features for a MongoDB application:

1. Read `references/structure.md` for the FastAPI project layout and folder conventions
2. Read `references/database.md` for MongoDB connection setup, seed script pattern, and index creation
3. Read `references/api-patterns.md` for route design, dependency injection, and error handling
4. Read `references/code-quality.md` for naming, typing, environment variables, and logging
5. Consult the `mongodb-schema-design` skill when designing collections or data models
6. Consult the `mongodb-query-and-index-optimize` skill when writing queries or creating indexes
7. If requirements are ambiguous, ask the user to clarify before generating code

