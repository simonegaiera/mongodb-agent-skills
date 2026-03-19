---
name: mongodb-application-agentic
description: Standards for building agentic AI applications and chatbots with MongoDB. Use when creating chatbots, conversational agents, AI assistants, or agentic workflows. Mandates LangChain and LangGraph for chatbot development, MongoDB MCP for database interactions, and Claude prompting best practices. Triggers on "chatbot", "agent", "agentic", "LangChain", "LangGraph", "conversational AI", "AI assistant", "MCP", "tool use", "prompt engineering".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.0.0"
---

# MongoDB Application — Agentic AI

Standards for building **agentic AI applications and chatbots** with MongoDB, using **LangChain**, **LangGraph**, and the **MongoDB MCP** server. Includes Claude/Sonnet prompting best practices for optimal agent behavior.

## When to Use

- Building a chatbot or conversational AI backed by MongoDB
- Creating agentic workflows that interact with databases
- Implementing tool-calling agents that need MongoDB access
- Setting up LangChain/LangGraph pipelines with MongoDB as the persistence layer
- Configuring the MongoDB MCP server for agent-database interaction
- Designing prompts for Claude-powered agentic systems

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangChain + LangGraph |
| LLM | Claude (Sonnet 4.6 / Opus 4.6) |
| Database | MongoDB (via MCP or Motor/PyMongo) |
| Database Access | MongoDB MCP Server |
| Memory | MongoDB Atlas (conversation history + semantic memory) |
| Vector Search | MongoDB Atlas Vector Search (via `mongodb-ai` skill) |

## Related MongoDB Skills

| Skill | When to Use |
|-------|-------------|
| `mongodb-ai` | Vector search, embeddings, RAG patterns, agent memory schemas |
| `mongodb-schema-design` | Designing conversation and memory collections |
| `mongodb-application-backend` | FastAPI backend serving the chatbot API |
| `mongodb-application-frontend` | Next.js frontend for the chat UI |

## Rule Categories

| Priority | Category | Impact | Reference |
|----------|----------|--------|-----------|
| 1 | Frameworks (LangChain + LangGraph) | CRITICAL | `references/frameworks.md` |
| 2 | MongoDB MCP | HIGH | `references/mcp.md` |
| 3 | Prompting Best Practices | HIGH | `references/prompting.md` |

## Key Principles

> **LangChain + LangGraph for all chatbots** — When the user asks to build a chatbot or conversational agent, always use LangChain for the chain/tool layer and LangGraph for stateful, multi-step agent orchestration.

> **MongoDB MCP for database access** — Use the MongoDB MCP server to give agents structured, safe access to MongoDB. Prefer MCP tools over raw driver calls for agent-initiated database operations.

> **Claude best practices** — Follow the prompting guide for XML-structured prompts, adaptive thinking, parallel tool calls, and agentic system design. See `references/prompting.md`.

> **MongoDB as memory** — Store conversation history and semantic memory in MongoDB collections. Use Atlas Vector Search for memory retrieval (see `mongodb-ai` skill).

## Instructions

When building an agentic AI application or chatbot:

1. Read `references/frameworks.md` for LangChain and LangGraph setup, graph design, and chatbot patterns
2. Read `references/mcp.md` for MongoDB MCP server configuration and tool usage
3. Read `references/prompting.md` for Claude prompting best practices in agentic contexts
4. Consult the `mongodb-ai` skill for vector search, RAG, and agent memory schemas
5. Consult the `mongodb-application-backend` skill for the FastAPI backend serving the agent
6. If requirements are ambiguous, ask the user to clarify before generating code

