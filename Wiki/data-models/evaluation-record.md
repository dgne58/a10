# Evaluation Record

## Overview
- Capture evidence that routing and workflow choices improved cost, latency, or reliability.
- Provide a stable unit of evidence for the demo, router tuning, and later comparisons.

## Producers
- evaluation harness
- orchestrator
- demo scripts
- manual comparison runs

## Consumers
- judging narrative
- router tuning
- fallback planning
- write-back into the wiki

## Core Shape

```json
{
  "eval_id": "string",
  "scenario": "string",
  "request_id": "string",
  "chosen_path": "string",
  "baseline_path": "string",
  "quality_score": 0.0,
  "latency_ms": 0,
  "estimated_cost": 0.0,
  "result": "pass|fail|partial",
  "notes": "string"
}
```

## Recommended Extended Shape

For meaningful routing analysis, the minimal record is often not enough. A stronger envelope is:

```json
{
  "eval_id": "string",
  "scenario": "string",
  "scenario_family": "wiki|cheap_model|tool_required|high_risk|hard_reasoning",
  "request_id": "string",
  "chosen_path": "string",
  "baseline_path": "string",
  "fallback_path": "string|null",
  "quality_score": 0.0,
  "quality_method": "exact|rubric|human|llm_judge",
  "latency_ms": 0,
  "estimated_cost": 0.0,
  "approval_required": false,
  "external_calls": 0,
  "result": "pass|fail|partial",
  "notes": "string"
}
```

The existing smaller shape is still acceptable for a hackathon, but these additional fields make post-hoc analysis much stronger.

## Field Semantics

### `scenario`
- human-readable description of the task family
- examples:
  - wiki-answerable
  - narrow-domain
  - tool-required
  - high-risk or approval-required

### `chosen_path`
- the actual branch selected by the router
- should be specific enough to interpret later

### `baseline_path`
- comparison branch used to test whether routing helped
- often "always use strongest model"

### `fallback_path`
- records the next branch used or available if the chosen path failed
- useful for diagnosing whether the system is robust or only lucky on the happy path

### `quality_score`
- can be rubric-based, exact-match, or human-scored
- should be consistent across comparable scenarios

### `quality_method`
- should explain how `quality_score` was obtained
- examples:
  - `exact`
  - `rubric`
  - `human`
  - `llm_judge`

If `llm_judge` is used, the notes should acknowledge reward-hacking / bias risk where relevant.

### `approval_required`
- indicates whether the route crossed a policy boundary that needed human or explicit policy approval

### `external_calls`
- rough count of model/tool/server calls made during the scenario
- useful as a proxy for operational complexity even when dollar cost is approximate

### `notes`
- should say whether the score was objective, estimated, or manually judged
- should capture anomalies or failure context

## Validation Rules
- every demo-critical scenario should have at least one baseline comparison
- a record without a clear baseline is weaker as evidence
- quality measurement method should stay consistent within a scenario family
- quality and latency should be captured for both routed and baseline paths whenever feasible
- fallback behavior should be recorded if it materially changed the outcome

## Scenario Families

### `wiki`
- answer should likely come from the local wiki
- best for demonstrating cost avoidance and memory reuse

### `cheap_model`
- low-risk task where a cheaper branch should be sufficient
- best for demonstrating cost reduction without quality collapse

### `tool_required`
- task requires verification, mutation, or external state
- best for demonstrating that routing is not only model selection

### `high_risk`
- route crosses approval, delegated identity, or DLP boundaries
- best for demonstrating policy-aware execution

### `hard_reasoning`
- task should justify escalation to the strongest branch
- best for showing why a fallback tier exists at all

## Comparison Patterns

### Routed vs strongest model
- the most common baseline
- demonstrates whether routing saves cost or latency while preserving quality

### Routed vs always-tool
- useful when the task family often tempts overuse of external systems

### Routed vs wiki-first-only
- useful when the team wants to show that pure local answering fails on some scenarios and correct escalation matters

## Typical Workflow

```text
run scenario
  -> capture routed path
  -> capture baseline
  -> compare outcome
  -> store record
  -> refine router or fallback policy
```

## Interpretation Guidance

### Strong record
- clear scenario family
- explicit baseline
- stable quality method
- latency and cost captured
- notes explain anomalies

### Weak record
- no baseline
- vague scenario
- score with no method
- no indication whether approval or fallback was involved

## Common Pitfalls
- using different quality rubrics across similar scenarios
- comparing a routed path against an unrealistically weak baseline
- omitting failed runs and only storing successes
- measuring quality but not latency or cost, which defeats the routing story
- using an LLM judge without acknowledging bias, verbosity preference, or reward-hacking risk

## Tradeoffs And Limitations
- hackathon metrics are often approximate
- cost estimates may be directional rather than exact
- a small scenario set can still be useful if it is stable and representative
- one perfect spreadsheet is less useful than a modest but repeatable scenario family with stable scoring

## Related Topics
- [[routed-request]]
- [[tool-invocation]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../workflows/routing-evaluation-loop|Routing Evaluation Loop]]
- [[../components/router|Router]]
- [[../components/orchestrator|Orchestrator]]
- [[../00-preload/judging-demo-narrative|Judging and Demo Narrative]]
