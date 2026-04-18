# MCP and Agentic Workflows

## Provenance
- Theme: `mcp-agentic-workflows`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Overview
- This theme defines how the system exposes capabilities, retrieves structured context, and coordinates execution across tools and services.
- It is the backbone of the "agentic workflows" half of the hackathon prompt.
- The most important conclusion from the source set is that MCP is a capability protocol, not a complete runtime architecture.

## Key Concepts

### MCP primitives
- Tools: callable actions exposed by a server
- Resources: structured or read-only context surfaces
- Prompts: parameterized templates that can shape the next step
- Notifications: server-pushed progress or state events

### Roles in the loop
- LLM: chooses and reasons
- MCP client: manages connections, discovery, and tool execution
- MCP server: exposes capabilities and context
- Orchestrator: governs when the loop advances and how outcomes are recorded

### Adjacent but distinct concepts
- Function tools are app-owned capabilities and are not the same thing as MCP tools.
- MCP servers can be nested or composed, but the surrounding system still needs routing, approvals, and memory.

## MCP Is A Capability Protocol, Not A Runtime

This distinction is the most important synthesis point in the whole page.

MCP gives you:
- capability discovery
- structured tools, resources, prompts, and notifications
- a reusable server boundary

MCP does **not** give you by itself:
- request routing
- policy enforcement
- durable workflow progression
- evaluation logic
- wiki write-back

That is why this wiki separates MCP from the router, orchestrator, and policy gateway pages.

## How It Works

### Capability discovery
- The client learns what an MCP server exposes.
- That capability surface can be dynamic, unlike a fixed static function list.

### Invocation loop
```text
user goal
  -> orchestrator prepares context
  -> model sees tool and resource surface
  -> model chooses tool, prompt, or answer path
  -> client executes MCP action or fetches MCP context
  -> result comes back
  -> orchestrator decides whether to continue, stop, or write back
```

### Prompt chaining
- One of the more interesting points in the corpus is that prompts can act like next-step instructions.
- That means an MCP server can help shape a workflow without the client hardcoding every branch.

### Server nesting
- An MCP server can also operate as a client to other servers.
- This supports "microservices for agents" patterns where one surface coordinates more specialized ones.

### Where the control loop actually lives
- The MCP client handles discovery and invocation mechanics.
- The orchestrator decides whether to continue the loop.
- The policy layer decides whether an action is permitted.
- The router decides whether MCP should be used at all.

## Capability Topologies

### Single-server topology
- one MCP server exposes one coherent capability surface
- easiest to reason about and debug

### Multi-server topology
- several servers expose different bounded domains
- appropriate when ownership, auth, or trust levels differ

### Nested-server topology
- one server brokers or coordinates downstream servers
- powerful, but dangerous if ownership and auth chains become unclear

### Design guidance
- prefer topologies that preserve explainability of ownership, auth, and failure boundaries

## Design Patterns From The Sources

### MCP as integration fabric
- Good for reusable capability surfaces such as filesystem, GitHub, Slack, internal APIs, or search.
- Reduces one-off integration code when multiple clients need the same capability.

### Thin prompt files, richer wiki
- The source set plus this project's goals strongly support keeping `CLAUDE.md` thin.
- Project memory belongs in the wiki, not in an unstable prompt-memory file.

### Narrow server inventory
- Too many tools degrade route quality and increase failure risk.
- Demo-critical inventory should stay small and tested.

### Platform engineering approach
- MCP is safer when treated as a governed platform concern rather than ad hoc per-developer experimentation.
- That includes:
  - templates or blueprints
  - org connectors
  - security defaults
  - dry-run validation before event day

### Resource-first context retrieval
- Large structured context is often better modeled as an MCP resource than as a tool returning a huge blob.
- This matters for token economy and for freshness tracking.

### Prompt-mediated workflows
- MCP prompts let a server shape the next step without pretending to be the whole orchestrator.
- They are best used as workflow hints or templates, not as a way to bury policy logic.

## Practical Usage Patterns

### Good uses in this project
- filesystem or wiki-adjacent reading
- authenticated access to external services
- reusable data sources
- external action surfaces behind clear policy boundaries

### Bad uses in this project
- exposing every possible tool "just in case"
- using MCP as a substitute for wiki maintenance
- treating tool access as equivalent to safe execution

## Operational Constraints

### Auth
- auth friction is often the real blocker in live demos
- every demo-critical server should be exercised in advance

### Context pressure
- a broad discovered tool set competes for model attention
- a few high-signal tools outperform a huge undifferentiated menu

### Ownership
- each server should have a clear owner, trust level, and failure policy

### Output control
- large outputs need truncation, summarization, or resource indirection
- otherwise one server can consume the whole context window

## Constraints And Limitations
- auth failures can dominate live demos
- discovery can overwhelm the model if the tool set is too broad
- MCP does not solve routing, policy, or write-back by itself
- server reliability and restart behavior matter in live sessions

## Sources Included
- `Introducing the Model Context Protocol.md`
- `Model Context Protocol.md`
- `How MCP Enables Agentic AI Workflows.md`
- `How to build a simple agentic AI server with MCP.md`
- `MCP and Connectors  OpenAI API.md`
- `Function calling  OpenAI API.md`
- `lastmile-aimcp-agent Build effective agents using Model Context Protocol and simple workflow patterns.md`
- `Put AI Agents to Work Faster Using MCP.md`
- `Agentic AI & MCP for Platform Engineering Teams.md`
- `Designing the workflow  n8n Docs.md`
- `Building a mini-workflow  n8n Docs.md`
- `Scheduling the workflow  n8n Docs.md`
- `Activating and examining the workflow.md`
- `Exporting and importing workflows.md`

## Related Topics
- [[mcp-overview]]
- [[../workflows/mcp-agentic-patterns|MCP Agentic Patterns]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../components/mcp-control-plane|MCP Control Plane]]
- [[../components/tool-surfaces|Tool Surfaces]]
- [[../components/orchestrator|Orchestrator]]
- [[../architecture/reference-driven-solution-shape|Reference-Driven Solution Shape]]
