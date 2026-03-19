---
title: PROMPT.md Generation
impact: CRITICAL
impactDescription: "Aligns LLM behavior across the entire build session"
tags: prompting, PROMPT.md, claude, xml-tags, system-prompt
---

# PROMPT.md Generation

`PROMPT.md` is the LLM's persistent system prompt for the project. It is written *for the LLM*, not for humans (that's `README.md`). Every time a new coding session starts, this file should be read first to restore full project context and behavioral alignment.

---

## File Location and Name

Always create at the project root:

```
my-app/
  PROMPT.md     ← here
  README.md
  app/
  ...
```

---

## Required Sections

### 1. Role

Give the LLM a specific role grounded in the project. Use a single `<role>` XML tag.

```xml
<role>
You are an expert full-stack developer building a MongoDB-powered e-commerce platform
using Next.js (App Router), FastAPI, and MongoDB Atlas. You follow the mongodb-application-frontend
and mongodb-application-backend skills strictly.
</role>
```

### 2. Project Context

Summarize the approved plan in structured XML. This is the LLM's source of truth for what is being built.

```xml
<project_context>
Application: E-commerce storefront with product catalog, cart, and checkout.
Stack: Next.js 14 + FastAPI + MongoDB Atlas 7+
MongoDB skills in effect: mongodb-schema-design, mongodb-query-and-index-optimize, mongodb-application-frontend, mongodb-application-backend
Key constraints:
  - All CSS in app/globals.css (no CSS Modules)
  - Seed script required: python -m scripts.seed
  - ObjectId serialized as string in all API responses
  - Vector search on product.embedding (voyage-3.5, 1024 dims)
</project_context>
```

### 3. Behavior Rules

Three behavior blocks are required in every `PROMPT.md`. Copy and adapt these:

```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make changes.
When the user's intent is ambiguous, default to providing information and recommendations
rather than taking action. Only proceed with edits when explicitly requested.
</do_not_act_before_instructions>

<safety_guidelines>
Consider the reversibility and potential impact of your actions.
Take local, reversible actions freely (reading files, running queries).
For destructive or shared-system actions (dropping collections, deleting files,
force-pushing git), ask the user before proceeding.
</safety_guidelines>

<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the calls,
make all independent calls in parallel. When reading 3 files, read all 3 at once.
Maximize parallel tool calls for speed and efficiency.
</use_parallel_tool_calls>
```

### 4. Coding Conventions

List the project-specific conventions derived from the approved plan and the applicable skills.

```xml
<coding_conventions>
Frontend:
  - Server Components by default; "use client" only for interactivity or browser APIs
  - All CSS in app/globals.css — no per-component stylesheets
  - Absolute imports via @/ alias
  - Functional components only, typed props interfaces, ~100 lines max

Backend:
  - One router per resource under app/routers/
  - Thin handlers → delegate to services
  - Full type hints everywhere, no Any
  - Motor (async) for all DB operations
  - MONGODB_URI always from environment, never hardcoded

Database:
  - Follow mongodb-schema-design skill for all collection decisions
  - Follow mongodb-query-and-index-optimize skill for all index decisions
  - All indexes created in scripts/seed.py with descriptive names
</coding_conventions>
```

### 5. Investigate Before Answering

Prevents hallucinations about the codebase:

```xml
<investigate_before_answering>
Never speculate about code you have not read. If the user references a file or function,
read it before answering. Give grounded, hallucination-free answers based only on what
you have actually seen in the codebase.
</investigate_before_answering>
```

---

## Keeping PROMPT.md Updated

Update `PROMPT.md` when:
- A significant technology decision changes (e.g., swapped auth provider)
- A feature is added or removed from scope
- A new constraint is agreed upon (e.g., "no third-party UI libraries")
- A new MongoDB skill is applied to the project

Do NOT update `PROMPT.md` for routine implementation decisions — only structural changes that affect future sessions.

---

## What PROMPT.md is NOT

- It is **not** a README — do not include setup steps, installation commands, or environment variable tables (those belong in `README.md`)
- It is **not** a task list — do not list TODOs or implementation steps
- It is **not** documentation for humans — write it as instructions to the LLM

---

## Reference

Full prompting guide: `CLAUDE Prompting Guide.md`
Anthropic docs: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

