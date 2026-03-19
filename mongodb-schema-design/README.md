# MongoDB Schema Design

A structured repository for creating and maintaining MongoDB Schema Design best practices optimized for agents and LLMs.

## Structure

- `SKILL.md` - Skill definition (for skills-based agents)
- `AGENTS.md` - Compressed context (for project-root embedding)
- `references/` - Individual rule files (one per rule)
  - `REFERENCE.md` - Full compiled guide with all rules expanded
  - `_sections.md` - Section metadata (titles, impacts, descriptions)
  - `area-description.md` - Individual rule files
- `assets/test-cases.json` - Test cases for LLM evaluation

## Installation (End Users)

### Passive context (recommended)
Copy the content of `AGENTS.md` into your project's root `AGENTS.md`. This gives any AI coding agent critical MongoDB schema design knowledge on every turn.

### Agent Skills CLI
```bash
npx skills add simonegaiera/mongodb-agent-skills --skill mongodb-schema-design
```

## Getting Started

1. Install dependencies:
   ```bash
   pnpm install
   ```

2. Build AGENTS.md from rules:
   ```bash
   pnpm build mongodb-schema-design
   ```

3. Validate rule files:
   ```bash
   pnpm validate mongodb-schema-design
   ```

4. Extract test cases:
   ```bash
   pnpm extract-tests mongodb-schema-design
   ```

## Creating a New Rule

1. Copy an existing rule file to `rules/area-description.md`
2. Choose the appropriate area prefix:
   - `antipattern-` for Schema Anti-Patterns (Section 1)
   - `fundamental-` for Schema Fundamentals (Section 2)
   - `relationship-` for Relationship Patterns (Section 3)
   - `pattern-` for Design Patterns (Section 4)
   - `validation-` for Schema Validation (Section 5)
3. Fill in the frontmatter and content
4. Ensure you have clear bad/good examples with explanations
5. Run `pnpm build mongodb-schema-design` to regenerate AGENTS.md

## Rule File Structure

Each rule file should follow this structure:

```markdown
---
title: Rule Title Here
impact: CRITICAL|HIGH|MEDIUM
impactDescription: Optional description
tags: tag1, tag2, tag3
---

## Rule Title Here

Brief explanation of the rule and why it matters.

**Incorrect (description of what's wrong):**

```javascript
// Bad code example using MongoDB Shell syntax
```

**Correct (description of what's right):**

```javascript
// Good code example using MongoDB Shell syntax
```

Optional explanatory text after examples.

Reference: [MongoDB Documentation](https://mongodb.com/docs/manual/)
```

## File Naming Convention

- Files starting with `_` are special (excluded from build)
- Rule files: `area-description.md` (e.g., `antipattern-unbounded-arrays.md`)
- Section is automatically inferred from filename prefix
- Rules are sorted alphabetically by title within each section
- IDs (e.g., 1.1, 1.2) are auto-generated during build

## Impact Levels

- `CRITICAL` - 10-100x improvement (collection scans to index usage)
- `HIGH` - 2-10x improvement (query optimization)
- `MEDIUM` - 20-100% improvement (pipeline optimizations)

## Scripts

- `pnpm build mongodb-schema-design` - Compile rules into AGENTS.md
- `pnpm validate mongodb-schema-design` - Validate all rule files
- `pnpm extract-tests mongodb-schema-design` - Extract test cases for LLM evaluation

## Contributing

When adding or modifying rules:

1. Use the correct filename prefix for your section
2. Follow the rule file structure above
3. Include clear bad/good examples using MongoDB Shell syntax
4. Add appropriate tags
5. Run `pnpm build mongodb-schema-design` to regenerate AGENTS.md
6. Rules are automatically sorted by title - no need to manage numbers