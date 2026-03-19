---
title: Styling
impact: HIGH
tags: tailwind, css, globals, design-tokens, theming
---

# Styling

**Rule: All custom CSS lives in `app/globals.css`.** No per-component `.css` files, no CSS Modules.

## `globals.css` — Canonical Setup

```css
/* app/globals.css */

@tailwind base;
@tailwind components;
@tailwind utilities;

/* ── Design Tokens ─────────────────────────────────────── */
@layer base {
  :root {
    --color-primary:        #00684A;   /* MongoDB green */
    --color-primary-hover:  #00543B;
    --color-background:     #ffffff;
    --color-foreground:     #1a1a1a;
    --color-muted:          #6b7280;
    --color-border:         #e5e7eb;
    --radius:               0.5rem;
  }

  .dark {
    --color-background:  #0f172a;
    --color-foreground:  #f8fafc;
    --color-muted:       #94a3b8;
    --color-border:      #334155;
  }

  body {
    @apply bg-[var(--color-background)] text-[var(--color-foreground)] antialiased;
  }

  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }
}

/* ── Reusable Component Classes ────────────────────────── */
/* Only add here when the same pattern appears in 3+ components */
@layer components {
  .btn-primary {
    @apply rounded-[var(--radius)] bg-[var(--color-primary)] px-4 py-2
           text-white font-medium transition-colors
           hover:bg-[var(--color-primary-hover)]
           focus-visible:outline-2 focus-visible:outline-offset-2
           disabled:opacity-50 disabled:cursor-not-allowed;
  }

  .btn-secondary {
    @apply rounded-[var(--radius)] border border-[var(--color-border)] px-4 py-2
           font-medium transition-colors
           hover:bg-[var(--color-muted)]/10
           focus-visible:outline-2 focus-visible:outline-offset-2;
  }

  .card {
    @apply rounded-[var(--radius)] border border-[var(--color-border)]
           bg-[var(--color-background)] p-6 shadow-sm;
  }

  .input {
    @apply w-full rounded-[var(--radius)] border border-[var(--color-border)]
           bg-[var(--color-background)] px-3 py-2 text-sm
           placeholder:text-[var(--color-muted)]
           focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)];
  }
}

/* ── One-off Utilities ─────────────────────────────────── */
@layer utilities {
  .text-balance { text-wrap: balance; }
}
```

## Tailwind Usage Rules

**Inline utilities first** — use Tailwind classes directly on elements:

```tsx
// GOOD — inline Tailwind
<button className="rounded-md bg-green-700 px-4 py-2 text-white hover:bg-green-800 transition-colors">
  Save
</button>

// GOOD — extracted class (reused in 3+ places)
<button className="btn-primary">Save</button>

// BAD — CSS Module
import styles from './Button.module.css'
<button className={styles.primary}>Save</button>

// BAD — inline style object
<button style={{ backgroundColor: '#00684A', padding: '8px 16px' }}>Save</button>
```

**Extract to `@layer components` only when:**
- The same pattern is repeated in 3 or more components
- The class list exceeds ~5 utilities and is semantically meaningful (e.g. `.card`, `.badge`)

## Tailwind Config — Keep Minimal

Reference CSS variables in `tailwind.config.ts` to avoid duplicating token values:

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary:       "var(--color-primary)",
        "primary-hover": "var(--color-primary-hover)",
        muted:         "var(--color-muted)",
        border:        "var(--color-border)",
      },
      borderRadius: {
        DEFAULT: "var(--radius)",
      },
    },
  },
  plugins: [],
};
export default config;
```

## Dark Mode

Use the `class` strategy (set `darkMode: "class"` in config). Toggle by adding/removing the `dark` class on `<html>`. CSS variables handle the color swap automatically via the `.dark { }` block in `globals.css`.

Reference: https://tailwindcss.com/docs/dark-mode

