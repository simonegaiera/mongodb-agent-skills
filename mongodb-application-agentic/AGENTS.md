# MongoDB Application — Agentic AI — Agent Context

> **IMPORTANT**: When the user asks to build a chatbot, conversational agent, or agentic AI workflow, **always use LangChain and LangGraph**. Use the MongoDB MCP server for agent-initiated database access. Follow Claude prompting best practices from `references/prompting.md`.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangChain + LangGraph |
| LLM | Claude (Sonnet 4.6 / Opus 4.6) |
| Database | MongoDB 7+ |
| Database Access (agents) | MongoDB MCP Server |
| Memory | MongoDB Atlas (chat history + semantic memory) |
| Vector Search | MongoDB Atlas Vector Search (`mongodb-ai` skill) |

---

## CRITICAL: LangChain + LangGraph for Chatbots

**Every chatbot must use LangGraph state graphs.** Never implement manual agent loops.

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5-20250514")
llm_with_tools = llm.bind_tools(tools)

def call_model(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)
graph.add_node("tools", call_tool)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
app = graph.compile()
```

**Required packages:** `langchain langchain-anthropic langchain-mongodb langgraph langmem langchain-voyageai pymongo`

**MongoDB integrations:**
- `MongoDBSaver` — thread-level checkpointing (short-term memory)
- `MongoDBStore` — cross-thread semantic memory (long-term memory)
- `create_manage_memory_tool` (langmem) — agent-controlled memory CRUD
- `MongoDBAtlasVectorSearch` — RAG retriever

---

## CRITICAL: Memory Architecture (3 Components)

| Component | Class | Purpose |
|-----------|-------|---------|
| **Checkpointer** | `MongoDBSaver` | Thread-level state (message history, tool results) |
| **Long-Term Store** | `MongoDBStore` | Cross-thread semantic memory (preferences, facts) |
| **Memory Tools** | `create_manage_memory_tool` | Agent decides what to remember/forget |

```python
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.store.mongodb.base import MongoDBStore, VectorIndexConfig
from langchain_voyageai import VoyageAIEmbeddings
from langmem import create_manage_memory_tool

# Checkpointer — saves thread state
checkpointer = MongoDBSaver(client, db_name="chatbot", collection_name="conversations")

# Long-term store — semantic memory with vector search
store = MongoDBStore(
    collection=client["memories"]["memory_store"],
    index_config=VectorIndexConfig(dims=1024, embed=VoyageAIEmbeddings(model="voyage-3.5")),
    auto_index_timeout=70,
)

# Agent with memory
agent = create_react_agent(
    "anthropic:claude-sonnet-4-5-20250514",
    prompt=lambda state: prompt_with_memories(state, store),
    tools=[create_manage_memory_tool(namespace=("memories",)), ...],
    store=store,
    checkpointer=checkpointer,
)
```

**Memory lifecycle:** User says "I'm vegan" → agent calls memory tool → `MongoDBStore` saves it → future conversations retrieve it via `store.search()` in the dynamic prompt.

---

## HIGH: MongoDB MCP Server

Use MCP for **agent-initiated, exploratory** database access. Use PyMongo/Motor for **application-level, predefined** operations.

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

**Action policy:** Read operations are safe for agents to use freely. **Never execute write operations (insert, update, delete, drop) without explicit user approval.**

**Security:**
- Connection string in env vars only — never hardcode
- Default to `--readOnly` for chatbots
- Use least-privilege MongoDB users
- Log all MCP tool invocations

---

## HIGH: Claude Prompting Best Practices

### Structure with XML Tags

```xml
<system_context>You are a MongoDB-powered chatbot...</system_context>
<tools_available>search_products, check_order_status</tools_available>
<response_guidelines>Be concise. Confirm before destructive actions.</response_guidelines>
```

### Key Prompting Rules

- **Be specific** — explicit instructions outperform vague ones
- **Explain why** — Claude generalizes from motivation ("limit to 5 results because the chat UI is narrow")
- **Default to action** — use `<default_to_action>` tag for agentic coding
- **Gate destructive ops** — use `<safety_guidelines>` to require confirmation
- **Parallel tool calls** — use `<use_parallel_tool_calls>` for throughput
- **3–5 examples** — wrap in `<example>` tags to steer format and tone
- **Minimize hallucinations** — use `<investigate_before_answering>` to force grounded answers

### Adaptive Thinking (Claude 4.6)

```python
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...],
)
```

- Prefer `adaptive` thinking for agentic workloads
- Use `effort: "medium"` for Sonnet 4.6, `effort: "high"` for Opus 4.6
- Guide post-tool reflection: "After receiving tool results, reflect on quality and plan next steps"

---

## Related MongoDB Skills

| Skill | When |
|-------|------|
| `mongodb-ai` | Vector search, embeddings, RAG, agent memory schemas |
| `mongodb-schema-design` | Designing conversation/memory collections |
| `mongodb-application-backend` | FastAPI backend serving the chatbot API |
| `mongodb-application-frontend` | Next.js frontend for the chat UI |

## Reference Index

| File | Rules |
|------|-------|
| `references/frameworks.md` | LangChain setup, LangGraph state graphs, memory architecture (MongoDBSaver, MongoDBStore, langmem), vector store, tools, human-in-the-loop |
| `references/mcp.md` | MCP server config, read/write tool lists, action policy, security, LangChain integration |
| `references/prompting.md` | XML tags, adaptive thinking, parallel tools, few-shot examples, hallucination prevention, long-running sessions |
| `CLAUDE Prompting Guide.md` | Full 700+ line prompting reference (source material) |

## Key Documentation

```
# LangChain:
https://python.langchain.com/docs/

# LangGraph:
https://langchain-ai.github.io/langgraph/

# MongoDB MCP Server:
https://github.com/mongodb-js/mongodb-mcp-server

# Claude Prompting:
https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

# MongoDB Atlas Vector Search (for RAG):
https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/
```

