# Project Map

## Goal
- Build a hackathon project around task-aware routing and agentic workflows.
- Turn the current research into a narrow, explainable product that non-technical judges can understand quickly.

## Problem Frame
- The problem is not only "which model should answer."
- The actual problem is "which execution path is cheapest and sufficient for this request?"
- Some requests are already answerable from local project memory.
- Some requests need cheap synthesis.
- Some requests need a medium-strength model.
- Some requests need a stronger model.

## Current System Shape
- `Clippings/`: immutable external references.
- `Wiki/`: operational knowledge and project memory.
- `Wiki/design-doc.md`: implementation-facing design for the current hackathon build.
- App/code layer: planned but not yet implemented in this vault.

## Intended Runtime Layers
- User-facing app surface.
- API/app layer.
- Routing layer to choose the execution branch.
- Local wiki/memory layer.
- OpenRouter-backed model access layer.
- Trace and fallback layer.

## Core Hackathon Components
- [[../components/knowledge-wiki|Knowledge Wiki]]
- [[../components/router|Router]]
- Compact Flask API
- Compact React UI
- Offline evaluation artifact

## Research-Backed Product Shape
- A request enters through an app or API surface.
- The system first checks whether the answer is already in the local wiki.
- If not, it routes among:
  - `mid_model`
  - `cheap_model`
  - `strong_model`
- Project/codebase questions still start with local memory before falling back to `cheap_model`.
- OpenRouter is the model access layer, not the whole product.
- Every response carries a visible routing trace.
- The demo shows that the system chooses the cheapest sufficient branch, not just the cheapest model.

## Planned Build Shape
- `backend/app.py`: Flask routes
- `backend/router.py`: branch classification and selection
- `backend/openrouter.py`: model-call wrapper
- `backend/config.py`: routing and model config
- `backend/eval_results.json`: precomputed evaluation artifact
- `data/`: mixed eval prompt set
- `scripts/run_eval.py`: offline eval generator
- `frontend/src/`: query UI plus trace/eval display

## Known Gaps
- Some preload/design pages still describe older branch names and need continued cleanup.
- The exact cheap/mid/strong model lineup may still change as evals improve.
- The final mixed eval artifacts should be refreshed after routing taxonomy changes.

## Related
- [[file-map]]
- [[../design-doc|Design Doc]]
- [[../architecture/hackathon-scope|Hackathon Scope]]
- [[../architecture/reference-driven-solution-shape|Reference-Driven Solution Shape]]
- [[../architecture/research-theses|Research Theses]]
