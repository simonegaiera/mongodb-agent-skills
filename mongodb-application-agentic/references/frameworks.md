---
title: Frameworks — LangChain + LangGraph
impact: CRITICAL
tags: langchain, langgraph, chatbot, agent, conversational-ai, stateful
---

# Frameworks — LangChain + LangGraph

When the user asks to build a **chatbot, conversational agent, or agentic AI workflow**, always use **LangChain** and **LangGraph**. Do not use raw LLM API calls or other frameworks unless explicitly requested.

## Why LangChain + LangGraph

- **LangChain** provides the chain/tool/retriever abstraction layer — prompt templates, output parsers, tool bindings, and MongoDB integrations (vector store, chat history).
- **LangGraph** adds **stateful, graph-based orchestration** — multi-step workflows, conditional branching, human-in-the-loop, and persistent checkpointing.

Together they handle the full chatbot lifecycle: user input → tool calls → LLM reasoning → state persistence → response.

## Required Packages

```bash
pip install langchain langchain-anthropic langchain-mongodb langgraph langmem langchain-voyageai pymongo
```

| Package | Purpose |
|---------|---------|
| `langchain` | Core abstractions (chains, tools, prompts) |
| `langchain-anthropic` | Claude LLM integration |
| `langchain-mongodb` | MongoDB vector store, chat history |
| `langgraph` | Stateful graph-based agent orchestration |
| `langmem` | Memory management tools for agents |
| `langchain-voyageai` | Voyage AI embeddings for semantic memory |
| `pymongo` / `motor` | Direct MongoDB driver access |

## LangGraph Chatbot Pattern

Build chatbots as **LangGraph state graphs**. Each node is a step (call LLM, use tool, check condition). Edges define transitions.

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_anthropic import ChatAnthropic

# 1. Define the LLM with tool bindings
llm = ChatAnthropic(model="claude-sonnet-4-5-20250514")
llm_with_tools = llm.bind_tools(tools)

# 2. Define graph nodes
def call_model(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def call_tool(state: MessagesState):
    # Execute tool calls from the LLM response
    ...

# 3. Build the graph
graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)
graph.add_node("tools", call_tool)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile()
```

## Key Rules

### Always Use LangGraph for Multi-Step Agents

Never implement agent loops manually (`while True: ...`). Use LangGraph's graph structure — it handles state, retries, and checkpointing.

```python
# BAD — manual agent loop
while True:
    response = llm.invoke(messages)
    if response.tool_calls:
        result = execute_tool(response.tool_calls[0])
        messages.append(result)
    else:
        break

# GOOD — LangGraph handles the loop
app = graph.compile()
result = app.invoke({"messages": [HumanMessage(content=user_input)]})
```

## Memory Architecture

Agent memory in LangGraph + MongoDB has **three components** that work together:

| Component | Class | Purpose |
|-----------|-------|---------|
| **Checkpointer** | `MongoDBSaver` | Short-term, thread-level state persistence (conversation history, tool results, intermediate steps) |
| **Long-Term Store** | `MongoDBStore` | Cross-thread semantic memory (user preferences, learned facts, purchase history) |
| **Memory Tools** | `create_manage_memory_tool` | Agent-controlled memory CRUD — the agent decides what to remember |

### Component 1: MongoDBSaver — Conversation Checkpointing

`MongoDBSaver` persists **thread-level state** — the full message history, tool call results, and agent state for a single conversation thread. This enables resuming conversations.

```python
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient

client = MongoClient(MONGODB_URI)
checkpointer = MongoDBSaver(client, db_name="chatbot", collection_name="thread_checkpoints")

# Compile graph with checkpointer
app = graph.compile(checkpointer=checkpointer)

# Each conversation gets a unique thread_id
config = {"configurable": {"thread_id": "user-123-session-1"}}
result = app.invoke({"messages": [HumanMessage(content=user_input)]}, config)

# Resume the same thread later — state is automatically loaded
result = app.invoke({"messages": [HumanMessage(content="follow up")]}, config)
```

**What it saves:** complete message history, agent state between interactions, tool call results, configuration and metadata.

### Component 2: MongoDBStore — Long-Term Semantic Memory

`MongoDBStore` provides **cross-thread, cross-session memory** using vector embeddings for semantic search. Memories persist across different conversations and are retrieved by meaning, not keywords.

```python
from langgraph.store.mongodb.base import MongoDBStore, VectorIndexConfig
from langchain_voyageai import VoyageAIEmbeddings

store = MongoDBStore(
    collection=client["memories"]["memory_store"],
    index_config=VectorIndexConfig(
        dims=1024,
        embed=VoyageAIEmbeddings(model="voyage-3.5"),
        fields=None,        # Auto-detect fields for indexing
        filters=None,       # Optional metadata filters
    ),
    auto_index_timeout=70,
)
```

**Key features:**
- **Semantic search** — finds memories by meaning, not keywords
- **Namespace organization** — memories grouped by category (`"memories"`, `"preferences"`, `"purchases"`)
- **Automatic vector indexing** — creates MongoDB Atlas Vector Search indexes
- **Cross-thread** — memories from one conversation are available in all future conversations

**Searching memories (used in dynamic prompts):**

```python
def prompt(state, store):
    memories = store.search(
        ("memories",),                            # Namespace
        query=state["messages"][-1].content,      # Semantic search query
        limit=5,
    )
    system_msg = f"""You are a helpful assistant with persistent memory.
## Relevant Memories
<memories>
{memories}
</memories>
Use these memories to provide personalized responses."""
    return [{"role": "system", "content": system_msg}, *state["messages"]]
```

### Component 3: Memory Management Tools — Agent-Controlled Memory

Use `langmem`'s `create_manage_memory_tool` to let the agent **autonomously decide** what to remember, update, or forget. The agent calls these tools just like any other tool.

```python
from langmem import create_manage_memory_tool

# Create memory tools scoped to namespaces
memory_tool = create_manage_memory_tool(namespace=("memories",))
preference_tool = create_manage_memory_tool(namespace=("preferences",))

tools = [memory_tool, preference_tool, search_products]
```

**How it works:** When a user says "I'm vegan", the agent autonomously calls the memory tool to save that preference. In future conversations, the dynamic prompt retrieves it via `store.search()`.

### Putting It All Together

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.store.mongodb.base import MongoDBStore, VectorIndexConfig
from langchain_voyageai import VoyageAIEmbeddings
from langmem import create_manage_memory_tool
from pymongo import MongoClient

client = MongoClient(MONGODB_URI)

# 1. Long-term memory store
store = MongoDBStore(
    collection=client["memories"]["memory_store"],
    index_config=VectorIndexConfig(
        dims=1024,
        embed=VoyageAIEmbeddings(model="voyage-3.5"),
    ),
    auto_index_timeout=70,
)

# 2. Conversation checkpointer
checkpointer = MongoDBSaver(client, db_name="chatbot", collection_name="conversations")

# 3. Dynamic prompt that injects relevant memories
def prompt(state, store):
    memories = store.search(("memories",), query=state["messages"][-1].content, limit=5)
    system_msg = f"""You are a helpful assistant with persistent memory.
## Relevant Memories
<memories>
{memories}
</memories>"""
    return [{"role": "system", "content": system_msg}, *state["messages"]]

# 4. Create agent with all three components
agent = create_react_agent(
    "anthropic:claude-sonnet-4-5-20250514",
    prompt=lambda state: prompt(state, store),
    tools=[
        create_manage_memory_tool(namespace=("memories",)),
        search_documents,
    ],
    store=store,
    checkpointer=checkpointer,
)

# 5. Use with thread-scoped config
config = {"configurable": {"thread_id": "user-123"}}
result = agent.invoke({"messages": [{"role": "user", "content": "I'm vegan"}]}, config)
```

### Memory Lifecycle

```
Conversation 1: "I'm vegan"
  → MongoDBSaver saves thread state
  → Agent calls memory tool → MongoDBStore saves "User is vegan"

Conversation 2 (new thread): "Find me pasta"
  → MongoDBSaver loads thread state (empty for new thread)
  → Dynamic prompt calls store.search("pasta") → finds "User is vegan"
  → Agent recommends vegan pasta options
```

---

## MongoDB as Vector Store (RAG)

Use `langchain-mongodb` for retrieval-augmented generation:

```python
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

client = MongoClient("mongodb+srv://...")
collection = client["mydb"]["documents"]

vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name="vector_index",
    text_key="content",
    embedding_key="embedding",
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
```

---

### Define Tools with `@tool` Decorator

```python
from langchain_core.tools import tool

@tool
def search_documents(query: str) -> str:
    """Search the knowledge base for relevant documents."""
    docs = retriever.invoke(query)
    return "\n".join(doc.page_content for doc in docs)

@tool
def get_user_info(user_id: str) -> str:
    """Retrieve user information from the database."""
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return str(user) if user else "User not found"

tools = [search_documents, get_user_info]
```

### Human-in-the-Loop

Use LangGraph's `interrupt` for approval workflows:

```python
from langgraph.types import interrupt

def sensitive_action(state: MessagesState):
    approval = interrupt({"question": "Approve this action?", "details": state})
    if approval != "yes":
        return {"messages": [AIMessage(content="Action cancelled by user.")]}
    # proceed with action
```

Reference: https://python.langchain.com/docs/ | https://langchain-ai.github.io/langgraph/

