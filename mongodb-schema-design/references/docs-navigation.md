# MongoDB Documentation Navigation — Schema Design

Quick-reference for AI agents to find MongoDB schema and data modeling documentation.

## Fetch Strategy

Append `.md` to any MongoDB doc URL for raw Markdown (most token-efficient). Strip trailing slash first.

```
https://www.mongodb.com/docs/manual/data-modeling.md
```

Fallback: `site:mongodb.com/docs {your query}`

## Key Documentation Pages

All URLs prefix: `https://www.mongodb.com/docs`

### Data Modeling & Schema

| Topic | Path |
|-------|------|
| Data Modeling Introduction | `/manual/data-modeling/` |
| Schema Design Patterns | `/manual/data-modeling/design-patterns/` |
| Schema Validation | `/manual/core/schema-validation/` |
| Specify JSON Schema | `/manual/core/schema-validation/specify-json-schema/` |
| Model Relationships | `/manual/data-modeling/concepts/relationships/` |
| Model Tree Structures | `/manual/data-modeling/concepts/tree-structures/` |
| Operational Factors | `/manual/data-modeling/concepts/data-model-operations/` |

### Schema Anti-Patterns

| Topic | Path |
|-------|------|
| Anti-Patterns Overview | `/manual/data-modeling/design-antipatterns/` |
| Unbounded Arrays | `/manual/data-modeling/design-antipatterns/unbounded-arrays/` |
| Bloated Documents | `/manual/data-modeling/design-antipatterns/bloated-documents/` |

### Collections & Documents

| Topic | Path |
|-------|------|
| BSON Types | `/manual/reference/bson-types/` |
| Document Limits | `/manual/reference/limits/` |
| Capped Collections | `/manual/core/capped-collections/` |
| Time Series Collections | `/manual/core/timeseries-collections/` |
| Views | `/manual/core/views/` |
| Clustered Collections | `/manual/core/clustered-collections/` |

### Relevant Aggregation Stages

All at `/manual/reference/operator/aggregation/{stage}/`:

| Stage | Use Case |
|-------|----------|
| `lookup` | Left outer join (referencing pattern) |
| `graphLookup` | Recursive tree/graph traversal |
| `unwind` | Flatten embedded arrays |
| `merge` | Write transformed data to collection |
| `out` | Replace collection with pipeline results |
| `group` | Aggregate by grouping key |
| `bucket` / `bucketAuto` | Bucket pattern implementation |
| `facet` | Multi-faceted analysis |

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
| Mongoose (ODM) | External: [mongoosejs.com/docs](https://mongoosejs.com/docs) |
| Drivers Hub | `/drivers/` |

## Gotchas

- Default `/manual/` = latest stable release. Pin version with `/manual/v{MAJOR}.{MINOR}/` only for version-specific debugging.
- Driver `current` = latest stable. PyMongo + C++ use `/languages/` path; others use `/drivers/`.
- Mongoose is a third-party ODM, not part of MongoDB official docs.
