# Reference-Driven Solution Shape

## Overview
- Translate the `Clippings/` research corpus into a plausible hackathon system architecture.
- Give agents and humans a concrete implementation shape before the final codebase exists.
- Make the design legible enough that routing, orchestration, security, and wiki memory can each be discussed and implemented independently.

## Architectural Thesis

The source corpus converges on a layered system:

```text
user or judge
  -> app or API surface
  -> orchestrator
      -> knowledge wiki and preload
      -> router
      -> tool surfaces
      -> policy gateway
      -> result trace and optional write-back

tool surfaces
  -> function tools
  -> MCP servers
  -> model providers
  -> optional serving infrastructure
```

This is not a monolithic "agent framework." It is a small set of cooperating layers with distinct jobs:
- the [[../components/knowledge-wiki|Knowledge Wiki]] stores persistent working memory
- the [[../components/router|Router]] decides which path is cheapest and sufficient
- the [[../components/orchestrator|Orchestrator]] runs the execution loop
- the [[../components/mcp-control-plane|MCP Control Plane]] exposes external capabilities
- the [[../components/policy-gateway|Policy Gateway]] constrains runtime behavior

## Responsibility Boundaries

### App or API surface
- Owns request intake, normalization, and UI/API framing.
- Should not silently absorb routing or policy logic that belongs deeper in the stack.

### Router
- Chooses the cheapest sufficient branch.
- Produces a routing rationale and fallback plan.
- Does not own retries, approvals, or write-back.

### Orchestrator
- Runs the execution lifecycle after the branch is chosen.
- Owns retries, verification, fallback behavior, and trace assembly.

### MCP control plane
- Owns capability inventory, auth state, exposure boundaries, and server-backed execution concerns.

### Policy gateway
- Owns allow / deny / approval decisions, not just advisory text.

### Wiki
- Owns persistent working memory and reusable context, not one-off execution state.

The most important boundary is that these layers are allowed to cooperate but should not collapse into one opaque "agent runtime."

## Data Flow

The compact flow below is expanded in [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]].

### 1. Request intake
- A request arrives from a user, operator, or judge.
- The app surface normalizes it into a [[../data-models/routed-request|Routed Request]].

### 2. Wiki-first grounding
- The orchestrator reads `hot.md` and the smallest relevant wiki pages.
- If the answer already exists in the wiki, the system should avoid unnecessary model or tool calls.

### 3. Routing
- The router evaluates:
  - task type
  - difficulty or complexity
  - modality
  - risk level
  - whether external access is necessary
  - whether the wiki already contains enough context
- It chooses a branch: wiki answer, cheap model, specialized model, tool path, or stronger model.

### 4. Execution
- The orchestrator executes the chosen path.
- Internal deterministic actions are better expressed as function tools.
- Externalized capabilities or reusable service surfaces are better expressed as MCP servers.

### 5. Runtime control
- The policy layer checks whether the action is allowed, requires approval, or should be denied.
- The gateway or control plane can also enforce rate limits, identity, and auditability.

### 6. Trace and write-back
- The system returns a final answer plus enough trace data to justify the path.
- High-value findings can be written back into the wiki as new or updated pages.

## Control Plane vs Data Plane

This distinction becomes important once the demo stops being a single-process toy.

### Data plane
- model responses
- tool invocations
- MCP resource reads
- API requests and responses

### Control plane
- route selection
- server inventory and exposure
- delegated identity and auth state
- policy evaluation
- execution tracing and write-back policy

Why this matters:
- the data plane may change per request
- the control plane defines which behaviors are even possible
- mixing them makes both judging and debugging harder

## Branch Taxonomy

The architecture only works if the available branch types are explicit:

| Branch | Best use | Cost profile | Failure mode |
| --- | --- | --- | --- |
| Wiki answer | repeated or already-synthesized knowledge | lowest | stale wiki state |
| Cheap model | low-risk synthesis or classification | low | quality drop on hard tail |
| Specialized model | narrow task family | low to medium | misroute outside domain |
| Function tool path | deterministic internal action | low | app bug / schema mismatch |
| MCP path | reusable external capability | medium | auth, availability, or policy failure |
| Strong model | hard reasoning or ambiguous tasks | high | cost / latency inflation |

## Deployment Shapes

### Minimal local hackathon shape
- one app process
- local wiki
- one router module
- one orchestrator loop
- one or two tool surfaces
- one visible policy decision point

### Slightly richer demo shape
- separate UI and API surface
- local deterministic tools plus one external MCP surface
- lightweight trace store or trace view
- explicit approval path for one risky action

### Stretch shape
- multi-provider model tier
- learned router
- remote MCP servers
- gateway enforcement and richer auth
- write-back automation from execution traces

## What Must Stay Observable

Even if the implementation is minimal, the following should be inspectable:
- why a route was chosen
- which tool or server was invoked
- whether approval was required
- what fallback happened on failure
- what evidence would be written back to the wiki

## Why This Fits The Prompt

### Task-aware routing
- Routing papers argue that quality, cost, and latency differ by task and query.
- The system therefore treats routing as a first-class design problem rather than an implicit model choice.

### Agentic workflows
- MCP and orchestration sources argue that tool use, loop management, and state handling matter more than raw model access.
- The orchestrator plus capability surfaces are the concrete expression of "agentic workflows."

### Specialized models and post-training
- Post-training sources argue that smaller specialized models are plausible when:
  - scope is narrow
  - routing is explicit
  - fallback to a stronger path exists

### Identity, security, and infrastructure
- Security and gateway sources argue that runtime policy belongs in infrastructure and control layers, not only in prompts.
- That justifies the gateway/control-plane split.

## Core Components

### App or API surface
- Provides the entry point.
- Converts user requests into normalized internal structures.
- Exposes a demoable interface for routing, traces, and status.

### Knowledge wiki
- Persistent memory between sessions.
- Avoids re-deriving architecture or demo state from raw documents every time.
- Lets the system answer common "how does X connect to Y?" questions cheaply.

### Router
- Not a mere provider switch.
- It is a policy and economics layer that chooses between:
  - wiki answer
  - cheap or specialized model
  - tool path
  - stronger model

### Orchestrator
- Converts routing decisions into concrete actions.
- Handles retries, verification, fallback, and write-back.

### MCP control plane
- Handles external capability exposure, discovery, and auth concerns.
- Separates function tools from reusable protocol-level surfaces.

### Policy gateway
- Makes runtime control explicit.
- Can be minimal in a hackathon build, but should still show:
  - allowlist or denylist behavior
  - audit trail
  - human approval for risky actions

## Design Patterns

### Wiki-first, then tools
- Most defensible for hackathon reliability.
- Uses the wiki as lowest-cost memory and tools only when needed.

### Transparent baseline router
- A rules-based baseline is valuable even if a learned router is planned later.
- Judges can understand it, and it provides a measurable baseline for future tuning.

### Capability layering
- Function tools for app-owned actions.
- MCP for external or reusable capabilities.
- Gateway or policy layer for runtime control.

### Persistent write-back
- Answers, comparisons, and resolved decisions should not disappear into chat history.
- They should become wiki artifacts.

## Interface Contracts To Keep Stable

The architecture can evolve, but a few boundaries should remain stable:
- normalized request shape -> [[../data-models/routed-request|Routed Request]]
- tool call envelope -> [[../data-models/tool-invocation|Tool Invocation]]
- evaluation evidence -> [[../data-models/evaluation-record|Evaluation Record]]

Stable envelopes matter because they let the team swap routing logic, model providers, or tool servers without rewriting every surrounding layer.

## Minimal Viable Slice
- One normalized input shape
- One router with at least two meaningful branches
- One tool or MCP-backed verification path
- One policy decision point
- One trace view
- One write-back example or at least a designed write-back path

## Stretch Slice
- Learned router or classifier-backed router
- Multiple providers or self-hosted model tier
- Remote MCP plus local MCP
- richer policy enforcement and audit log
- automatic wiki compilation from execution traces

## Tradeoffs And Failure Modes
- Over-building infra before the happy path works
- Treating MCP as the whole product
- letting the demo depend on too many live integrations
- hiding routing logic in prompts instead of exposing it
- allowing the wiki to remain research-only after code arrives
- blurring router, orchestrator, and policy responsibilities until failures are impossible to attribute

## Related Topics
- [[research-theses]]
- [[persistent-memory-vs-rag]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../components/tool-surfaces|Tool Surfaces]]
- [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]
- [[../sources/task-aware-routing|Task-Aware Routing]]
- [[../sources/security-networking-and-governance|Security, Networking, and Governance]]
- [[../workflows/routing-evaluation-loop|Routing Evaluation Loop]]
