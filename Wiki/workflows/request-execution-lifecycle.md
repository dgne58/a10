---
tags: [workflow, routing, orchestration, policy, mcp, lifecycle]
last_updated: 2026-04-15
---

# Request Execution Lifecycle

## Overview
- This page is the canonical end-to-end flow for how a single request should move through the system described by this wiki.
- It exists to prevent the architecture, router, orchestrator, MCP, and policy pages from each re-explaining the same lifecycle differently.
- Read this page when the question is: "what actually happens, in order, from request intake to result and write-back?"

## Core Stages

```text
request intake
  -> normalization
  -> wiki-first grounding
  -> route selection
  -> branch execution
  -> policy checks
  -> verification / fallback
  -> response assembly
  -> trace capture
  -> optional wiki write-back
```

## Stage 1: Intake And Normalization

### Inputs
- user message, operator action, judge scenario, or automated test request
- session metadata such as latency budget, risk level, or desired output type

### Output
- one [[../data-models/routed-request|Routed Request]] structure

### Why this matters
- The router should not infer everything from raw prose every time.
- Normalization is where the system turns a free-form request into something the rest of the stack can reason about consistently.

### Practical fields
- request identifier
- goal text
- task family
- domain hints
- risk level
- cost / latency preference
- whether external systems are allowed or required

## Stage 2: Wiki-First Grounding

### Goal
- Determine whether the answer already exists in the wiki or whether external execution is actually necessary.

### Minimum read order
1. `Wiki/00-preload/hot.md`
2. other preload pages as needed
3. the smallest relevant source/component/workflow pages

### Outcomes
- `answerable_from_wiki`
- `needs_tool_or_model_execution`
- `needs_more_local_context`

### Why this stage exists
- The wiki is the cheapest memory layer in the architecture.
- It reduces repeated model calls, repeated file exploration, and repeated architecture rediscovery.

## Stage 3: Route Selection

### Goal
- Choose the cheapest sufficient branch, not merely the "best" model.

### Candidate branch families
- wiki-only answer
- cheap model / simple synthesis
- specialized model
- function-tool path
- MCP-backed path
- stronger model / escalation path

### Inputs to the decision
- task difficulty
- modality
- domain fit
- risk level
- tool availability
- current auth state
- whether the wiki already resolved the query

### Output
- selected branch
- rationale
- fallback branch

See [[../components/router|Router]] for the branch-selection logic.

## Stage 4: Branch Execution

### Branch A: Wiki Answer
- Answer directly from local wiki knowledge.
- No external side effects.
- Fastest and cheapest path.

### Branch B: Model-Only Path
- Use a model for synthesis, classification, transformation, or generation.
- Appropriate when:
  - no external verification is required
  - the answer is not already in the wiki
  - tool use would be unnecessary overhead

### Branch C: Function Tool Path
- Use application-owned deterministic logic.
- Appropriate for:
  - validation
  - schema transformation
  - formatting
  - internal evaluation or trace generation

### Branch D: MCP Path
- Use an externalized capability surface through MCP.
- Appropriate for:
  - reusable integrations
  - authenticated external systems
  - resource retrieval too structured or dynamic for static prompts

See [[../components/tool-surfaces|Tool Surfaces]] and [[../components/mcp-control-plane|MCP Control Plane]].

## Stage 5: Policy Checks

### Goal
- Convert trust assumptions into explicit runtime decisions.

### Typical order
1. identify caller and delegated scope
2. classify requested action
3. determine risk
4. allow, deny, or require approval
5. emit an audit record

### What should be checked
- which identity is acting
- on whose behalf the action is taken
- which tool or resource is targeted
- whether outbound data contains sensitive material
- whether the action is destructive or externally visible

See [[../components/policy-gateway|Policy Gateway]].

## Stage 6: Verification And Recovery

### Verification examples
- objective comparison against known expected output
- schema validation
- read-after-write confirmation
- second-pass model or rule check
- human approval for high-risk actions

### Recovery paths
- retry same branch
- retry with smaller context or different tool
- degrade to manual / semi-automatic path
- escalate to stronger model
- stop and surface a structured failure

The orchestrator owns this stage, not the router.

## Stage 7: Response Assembly

### Final response may contain
- user-facing answer
- artifact or output reference
- short rationale for chosen path
- approval or verification status
- pointer to trace or evaluation record

### Design rule
- user response and execution trace are related but not identical.
- The system should be able to show trace data to a judge or operator without polluting every normal response.

## Stage 8: Trace Capture

### Trace should capture
- request id
- route selected
- tools invoked
- approvals requested or granted
- verification outcome
- fallback events
- latency and estimated cost

### Main data structures
- [[../data-models/routed-request|Routed Request]]
- [[../data-models/tool-invocation|Tool Invocation]]
- [[../data-models/evaluation-record|Evaluation Record]]

## Stage 9: Wiki Write-Back

### Good write-back candidates
- resolved architectural decisions
- recurring operational findings
- verified command patterns
- newly clarified system relationships
- benchmark or evaluation outcomes worth reusing

### Bad write-back candidates
- transient chat filler
- low-confidence speculation
- duplicate material that belongs on an existing page

## Control Boundaries

### Router
- chooses branch
- does not run the whole loop

### Orchestrator
- advances the loop
- owns retries, verification, and write-back

### MCP control plane
- manages capability exposure, auth state, and server-backed execution

### Policy gateway
- decides whether the requested action is permitted

### Wiki
- persistent memory and reusable working context

## Failure Modes
- normalization is skipped and every downstream stage guesses
- wiki-first grounding is bypassed and cost explodes
- router chooses paths that are unavailable or unauthenticated
- policy exists only as prose
- orchestrator loops without visible verification or stop conditions
- write-back is omitted and the same work repeats next session

## Related Topics
- [[../architecture/reference-driven-solution-shape|Reference-Driven Solution Shape]]
- [[../components/router|Router]]
- [[../components/orchestrator|Orchestrator]]
- [[../components/mcp-control-plane|MCP Control Plane]]
- [[../components/policy-gateway|Policy Gateway]]
- [[../workflows/demo-flow|Demo Flow]]
