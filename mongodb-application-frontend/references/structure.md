---
title: Project Structure
impact: CRITICAL
tags: nextjs, app-router, typescript, file-organization
---

# Project Structure

Use the Next.js App Router (`app/` directory). Never use the legacy `pages/` directory.

## Canonical Layout

```
app/
  layout.tsx          # Root layout — fonts, providers, global wrappers
  page.tsx            # Home route
  globals.css         # ALL styles live here (see styling.md)
  (routes)/
    dashboard/
      page.tsx
      loading.tsx     # Suspense boundary for this segment
      error.tsx       # Error boundary for this segment
    settings/
      page.tsx
components/
  ui/                 # Reusable primitives: Button, Input, Card, Badge
  features/           # Feature-specific composite components
hooks/                # Shared custom hooks (useDocuments, useDebounce…)
lib/                  # Utilities, helpers, MongoDB API client wrappers
types/                # Shared TypeScript type definitions
public/               # Static assets (images, fonts, icons)
```

## Server vs Client Components

All components are **Server Components** by default. Only add `"use client"` when the component uses:
- Browser APIs (`window`, `localStorage`, `navigator`)
- React hooks that manage state or side effects (`useState`, `useEffect`, `useReducer`)
- Event handlers (`onClick`, `onChange`, etc.)

```tsx
// BAD — "use client" added without a reason
"use client"
export function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u._id}>{u.name}</li>)}</ul>
}

// GOOD — Server Component, no client directive needed
export function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u._id}>{u.name}</li>)}</ul>
}
```

Push `"use client"` as deep as possible — keep data-fetching and rendering server-side, isolate interactivity to leaf components.

## File Co-location

Keep component files, types, and tests together:

```
components/ui/Button/
  Button.tsx
  Button.test.tsx
  index.ts            # re-export: export { Button } from './Button'
```

## TypeScript — Strict Mode Required

Enable strict mode in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": { "@/*": ["./*"] }
  }
}
```

Rules:
- Never use `any` — use `unknown` and narrow with type guards
- Define explicit interfaces for all component props
- Define explicit types for all API responses and MongoDB document shapes
- Use `as const` for literal objects and enums

## Route Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI |
| `layout.tsx` | Shared wrapper for a segment and its children |
| `loading.tsx` | Streaming Suspense fallback |
| `error.tsx` | Error boundary for the segment |
| `not-found.tsx` | 404 handler for the segment |
| `route.ts` | API route handler (replaces `pages/api/`) |

Reference: https://nextjs.org/docs/app/building-your-application/routing

