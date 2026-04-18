# Persistent Memory vs RAG

## Overview
- This page captures the core LLM Wiki distinction that motivated the vault.
- Standard RAG answers a question by retrieving raw chunks at query time.
- A persistent wiki compiles knowledge ahead of time into linked markdown pages that can be reused and updated.

## The Core Difference

### RAG
- Raw sources remain the main knowledge layer.
- The model retrieves chunks from those sources at question time.
- Synthesis happens repeatedly from scratch.

### Persistent wiki
- Raw sources are still the source of truth.
- The model writes and maintains an intermediate knowledge layer.
- Summaries, entity pages, comparisons, contradictions, and running theses accumulate over time.

## Why It Matters In This Project
- The hackathon problem involves repeated questions about:
  - routing architecture
  - MCP role boundaries
  - security and policy
  - stack choices
- Recomputing those answers from 141 clippings every session is wasteful.
- A persistent wiki turns those repeated syntheses into reusable artifacts.

## Data Flow Comparison

### RAG-style
```text
query
  -> retrieve chunks from raw documents
  -> synthesize answer
  -> answer disappears into chat history
```

### Persistent wiki-style
```text
source arrives
  -> ingest and summarize
  -> update linked wiki pages
  -> future query reads wiki first
  -> useful new answer can be written back
```

## Strengths Of Persistent Memory
- cheaper repeated retrieval for stable project knowledge
- better cross-linking between concepts
- easier contradiction handling
- more durable session continuity across agents and days

## Limitations
- the wiki can drift stale if not maintained
- ingestion quality matters
- low-value or overly broad pages can become noise
- raw sources and code still need to exist as the verification layer

## Design Rules For This Vault
- keep raw sources immutable in `Clippings/`
- use the wiki as the working memory layer
- answer from the wiki first when the question is already covered
- verify against raw source or code when implementation or factual precision matters

## Related Topics
- [[reference-driven-solution-shape]]
- [[../components/knowledge-wiki|Knowledge Wiki]]
- [[../workflows/clippings-ingest-workflow|Clippings Ingest Workflow]]
