# MCP Control Plane

## Overview
- Provide a structured inventory of MCP clients, servers, connector-backed capabilities, and their runtime status.
- Keep capability access explicit, authenticated, and testable.
- Separate "capability exposure" from "orchestration logic" and from "policy enforcement."

## Why This Layer Exists
- The control plane prevents MCP from degenerating into "whatever tools happen to be installed right now."
- It turns a raw server list into a governed capability surface the router and orchestrator can reason about.
- It is also the natural place to record auth state, freshness, ownership, and demo criticality.

## Inputs
- configured MCP servers
- connector settings
- auth state
- tool and resource inventory
- per-server ownership and trust level

## Outputs
- capability surface available to the orchestrator
- auth and health status
- execution traces for MCP-backed actions
- constrained inventory that the router can reason about

## Key Concepts

### MCP primitives in practice
| Primitive | What it provides | Good use |
| --- | --- | --- |
| Tools | callable actions | actions against systems |
| Resources | read-only context | large or structured context surfaces |
| Prompts | parameterized instructions | next-step guidance or server-shaped workflows |
| Notifications | progress or events | async execution or progress reporting |

### Control-plane responsibility
- inventory which servers exist
- decide which servers are exposed to which client or agent
- track auth and health
- keep the exposed surface small enough that routing remains legible

### Capability bundle responsibility
- form narrow bundles per task or agent role
- avoid exposing every possible server globally
- make exposure changes explicit enough to debug after a failure

## Function Tools vs MCP

This distinction is important enough to repeat because it affects routing and safety.

| Aspect | Function tools | MCP surfaces |
| --- | --- | --- |
| Ownership | app-owned | server-owned |
| Discovery | static | protocol-level and often dynamic |
| Best use | deterministic internal actions | reusable externalized capabilities |
| Failure model | app bug | server availability plus auth plus app logic |
| Policy boundary | internal code boundary | network or server boundary |

See also [[tool-surfaces]].

## How It Works

### 1. Inventory
- Enumerate which MCP servers are available.
- Record:
  - purpose
  - auth model
  - owner
  - risk level
  - criticality to the demo

### 2. Exposure
- Do not expose every available server to every agent.
- Build narrow capability bundles by task.

### 3. Discovery
- Let the client discover tools, resources, and prompts.
- Filter or segment the inventory so the model is not overloaded.

### 4. Runtime execution
- The orchestrator requests a tool call.
- The control plane executes it through the proper server.
- Policy and gateway layers validate whether the call is permitted.

### 5. Recovery
- If a server fails or auth expires, the control plane should surface a recoverable error path.

## Capability Bundle Design

### Why bundles matter
- Too many discovered tools degrade tool selection quality.
- Different tasks require different trust boundaries.
- Per-agent or per-workflow bundles make traces easier to explain.

### Example bundle types
| Bundle | Typical contents |
| --- | --- |
| `wiki_readonly` | filesystem-like resources, local knowledge surfaces |
| `research_external` | search, fetch, citation-friendly retrieval |
| `repo_ops` | git, GitHub, issue or PR actions |
| `high_risk_mutation` | only tightly approved external actions |

### Design rule
- Bundle by task boundary, not by "what happens to be installed."

## Auth And Session Lifecycle

The control plane should know for each server:
- auth mechanism
- who owns the credential
- refresh behavior
- whether human login is required
- what failure looks like when auth expires

This is especially important for live demos because auth drift is one of the most common MCP failure modes.

## Output Normalization

Server outputs are rarely shaped ideally for direct model consumption.

The control plane should be able to record or enforce:
- maximum payload sizes
- truncation or summarization policy
- structured error envelopes
- provenance and freshness metadata

Otherwise one noisy server can bloat the entire context window.

## Recommended Inventory Strategy For This Vault

### Baseline
- one local or low-risk read surface
- one external fetch or search surface if truly needed
- one optional authenticated service for the demo if it materially strengthens the story

### Anti-pattern
- ten half-tested servers with overlapping purposes

## Relationship To Adjacent Layers

### Router
- asks what capability bundles are actually available
- should not pick impossible branches

### Orchestrator
- uses the bundle to execute concrete calls
- depends on recoverable error reporting from the control plane

### Policy gateway
- evaluates whether a bundle or individual tool call is allowed
- should not be bypassed merely because a server is installed

## Auth And Reliability Checklist
- every server used in the demo has been invoked successfully at least once
- auth storage and refresh behavior are known
- restart behavior is known
- timeouts and expected failure modes are known
- policy allowlist matches the actual exposed tool set

## Failure Modes
- auth tokens expire mid-demo
- too many tools degrade tool selection quality
- a server crash leaves no fallback path
- giant tool outputs bloat the context window
- resources are exposed without ownership or freshness tracking
- capability bundles drift from what the router assumes is available

## Related Topics
- [[tool-surfaces]]
- [[orchestrator]]
- [[policy-gateway]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]
- [[../workflows/mcp-agentic-patterns|MCP Agentic Patterns]]
- [[../data-models/tool-invocation|Tool Invocation]]
