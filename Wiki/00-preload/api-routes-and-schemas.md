# API Routes and Schemas

## Current State
- The current design doc defines a small hackathon API surface.
- These routes are design targets until implemented.

## Planned Routes

### POST /api/route
- Purpose: accept one query and return answer plus routing trace.
- Handler file: `backend/app.py`
- Auth: none for hackathon scope
- Request body:

```json
{
  "query": "..."
}
```

- Response shape:

```json
{
  "answer": "...",
  "task_category": "wiki_lookup | simple_synthesis | hard_reasoning | local_verification",
  "selected_path": "wiki_answer | cheap_model | strong_model | verification_tool",
  "model_used": "...",
  "rationale": "...",
  "cost_usd": 0.0,
  "latency_ms": 0,
  "fallback": false,
  "source_refs": []
}
```

- Failure cases:
  - empty query -> `400`
  - provider failure -> fallback path or cached response
  - internal error -> structured `500`

### GET /api/eval/summary
- Purpose: return precomputed evaluation summary for the dashboard.
- Handler file: `backend/app.py`
- Auth: none
- Response:
  - total prompts
  - router quality metric
  - baseline quality metrics
  - cost totals
  - cost reduction percentage
  - path/model distribution

### GET /api/health
- Purpose: cheap smoke test for backend availability.
- Handler file: `backend/app.py`
- Auth: none
- Response:

```json
{
  "ok": true
}
```

## Deliberately Not In Scope
- auth endpoints
- admin endpoints
- broad workflow execution API
- direct tool-invocation API for judges
- paginated data browsing surface

## Related
- [[data-contracts]]
- [[../design-doc|Design Doc]]
- [[../data-models/routed-request|Routed Request]]
- [[../data-models/tool-invocation|Tool Invocation]]
