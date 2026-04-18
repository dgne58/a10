# Orchestrator

## Purpose
- Run the agent loop around planning, retrieval, execution, verification, and write-back.
- Separate "what to do next" from the router's narrower decision about "which branch is best."

## What The Orchestrator Owns
- lifecycle progression
- retries and backoff
- tool or server invocation ordering
- verification and fallback
- trace assembly
- optional wiki write-back

It should not be reduced to "tool caller" only. It is the control loop.

## Inputs
- user request
- routing decision
- tool availability
- wiki context
- policy and approval signals

## Outputs
- execution trace
- final response or artifact
- optional wiki updates
- evaluation data for the demo or offline analysis

## Key Files
- Not implemented yet in source code.
- Design references:
  - [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]
  - [[../workflows/hackathon-build-loop|Hackathon Build Loop]]
  - [[../workflows/mcp-agentic-patterns|MCP Agentic Patterns]]
  - [[../sources/mcp-overview|MCP Source Overview]]

## Typical Loop

```text
1. Read preload and wiki first -> check hot.md, project-map, and relevant pages
2. Ask the router for the path -> choose the cheapest reliable execution branch
3. Execute tool or model calls -> function tools or MCP server tools
4. Check policy and gateway constraints -> allow, deny, or require approval
5. Verify or recover on failure -> retry, fallback, or escalate
6. Write useful outcomes to the wiki -> update hot.md or narrower pages
```

The fuller version of this flow lives in [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]].

## Execution State Machine

One useful mental model is a small state machine:

```text
received
  -> grounded
  -> routed
  -> executing
  -> verifying
  -> completed
  -> archived or written back
```

Failure edges:
- `executing -> routed` for fallback
- `verifying -> executing` for retry
- `any -> failed` for terminal error

Keeping the loop legible matters more than fancy autonomy.

## Workflow Patterns

| Pattern | When to use in this system |
| --- | --- |
| Parallel | Fan out multiple specialist queries; aggregate results |
| Router | Direct to the best agent or MCP server by task type |
| Intent Classifier | Bucket request before deciding route |
| Orchestrator-Workers | Generate a plan and dispatch subtasks |
| Evaluator-Optimizer | Loop until output passes a quality check |
| Swarm | Multi-agent handoff for cross-domain tasks |

## Execution Responsibilities By Stage

### Grounding
- read preload and relevant wiki pages
- update request context before execution

### Invocation planning
- decide which concrete tool, server, or model call should happen first
- translate branch choice into one or more [[../data-models/tool-invocation|Tool Invocation]] records

### Verification
- perform schema, factual, or policy checks
- compare against expected artifacts when available

### Recovery
- retry same path when failure is transient
- change path when failure is structural
- escalate to human or stronger branch when confidence collapses

### Persistence
- store trace evidence
- promote reusable findings into the wiki

## mcp-agent Note
- `mcp-agent` is a useful reference because it packages several of these patterns cleanly.
- Treat it as an implementation option, not a requirement.
- If adopted, keep the server set narrow and the trace explicit.

## Durable Execution Option
- If long-running work matters, a durable executor such as Temporal-backed `mcp-agent` can help with pause, resume, and retries.
- This is a stretch feature, not a baseline requirement.

## Function Tools vs MCP In The Loop

- Function tools are best when the orchestrator needs deterministic internal behavior with tight ownership.
- MCP is best when the orchestrator needs reusable externalized capabilities with their own server boundary.
- The orchestrator should not hide this distinction in implementation because the failure and policy models differ materially.

## Write-Back Policy

The orchestrator should write back only when the result is:
- verified or high-confidence
- reusable in future sessions
- better expressed as a page update than as ephemeral trace noise

Examples:
- command patterns
- clarified architecture decisions
- benchmark findings
- proven failure modes and fallbacks

## Trace Requirements
- every material branch decision should be reconstructable
- every tool call should have a reason
- every fallback should be visible
- destructive or externally visible actions should carry approval context

## Failure Modes
- Too many loops for a demo: cap iteration count and show the trace.
- No visible trace of why a step happened: log every tool call.
- Tool sprawl without a clear task boundary: scope tools per agent or workflow branch.
- Missing fallback to a manual or semi-automatic path.
- Letting verification become optional and silently trusting first outputs.

## Related
- [[router]]
- [[mcp-control-plane]]
- [[policy-gateway]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../workflows/demo-flow|Demo Flow]]
- [[../workflows/mcp-agentic-patterns|MCP Agentic Patterns]]
