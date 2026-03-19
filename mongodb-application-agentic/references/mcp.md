---
title: MongoDB MCP Server
impact: HIGH
tags: mcp, model-context-protocol, mongodb, tools, agent, database-access
---

# MongoDB MCP Server

The [MongoDB MCP Server](https://github.com/mongodb-js/mongodb-mcp-server) gives AI agents structured, safe access to MongoDB through the Model Context Protocol. Use it when agents need to query, inspect, or modify MongoDB data.

## When to Use MCP

| Scenario | Use MCP? |
|----------|----------|
| Agent needs to query/inspect MongoDB at runtime | ✅ Yes |
| Agent needs to create indexes or collections | ✅ Yes |
| Agent explores schema or data during development | ✅ Yes |
| Application backend with fixed queries (FastAPI routes) | ❌ No — use PyMongo/Motor directly |
| Batch data processing pipeline | ❌ No — use PyMongo/Motor directly |

**Rule**: Use MCP for **agent-initiated, exploratory** database access. Use PyMongo/Motor for **application-level, predefined** database operations.

## Configuration

Add the MongoDB MCP server to your agent's MCP configuration:

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb+srv://user:pass@cluster.mongodb.net/mydb"
      }
    }
  }
}
```

### Read-Only Mode (Recommended for Chatbots)

For chatbots and agents that should not modify data, use read-only mode:

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server", "--readOnly"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb+srv://user:pass@cluster.mongodb.net/mydb"
      }
    }
  }
}
```

## Available MCP Tools

### Read Operations (Safe — agents can use freely)

| Tool | Purpose |
|------|---------|
| `find` | Query documents with filters and projections |
| `aggregate` | Run aggregation pipelines including `$vectorSearch` |
| `count` | Count documents matching a filter |
| `collection-schema` | Infer schema from sample documents |
| `collection-indexes` | List indexes on a collection |
| `collection-storage-size` | Get collection size |
| `list-databases` | List all databases |
| `list-collections` | List collections in a database |
| `explain` | Analyze query execution plans |
| `db-stats` | Database statistics |
| `mongodb-logs` | Recent server log entries |

### Write Operations (Require explicit user approval)

| Tool | Purpose |
|------|---------|
| `insert-many` | Insert documents |
| `update-many` | Update documents matching a filter |
| `delete-many` | Delete documents matching a filter |
| `create-index` | Create an index |
| `drop-index` | Drop an index |
| `create-collection` | Create a collection |
| `drop-collection` | Drop a collection |
| `drop-database` | Drop a database |
| `rename-collection` | Rename a collection |

## Action Policy

**Never execute write operations without explicit user approval.** This is critical for chatbot safety.

```python
# In your LangGraph agent, gate write operations:
def should_approve_write(state):
    last_msg = state["messages"][-1]
    if any(tc.name in WRITE_TOOLS for tc in last_msg.tool_calls):
        return "human_approval"
    return "execute"
```

## Integrating MCP with LangChain

When building a LangChain/LangGraph agent, expose MCP tools as LangChain tools:

```python
from langchain_core.tools import tool

@tool
def query_mongodb(database: str, collection: str, filter: dict) -> str:
    """Query MongoDB using the MCP server. Use for exploratory data access."""
    # The MCP server handles this — this tool definition tells the LLM
    # what's available. The actual execution goes through MCP.
    ...

@tool
def inspect_schema(database: str, collection: str) -> str:
    """Inspect the schema of a MongoDB collection."""
    ...
```

For direct MCP integration, configure your agent runtime to connect to the MCP server and expose its tools automatically.

## Security Rules

1. **Connection string in environment** — Never hardcode credentials. Use `MDB_MCP_CONNECTION_STRING` env var.
2. **Read-only for chatbots** — Default to `--readOnly` unless write access is explicitly needed.
3. **Least privilege** — Use a MongoDB user with only the permissions the agent needs.
4. **No `drop-database` in production** — Disable destructive tools in production environments.
5. **Audit tool calls** — Log all MCP tool invocations for observability.

Reference: https://github.com/mongodb-js/mongodb-mcp-server | https://modelcontextprotocol.io/

