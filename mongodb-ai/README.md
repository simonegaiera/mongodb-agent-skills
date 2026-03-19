# MongoDB AI Skill

MongoDB Atlas Vector Search and AI integration patterns for AI agents and developers.

## Why This Skill Exists

AI coding agents have knowledge cutoffs and lack accurate information about MongoDB's newer AI capabilities:

- **Atlas Vector Search** syntax and configuration
- **$vectorSearch** aggregation stage
- **numCandidates** tuning (the 20x rule)
- **Vector Quantization** (scalar/binary)
- **Hybrid Search** with $rankFusion
- **RAG implementation** patterns
- **AI Agent memory** storage

This skill bridges that knowledge gap with accurate, up-to-date guidance.

## Installation

### Passive context (recommended)
Copy the content of `AGENTS.md` into your project's root `AGENTS.md`. This gives any AI coding agent critical MongoDB AI knowledge on every turn.

### Agent Skills CLI
```bash
npx skills add simonegaiera/mongodb-agent-skills --skill mongodb-ai
```

### Web-based agents
Add the skill to project knowledge or paste `SKILL.md` contents into the conversation.

## What's Included

### 33 Rules Across 6 Categories

| Category | Impact | Rules |
|----------|--------|-------|
| Vector Index Creation | CRITICAL | 9 |
| $vectorSearch Queries | CRITICAL | 7 |
| Performance Tuning | HIGH | 6 |
| RAG Patterns | HIGH | 4 |
| Hybrid Search | MEDIUM | 4 |
| AI Agent Integration | MEDIUM | 3 |

### Key Topics

- Vector index definition (type, path, numDimensions, similarity)
- Similarity function selection (cosine vs euclidean vs dotProduct)
- Filter field indexing for pre-filtering
- Vector quantization for scale (scalar: 3.75x, binary: 24x RAM reduction)
- $vectorSearch syntax and constraints
- numCandidates tuning (the 20x rule)
- ANN vs ENN search selection
- Pre-filtering vs post-filtering
- Score retrieval with $meta
- RAG ingestion, retrieval, and context management
- Hybrid search with $rankFusion
- AI agent memory schemas

## Usage

When you're working on MongoDB AI features, the skill triggers automatically on keywords like:
- "vector search", "vector index"
- "$vectorSearch", "embedding"
- "semantic search", "RAG"
- "numCandidates", "similarity"
- "hybrid search", "$rankFusion"
- "AI agent", "LLM memory"

## MCP Integration

For automatic verification, connect the MongoDB MCP Server:

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server", "--readOnly"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "your-connection-string"
      }
    }
  }
}
```

## Files

```
mongodb-ai/
  SKILL.md           # Skill definition (for skills-based agents)
  AGENTS.md          # Compressed context (for project-root embedding)
  README.md          # This file
  references/
    REFERENCE.md     # Full compiled guide with all rules expanded
    _sections.md     # Section definitions
    index-*.md       # Vector index rules
    query-*.md       # $vectorSearch rules
    perf-*.md        # Performance rules
    rag-*.md         # RAG pattern rules
    hybrid-*.md      # Hybrid search rules
    agent-*.md       # AI agent rules
  assets/
    test-cases.json  # Validation test cases
```

## License

Apache-2.0

## Contributing

Issues and PRs welcome at the main repository.
