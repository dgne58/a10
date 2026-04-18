# Knowledge Wiki

## Purpose
- Serve as the persistent memory layer for Codex, Claude Code, and related agents.
- Compress research, architecture, commands, contracts, and current state into query-oriented pages.
- Prevent repeated rediscovery and hallucinated architecture during fragmented hackathon sessions.

## Inputs
- raw references from `Clippings/`
- codebase files once the repo is present
- query outputs and design decisions worth preserving
- agent findings and tool-call results worth retaining

## Outputs
- preload pages for fast session startup
- architecture, component, data-model, workflow, and source pages
- audit trail in `Wiki/log.md`

## Key Files
- `Wiki/00-preload/*`: fast-start pages; read first every session
- `Wiki/index.md`: navigational catalog of pages
- `Wiki/log.md`: append-only chronological update log
- `AGENTS.md`: canonical operating contract
- `WIKI.md`: shared schema definition and page pattern

## Agent Search Order

Before broad search or internet use, follow this order:

```text
1. Wiki/00-preload/hot.md
2. Wiki/00-preload/project-map.md
3. Wiki/00-preload/file-map.md
4. Wiki/00-preload/commands.md
5. most relevant preload for the task
6. Wiki/index.md
7. architecture and component pages
8. local source files
9. MCP tools
10. web
```

## hot.md Protocol

`Wiki/00-preload/hot.md` should hold:
- current implementation state
- next priorities
- current blockers or stubs
- what changed since the last session

Rules:
- update it at the end of meaningful work
- keep it short enough to scan quickly
- if it grows too much, move stable material elsewhere

## Query Workflow

When answering a question:
1. read preload first
2. use `Wiki/index.md` to find the smallest sufficient set of pages
3. answer from the wiki when possible
4. verify against code if the question is implementation-sensitive
5. file useful new answers back into the wiki

## Ingest Workflow

When new information arrives:
1. classify it as repo code, design note, external reference, or meeting note
2. choose the narrowest wiki section it affects
3. update the smallest useful set of pages
4. update `Wiki/index.md` if navigation changes
5. append a timestamped entry to `Wiki/log.md`
6. update `hot.md` if current execution state changed

## Hackathon Questions This Wiki Should Answer
- How does X connect to Y?
- Which file should I edit?
- What command do I run?
- What data shape does this route or tool expect?
- What is broken, risky, or stubbed right now?
- What is the fallback demo path?
- Which tool or MCP server should I use?

## Data / Contracts
- [[../data-models/knowledge-artifact|Knowledge Artifact]]

## Failure Modes
- pages become broad and stop being query-friendly
- the wiki drifts behind the implementation
- agents bypass the wiki and re-derive context from scratch
- index links point to pages that do not exist

## Related
- [[router]]
- [[orchestrator]]
- [[../workflows/clippings-ingest-workflow|Clippings Ingest Workflow]]
- [[../workflows/hackathon-build-loop|Hackathon Build Loop]]
