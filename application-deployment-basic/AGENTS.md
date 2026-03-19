# Application Deployment Basic — Agent Context

> **IMPORTANT**: When a user asks to **build**, **create**, or **implement** an application, **always present a detailed plan and wait for explicit approval before writing any code**. Also generate a `PROMPT.md` at the project root before the first line of implementation.

---

## CRITICAL: Plan-First Approval Gate

**Never write implementation code until the user explicitly approves a plan.**

Present the plan as a structured document. Include ALL of these sections — a missing section is an unvalidated assumption:

| Section | What to include |
|---------|----------------|
| **Application Overview** | What it does, who uses it, what problem it solves |
| **Tech Stack** | Every technology + version + reason (reference applicable MongoDB skills) |
| **Feature List** | In-scope and explicitly out-of-scope features |
| **Folder Structure** | Complete directory tree for all new code |
| **Data Model** | Every MongoDB collection: fields, types, indexes |
| **API Design** | Every endpoint: method, path, request/response shape |
| **Key Decisions** | Non-obvious technical choices and rationale |
| **Out of Scope** | Explicit list of what will NOT be built |

After presenting the plan, end with this exact block:

```
---
**Please review the plan above.**
- Reply **"approved"** (or "looks good", "go ahead") to proceed.
- Reply with changes if anything is wrong or missing.

I will not write any code until you approve.
---
```

**Do NOT proceed if the user asks a question, makes a suggestion, or stays silent.** Only an explicit approval unlocks code generation.

---

## CRITICAL: Generate PROMPT.md Before Coding

Once the plan is approved, **generate `PROMPT.md` at the project root** before writing any implementation code.

`PROMPT.md` is written *for the LLM* (not for humans — that's `README.md`). It is the persistent system prompt for the entire project build. Every new coding session should start by reading it.

**Required sections** (use XML tags throughout):

```xml
<role>
You are an expert [stack] developer building [app description].
You follow [list applicable MongoDB skills] strictly.
</role>

<project_context>
Application: [one-line description]
Stack: [technologies]
MongoDB skills in effect: [list]
Key constraints: [bullet list of non-obvious rules from the plan]
</project_context>

<do_not_act_before_instructions>
Do not jump into implementation unless clearly instructed. Default to information
and recommendations. Only make changes when explicitly asked.
</do_not_act_before_instructions>

<safety_guidelines>
Take local, reversible actions freely. For destructive operations (dropping collections,
deleting files, force-pushing), ask the user before proceeding.
</safety_guidelines>

<use_parallel_tool_calls>
Make all independent tool calls in parallel. When reading multiple files, read them
simultaneously. Maximize parallelism for speed and efficiency.
</use_parallel_tool_calls>

<coding_conventions>
[Project-specific conventions from the approved plan and applicable skills]
</coding_conventions>

<investigate_before_answering>
Never speculate about code you have not read. Read files before answering questions
about them. Give grounded, hallucination-free answers.
</investigate_before_answering>
```

**Keep `PROMPT.md` updated** when major decisions change (tech swap, feature added/removed, new constraints). Do NOT update it for routine implementation decisions.

**`PROMPT.md` is not `README.md`** — no setup steps, no env var tables, no human-facing docs. Write it as instructions to the LLM.

---

## Workflow Summary

```
User: "Build me a [app]"
  └─→ LLM: Present full plan (8 sections)
  └─→ LLM: Wait for explicit approval
        ├─ Changes requested → Revise and re-present → Wait again
        └─ Approved
              └─→ LLM: Generate PROMPT.md
              └─→ LLM: Begin implementation
                    └─→ Keep PROMPT.md updated on major changes
```

---

## Reference Index

| File | Rules |
|------|-------|
| `references/planning.md` | Required plan sections, approval gate wording, revision workflow |
| `references/prompt-file.md` | PROMPT.md structure, XML tags, behavior blocks, update policy |
| `CLAUDE Prompting Guide.md` | Full Claude prompting reference (source material) |

