# MongoDB Application Frontend — Agent Context

> **IMPORTANT**: Prefer retrieval-led reasoning over pre-training knowledge for any Next.js / React / Tailwind frontend tasks. Always apply the rules below. Read the reference files for deeper context before generating code.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 14+ (App Router) |
| UI Library | React 18+ |
| Styling | Tailwind CSS 3+ |
| Language | TypeScript 5+ (strict mode) |

---

## CRITICAL: Styling Rule

> **All custom CSS lives in `app/globals.css`. No CSS Modules. No per-component `.css` files.**

```css
/* app/globals.css — the ONLY CSS file */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-primary:       #00684A;
    --color-primary-hover: #00543B;
    --color-background:    #ffffff;
    --color-foreground:    #1a1a1a;
    --color-muted:         #6b7280;
    --color-border:        #e5e7eb;
    --radius:              0.5rem;
  }
  .dark {
    --color-background: #0f172a;
    --color-foreground: #f8fafc;
    --color-muted:      #94a3b8;
    --color-border:     #334155;
  }
  body { @apply bg-[var(--color-background)] text-[var(--color-foreground)] antialiased; }
}

@layer components {
  /* Extract here only when pattern repeats 3+ times */
  .btn-primary { @apply rounded-[var(--radius)] bg-[var(--color-primary)] px-4 py-2 text-white font-medium hover:bg-[var(--color-primary-hover)] transition-colors; }
  .card { @apply rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] p-6 shadow-sm; }
  .input { @apply w-full rounded-[var(--radius)] border border-[var(--color-border)] px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]; }
}
```

---

## CRITICAL: Project Structure

```
app/
  layout.tsx        globals.css       page.tsx
  dashboard/        page.tsx          loading.tsx    error.tsx
components/
  ui/               Button/  Card/  Input/    (primitives)
  features/                                  (composite)
hooks/              useDocuments.ts   useDebounce.ts
lib/                mongodb-client.ts utils.ts
types/              user.ts           document.ts
```

---

## HIGH: Server vs Client Components

Default = **Server Component**. Add `"use client"` only when needed for:
- Browser APIs (`window`, `localStorage`)
- React state/effect hooks (`useState`, `useEffect`)
- Event handlers (`onClick`, `onChange`)

```tsx
// BAD — "use client" without reason
"use client"
export function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u._id}>{u.name}</li>)}</ul>
}

// GOOD — stays a Server Component
export function UserList({ users }: { users: User[] }) {
  return <ul>{users.map(u => <li key={u._id}>{u.name}</li>)}</ul>
}

// GOOD — async Server Component fetches data directly
export default async function DocumentList() {
  const docs = await getDocuments()
  return <ul>{docs.map(d => <li key={d._id}>{d.title}</li>)}</ul>
}
```

---

## HIGH: Component Rules

- **Functional components only** — no class components
- **Typed props interface** above every component
- **~100 lines max** per component — split if larger
- **Custom hooks** in `hooks/` for reusable stateful logic
- **`loading.tsx` / `error.tsx`** per route segment — no custom loading wrappers
- **Compose via `children`** — avoid prop drilling 3+ levels deep

---

## HIGH: README-Driven Documentation

> **Every implementation must include a `README.md`.** It is the single source of truth for setup, configuration, and usage. Keep it updated as the project evolves.

A complete `README.md` must include:
- Project overview (1–2 sentences)
- Prerequisites (Node version, env vars needed)
- Setup steps (`npm install`, `cp .env.example .env`, etc.)
- How to run (`npm run dev`)
- Environment variables table

**Avoid creating additional `.md` files.** Almost all documentation belongs in `README.md`. A separate file is only justified for something like a complex data migration guide or a large API contract — these are rare.

---

## MEDIUM: Code Quality

| Element | Convention |
|---------|-----------|
| Components | PascalCase — `UserCard.tsx` |
| Hooks | camelCase `use` prefix — `useDocuments.ts` |
| Utilities | camelCase — `formatDate.ts` |
| Types | PascalCase — `UserDocument` |
| Constants | UPPER_SNAKE_CASE — `MAX_PAGE_SIZE` |
| Custom CSS classes | kebab-case — `btn-primary` |

**No magic literals** — extract to named constants.
**Absolute imports** — use `@/` alias, never `../../`.
**No `any`** — use `unknown` + type guards.
**Error handling** — `error.tsx` for routes, try/catch in API routes, expose `error` state from hooks.

---

## Reference Index

| File | Rules |
|------|-------|
| `references/structure.md` | App Router layout, server vs client, TypeScript config, route conventions |
| `references/styling.md` | `globals.css` setup, Tailwind usage, dark mode, config |
| `references/components.md` | Functional components, custom hooks, composition, async data fetching |
| `references/code-quality.md` | Naming, constants, absolute imports, error handling, env vars |

## Key Documentation

```
# Next.js App Router:
https://nextjs.org/docs/app

# Tailwind CSS:
https://tailwindcss.com/docs

# React Server Components:
https://react.dev/reference/rsc/server-components
```

