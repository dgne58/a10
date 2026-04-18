# Known Bugs and Assumptions

## Current Assumptions
- The hackathon app will be created directly from `Wiki/design-doc.md`.
- The wiki will be updated alongside code changes rather than retroactively.
- Claude Code and Codex will both use the same shared wiki.
- A transparent rules-based router is sufficient for the first version.
- The strongest judge story is branch routing, not provider switching.
- The benchmark should reflect branch choice and grounded verification, not only academic QA.

## Current Risks
- Several preload pages still describe the repo as unimplemented even though the backend and frontend now exist under `project/`.
- If `CLAUDE.md` is edited automatically, important instructions could drift unless `WIKI.md` remains canonical.
- If the project collapses back into "model cost router," judges may see it as a thin wrapper.
- If the eval stays MMLU-only, the benchmark will not match the actual product claim.
- The verification path could become brittle if the allowlisted local sources are not chosen carefully.
- Live provider failures could undercut the demo unless cached responses are prepared.
- Running `python scripts/run_eval.py` still incurs real provider calls; use the local regression test first when validating import or routing changes.

## To Track Once Implementation Starts
- broken routes
- flaky eval generation
- router/eval contract drift
- manual setup steps
- fallback/cached response correctness
- demo-only shortcuts
- router misclassifications
- verification path failures
- slow or expensive model paths
- stale wiki pages after code changes

## Related
- [[fallback-plans]]
- [[hot]]
- [[../design-doc|Design Doc]]
- [[../architecture/research-theses|Research Theses]]
