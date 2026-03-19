---
title: Code Quality
impact: MEDIUM
tags: naming, typescript, imports, error-handling, constants
---

# Code Quality

Conventions for naming, error handling, imports, and maintainability.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Components | PascalCase | `UserCard.tsx`, `DocumentTable.tsx` |
| Hooks | camelCase, `use` prefix | `useDocuments.ts`, `useDebounce.ts` |
| Utilities | camelCase | `formatDate.ts`, `parseObjectId.ts` |
| Types / Interfaces | PascalCase | `UserDocument`, `ApiResponse` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE`, `DEFAULT_LOCALE` |
| Custom CSS classes | kebab-case | `btn-primary`, `card` |
| Files (non-component) | kebab-case | `mongodb-client.ts`, `auth-helpers.ts` |
| Folders | kebab-case | `user-settings/`, `api-client/` |

## No Magic Numbers or Strings

Extract all literals into named constants. Group related constants in a dedicated file.

```tsx
// BAD
if (items.length > 25) { ... }
const url = `https://api.example.com/v1/documents`

// GOOD
const MAX_PAGE_SIZE = 25
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

if (items.length > MAX_PAGE_SIZE) { ... }
```

Use `as const` for literal objects:

```tsx
const SORT_DIRECTIONS = { ASC: "asc", DESC: "desc" } as const
type SortDirection = typeof SORT_DIRECTIONS[keyof typeof SORT_DIRECTIONS]
```

## Absolute Imports

Configure `@/` path alias in `tsconfig.json` and always use it — never use relative paths that traverse upward (`../../`).

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./*"] }
  }
}
```

```tsx
// BAD
import { UserCard } from "../../../components/ui/UserCard"

// GOOD
import { UserCard } from "@/components/ui/UserCard"
import { formatDate } from "@/lib/utils"
import type { UserDocument } from "@/types/user"
```

## Error Handling

**Route level** — use `error.tsx` for automatic error boundaries:

```tsx
// app/dashboard/error.tsx
"use client"
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  // Log to monitoring service server-side, not in the browser
  return (
    <div className="card text-center">
      <p className="font-semibold text-red-600 mb-2">Something went wrong</p>
      <p className="text-[var(--color-muted)] mb-4 text-sm">{error.message}</p>
      <button className="btn-primary" onClick={reset}>Retry</button>
    </div>
  )
}
```

**API routes / Server Actions** — always wrap in try/catch and return structured errors:

```tsx
// app/api/documents/route.ts
export async function GET(request: Request) {
  try {
    const documents = await db.collection("documents").find().toArray()
    return Response.json(documents)
  } catch (error) {
    console.error("[GET /api/documents]", error)  // server-side only
    return Response.json({ error: "Failed to fetch documents" }, { status: 500 })
  }
}
```

**Client hooks** — expose `error` state and let UI decide how to display:

```tsx
const { documents, isLoading, error } = useDocuments("products")
if (error) return <ErrorMessage message={error.message} />
```

## Strict TypeScript

- No `any` — use `unknown` and narrow with type guards or `zod`
- Define return types for all exported functions
- Define explicit interfaces for MongoDB document shapes

```tsx
// BAD
async function fetchUser(id: any): Promise<any> { ... }

// GOOD
interface UserDocument {
  _id: string
  name: string
  email: string
  role: "admin" | "user" | "viewer"
  createdAt: Date
}

async function fetchUser(id: string): Promise<UserDocument | null> { ... }
```

## Environment Variables

- Prefix browser-exposed variables with `NEXT_PUBLIC_`
- Never expose secrets to the client
- Access via `process.env.VAR_NAME` — never hardcode values

```tsx
// .env.local
MONGODB_URI=mongodb+srv://...       # server-only
NEXT_PUBLIC_APP_URL=https://...     # safe for browser
```

Reference: https://nextjs.org/docs/app/building-your-application/configuring/environment-variables

