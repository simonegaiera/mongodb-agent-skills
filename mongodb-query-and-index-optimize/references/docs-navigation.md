# MongoDB Documentation Navigation — Query & Index Optimization

Quick-reference for AI agents to find MongoDB query and index documentation.

## Fetch Strategy

Append `.md` to any MongoDB doc URL for raw Markdown (most token-efficient). Strip trailing slash first.

```
https://www.mongodb.com/docs/manual/indexes.md
```

Fallback: `site:mongodb.com/docs {your query}`

## Key Documentation Pages

All URLs prefix: `https://www.mongodb.com/docs`

### Indexes

| Topic | Path |
|-------|------|
| Indexes Overview | `/manual/indexes/` |
| Compound Indexes | `/manual/core/index-compound/` |
| Multikey Indexes | `/manual/core/index-multikey/` |
| Text Indexes | `/manual/core/index-text/` |
| Wildcard Indexes | `/manual/core/index-wildcard/` |
| 2dsphere Indexes | `/manual/core/2dsphere/` |
| Hashed Indexes | `/manual/core/index-hashed/` |
| Partial Indexes | `/manual/core/index-partial/` |
| Sparse Indexes | `/manual/core/index-sparse/` |
| TTL Indexes | `/manual/core/index-ttl/` |
| Unique Indexes | `/manual/core/index-unique/` |
| Hidden Indexes | `/manual/core/index-hidden/` |
| Clustered Collections | `/manual/core/clustered-collections/` |
| Index Build on Populated Collections | `/manual/core/index-creation/` |

### CRUD & Query

| Topic | Path |
|-------|------|
| CRUD Operations | `/manual/crud/` |
| Query Documents | `/manual/tutorial/query-documents/` |
| Explain Results | `/manual/reference/explain-results/` |
| explain Command | `/manual/reference/command/explain/` |
| Read Preference | `/manual/core/read-preference/` |
| Profiler | `/manual/tutorial/manage-the-database-profiler/` |

### Query Operators

All at `/manual/reference/operator/query/{op}/`:

| Operator | Purpose |
|----------|---------|
| `eq`, `ne`, `gt`, `gte`, `lt`, `lte` | Comparison |
| `in`, `nin` | Set membership |
| `and`, `or`, `not`, `nor` | Logical |
| `exists`, `type` | Element |
| `regex` | Pattern matching |
| `elemMatch` | Array element matching |
| `all`, `size` | Array queries |
| `near`, `geoWithin`, `geoIntersects` | Geospatial |
| `text` | Text search |
| `expr` | Aggregation expressions in queries |

### Aggregation

| Topic | Path |
|-------|------|
| Aggregation Overview | `/manual/aggregation/` |
| Aggregation Pipeline | `/manual/core/aggregation-pipeline/` |
| allowDiskUse | `/manual/reference/command/aggregate/#std-label-aggregate-cmd-allowDiskUse` |

### Aggregation Stages

All at `/manual/reference/operator/aggregation/{stage}/`:

| Stage | Use Case |
|-------|----------|
| `match` | Filter documents |
| `group` | Group and aggregate |
| `project` | Reshape documents |
| `sort` | Order results |
| `limit` / `skip` | Pagination |
| `lookup` | Left outer join |
| `graphLookup` | Recursive graph traversal |
| `unwind` | Flatten arrays |
| `merge` | Write results to collection |
| `out` | Replace collection with results |
| `facet` | Multi-faceted aggregation |
| `bucket` / `bucketAuto` | Categorical grouping |
| `unionWith` | Combine pipeline results |
| `indexStats` | Index usage statistics |

### Performance & Diagnostics

| Topic | Path |
|-------|------|
| Shell Methods | `/manual/reference/method/` |
| Database Commands | `/manual/reference/command/` |
| Limits | `/manual/reference/limits/` |
| Error Codes | `/manual/reference/error-codes/` |
| Connection Strings | `/manual/reference/connection-string/` |

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

- Default `/manual/` = latest stable release. Pin version with `/manual/v{MAJOR}.{MINOR}/` only for version-specific debugging.
- Driver `current` = latest stable. PyMongo + C++ use `/languages/` path; others use `/drivers/`.
- Atlas CLI uses `/atlas/cli/current/` not `/atlas/cli/latest/`.
