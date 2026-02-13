# MongoDB Documentation Navigation — Transactions & Consistency

Quick-reference for AI agents to find MongoDB transaction and consistency documentation.

## Fetch Strategy

Append `.md` to any MongoDB doc URL for raw Markdown (most token-efficient). Strip trailing slash first.

```
https://www.mongodb.com/docs/manual/core/transactions.md
```

Fallback: `site:mongodb.com/docs {your query}`

## Key Documentation Pages

All URLs prefix: `https://www.mongodb.com/docs`

### Transactions

| Topic | Path |
|-------|------|
| Transactions Overview | `/manual/core/transactions/` |
| Transactions in Applications | `/manual/core/transactions-in-applications/` |
| Production Considerations | `/manual/core/transactions-production-consideration/` |
| Sharded Cluster Transactions | `/manual/core/transactions-sharded-clusters/` |
| Drivers API (Callback & Core) | `/manual/core/transactions-in-applications/#callback-api-vs-core-api` |

### Read & Write Concerns

| Topic | Path |
|-------|------|
| Read Concern | `/manual/reference/read-concern/` |
| Read Concern "local" | `/manual/reference/read-concern-local/` |
| Read Concern "majority" | `/manual/reference/read-concern-majority/` |
| Read Concern "snapshot" | `/manual/reference/read-concern-snapshot/` |
| Write Concern | `/manual/reference/write-concern/` |
| Read Preference | `/manual/core/read-preference/` |

### Consistency & Sessions

| Topic | Path |
|-------|------|
| Causal Consistency | `/manual/core/causal-consistency-read-write-guarantees/` |
| Client Sessions | `/manual/reference/server-sessions/` |
| Retryable Writes | `/manual/core/retryable-writes/` |
| Retryable Reads | `/manual/core/retryable-reads/` |

### Replication & Durability

| Topic | Path |
|-------|------|
| Replication Overview | `/manual/replication/` |
| Replica Set Elections | `/manual/core/replica-set-elections/` |
| Rollbacks | `/manual/core/replica-set-rollbacks/` |
| Write Acknowledgement | `/manual/reference/write-concern/#w-option` |

### Relevant Commands

| Command | Path |
|---------|------|
| commitTransaction | `/manual/reference/command/commitTransaction/` |
| abortTransaction | `/manual/reference/command/abortTransaction/` |
| serverStatus | `/manual/reference/command/serverStatus/` |
| currentOp | `/manual/reference/command/currentOp/` |
| setParameter | `/manual/reference/command/setParameter/` |

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

- **Transaction docs** reference both replica set and sharded cluster behavior — always check which topology applies.
- Default `/manual/` = latest stable release. Pin version with `/manual/v{MAJOR}.{MINOR}/` only for version-specific debugging.
- Driver `current` = latest stable. PyMongo + C++ use `/languages/` path; others use `/drivers/`.
