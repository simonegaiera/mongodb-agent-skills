---
title: Plan-First Approval Workflow
impact: CRITICAL
impactDescription: "Prevents misaligned builds that require significant rework"
tags: planning, approval, pre-build, workflow
---

# Plan-First Approval Workflow

Never write implementation code until the user has explicitly approved a plan. Misaligned assumptions (wrong stack, missing features, incorrect data model) discovered mid-build are far more costly to fix than getting alignment upfront.

## Required Plan Sections

Present the plan as a structured document. All sections below are required. Skip none — a missing section is an assumption.

### 1. Application Overview
One paragraph describing what the application does, who uses it, and what problem it solves. This confirms the LLM and user share the same understanding of scope.

### 2. Tech Stack
List every technology with a version and the reason it was chosen. Reference applicable MongoDB skills.

```
| Layer      | Technology          | Why |
|------------|---------------------|-----|
| Frontend   | Next.js 14 (App Router) | mongodb-application-frontend skill |
| Backend    | FastAPI + Motor     | mongodb-application-backend skill |
| Database   | MongoDB Atlas 7+    | Primary datastore |
| Auth       | NextAuth.js         | Session management |
```

### 3. Feature List
Numbered list of every feature to be built. For each feature, note whether it is in scope for this build or deferred.

```
In scope:
1. User registration and login (NextAuth + MongoDB)
2. Product catalog with search (Atlas Vector Search)
3. Shopping cart (session-based, MongoDB)

Out of scope / future:
- Payment processing
- Order history
- Admin dashboard
```

### 4. Folder Structure
Show the complete directory tree for all new code. Use the conventions from the relevant skills.

```
my-app/
  app/               ← Next.js App Router
  components/
  hooks/
  backend/
    app/
      routers/
      models/
      services/
    scripts/
      seed.py        ← REQUIRED
  PROMPT.md          ← LLM instructions (generated next)
  README.md          ← Human setup guide
```

### 5. Data Model
For every MongoDB collection, list the fields, types, and indexes. Reference the `mongodb-schema-design` skill.

```
Collection: products
  _id: ObjectId
  name: string (required)
  price: Decimal128
  category: string
  embedding: array[float]  ← for vector search
Indexes:
  { category: 1 }
  { name: "text" }
  Vector index on embedding
```

### 6. API Design (if backend)
List every endpoint with method, path, request shape, and response shape.

```
POST /api/products       → Create product
GET  /api/products       → List (paginated, filter by category)
GET  /api/products/{id}  → Get by ID
PUT  /api/products/{id}  → Update
```

### 7. Key Implementation Decisions
List any non-obvious technical choices and the reason for each.

- "Embedding generation at write time (not query time) to keep read latency low"
- "ObjectId serialized as string in API responses to avoid frontend issues"

### 8. Out of Scope
Explicit list of what will NOT be built in this iteration. This prevents scope creep.

## Approval Gate

After presenting the plan, include exactly this prompt:

```
---
**Please review the plan above.**
- Reply **"approved"** (or "looks good", "go ahead") to proceed.
- Reply with changes if anything is wrong or missing.

I will not write any code until you approve.
---
```

Do NOT proceed to code generation if the user says anything other than an explicit approval. Questions, suggestions, or silence are not approvals — ask for explicit confirmation.

## Revision Workflow

If the user requests changes:
1. Update only the affected sections
2. Re-present the full updated plan
3. Repeat the approval gate

Do not start coding after the first revision — always re-confirm.

