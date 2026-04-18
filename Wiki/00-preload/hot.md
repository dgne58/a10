# Hot

## Right Now
- Project has a concrete hackathon direction in `Wiki/design-doc.md`.
- The chosen product is a **task-aware execution router**, not only a model cost router.
- The backend implementation now exists under `project/backend/` with live router, memory, and OpenRouter wrappers.
- The minimal branch set is:
  - `memory_answer`
  - `cheap_model`
  - `mid_model`
  - `strong_model`
- `project/scripts/run_eval.py` now matches the router contract again after restoring `router.select_model()` compatibility and making the eval script branch-aware.

## Immediate Priorities
- Run the full MMLU eval once provider spend is acceptable and commit `project/backend/eval_results.json`.
- Verify the frontend reflects router branch distribution as intended by the design doc.
- Tighten preload wiki pages that still describe the project as unimplemented.
- Prepare cached outputs for the core demo prompts.

## Current Assumptions
- Both Claude Code and Codex will operate against the same wiki and repo.
- A transparent rules-based router is sufficient for hackathon scope.
- The strongest story for judges is cheapest sufficient **execution path**, not cheapest sufficient model.
- Project/codebase questions should hit local memory first, then fall back to `cheap_model` if memory misses.
- Internet use should remain exceptional during implementation and demo prep.

## Next Best Actions
- Scaffold the repo exactly as described in `Wiki/design-doc.md`.
- Implement request normalization and trace output shape first.
- Choose the exact cheap, mid, and strong OpenRouter models.
- Rehearse the 4-step demo path:
  - memory answer
  - cheap model
  - mid model
  - strong model
