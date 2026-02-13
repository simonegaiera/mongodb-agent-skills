# MongoDB Documentation Navigation — AI & Vector Search

Quick-reference for AI agents to find MongoDB AI and Vector Search documentation.

## Fetch Strategy

Append `.md` to any MongoDB doc URL for raw Markdown (most token-efficient). Strip trailing slash first.

```
https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview.md
```

Fallback: `site:mongodb.com/docs {your query}`

## Key Documentation Pages

All URLs prefix: `https://www.mongodb.com/docs`

### Atlas Vector Search

| Topic | Path |
|-------|------|
| Vector Search Overview | `/atlas/atlas-vector-search/vector-search-overview/` |
| $vectorSearch Stage | `/atlas/atlas-vector-search/vector-search-stage/` |
| Vector Search Index Definition | `/atlas/atlas-vector-search/vector-search-type/` |
| Vector Search Tutorials | `/atlas/atlas-vector-search/tutorials/` |
| Vector Search Filters | `/atlas/atlas-vector-search/vector-search-stage/#atlas-vector-search-pre-filter` |

### Atlas Search (for Hybrid Search)

| Topic | Path |
|-------|------|
| Atlas Search Overview | `/atlas/atlas-search/` |
| $search Stage | `/atlas/atlas-search/query-syntax/` |
| Search Index Definition | `/atlas/atlas-search/define-field-mappings/` |
| Scoring | `/atlas/atlas-search/scoring/` |

### AI Integrations

| Topic | Path |
|-------|------|
| AI Integrations Hub | `/atlas/ai-integrations/` |
| LangChain Integration | `/atlas/ai-integrations/langchain/` |
| LlamaIndex Integration | `/atlas/ai-integrations/llamaindex/` |

### Relevant Aggregation Stages

All at `/manual/reference/operator/aggregation/{stage}/`:

| Stage | Use Case |
|-------|----------|
| `vectorSearch` | Atlas Vector Search queries |
| `search` | Atlas Search queries |
| `rankFusion` | Hybrid search — reciprocal rank (8.0+) |
| `scoreFusion` | Hybrid search — score-based (8.2+) |
| `project` | Reshape documents, extract scores |
| `match` | Filter results post-search |
| `limit` | Cap result count |
| `unwind` | Flatten array results |

## Driver Documentation

| Driver | URL Path |
|--------|----------|
| Node.js | `/drivers/node/current/` |
| PyMongo | `/languages/python/pymongo-driver/current/` |
| Java Sync | `/drivers/java/sync/current/` |
| Go | `/drivers/go/current/` |
| C#/.NET | `/drivers/csharp/current/` |
| Rust | `/drivers/rust/current/` |
| Kotlin | `/drivers/kotlin/coroutine/current/` |
| Motor (async Python) | `/drivers/motor/` |
| Drivers Hub | `/drivers/` |

## Gotchas

- **Vector Search docs live under `/atlas/`**.
- Driver `current` = latest stable. PyMongo + C++ use `/languages/` path; others use `/drivers/`.
- Default `/manual/` = latest stable release. Pin version with `/manual/v{MAJOR}.{MINOR}/` only when debugging version-specific behavior.
