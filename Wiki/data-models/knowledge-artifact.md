# Knowledge Artifact

## Purpose
- Track how raw information becomes a persistent wiki page or update.

## Producers
- ingest workflow
- agents writing back useful analyses

## Consumers
- wiki maintenance
- source traceability

## Shape
```json
{
  "artifact_id": "string",
  "kind": "preload|source-summary|architecture|component|workflow|analysis",
  "title": "string",
  "source_refs": ["string"],
  "target_page": "string",
  "last_updated": "timestamp",
  "status": "draft|active|stale",
  "summary": "string"
}
```

## Validation Rules
- `source_refs` should point to raw files, repo files, or prior wiki pages.
- `summary` should explain why the artifact exists.

## Failure / Compatibility Notes
- Too much metadata turns the wiki into a database project.
- Keep the minimal fields that help agents reason about freshness and provenance.

## Related
- [[../components/knowledge-wiki|Knowledge Wiki]]
- [[../workflows/clippings-ingest-workflow|Clippings Ingest Workflow]]
