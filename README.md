# MongoDB Agent Skills

**Packaged MongoDB best practices for AI coding agents and LLMs.**

This repository provides structured, up-to-date guidance across seven MongoDB domains — four database-focused and three application-focused — designed to bridge the knowledge gap where AI assistants have outdated or incorrect information about MongoDB's evolving capabilities.

## 🎯 What Are Agent Skills?

Agent Skills are packaged instructions that extend AI coding agents' capabilities. Each skill contains:

- **Frontmatter-based rules** with impact levels (CRITICAL/HIGH/MEDIUM)
- **MongoDB Shell syntax examples** showing bad → good transformations
- **Official MongoDB documentation references**
- **Test cases** for LLM evaluation
- **Compressed context** for efficient token usage

## 📦 Available Skills

### 1. [mongodb-schema-design](./mongodb-schema-design/)
**30 rules** for data modeling patterns and anti-patterns.

**Use when**: Designing schemas, migrating from SQL, troubleshooting performance issues caused by schema problems.

**Key topics**: Embed vs reference, unbounded arrays, document size limits, relationship patterns, schema validation.

### 2. [mongodb-query-and-index-optimize](./mongodb-query-and-index-optimize/)
Query and index optimization best practices.

**Use when**: Optimizing slow queries, designing indexes, reducing query execution time.

**Key topics**: Index design, compound indexes, covered queries, query planning, aggregation optimization.

### 3. [mongodb-ai](./mongodb-ai/)
**33 rules** for Atlas Vector Search, RAG, and AI integration.

**Use when**: Building AI applications, implementing semantic search, working with embeddings.

**Key topics**: Vector search indexes, embedding generation, hybrid search, RAG patterns, chunking strategies.

### 4. [mongodb-transactions-consistency](./mongodb-transactions-consistency/)
**20 rules** for transaction correctness and consistency.

**Use when**: Implementing multi-document transactions, ensuring data consistency, handling concurrent operations.

**Key topics**: ACID guarantees, transaction patterns, read/write concerns, retryable operations.

### 5. [mongodb-application-frontend](./mongodb-application-frontend/)
Frontend application standards with Next.js, React, and Tailwind CSS.

**Use when**: Building a frontend application that connects to a MongoDB backend.

**Key topics**: App Router, server/client components, global CSS with Tailwind, component patterns, TypeScript.

### 6. [mongodb-application-backend](./mongodb-application-backend/)
Backend application standards with Python, FastAPI, and Motor.

**Use when**: Building a Python backend API backed by MongoDB.

**Key topics**: FastAPI project structure, Motor async driver, mandatory seed script, Pydantic models, API patterns.

### 7. [mongodb-application-agentic](./mongodb-application-agentic/)
Standards for building agentic AI applications and chatbots with MongoDB.

**Use when**: Building chatbots, conversational agents, or agentic AI workflows with MongoDB.

**Key topics**: LangChain + LangGraph, MongoDBSaver (checkpointing), MongoDBStore (long-term memory), MongoDB MCP, Claude prompting best practices.

## 🚀 Installation

Each skill supports **two consumption paths** for maximum flexibility:

### Option 1: Passive Context (Recommended for Best Results)

Copy the skill's `AGENTS.md` content into your project's root `AGENTS.md` file. This gives the agent critical MongoDB knowledge on every turn without needing to invoke a skill.

**Why this works better**: Research shows passive context achieves 100% pass rate vs 53-79% for skills alone, because agents don't always decide to invoke skills when needed.

```bash
# Example: Add schema design knowledge to your project
cat mongodb-schema-design/AGENTS.md >> /path/to/your/project/AGENTS.md
```

### Option 2: Agent Skills CLI

```bash
# Install all MongoDB skills
npx skills add mongodb/mongodb-agent-skills --skill '*'

# Install a specific skill
npx skills add mongodb/mongodb-agent-skills --skill mongodb-schema-design
```

### Option 3: Web-Based Agents

For web-based AI assistants (ChatGPT, Claude, etc.):
1. Navigate to the skill directory (e.g., `mongodb-schema-design/`)
2. Copy the contents of `SKILL.md`
3. Paste into your conversation or add to project knowledge

## 📊 Why Dual Distribution?

This repository implements a **hybrid approach** based on [Vercel's AGENTS.md research](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals):

| Approach | Pass Rate | Pros | Cons |
|----------|-----------|------|------|
| **Skills only** | 53-79% | On-demand loading, modular | Agents don't always invoke when needed |
| **AGENTS.md only** | 100% | Always available, no invocation decision | Uses more context tokens |
| **Hybrid (both)** | Best of both | Passive fallback + progressive detail | Requires maintaining both formats |

Each skill provides:
- **SKILL.md** (~500 lines) - Agent discovers and activates when relevant
- **AGENTS.md** (~7-9KB) - Compressed index for passive context
- **references/** - Detailed rules loaded progressively (40-289KB total, 82-97% compression)

## 🏗️ Repository Structure

```
mongodb-agent-skills/
├── AGENTS.md                              # Guidelines for AI agents working on this repo
├── README.md                              # This file
├── mongodb-schema-design/                 # Schema design skill
│   ├── SKILL.md                          # Skill definition (on-demand)
│   ├── AGENTS.md                         # Compressed context (passive)
│   ├── README.md                         # Human-readable docs
│   ├── references/                       # Detailed rule files
│   │   ├── REFERENCE.md                  # Compiled guide
│   │   ├── docs-navigation.md            # MongoDB docs URLs
│   │   └── *.md                          # Individual rules
│   └── assets/
│       └── test-cases.json               # Validation tests
├── mongodb-query-and-index-optimize/     # Query optimization skill
├── mongodb-ai/                            # AI/Vector Search skill
├── mongodb-transactions-consistency/      # Transactions skill
├── mongodb-application-frontend/          # Frontend (Next.js + Tailwind) skill
├── mongodb-application-backend/           # Backend (Python + FastAPI) skill
└── mongodb-application-agentic/           # Agentic AI (LangGraph + MCP) skill
```

## 🎓 Example Usage

### With an AI Coding Agent

```
User: "Design a schema for a blog platform with posts, comments, and users"

Agent: [Activates mongodb-schema-design skill]
- Recommends embedding comments (one-to-few) if <100 per post
- Suggests referencing users to avoid duplication
- Warns about unbounded comment arrays
- Provides schema validation example
```

### With Passive Context

```
User: "Why is my query slow?"

Agent: [Has mongodb-query-and-index-optimize in AGENTS.md]
- Immediately checks for missing indexes
- Suggests compound index field order
- Recommends covered queries
- No skill invocation needed
```

## 🤝 Contributing

See [AGENTS.md](./AGENTS.md) for detailed guidelines on creating new skills or improving existing ones.

Key principles:
- Keep SKILL.md under 500 lines
- Keep AGENTS.md under 10KB
- Use MongoDB Shell syntax (not driver-specific)
- Provide clear bad → good examples
- Reference official MongoDB documentation


## 🔗 Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Vercel AGENTS.md Research](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)

