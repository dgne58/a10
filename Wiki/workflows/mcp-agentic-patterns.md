---
tags: [mcp, agentic, workflows, orchestration]
sources: [Introducing MCP, How MCP Enables Agentic AI, lastmile-ai/mcp-agent, Agentic AI & MCP for Platform Engineering]
last_updated: 2026-04-13
---

# MCP Agentic Patterns

## Overview
- This page answers: what are the core MCP workflow patterns, how do they compose, and what belongs in the agent loop versus outside it?
- It is more execution-oriented than [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]].

## MCP Primitives

| Primitive | What it is | Primary use |
| --- | --- | --- |
| Tools | callable actions | perform side effects or fetch data |
| Resources | read-only context | expose structured context without giant prompts |
| Prompts | parameterized instructions | shape the next step in a workflow |
| Notifications | async state or progress | report progress or completion |

## Agentic Loop

```text
user sets goal
  -> client prepares context and tool surface
  -> model selects answer, prompt, or tool path
  -> client executes tool or fetches resource
  -> result comes back
  -> orchestrator decides whether to continue
  -> final answer or write-back
```

## Workflow Patterns

### Parallel
- fan out sub-questions or subtasks
- aggregate the results
- useful when subtasks are independent

### Router
- select the right downstream agent, server, or branch
- often sits before more expensive orchestration

### Intent classifier
- lightweight decision stage before route selection
- useful for cold-start narrowing

### Orchestrator-workers
- plan centrally, delegate locally
- useful for multi-step tasks with bounded subtasks

### Evaluator-optimizer
- generate, critique, refine
- useful where quality checks matter more than latency

### Swarm or handoff
- pass work among specialized agents
- useful only when agent boundaries are real and stable

## Composition Guidance
- start with the simplest viable pattern
- prefer explicit loops over ornamental complexity
- only add deeper orchestration when the task genuinely requires it

## Where MCP Helps Most
- external capability discovery
- server-level boundaries between tools
- reusable context surfaces
- prompt chaining when next-step logic belongs with the server

## Where MCP Does Not Replace Other Layers
- wiki memory
- router policy
- runtime approval logic
- evaluation and write-back

## mcp-agent Relevance
- `mcp-agent` is useful because it packages several workflow patterns cleanly.
- It is a candidate implementation, not a required framework.
- The most important idea to retain from that material is not the package itself, but the preference for simple composable patterns.

## Failure Modes
- too many servers or tools in one loop
- no clear trace of why a tool was used
- prompt chaining without policy visibility
- server nesting that hides ownership and auth boundaries

## Related Topics
- [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]
- [[../components/mcp-control-plane|MCP Control Plane]]
- [[../components/orchestrator|Orchestrator]]
- [[../components/tool-surfaces|Tool Surfaces]]
