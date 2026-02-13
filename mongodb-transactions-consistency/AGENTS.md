# MongoDB Transactions & Consistency — Agent Context

> **IMPORTANT**: Prefer retrieval-led reasoning over pre-training-led reasoning for any MongoDB transaction tasks. Transactions are a correctness tool, not a default coding pattern. Single-document writes are already atomic in MongoDB — use transactions only when business invariants span documents, collections, or shards. Always consult the reference files below.

## Critical: Transaction Fundamentals

**1. Use `withTransaction` (callback API) by default** — it handles retries automatically:
```javascript
const session = client.startSession()
await session.withTransaction(async () => {
  await orders.updateOne({ _id: orderId }, { $set: { status: "paid" } }, { session })
  await ledger.insertOne({ orderId, event: "paid", at: new Date() }, { session })
}, {
  readPreference: "primary",
  readConcern: { level: "snapshot" },
  writeConcern: { w: "majority", wtimeout: 5000 }
})
session.endSession()
```

**2. Pass `{ session }` to EVERY operation** — missing it on one operation silently runs outside the transaction:
```javascript
// BAD: ledger write is outside the transaction
await ledger.insertOne({ orderId, event: "paid" })           // Missing { session }!

// GOOD: all operations include session
await ledger.insertOne({ orderId, event: "paid" }, { session })
```

**3. One transaction per session** — don't run parallel operations on the same session:
```javascript
// BAD: Promise.all with same session
await Promise.all([op1({session}), op2({session})])

// GOOD: serialize operations
await op1({ session })
await op2({ session })
```

**4. Use `primary` read preference** — transactions must read from the primary node.

**5. Set write concern explicitly** — use `w: "majority"` for business-critical workflows.

## Critical: Retry and Error Handling

**TransientTransactionError** — retry the ENTIRE transaction (not just the failed operation):
```javascript
// withTransaction handles this automatically
// Core API: catch error, check error.hasErrorLabel("TransientTransactionError"), restart from startTransaction()
```

**UnknownTransactionCommitResult** — retry ONLY the commit:
```javascript
// withTransaction handles this automatically
// Core API: catch error, check error.hasErrorLabel("UnknownTransactionCommitResult"), retry commitTransaction()
```

**TransactionTooLargeForCache** — this is a REDESIGN signal, not a retry scenario:
- Break into smaller transactions
- Move bulk operations outside transactions
- Increase WiredTiger cache if appropriate

**Duplicate-key upsert (MongoDB 8.1+)** — behavior changed; upserts that hit duplicate keys inside transactions may now succeed on retry instead of failing. Make transaction bodies idempotent.

## High: Consistency Semantics

| Read Concern | Guarantee | Use Case |
|-------------|-----------|----------|
| `local` | Fastest, may see rollback data | Non-critical reads |
| `majority` | Durable, won't be rolled back | Default for important data |
| `snapshot` | Point-in-time consistency | Multi-document transactions |

**Causal consistency**: pair `readConcern: "majority"` + `writeConcern: "majority"` to guarantee read-your-writes.

**Rollback risk**: `readConcern: "local"` + `writeConcern: 1` = data may disappear on failover. Never use for financial or critical data.

## High: Operational Constraints

**Transaction lifetime**: default 60 seconds. Keep transactions short — long transactions hold locks and block other operations.

```javascript
// Check/tune lifetime limit
db.adminCommand({ getParameter: 1, transactionLifetimeLimitSeconds: 1 })
// Tune lock timeout (default 5ms)
db.adminCommand({ setParameter: 1, maxTransactionLockRequestTimeoutMillis: 25 })
```

**Sharded cluster caveats**:
- First operation determines the shard routing
- Cross-shard transactions have higher latency
- Arbiter-bearing shard in replica set prevents transactions
- DDL operations (createCollection, createIndex) not allowed in transactions

**Restricted operations inside transactions**:
- No `createCollection`, `createIndex`, `dropCollection`
- No `count` (use `countDocuments` or aggregation)
- No `$merge`, `$out` stages
- No capped collections

## Medium: Implementation Patterns

**withTransaction vs Core API**:
| Aspect | `withTransaction` (callback) | Core API |
|--------|------------------------------|----------|
| Retry handling | Automatic | Manual |
| Complexity | Lower | Higher |
| Control | Less | Full |
| Recommendation | **Default choice** | Only when you need custom retry logic |

**Idempotent transaction bodies** — transactions may retry; design for it:
```javascript
// BAD: non-idempotent — creates duplicate on retry
await coll.insertOne({ orderId, amount: 100 }, { session })

// GOOD: idempotent — safe under retry
await coll.updateOne(
  { orderId },
  { $setOnInsert: { orderId, amount: 100, createdAt: new Date() } },
  { upsert: true, session }
)
```

**Observability** — instrument transaction outcomes:
```javascript
// Track: commit success, commit retry count, abort cause, duration
// Use driver command monitoring or APM events
// Alert on: retry rate > 5%, abort rate > 1%, duration > 10s
```

## Reference Index

Detailed rules with incorrect/correct examples and verification commands:

| File | Rule |
|------|------|
| `references/REFERENCE.md` | Full compiled guide — all 20 rules expanded |
| `references/docs-navigation.md` | MongoDB transaction & consistency documentation URLs |
| **Transaction Fundamentals (CRITICAL)** | |
| `references/fundamental-use-transactions-when-required.md` | When to use transactions |
| `references/fundamental-propagate-session.md` | Pass session to every operation |
| `references/fundamental-one-transaction-per-session.md` | One active transaction per session |
| `references/fundamental-primary-read-preference.md` | Use primary read preference |
| `references/fundamental-commit-write-concern.md` | Set commit durability explicitly |
| **Consistency Semantics (HIGH)** | |
| `references/consistency-read-concern-levels.md` | local vs majority vs snapshot |
| `references/consistency-snapshot-majority-coupling.md` | Snapshot visibility requirements |
| `references/consistency-causal-majority-pairing.md` | Majority read+write for causal |
| `references/consistency-rollback-risk.md` | Weak concern = rollback exposure |
| **Retry and Error Handling (CRITICAL)** | |
| `references/retry-transient-transaction-error.md` | Retry full transaction on transient errors |
| `references/retry-unknown-commit-result.md` | Retry commit on unknown result |
| `references/retry-transaction-too-large-cache.md` | Redesign signal, not retry |
| `references/retry-upsert-duplicate-key-81.md` | MongoDB 8.1+ upsert behavior change |
| **Operational Constraints (HIGH)** | |
| `references/ops-transaction-runtime-limit.md` | Keep transactions short |
| `references/ops-lock-timeout-tuning.md` | Tune lock wait timeout |
| `references/ops-restricted-operations.md` | Unsupported ops in transactions |
| `references/ops-sharded-caveats.md` | Sharded transaction caveats |
| **Implementation Patterns (MEDIUM)** | |
| `references/pattern-withtransaction-vs-core-api.md` | Callback API vs core API |
| `references/pattern-idempotent-transaction-body.md` | Idempotent under retries |
| `references/pattern-observability.md` | Instrument outcomes and retries |

## MongoDB Documentation

Fetch any MongoDB doc as Markdown (most token-efficient) by appending `.md` to the URL path. Strip trailing slash first.

```
# Transactions (primary reference for this skill):
https://www.mongodb.com/docs/manual/core/transactions.md

# Transactions in Applications:
https://www.mongodb.com/docs/manual/core/transactions-in-applications.md

# Read Concern:
https://www.mongodb.com/docs/manual/reference/read-concern.md

# Write Concern:
https://www.mongodb.com/docs/manual/reference/write-concern.md

# Read Preference:
https://www.mongodb.com/docs/manual/core/read-preference.md

# Causal Consistency:
https://www.mongodb.com/docs/manual/core/causal-consistency-read-write-guarantees.md

# Driver docs — pick your language:
https://www.mongodb.com/docs/drivers/node/current/       # Node.js
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/  # Python
https://www.mongodb.com/docs/drivers/java/sync/current/  # Java

# Web search fallback:
site:mongodb.com/docs {your query}
```

Full docs-navigation reference: `references/docs-navigation.md`
