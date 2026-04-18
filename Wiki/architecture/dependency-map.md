# Dependency Map

## Overview
- This page tracks the major dependency layers implied by the current wiki architecture before a concrete app codebase exists.
- It is not yet a package manifest. It is an architectural dependency map: which subsystems depend on which others, where the trust boundaries sit, and which dependencies are optional versus demo-critical.

## Core Dependency Layers

### 1. Local knowledge layer
- `Wiki/` pages
- preload pages
- `Clippings/` corpus

This layer is the cheapest context source and the main persistence surface for learned project knowledge.

### 2. Decision layer
- routing logic
- policy logic
- evaluation criteria

This layer determines:
- which path to take
- whether the path is allowed
- how the outcome is judged later

### 3. Execution layer
- orchestrator loop
- function tools
- MCP client behavior
- response / trace assembly

This layer turns a route into concrete actions.

### 4. Capability layer
- local deterministic tools
- MCP servers
- model providers
- external services reached through connectors or APIs

This layer is where useful work actually happens outside the wiki itself.

### 5. Infrastructure and security layer
- identity and delegated scope
- auth state and credentials
- network / gateway enforcement
- data-flow controls such as DLP

This layer constrains what the execution layer is allowed to do.

## Dependency Graph

```text
request intake
  -> routed-request normalization
  -> wiki / preload context
  -> router
  -> orchestrator
      -> function tools
      -> MCP control plane
          -> MCP servers
          -> authenticated backends
      -> model providers
  -> policy gateway
  -> trace + evaluation record
  -> optional wiki write-back
```

The detailed lifecycle is documented in [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]].

## Dependency Classes By Architectural Role

### Required for the current architecture
- local wiki and preload pages
- router
- orchestrator
- at least one execution path beyond pure wiki lookup
- trace and evaluation capture

### Strongly recommended
- one policy decision point
- one narrow MCP or external capability surface
- one fallback path when external execution fails

### Optional / stretch
- learned routing
- durable execution engine
- multiple model providers
- multiple authenticated MCP servers
- gateway-grade network enforcement

## Coupling And Failure Surfaces

### Wiki coupling
- The router and orchestrator both depend on the wiki for cheap grounding.
- If the wiki is stale, the cheapest branch becomes less trustworthy and the system over-escalates.

### Capability coupling
- The router depends on the MCP control plane and auth state indirectly because impossible branches must be pruned before selection.
- The orchestrator depends on capability reliability directly because it owns retries and fallback.

### Policy coupling
- Policy depends on identity, delegated scope, and data classification.
- If those inputs are missing, approval logic degrades into guesswork.

### Evaluation coupling
- Router tuning depends on evaluation records.
- If evaluation is weak, routing policy becomes anecdotal rather than evidence-backed.

## Current Known Dependency Classes
- foundation models / SLMs
- routing logic or policy engine
- agent runtime
- MCP servers and their authenticated backends
- infra/security controls
- local wiki and source corpus

## External Reference Themes Already Present In `Clippings/`
- MCP and agentic workflows
- model routing
- post-training and RLHF
- Flask/API references
- TypeScript/React references
- Envoy and gateway/security notes
- networking/protocol references

## Concrete Dependency Questions To Answer Once Code Exists

### App dependencies
- which framework serves the UI and API surface
- which validation / schema libraries shape request and response contracts
- which trace or logging layer stores execution evidence

### Model dependencies
- which providers are actually reachable
- whether there is one strong model path and one cheap path
- whether specialized models are static, fine-tuned, or adapter-based

### MCP dependencies
- which servers are enabled in practice
- which are read-only versus mutating
- which require human login or short-lived credentials

### Data and persistence dependencies
- where traces live
- whether wiki write-back is file-only or mirrored elsewhere
- whether evaluation records are persisted outside markdown

### Security dependencies
- how delegated identity is represented
- where approval state is stored
- whether DLP or outbound content controls exist

## Risks And Design Pressure
- over-coupling routing to a specific provider instead of a branch type
- treating every installed MCP server as a dependency instead of only the exposed bundle
- depending on live auth for demo-critical paths without a fallback
- leaving evaluation as an optional afterthought rather than a first-class dependency of routing
- allowing the wiki to depend on manual upkeep only, with no disciplined write-back or ingest path

## What To Add Once The App Exists
- exact packages/frameworks
- external APIs
- model providers
- data stores
- queues/events
- deployment/runtime dependencies

## Related
- [[reference-driven-solution-shape]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../components/router|Router]]
- [[../components/orchestrator|Orchestrator]]
- [[../components/mcp-control-plane|MCP Control Plane]]
- [[../components/policy-gateway|Policy Gateway]]
- [[../data-models/evaluation-record|Evaluation Record]]
- [[hackathon-scope]]
- [[../sources/README|Sources Hub]]
