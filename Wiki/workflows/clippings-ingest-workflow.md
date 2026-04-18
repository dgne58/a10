# Clippings Ingest Workflow

## Purpose
- Turn raw clipped references into persistent, queryable wiki knowledge.

## Flow
1. Classify the clipping into a theme.
2. Read representative sources first, not the entire corpus blindly.
3. Synthesize the smallest useful wiki page for that theme.
4. Update preload or architecture pages if the source changes system design.
5. Append an entry to `Wiki/log.md`.
6. Leave the raw file untouched in `Clippings/`.

## Output Types
- source synthesis page
- architecture update
- component page
- workflow page
- preload update

## Rules
- Prefer thematic synthesis over page-per-source churn when the corpus is large.
- Preserve traceability by listing the relevant raw filenames.
- Promote only high-signal claims into preload pages.

## Failure Modes
- Over-ingesting low-value background reading.
- Writing summaries that are too generic to help a future coding task.
- Forgetting to update preload after learning something important.

## Related
- [[hackathon-build-loop]]
- [[../components/knowledge-wiki|Knowledge Wiki]]
- [[../sources/corpus-overview|Corpus Overview]]
