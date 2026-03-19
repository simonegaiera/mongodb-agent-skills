# MongoDB Transactions and Consistency

A structured repository for creating and maintaining MongoDB transaction correctness and consistency best practices optimized for agents and LLMs.

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
Copy the content of `AGENTS.md` into your project's root `AGENTS.md`. This gives any AI coding agent critical MongoDB transaction/consistency knowledge on every turn.

### Agent Skills CLI
```bash
npx skills add simonegaiera/mongodb-agent-skills --skill mongodb-transactions-consistency
```

## Getting Started

1. Install dependencies:
   ```bash
   pnpm install
   ```

2. Build AGENTS.md from rules:
   ```bash
   pnpm build-transactions
   ```

3. Validate rule files:
   ```bash
   pnpm validate
   ```

4. Extract test cases:
   ```bash
   pnpm extract-tests-transactions
   ```

## Contributing

When adding or modifying rules:

1. Use the correct filename prefix for your section
2. Follow the rule file structure used in existing rules
3. Include clear incorrect/correct examples using MongoDB Shell syntax
4. Include a `## Verify with` section and an official MongoDB docs reference
5. Run `pnpm build-transactions` and commit generated outputs