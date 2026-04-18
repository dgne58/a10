# Routed Request

## Purpose
- Normalize the information the router needs to pick a model, tool, or policy branch.

## Producers
- UI client
- API server
- test harness

## Consumers
- router
- orchestrator
- evaluation harness

## Shape
```json
{
  "request_id": "string",
  "user_goal": "string",
  "task_type": "question|code|analysis|tool_use|agent_workflow",
  "domain": "routing|security|mcp|frontend|backend|unknown",
  "modality": "text|image|mixed",
  "risk_level": "low|medium|high",
  "latency_budget_ms": 0,
  "cost_sensitivity": "low|medium|high",
  "needs_external_data": true,
  "can_answer_from_wiki": true,
  "preferred_output": "answer|trace|artifact|update"
}
```

## Field Semantics

### `task_type`
- should describe the dominant execution mode, not every possible sub-step
- examples:
  - `question`
  - `analysis`
  - `tool_use`
  - `agent_workflow`

### `risk_level`
- should be conservative when uncertain
- useful interpretation:
  - `low`: read-only, locally answerable, no side effects
  - `medium`: internal mutation or write-back possible
  - `high`: external side effects, delegated identity, or sensitive data movement

### `can_answer_from_wiki`
- is a dynamic field, not just an intake hint
- should be updated after the wiki-first grounding stage rather than guessed once at the edge

### `preferred_output`
- helps the orchestrator choose between a direct answer, a trace-heavy response, an artifact, or a wiki update path

## Design Notes
- This object is intentionally smaller than a full execution trace.
- It is the handoff envelope into routing, not a complete record of everything that happened afterward.
- If fields keep growing without improving branch choice, the router is probably compensating for missing lifecycle structure elsewhere.

## Validation Rules
- `user_goal` must be present.
- `task_type` and `risk_level` should default conservatively when unknown.
- `can_answer_from_wiki` should be updated after preload/wiki lookup.

## Failure / Compatibility Notes
- Over-specified inputs can make the router brittle.
- Under-specified inputs force the router to rely on expensive fallback behavior.

## Related
- [[tool-invocation]]
- [[evaluation-record]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../components/router|Router]]
