# MongoDB Query & Index Optimization — Agent Context

> **IMPORTANT**: Prefer retrieval-led reasoning over pre-training-led reasoning for any MongoDB query or index tasks. If there is no index, it is a collection scan. A 10ms query on 10K documents becomes a 10-second query on 10M documents. Always consult the reference files below.

## Critical: The ESR Rule (Equality-Sort-Range)

The single most important rule for compound index field order:

```javascript
// Query: status = "active" AND createdAt > lastWeek ORDER BY priority
// Index: Equality → Sort → Range
db.tasks.createIndex({ status: 1, priority: 1, createdAt: 1 })
```

| Position | Type | Why |
|----------|------|-----|
| First | Equality (`=`) | Narrows to exact matches |
| Second | Sort (`ORDER BY`) | Avoids in-memory sort |
| Third | Range (`>`, `<`, `$in`) | Scans within sorted data |

**Wrong order causes in-memory sorts (100x slower) or full collection scans.**

## Critical: Index Essentials

```javascript
// Compound indexes serve PREFIX queries (left-to-right)
// Index {a, b, c} serves: {a}, {a,b}, {a,b,c} — NOT {b}, {c}, {b,c}
db.coll.createIndex({ a: 1, b: 1, c: 1 })

// Covered queries: include projected fields in index → skip document fetch (10-100x faster)
db.orders.createIndex({ status: 1, total: 1 })
db.orders.find({ status: "active" }, { _id: 0, status: 1, total: 1 })  // Covered!

// Verify with explain():
db.coll.find(query).explain("executionStats")
// Look for: stage: "IXSCAN" (good) vs "COLLSCAN" (bad)
// Look for: totalDocsExamined vs totalKeysExamined

// Remove unused indexes (each index costs RAM + write overhead):
db.coll.aggregate([{ $indexStats: {} }])
// Drop indexes with 0 ops over 30+ days
```

## High: Specialized Indexes

| Type | Use Case | Syntax |
|------|----------|--------|
| Unique | Enforce uniqueness | `createIndex({email:1}, {unique:true})` |
| Partial | Index subset of docs | `createIndex({status:1}, {partialFilterExpression:{status:"active"}})` |
| TTL | Auto-expire documents | `createIndex({createdAt:1}, {expireAfterSeconds:86400})` |
| Text | Full-text search | `createIndex({content:"text"})` |
| Wildcard | Dynamic/polymorphic fields | `createIndex({"metadata.$**":1})` |
| 2dsphere | Geospatial queries | `createIndex({location:"2dsphere"})` |
| Hashed | Equality-only, shard keys | `createIndex({userId:"hashed"})` |
| Hidden | Test removal safely | `db.coll.hideIndex("index_name")` |

## High: Query Anti-Patterns

```javascript
// BAD: $ne/$nin — cannot use index efficiently, causes COLLSCAN
db.users.find({ status: { $ne: "deleted" } })
// GOOD: use $in with the values you want
db.users.find({ status: { $in: ["active", "pending"] } })

// BAD: unanchored regex — full index/collection scan
db.users.find({ name: /smith/ })
// GOOD: anchored regex — uses index prefix
db.users.find({ name: /^smith/i })

// BAD: skip-based pagination — O(n) for deep pages
db.items.find().sort({_id:1}).skip(10000).limit(20)
// GOOD: range-based pagination — O(1)
db.items.find({_id: {$gt: lastSeenId}}).sort({_id:1}).limit(20)

// BAD: N+1 queries in a loop
for (const id of orderIds) { await db.products.findOne({_id: id}) }
// GOOD: batch with $in
db.products.find({ _id: { $in: orderIds } })
```

## High: Aggregation Optimization

```javascript
// 1. $match FIRST — use indexes, reduce documents early
db.orders.aggregate([
  { $match: { status: "active", date: { $gte: cutoff } } },  // First!
  { $group: { _id: "$customerId", total: { $sum: "$amount" } } }
])

// 2. $project early — reduce document size through pipeline
// 3. $sort + $limit coalesce — top-N uses bounded memory
{ $sort: { score: -1 } }, { $limit: 10 }  // MongoDB optimizes this internally

// 4. $lookup MUST have index on foreign field
db.orders.aggregate([
  { $lookup: { from: "products", localField: "productId", foreignField: "_id", as: "product" } }
])
// Ensure: db.products has index on _id (default) or the foreignField used

// 5. allowDiskUse for >100MB aggregations
db.coll.aggregate(pipeline, { allowDiskUse: true })
```

## Medium: Performance Diagnostics

```javascript
// explain() — always check query plans
db.coll.find(query).explain("executionStats")
// Key fields: winningPlan.stage, totalDocsExamined, executionTimeMillis

// Slow query profiler (operations >100ms)
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(5)

// MongoDB 8.0: $queryStats for workload analysis
db.aggregate([{ $queryStats: {} }, { $sort: { "key.queryShape": 1 } }])

// MongoDB 8.0: persistent index hints via Query Settings
db.adminCommand({ setQuerySettings: queryShape, settings: { indexHints: { ns: {...}, allowedIndexes: ["idx"] } } })
```

## MongoDB 8.0 Features

```javascript
// Cross-collection atomic bulkWrite (new in 8.0)
db.adminCommand({
  bulkWrite: 1,
  ops: [
    { insert: 0, document: { _id: 1, item: "abc" } },
    { update: 1, filter: { stock: "abc" }, updateMods: { $inc: { qty: -1 } } }
  ],
  nsInfo: [{ ns: "db.orders" }, { ns: "db.inventory" }]
})

// Deterministic updateOne with sort (new in 8.0)
db.tasks.updateOne({ status: "pending" }, { $set: { status: "processing" } }, { sort: { priority: -1 } })
```

## Reference Index

Detailed rules with incorrect/correct examples and verification commands:

| File | Rule |
|------|------|
| `references/REFERENCE.md` | Full compiled guide — all 46 rules expanded |
| `references/docs-navigation.md` | MongoDB query & index documentation URLs |
| **Index Essentials (CRITICAL)** | |
| `references/index-compound-field-order.md` | ESR rule — Equality, Sort, Range |
| `references/index-compound-multi-field.md` | Compound indexes for multi-field queries |
| `references/index-ensure-usage.md` | Avoid COLLSCAN, verify with explain() |
| `references/index-remove-unused.md` | Audit with $indexStats |
| `references/index-high-cardinality-first.md` | Selective fields at index start |
| `references/index-covered-queries.md` | Include projected fields |
| `references/index-prefix-principle.md` | Compound prefix serves subset queries |
| `references/index-creation-background.md` | Non-blocking index builds |
| `references/index-size-considerations.md` | Keep indexes in RAM |
| **Specialized Indexes (HIGH)** | |
| `references/index-unique.md` | Enforce uniqueness |
| `references/index-partial.md` | Index document subsets |
| `references/index-sparse.md` | Skip missing fields |
| `references/index-ttl.md` | Auto-expire documents |
| `references/index-text-search.md` | Full-text search |
| `references/index-wildcard.md` | Dynamic field indexing |
| `references/index-multikey.md` | Array field indexing |
| `references/index-geospatial.md` | Location queries |
| `references/index-hashed.md` | Equality + shard keys |
| `references/index-clustered.md` | Ordered storage |
| `references/index-hidden.md` | Safe index removal testing |
| **Query Patterns (HIGH)** | |
| `references/query-use-projection.md` | Fetch only needed fields |
| `references/query-avoid-ne-nin.md` | Use $in instead |
| `references/query-or-index.md` | All $or clauses need indexes |
| `references/query-anchored-regex.md` | Start regex with ^ |
| `references/query-batch-operations.md` | Avoid N+1 |
| `references/query-pagination.md` | Range-based pagination |
| `references/query-exists-with-sparse.md` | $exists with sparse indexes |
| `references/query-sort-collation.md` | Match sort to indexes |
| `references/query-bulkwrite-command.md` | MongoDB 8.0 cross-collection batch |
| `references/query-updateone-sort.md` | MongoDB 8.0 deterministic updates |
| **Aggregation (HIGH)** | |
| `references/agg-match-early.md` | $match at pipeline start |
| `references/agg-project-early.md` | Reduce document size early |
| `references/agg-sort-limit.md` | $sort + $limit coalescence |
| `references/agg-lookup-index.md` | Index $lookup foreign fields |
| `references/agg-graphlookup.md` | Recursive graph traversal |
| `references/agg-avoid-large-unwind.md` | Don't $unwind massive arrays |
| `references/agg-allowdiskuse.md` | Handle >100MB aggregations |
| `references/agg-group-memory-limit.md` | Control $group memory |
| **Diagnostics (MEDIUM)** | |
| `references/perf-explain-interpretation.md` | Read explain() output |
| `references/perf-slow-query-log.md` | Find slow operations |
| `references/perf-index-stats.md` | Find unused indexes |
| `references/perf-query-plan-cache.md` | Manage query plan cache |
| `references/perf-use-hint.md` | Force index selection |
| `references/perf-atlas-performance-advisor.md` | Atlas index suggestions |
| `references/perf-query-stats.md` | MongoDB 8.0 $queryStats |
| `references/perf-query-settings.md` | MongoDB 8.0 persistent hints |

## MongoDB Documentation

Fetch any MongoDB doc as Markdown (most token-efficient) by appending `.md` to the URL path. Strip trailing slash first.

```
# Indexes (primary reference for this skill):
https://www.mongodb.com/docs/manual/indexes.md

# Aggregation:
https://www.mongodb.com/docs/manual/aggregation.md

# Aggregation stage reference (e.g. $match, $group, $lookup, $graphLookup):
https://www.mongodb.com/docs/manual/reference/operator/aggregation/{stage}.md

# Query operator reference (e.g. $eq, $in, $regex, $elemMatch):
https://www.mongodb.com/docs/manual/reference/operator/query/{op}.md

# explain() reference:
https://www.mongodb.com/docs/manual/reference/command/explain.md

# CRUD operations:
https://www.mongodb.com/docs/manual/crud.md

# Driver docs — pick your language:
https://www.mongodb.com/docs/drivers/node/current/       # Node.js
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/  # Python
https://www.mongodb.com/docs/drivers/java/sync/current/  # Java

# Web search fallback:
site:mongodb.com/docs {your query}
```

Full docs-navigation reference: `references/docs-navigation.md`
