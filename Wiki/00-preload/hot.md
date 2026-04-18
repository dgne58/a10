# Hot

## Right Now
- Project has a concrete hackathon direction in `Wiki/design-doc.md`.
- The chosen product is a **task-aware execution router**, not only a model cost router.
- The backend implementation now exists under `project/backend/` with live router, memory, verifier, and OpenRouter wrappers.
- The minimal branch set is:
  - `wiki_answer`
  - `cheap_model`
  - `strong_model`
  - `verification_tool`
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
- Verification from local project artifacts is part of the product value.
- Internet use should remain exceptional during implementation and demo prep.

## Next Best Actions
- Scaffold the repo exactly as described in `Wiki/design-doc.md`.
- Implement request normalization and trace output shape first.
- Lock the allowlisted local sources for the verification path.
- Choose the exact cheap and strong OpenRouter models.
- Rehearse the 4-step demo path:
  - wiki answer
  - cheap model
  - strong model
  - verification tool
