---
title: Component Patterns
impact: HIGH
tags: react, components, hooks, server-components, composition
---

# Component Patterns

Rules for writing React components in Next.js App Router projects.

## Functional Components Only

Never use class components. Use named function declarations or arrow functions.

```tsx
// BAD — class component
class UserCard extends React.Component<Props> {
  render() { return <div>{this.props.name}</div> }
}

// GOOD — named function
export function UserCard({ name, email }: UserCardProps) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="text-[var(--color-muted)]">{email}</p>
    </div>
  )
}
```

Always define a typed props interface above the component:

```tsx
interface UserCardProps {
  name: string
  email: string
  avatarUrl?: string
}
```

## Keep Components Small and Focused

One responsibility per component. If a component exceeds ~100 lines or renders more than one distinct UI concern, split it.

```
// BAD — one component does data fetching, table, pagination, and filters
export function DocumentsPage() { /* 200 lines */ }

// GOOD — split by concern
export function DocumentsPage() {
  return (
    <main>
      <DocumentFilters />
      <DocumentTable />
      <Pagination />
    </main>
  )
}
```

## Custom Hooks for Reusable Logic

Extract stateful or side-effect logic into custom hooks in `hooks/`. Mark the hook file `"use client"` if it uses browser APIs or React state hooks.

```tsx
// hooks/useDocuments.ts
"use client"
import { useState, useEffect } from "react"

export function useDocuments(collectionName: string) {
  const [documents, setDocuments] = useState<Document[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    fetch(`/api/${collectionName}`)
      .then(res => {
        if (!res.ok) throw new Error(res.statusText)
        return res.json()
      })
      .then(data => setDocuments(data))
      .catch(err => setError(err))
      .finally(() => setIsLoading(false))
  }, [collectionName])

  return { documents, isLoading, error }
}
```

## Use `loading.tsx` and `error.tsx` Conventions

Leverage Next.js file conventions instead of building custom loading/error wrappers:

```tsx
// app/dashboard/loading.tsx — automatic Suspense boundary
export default function Loading() {
  return <div className="flex items-center justify-center p-8">Loading…</div>
}

// app/dashboard/error.tsx — automatic error boundary
"use client"
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="card text-center">
      <p className="text-red-600 mb-4">{error.message}</p>
      <button className="btn-primary" onClick={reset}>Try again</button>
    </div>
  )
}
```

## Composition Over Prop Drilling

Prefer passing `children` or using React Context over threading props through 3+ levels.

```tsx
// BAD — prop drilling
<Page user={user}>
  <Layout user={user}>
    <Sidebar user={user} />
  </Layout>
</Page>

// GOOD — pass children, fetch data at layout level
// app/dashboard/layout.tsx (Server Component)
export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const user = await getCurrentUser()  // fetch once at the top
  return (
    <UserContext.Provider value={user}>
      <div className="flex">
        <Sidebar />
        <main>{children}</main>
      </div>
    </UserContext.Provider>
  )
}
```

## Async Server Components for Data Fetching

Fetch data directly in Server Components using `async/await`. Do not use `useEffect` for data fetching in server-rendered pages.

```tsx
// GOOD — Server Component fetches data directly
export default async function DocumentList() {
  const documents = await getDocuments()   // direct DB/API call server-side

  return (
    <ul>
      {documents.map(doc => (
        <li key={doc._id} className="card mb-2">{doc.title}</li>
      ))}
    </ul>
  )
}
```

Reference: https://nextjs.org/docs/app/building-your-application/rendering/server-components

