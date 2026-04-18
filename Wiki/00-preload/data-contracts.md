# Data Contracts

## Current State
- The design doc now defines a small set of project-specific contracts.

## Priority Contracts
- route request
- routing trace
- route response
- local verification result
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
  "task_category": "wiki_lookup | simple_synthesis | hard_reasoning | local_verification",
  "selected_path": "wiki_answer | cheap_model | strong_model | verification_tool",
  "rationale": "...",
  "fallback_available": true,
  "cost_tier": "free | cheap | expensive"
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
  "task_category": "local_verification",
  "selected_path": "verification_tool",
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

### Local Verification Result
- Producers: verification path
- Consumers: route response assembly
- Shape:

```json
{
  "fact": "...",
  "source": "Wiki/00-preload/file-map.md"
}
```

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
