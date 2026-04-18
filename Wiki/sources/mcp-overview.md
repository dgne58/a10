---
tags: [mcp, sources, protocol]
last_updated: 2026-04-13
---

# MCP Source Overview

## Provenance
- Theme: `mcp-agentic-workflows`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why these matter

MCP is the core coordination protocol for Track 2. These sources define the spec, patterns, and platform engineering considerations.

---

## Introducing MCP (Anthropic, Nov 2024)

- **What**: Open standard for two-way connections between AI systems and data sources.
- **Three primitives**: Tools (actions), Resources (read-only data), Prompts (parameterized templates).
- **Architecture**: MCP Servers expose data/tools. MCP Clients (AI apps) connect to servers.
- **SDKs available**: Python, TypeScript. Pre-built servers: GitHub, Slack, Google Drive, Postgres, Puppeteer.
- **Key insight**: Replaces fragmented custom integrations (one per tool) with one standard protocol.
- **Source**: `Clippings/Introducing the Model Context Protocol.md`

---

## How MCP Enables Agentic AI Workflows (TheNewStack, 2025)

- **Agentic loop**: LLM reasons + MCP servers expose tools/dynamic prompts + MCP client orchestrates + user sets goal.
- **Prompts as step chaining**: A tool result can include a next-step prompt template — effectively chains the workflow without hardcoding it.
- **Server nesting**: MCP servers can be clients to other MCP servers. Enables microservices-for-agents patterns.
- **mcp.run**: Platform for remotely-hosted MCP servers ("servlets") — no local install required.
- **Key insight**: The emergent agent comes from the interplay of LLM + MCP servers + MCP client — not from a single monolithic agent system.
- **Source**: `Clippings/How MCP Enables Agentic AI Workflows.md`

---

## lastmile-ai/mcp-agent (Framework)

- **What**: Python framework that fully implements MCP and adds composable workflow patterns.
- **Patterns**: Parallel, Router, Intent Classifier, Orchestrator, Evaluator-Optimizer, Swarm, Deep Research.
- **Core components**: MCPApp, Agent, AugmentedLLM, Workflow decorators, Temporal execution engine.
- **Agent-as-server**: Any MCPApp can be exposed as an MCP server (enables nested agent architectures).
- **Durable execution**: Temporal backend for pause/resume/retry without changing workflow code.
- **Key insight**: Simple code patterns (if/else, while loops) are more robust than graph-based orchestration.
- **Source**: `Clippings/lastmile-aimcp-agent Build effective agents using Model Context Protocol and simple workflow patterns.md`
- [[../workflows/mcp-agentic-patterns|→ Full synthesis]]

---

## Agentic AI & MCP for Platform Engineering (CyberArk/Ran Isenberg, 2025)

- **Platform Engineering angle**: Teams need governed, secure MCP adoption — not every developer rolling their own insecure server.
- **Three foundations**:
  1. Prompt library + CLI (org-specific prompts, not generic)
  2. MCP server blueprint (security baked in: WAF, IP restrictions, id tokens)
  3. Org data connectors (GitHub, Jira, Confluence via official MCP servers)
- **Vibe platform adoption**: Use agentic AI + MCP to auto-enforce org standards (correlation IDs, SDK usage, IaC patterns).
- **Key warning**: Out-of-the-box MCP servers are public and unauthenticated. Security is your responsibility.
- **Source**: `Clippings/Agentic AI & MCP for Platform Engineering Teams.md`

---

## MCP and Connectors (OpenAI API)

- **OpenAI perspective**: MCP is the standard for structured context exchange in agent pipelines.
- OpenAI supports MCP in their Agents SDK (compatible with any MCP server, not just Anthropic).
- **Source**: `Clippings/MCP and Connectors OpenAI API.md`

---

## How to Build a Simple Agentic MCP Server

- Practical walkthrough of building an MCP server from scratch.
- Key: tool definitions, resource exposure, running the server.
- **Source**: `Clippings/How to build a simple agentic AI server with MCP.md`
