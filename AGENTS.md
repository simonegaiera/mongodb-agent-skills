# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Repository Overview

A collection of agent skills for MongoDB development. Skills are packaged instructions that extend any AI coding agent's capabilities for schema design, query/index optimization, AI/vector search, transaction consistency, and full-stack application development (frontend, backend, agentic AI).

## Creating a New Skill

### Directory Structure

```
{skill-name}/                   # kebab-case directory name (must match SKILL.md name field)
  SKILL.md                      # Required: skill definition (frontmatter + instructions)
  AGENTS.md                     # Compressed context for project-root embedding (~7-9KB)
  README.md                     # Optional: human-readable installation docs
  references/                   # Optional: additional reference documents
    REFERENCE.md                # Compiled guide with all rules expanded
    docs-navigation.md          # MongoDB docs URLs tailored to this skill
    _sections.md                # Section definitions
    {prefix}-{name}.md          # Individual rule files
  assets/                       # Optional: non-executable supporting files
    test-cases.json             # Validation test cases
  {skill-name}.zip              # Optional: packaged for distribution
```

### Naming Conventions

- **Skill directory**: `kebab-case` (e.g., `mongodb-schema-design`, `mongodb-transactions-consistency`). Must match the `name` field in `SKILL.md` frontmatter.
- **SKILL.md**: Always uppercase, always this exact filename. Required per the [Agent Skills specification](https://agentskills.io/specification).
- **Rule files**: `{section-prefix}-{rule-name}.md` (e.g., `index-compound-field-order.md`), stored under `references/`
- **Zip file**: Must match directory name exactly: `{skill-name}.zip`

### SKILL.md Format

```markdown
---
name: {skill-name}
description: {One sentence describing when to use this skill. Include trigger phrases.}
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.0.0"
---

# {Skill Title}

{Brief description of what the skill does.}

## When to Apply

{List of scenarios when this skill should be used}

## Rule Categories by Priority

{Table of categories with impact levels and prefixes}

## Quick Reference

{List of rules organized by category}
```

### Rule File Format

```markdown
---
title: Rule Title
impact: CRITICAL|HIGH|MEDIUM
impactDescription: "e.g., 10-100× improvement"
tags: tag1, tag2, tag3
---

## Rule Title

Brief explanation of why this matters.

**Incorrect (problem):**
```javascript
// Bad code example
```

**Correct (solution):**
```javascript
// Good code example
```

Reference: [Link to MongoDB docs]
```

### Hybrid Approach: Skills + AGENTS.md

Each skill provides **two consumption paths** (see [Vercel's AGENTS.md research](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)):

1. **Skills-based (on-demand)**: Agent discovers `SKILL.md` via skill registry, activates when relevant, reads `references/` files progressively. Best for plugin/CLI distribution.

2. **AGENTS.md (passive context)**: User copies the skill's `AGENTS.md` content into their project root. Agent always has critical rules in context — no invocation decision needed. Best for broad framework knowledge.

**Why both?** Vercel's evals showed passive context (AGENTS.md) achieves 100% pass rate vs 53-79% for skills alone. Skills weren't invoked reliably — agents didn't always decide to look up documentation. Passive context eliminates that decision point.

#### AGENTS.md Design Principles

Each skill's `AGENTS.md` is a **compressed index** (~7-8KB) containing:
- Retrieval-led reasoning instruction (prefer docs over pre-training)
- Critical rules inlined (key syntax, anti-patterns agents get wrong)
- Reference index pointing to `references/*.md` for deep dives
- Common errors and diagnostic commands

Target: **<10KB per skill** — compressed from 40-289KB full references (82-97% reduction).

### Best Practices for Context Efficiency

Skills are loaded on-demand — only the skill name and description are loaded at startup. The full `SKILL.md` loads into context only when the agent decides the skill is relevant. To minimize context usage:

- **Keep SKILL.md under 500 lines** — put detailed rules in separate files
- **Write specific descriptions** — helps the agent know exactly when to activate the skill
- **Use progressive disclosure** — reference rule files that get read only when needed
- **Keep rules under 50 lines** — split large concepts into multiple rules
- **Provide AGENTS.md** — compressed passive context as a fallback when skills aren't triggered

### End-User Installation

Document these installation methods for users:

**Option 1: Passive context (recommended for best results):**
Copy the skill's `AGENTS.md` content into your project's root `AGENTS.md`. This gives the agent critical MongoDB knowledge on every turn without needing to invoke a skill.

**Option 2: Agent Skills CLI:**
```bash
npx skills add <owner>/<repo> --skill '*'
npx skills add <owner>/<repo> --skill <skill-name>
```

**Option 3: Web-based agents:**
Add the skill to project knowledge or paste `SKILL.md` contents into the conversation.

## MongoDB-Specific Guidelines

### Code Examples

- Use MongoDB Shell syntax (universal, works everywhere)
- Do NOT use driver-specific syntax (Node.js, Python, etc.)
- Keep examples under 15 lines
- Show clear bad → good transformations

### Impact Levels

- **CRITICAL**: 10-100× improvement (collection scans → index usage)
- **HIGH**: 2-10× improvement (query optimization)
- **MEDIUM**: 20-100% improvement (pipeline optimizations)

### Sources

All rules should reference official MongoDB documentation:
- https://mongodb.com/docs/manual/
- https://mongodb.com/docs/atlas/
- https://mongodb.com/blog/
