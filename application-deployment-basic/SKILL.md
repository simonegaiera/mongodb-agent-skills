---
name: application-deployment-basic
description: Pre-build planning workflow for any application. Use when a user asks to "build", "create", or "implement" an application. Enforces plan-first approval before coding and generates a PROMPT.md to guide the LLM throughout the build. Triggers on "build an app", "create an application", "implement a feature", "let's build", "start the project".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.0.0"
---

# Application Deployment — Basic Planning Workflow

A pre-build ritual that prevents wasted work. Before writing any code, the LLM must **present a detailed plan and wait for explicit user approval**. It must also **generate a `PROMPT.md`** — a project-specific prompt file that captures role, constraints, and behavior rules for the LLM to follow throughout the entire build.

## When to Apply

- User asks to "build", "create", "implement", or "start" any application or feature
- A new project is being scaffolded from scratch
- A significant new capability is being added to an existing project
- Any time the scope is large enough that misaligned assumptions would cost significant rework

## Rule Categories

| Priority | Category | Impact | Reference |
|----------|----------|--------|-----------|
| 1 | Plan-First Approval | CRITICAL | `references/planning.md` |
| 2 | PROMPT.md Generation | CRITICAL | `references/prompt-file.md` |

## Key Principles

> **Plan before code** — Never write implementation code until the user has reviewed and explicitly approved a detailed plan. Assumptions that turn out to be wrong are expensive to undo.

> **PROMPT.md is mandatory** — Before the first line of code, generate a `PROMPT.md` at the project root. This file is the LLM's persistent system prompt for the project — it captures role, tech stack, behavior rules, and key constraints. It must be kept up to date as the project evolves.

> **One approval gate** — The plan approval and `PROMPT.md` review happen together in a single step. The user approves both before any code is written.

> **PROMPT.md is not README.md** — `PROMPT.md` is written *for the LLM*. `README.md` is written *for humans*. Both are required but serve different audiences.

## Instructions

When a user asks to build an application:

1. **Read `references/planning.md`** — understand what sections the plan must contain
2. **Read `references/prompt-file.md`** — understand how to write the `PROMPT.md` using Claude prompting best practices
3. **Present the plan** — a structured document covering stack, features, folder structure, data model, API design, and out-of-scope items
4. **Wait for explicit user approval** — do NOT start coding until the user says "approved", "looks good", "go ahead", or equivalent. If the user requests changes, revise and re-present.
5. **Generate `PROMPT.md`** — write the project-specific prompt file at the project root alongside the plan approval
6. **Begin implementation** — only after both plan and `PROMPT.md` are accepted
7. **Keep `PROMPT.md` updated** — if major decisions change during the build (new tech, removed features, new constraints), update `PROMPT.md` to reflect them
