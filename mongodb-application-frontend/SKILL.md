---
name: mongodb-application-frontend
description: Frontend application standards for MongoDB projects using Next.js, React, and Tailwind CSS. Use when creating UI components, pages, layouts, styling, or frontend project structure. Triggers on "frontend", "Next.js", "React component", "Tailwind", "CSS", "page layout", "UI", "app router".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.0.0"
---

# MongoDB Application Frontend

Standards for building frontend applications with **Next.js (App Router)**, **React**, and **Tailwind CSS**. Covers project structure, styling strategy, component patterns, and code quality.

## When to Use

- Creating a new Next.js frontend for a MongoDB-backed app
- Building or reviewing React components, pages, or layouts
- Writing or organizing CSS and Tailwind styles
- Setting up project structure and TypeScript configuration
- Deciding where CSS, components, or logic should live

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 14+ (App Router) |
| UI Library | React 18+ |
| Styling | Tailwind CSS 3+ |
| Language | TypeScript 5+ (strict mode) |

## Rule Categories

| Priority | Category | Impact | Reference |
|----------|----------|--------|-----------|
| 1 | Project Structure | CRITICAL | `references/structure.md` |
| 2 | Styling | HIGH | `references/styling.md` |
| 3 | Component Patterns | HIGH | `references/components.md` |
| 4 | Code Quality | MEDIUM | `references/code-quality.md` |

## Key Principles

> **Single CSS file** — All styles live in `app/globals.css`. No CSS modules, no per-component stylesheets.

> **Server-first** — Default to Server Components. Add `"use client"` only when required for interactivity or browser APIs.

> **Type everything** — Strict TypeScript, no `any`. Explicit interfaces for all props and data shapes.

> **Tailwind-first** — Utility classes inline. Extract to `@layer components` in `globals.css` only for patterns repeated 3+ times.

> **Small, focused components** — One responsibility per component. Compose via children and custom hooks.

> **One README** — Every implementation includes a `README.md` with setup instructions, environment variables, and usage. Keep it updated as the project evolves. Avoid creating additional `.md` files — almost all documentation belongs in `README.md`.

## Instructions

When building frontend features for a MongoDB application:

1. Read `references/structure.md` for project layout and App Router conventions
2. Read `references/styling.md` for the `globals.css` setup, CSS variables, and Tailwind usage rules
3. Read `references/components.md` for server vs client component decisions and component patterns
4. Read `references/code-quality.md` for naming, error handling, and import conventions
5. Always create or update `README.md` with setup steps, env vars, and how to run the project
6. If requirements are ambiguous, use the ask questions tool to clarify before generating code

