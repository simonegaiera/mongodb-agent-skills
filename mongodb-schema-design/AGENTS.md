# MongoDB Schema Design — Agent Context

> **IMPORTANT**: Prefer retrieval-led reasoning over pre-training-led reasoning for any MongoDB schema design tasks. Bad schema is the root cause of most MongoDB performance and cost issues — queries and indexes cannot fix a fundamentally wrong model. Always consult the reference files below.

## Core Principle

> **Data that is accessed together should be stored together.**

Embedding related data eliminates joins, reduces round trips, and enables atomic updates. Reference only when you must.

## Critical: Schema Anti-Patterns

These are the #1 cause of MongoDB production outages:

**1. Unbounded arrays** — arrays that grow without limit hit the 16MB BSON limit and crash writes.
```javascript
// BAD: activity log grows forever in user document
{ _id: "user123", activityLog: [ /* grows to 100K+ entries → 15MB+ → crash */ ] }

// GOOD: separate collection with reference
{ _id: "user123", lastActivity: ISODate() }
// activities collection: { userId: "user123", action: "login", ts: ISODate() }
```

**2. Bloated documents** — MongoDB loads entire documents into RAM, even when queries need few fields.
```javascript
// BAD: 665KB document (images, reviews, history all embedded)
// 1GB RAM = 1,500 products cached

// GOOD: hot data only (~500 bytes), cold data in separate collections
{ _id: "prod123", name: "Laptop", price: 999, thumbnail: "url", avgRating: 4.5 }
// 1GB RAM = 2,000,000 products cached
```

**3. Massive arrays (>1000 elements)** — degrade read/write performance even before hitting 16MB.

**4. Excessive $lookup** — if you're doing 3+ $lookups, your schema is too normalized. Denormalize.

**5. Schema drift** — enforce structure with JSON Schema validation to prevent inconsistent documents.

## High: Embed vs Reference Decision

| Relationship | Cardinality | Access Pattern | Recommendation |
|-------------|-------------|----------------|----------------|
| One-to-One | 1:1 | Always together | **Embed** |
| One-to-Few | 1:N (N < 100) | Usually together | **Embed array** |
| One-to-Many | 1:N (N > 100) | Often separate | **Reference** |
| One-to-Squillions | 1:N (N > 10K) | Always separate | **Reference + summary** |
| Many-to-Many | M:N | Varies | **Two-way reference** |

**Embed when**: data is read together, bounded, and doesn't change independently.
**Reference when**: data is unbounded, changes independently, or is shared across entities.

## High: Relationship Patterns

```javascript
// One-to-Few: embed bounded arrays (addresses, phones)
{ name: "Alice", addresses: [{ street: "123 Main", city: "NYC" }] }  // Max ~10 addresses

// One-to-Many: reference by parent ID
// parent: { _id: "dept1", name: "Engineering" }
// children: { _id: "emp1", deptId: "dept1", name: "Bob" }

// One-to-Squillions: reference + denormalized summary
{ _id: "host1", name: "web-01", lastLog: ISODate(), logCount: 5000000 }
// logs: { hostId: "host1", message: "...", ts: ISODate() }

// Many-to-Many: two-way references
{ _id: "student1", courseIds: ["c1", "c2"] }
{ _id: "c1", studentIds: ["student1", "student2"] }

// Tree: materialized path for fast subtree queries
{ _id: "cat1", name: "Electronics", path: ",root,electronics," }
// Find subtree: db.categories.find({ path: /,electronics,/ })
```

## Medium: Design Patterns

| Pattern | Use Case | Key Idea |
|---------|----------|----------|
| Bucket | Time-series/IoT data | Group events into time-windowed documents |
| Time Series Collections | Native time-series | Use `timeseries` collection option (MongoDB 5.0+) |
| Attribute | Many optional fields | Collapse into `attributes: [{k,v}]` array |
| Polymorphic | Different types in one collection | Add `type` discriminator field |
| Schema Versioning | Schema evolution | Add `schemaVersion` field, migrate on read |
| Computed | Expensive aggregations | Pre-calculate and store results |
| Subset | Hot/cold data split | Main doc has recent data, archive has history |
| Outlier | Exceptional large documents | Flag with `hasOverflow: true`, store excess separately |
| Extended Reference | Reduce $lookup | Cache frequently-accessed fields from related docs |
| Archive | Historical data | Move old data to cheaper storage |

## Medium: Schema Validation

```javascript
// Define validation at collection level
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name", "role"],
      properties: {
        email: { bsonType: "string", pattern: "^.+@.+$" },
        name: { bsonType: "string", minLength: 1 },
        role: { enum: ["admin", "user", "viewer"] }
      }
    }
  },
  validationLevel: "moderate",   // "strict" (all docs) or "moderate" (inserts + updates to valid docs)
  validationAction: "error"      // "error" (reject) or "warn" (log only)
})

// Rollout strategy: warn → monitor → error
db.runCommand({ collMod: "users", validationAction: "warn" })      // Phase 1: observe
// ... fix violations ...
db.runCommand({ collMod: "users", validationAction: "error" })     // Phase 2: enforce
```

## Diagnostic Commands

```javascript
// Find largest documents (bloat detection)
db.coll.aggregate([
  { $project: { size: { $bsonSize: "$$ROOT" }, name: 1 } },
  { $sort: { size: -1 } },
  { $limit: 10 }
])

// Find largest arrays (unbounded array detection)
db.coll.aggregate([
  { $project: { arrayLen: { $size: { $ifNull: ["$items", []] } } } },
  { $sort: { arrayLen: -1 } },
  { $limit: 10 }
])
```

## Reference Index

Detailed rules with incorrect/correct examples and verification commands:

| File | Rule |
|------|------|
| `references/REFERENCE.md` | Full compiled guide — all 30 rules expanded |
| `references/docs-navigation.md` | MongoDB schema design documentation URLs |
| **Anti-Patterns (CRITICAL)** | |
| `references/antipattern-unbounded-arrays.md` | Never allow arrays to grow without limit |
| `references/antipattern-bloated-documents.md` | Keep documents under 16KB for working set |
| `references/antipattern-massive-arrays.md` | Arrays >1000 elements hurt performance |
| `references/antipattern-unnecessary-collections.md` | Fewer collections, more embedding |
| `references/antipattern-excessive-lookups.md` | Reduce $lookup by denormalizing |
| `references/antipattern-schema-drift.md` | Enforce consistent structure |
| **Fundamentals (HIGH)** | |
| `references/fundamental-embed-vs-reference.md` | Decision framework for relationships |
| `references/fundamental-data-together.md` | Data accessed together stored together |
| `references/fundamental-document-model.md` | Embrace documents, avoid SQL patterns |
| `references/fundamental-schema-validation.md` | Enforce structure with JSON Schema |
| `references/fundamental-16mb-awareness.md` | Design around BSON document limit |
| **Relationships (HIGH)** | |
| `references/relationship-one-to-one.md` | Embed for simplicity |
| `references/relationship-one-to-few.md` | Embed bounded arrays |
| `references/relationship-one-to-many.md` | Reference for large sets |
| `references/relationship-one-to-squillions.md` | Reference + summaries |
| `references/relationship-many-to-many.md` | Two-way referencing |
| `references/relationship-tree-structures.md` | Parent/child/materialized path |
| **Design Patterns (MEDIUM)** | |
| `references/pattern-archive.md` | Historical data management |
| `references/pattern-attribute.md` | Key-value for optional fields |
| `references/pattern-bucket.md` | Time-series grouping |
| `references/pattern-time-series-collections.md` | Native time series |
| `references/pattern-extended-reference.md` | Cache related data |
| `references/pattern-subset.md` | Hot/cold data split |
| `references/pattern-computed.md` | Pre-calculated aggregations |
| `references/pattern-outlier.md` | Handle exceptional documents |
| `references/pattern-polymorphic.md` | Heterogeneous documents |
| `references/pattern-schema-versioning.md` | Safe schema evolution |
| **Validation (MEDIUM)** | |
| `references/validation-json-schema.md` | Data type and structure validation |
| `references/validation-action-levels.md` | Warn vs error mode |
| `references/validation-rollout-strategy.md` | Safe production rollout |

## MongoDB Documentation

Fetch any MongoDB doc as Markdown (most token-efficient) by appending `.md` to the URL path. Strip trailing slash first.

```
# Data Modeling (primary reference for this skill):
https://www.mongodb.com/docs/manual/data-modeling.md

# Schema Design Patterns:
https://www.mongodb.com/docs/manual/data-modeling/design-patterns.md

# Schema Validation:
https://www.mongodb.com/docs/manual/core/schema-validation.md

# BSON Types & Limits:
https://www.mongodb.com/docs/manual/reference/limits.md

# Time Series Collections:
https://www.mongodb.com/docs/manual/core/timeseries-collections.md

# Driver docs — pick your language:
https://www.mongodb.com/docs/drivers/node/current/       # Node.js
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/  # Python
https://www.mongodb.com/docs/drivers/java/sync/current/  # Java

# Web search fallback:
site:mongodb.com/docs {your query}
```

Full docs-navigation reference: `references/docs-navigation.md`
