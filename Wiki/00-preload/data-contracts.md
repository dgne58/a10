# Data Contracts

## Current State
- The design doc now defines a small set of project-specific contracts.

## Priority Contracts
- route request
- routing trace
- route response
- evaluation summary
- evaluation row

### Route Request
- Producers: frontend, curl/Postman, demo scripts
- Consumers: `POST /api/route`
- Shape:

```json
{
  "query": "..."
}
```

- Required fields:
  - `query`
- Validation rules:
  - trimmed non-empty string

### Routing Trace
- Producers: backend router
- Consumers: frontend trace panel, demo reviewers
- Shape:

```json
{
  "task_category": "memory_lookup | simple_synthesis | medium_synthesis | hard_reasoning",
  "selected_path": "memory_answer | cheap_model | mid_model | strong_model",
  "rationale": "...",
  "fallback_available": true,
  "cost_tier": "free | cheap | medium | expensive"
}
```

- Required fields:
  - `task_category`
  - `selected_path`
  - `rationale`

### Route Response
- Producers: backend API
- Consumers: frontend UI, demo scripts
- Shape:

```json
{
  "answer": "...",
  "task_category": "memory_lookup",
  "selected_path": "memory_answer",
  "model_used": null,
  "rationale": "...",
  "cost_usd": 0.0,
  "latency_ms": 42,
  "fallback": false,
  "source_refs": ["Wiki/00-preload/file-map.md"]
}
```

- Required fields:
  - `answer`
  - `selected_path`
  - `rationale`
  - `cost_usd`
  - `latency_ms`
  - `fallback`
- Optional fields:
  - `model_used`
  - `source_refs`

### Evaluation Summary
- Producers: offline eval script
- Consumers: `/api/eval/summary`, dashboard
- Required fields:
  - `total`
  - `router_quality`
  - `always_strong_quality`
  - `always_cheap_quality`
  - `router_cost_usd`
  - `always_strong_cost_usd`
  - `cost_reduction_pct`
  - `path_distribution`

### Evaluation Row
- Producers: offline eval script
- Consumers: dashboard table, manual review
- Required fields:
  - `id`
  - `prompt`
  - `expected_path`
  - `selected_path`
  - `router_correct`
  - `always_strong_correct`
  - `router_cost`
  - `always_strong_cost`

## Related
- [[api-routes-and-schemas]]
- [[../design-doc|Design Doc]]
- [[../data-models/routed-request|Routed Request]]
- [[../data-models/tool-invocation|Tool Invocation]]
- [[../data-models/evaluation-record|Evaluation Record]]
