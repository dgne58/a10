# File Map

## Top-Level
- `AGENTS.md`: Codex-facing operating contract and wiki search order.
- `WIKI.md`: shared schema for all agents.
- `CLAUDE.md`: minimal Claude pointer file.
- `Wiki/design-doc.md`: current implementation-facing design for the hackathon build.
- `slides/canva-hackathon-presentation.md`: Canva-ready presentation script aligned to the current web app, CLI, backend router, and honest benchmark placeholders.
- `Clippings/`: immutable external references and clipped docs.
- `scripts/sync-clippings.ps1`: validates and updates clipping tracking pages from the raw `Clippings/` directory.
- `scripts/sync-clippings.cmd`: Windows wrapper for the clipping sync command.
- `Wiki/`: generated and maintained wiki pages.

## High-Signal Files To Read First
- `Wiki/00-preload/hot.md`
- `Wiki/00-preload/project-map.md`
- `Wiki/00-preload/file-map.md`
- `Wiki/00-preload/commands.md`
- `Wiki/design-doc.md`
- `Wiki/index.md`

## High-Signal Research Pages
- `Wiki/sources/corpus-overview.md`
- `Wiki/sources/task-aware-routing.md`
- `Wiki/sources/mcp-agentic-workflows.md`
- `Wiki/sources/post-training-and-alignment.md`
- `Wiki/sources/security-networking-and-governance.md`

## Planned Hackathon Files
- `backend/app.py`: primary Flask API surface
- `backend/router.py`: branch classification and selection
- `backend/openrouter.py`: model-call wrapper
- `backend/config.py`: model IDs and routing config
- `backend/eval_results.json`: committed offline evaluation artifact
- `data/*.json` or `data/*.csv`: mixed prompt eval set
- `scripts/run_eval.py`: offline eval generator
- `frontend/src/App.tsx`: minimal query + trace UI

## Current Gap
- Those application source directories are planned but not created yet.

## What To Add Once Code Exists
- Entry points
- Main services/modules
- Config files
- Route definitions
- Schema/model definitions
- Test directories
- Deployment manifests

## Related
- [[commands]]
- [[../design-doc|Design Doc]]
- [[../components/README|Components Hub]]
- [[../data-models/README|Data Models Hub]]
- [[../sources/corpus-overview|Corpus Overview]]
