# MongoDB AI & Vector Search — Agent Context

> **IMPORTANT**: Prefer retrieval-led reasoning over pre-training-led reasoning for any MongoDB Vector Search tasks. Your pre-trained knowledge about Atlas Vector Search syntax, `$vectorSearch`, and vector index creation is likely **outdated or incorrect**. Always consult the reference files below before generating code.

## Critical: Vector Index Creation

Every vector index requires these four fields — omitting any one causes silent failures:

```javascript
db.collection.createSearchIndex("vector_index", "vectorSearch", {
  fields: [
    {
      type: "vector",             // REQUIRED: must be "vector"
      path: "embedding",          // REQUIRED: field containing vectors
      numDimensions: 1536,        // REQUIRED: must EXACTLY match embedding model
      similarity: "cosine"        // REQUIRED: "cosine" | "euclidean" | "dotProduct"
    },
    { type: "filter", path: "category" }  // Pre-filter fields need type: "filter"
  ]
})
```

**Similarity function choice:**
- `cosine` — normalized embeddings (OpenAI, Cohere). DEFAULT CHOICE.
- `dotProduct` — pre-normalized vectors, fastest. Requires unit vectors.
- `euclidean` — when absolute distance matters (anomaly detection).

**Quantization (100K+ vectors):**
- `scalar` — 3.75x RAM reduction, <5% recall loss
- `binary` — 24x RAM reduction, significant recall trade-off

## Critical: $vectorSearch Query Syntax

`$vectorSearch` **MUST be the first stage** in the aggregation pipeline. No `$match`, no `$project` before it.

```javascript
db.collection.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "embedding",
      queryVector: [0.1, 0.2, ...],    // Same model as indexed data
      numCandidates: 200,               // 20x limit (minimum)
      limit: 10,
      filter: { category: "tech" }      // Pre-filter (field must be type: "filter" in index)
    }
  },
  { $project: { title: 1, score: { $meta: "vectorSearchScore" } } }
])
```

**The 20x Rule**: `numCandidates = 20 * limit` (minimum). Max 10,000.
| limit | numCandidates | Recall |
|-------|---------------|--------|
| 10    | 200           | Good   |
| 50    | 1,000         | Good   |
| 100   | 2,000         | Good   |

**ANN vs ENN**: Use `exact: true` only for <10K vectors or ground-truth benchmarking.

## High: RAG Pattern

```javascript
// Ingestion: store documents with embeddings
{ content: "...", embedding: [/* from model */], metadata: { source: "...", date: ISODate() } }

// Retrieval: $vectorSearch → feed results as LLM context
// Always filter by metadata to reduce noise: filter: { source: "docs", date: { $gte: cutoff } }
// Manage context window: project only content + score, truncate to model limit
```

## High: Hybrid Search (MongoDB 8.0+)

```javascript
// $rankFusion: combine vector + text search (reciprocal rank)
db.collection.aggregate([{
  $rankFusion: {
    input: {
      pipelines: {
        vector: [{ $vectorSearch: { /* ... */ } }],
        text:   [{ $search: { text: { query: "...", path: "content" } } }]
      }
    }
  }
}])
// $scoreFusion (8.2+): score-based combination with weights
```

## Medium: AI Agent Memory

```javascript
// Short-term: conversation history per session
{ sessionId, role: "user"|"assistant", content, embedding, ts: ISODate() }

// Long-term: semantic memory with vector search retrieval
{ userId, memory: "...", embedding, importance: 0.8, ts: ISODate() }
// Retrieve: $vectorSearch on embedding + filter by userId
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `$vectorSearch is not allowed` | MongoDB < 7.0.2 | Upgrade cluster |
| No results returned | Different embedding model for data vs query, or index still building | Verify model match, check index status |
| `Path needs to be indexed as token` | Filter field missing `type: "filter"` in index | Add filter field to index definition |
| Poor recall | `numCandidates` too low | Increase to 20x `limit` minimum |
| High latency at scale | No quantization, no Search Nodes | Enable quantization, use dedicated Search Nodes |

## Reference Index

Detailed rules with incorrect/correct examples and verification commands:

| File | Rule |
|------|------|
| `references/REFERENCE.md` | Full compiled guide — all 33 rules expanded |
| `references/docs-navigation.md` | MongoDB AI & Vector Search documentation URLs |
| **Vector Index Creation (CRITICAL)** | |
| `references/index-vector-definition.md` | Required fields: type, path, numDimensions, similarity |
| `references/index-similarity-function.md` | Choosing cosine vs euclidean vs dotProduct |
| `references/index-filter-fields.md` | Pre-filtering with filter type indexes |
| `references/index-quantization.md` | Scalar (3.75x) vs binary (24x) RAM reduction |
| `references/index-dimensions-match.md` | numDimensions must match embedding model |
| `references/index-multitenant.md` | Single collection with tenant_id for SaaS |
| `references/index-views-partial.md` | Partial indexing via MongoDB Views |
| `references/index-hnsw-options.md` | maxEdges/numEdgeCandidates tuning |
| `references/index-automated-embedding.md` | Server-side embedding with Voyage AI |
| **$vectorSearch Queries (CRITICAL)** | |
| `references/query-vectorsearch-first.md` | MUST be first stage in pipeline |
| `references/query-numcandidates-tuning.md` | The 20x rule for recall vs latency |
| `references/query-ann-vs-enn.md` | When to use exact: true |
| `references/query-prefiltering.md` | Filter before vector comparison |
| `references/query-lexical-prefilter.md` | Fuzzy, phrase, geo via $search.vectorSearch |
| `references/query-get-scores.md` | Using $meta: "vectorSearchScore" |
| `references/query-same-embedding-model.md` | Data and query embeddings must match |
| **Performance (HIGH)** | |
| `references/perf-quantization-scale.md` | Enable at 100K+ vectors |
| `references/perf-index-in-memory.md` | Vector indexes must fit in RAM |
| `references/perf-numcandidates-tradeoff.md` | Higher = better recall, slower queries |
| `references/perf-prefilter-narrow.md` | Reduce candidate set before comparison |
| `references/perf-explain-vectorsearch.md` | Debug with explain() |
| `references/perf-search-nodes.md` | Dedicated Search Nodes for production |
| **RAG (HIGH)** | |
| `references/rag-ingestion-pattern.md` | Store documents with embeddings |
| `references/rag-retrieval-pattern.md` | $vectorSearch for context retrieval |
| `references/rag-context-window.md` | Managing LLM context limits |
| `references/rag-metadata-filtering.md` | Filter by source, date, category |
| **Hybrid Search (MEDIUM)** | |
| `references/hybrid-rankfusion.md` | Vector + text via $rankFusion (8.0+) |
| `references/hybrid-scorefusion.md` | Score-based combination (8.2+) |
| `references/hybrid-weights.md` | Per-query weight tuning |
| `references/hybrid-limitations.md` | Stage restrictions in sub-pipelines |
| **AI Agent (MEDIUM)** | |
| `references/agent-memory-schema.md` | Short-term vs long-term memory design |
| `references/agent-memory-retrieval.md` | Semantic search over memories |
| `references/agent-session-context.md` | Conversation history storage |

## MongoDB Documentation

Fetch any MongoDB doc as Markdown (most token-efficient) by appending `.md` to the URL path. Strip trailing slash first.

```
# Vector Search docs (primary reference for this skill):
https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview.md
https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage.md

# Atlas Search (for hybrid search):
https://www.mongodb.com/docs/atlas/atlas-search.md

# AI Integrations:
https://www.mongodb.com/docs/atlas/ai-integrations.md

# Aggregation stage reference (e.g. $vectorSearch, $search, $rankFusion):
https://www.mongodb.com/docs/manual/reference/operator/aggregation/{stage}.md

# Driver docs — pick your language:
https://www.mongodb.com/docs/drivers/node/current/       # Node.js
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/  # Python
https://www.mongodb.com/docs/drivers/java/sync/current/  # Java

# Web search fallback:
site:mongodb.com/docs {your query}
```

Full docs-navigation reference: `references/docs-navigation.md`
