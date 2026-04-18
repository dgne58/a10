# Router

## Purpose
- Decide which model, tool, or execution path should handle a request.
- Balance quality, latency, cost, modality, risk, and domain fit.

## What The Router Is Not
- It is not the whole agent loop.
- It is not the policy engine.
- It is not a hidden provider switch embedded in prompts.

The router chooses a branch. The [[orchestrator]] runs the branch. The [[policy-gateway]] decides whether the branch is allowed.

## Inputs
- [[../data-models/routed-request|Routed Request]]
- current session budget or latency target
- task type or domain hints
- availability of local wiki answers, tools, or MCP servers
- policy constraints from the gateway layer

## Outputs
- routing decision
- selected model or branch
- rationale or trace metadata
- fallback branch if the preferred path fails

## Key Files
- Not implemented yet in source code.
- Design references:
  - [[../sources/task-aware-routing|Task-Aware Routing]]
  - [[../architecture/reference-driven-solution-shape|Reference-Driven Solution Shape]]
  - [[../workflows/llm-routing-approaches|LLM Routing Approaches]]
  - [[../sources/routing-papers|Routing Papers]]

## Routing Algorithm Options

| Approach | When to use | Cold-start |
| --- | --- | --- |
| Rules-based tiers | No training data; hackathon day zero | Works immediately |
| Intent classification | Semantic task bucketing without labeled pairs | Prompt-tunable |
| Preference-based | Have A/B evals or preference data | Needs labeled pairs |
| Embedding similarity | Need fast routing with few-shot examples | Few examples enough |
| Signal-decision chain | Want modular signals such as domain, keyword, factuality | Modular, additive |
| Online adaptation | Need to adapt over time without full offline calibration | Viable with care |

## Branch Taxonomy

The router should reason over explicit branch families, not only over model names:

| Branch | Example decision |
| --- | --- |
| `wiki_answer` | answer directly from local wiki pages |
| `cheap_model` | run low-cost synthesis or classification |
| `specialized_model` | use a narrow-domain or post-trained path |
| `function_tool` | call deterministic app-owned logic |
| `mcp_tool_or_resource` | use a server-backed capability |
| `strong_model` | escalate to the high-quality fallback |

This keeps the router architecture-aligned even before concrete providers are chosen.

## How It Works

### 1. Normalize the request
- Read the [[../data-models/routed-request|Routed Request]].
- Fill in missing conservative defaults where needed.

### 2. Evaluate cheap eliminations first
- Can the wiki answer this directly?
- Is the request obviously tool-requiring?
- Is a branch impossible because auth or capability is unavailable?

### 3. Score viable branches
- Estimate quality sufficiency
- estimate latency fit
- estimate cost
- account for risk and approval burden

### 4. Emit a decision package
- chosen branch
- rationale
- fallback branch
- confidence or explanation metadata

### 5. Hand off to orchestrator
- The router stops once branch choice is made.
- It should not directly absorb retries or multi-step execution.

## Suggested Decision Heuristics

### Wiki-first heuristic
- If the query is answerable from local wiki content with low ambiguity, route to `wiki_answer`.

### Tool-needed heuristic
- If the request requires verification, external state, or side effects, prefer `function_tool` or `mcp_tool_or_resource`.

### Strong-model heuristic
- If the task is hard, ambiguous, or safety-sensitive and no deterministic path exists, escalate to `strong_model`.

### Cheap-path heuristic
- If the task is narrow, low-risk, and quality-sensitive only up to a modest bar, prefer `cheap_model` or `specialized_model`.

## Minimal Routing Policy

```text
1. If the answer already exists in the wiki, answer from the wiki first.
2. If the task is simple, low-risk, and narrow, use a cheaper or specialized path.
3. If the task requires tools or external systems, use an orchestrated tool or MCP path.
4. Otherwise, use the stronger general model path.
```

This policy is intentionally provider-agnostic until the real stack is chosen.

## Routing Signals To Log
- `task_category`: e.g. `simple_qa`, `code_gen`, `tool_use`, `wiki_lookup`
- `selected_path`: model, tool path, or workflow branch
- `rationale`: one-sentence rule or score that triggered the decision
- `cost_tier`: `free`, `cheap`, `expensive`
- `fallback_available`: boolean
- `policy_pressure`: whether the branch implies approval or elevated controls
- `capability_state`: whether the chosen path depended on server availability or auth

This trace feeds the [[../data-models/evaluation-record|Evaluation Record]] and makes the demo explainable.

## Design Notes
- The first router does not need to be learned.
- A transparent rules-based router is acceptable if it uses:
  - task complexity
  - modality
  - safety or risk level
  - whether the answer already exists in the wiki
- Learned routing should improve a stable baseline, not replace explainability with opacity.

## Interface With Adjacent Components

### Router -> Orchestrator
- passes chosen branch and fallback
- passes rationale needed for trace or judging

### Router -> Policy Gateway
- policy does not choose the branch, but the router should be aware of likely approval costs

### Router -> MCP Control Plane
- capability availability should constrain candidate branches
- impossible branches should be pruned before final selection

## Tradeoffs
- A richer router can improve cost and quality, but every extra signal makes the decision harder to explain live.
- A minimal router is easier to defend but may overuse the strong fallback path.
- Branch-level routing is more durable than provider-specific routing because the underlying model or tool vendor can change later.

## Failure Modes
- Hidden heuristics that judges cannot understand.
- Overfitting to a tiny prompt set.
- Ignoring tool or MCP availability and routing to impossible branches.
- No graceful escalation to a stronger model or safer fallback.
- Evaluating branches in the wrong order and paying expensive cost before checking the wiki.

## Related
- [[orchestrator]]
- [[mcp-control-plane]]
- [[policy-gateway]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../sources/task-aware-routing|Task-Aware Routing]]
- [[../workflows/llm-routing-approaches|LLM Routing Approaches]]
