# Raw Source Verification

## Purpose
- Define when the model should go back from the wiki to the raw `Clippings/` files.
- Preserve the wiki as the primary memory layer without losing the ability to recover exact source detail.

## When To Reopen The Raw Clipping
- direct quotes are needed
- exact benchmark numbers or percentages are needed
- exact hyperparameters or commands are needed
- protocol fields or API behavior need precise wording
- two wiki pages seem inconsistent
- a page is clearly too shallow for the current question

## Default Retrieval Order
1. Read the relevant wiki page.
2. Identify the exact raw filenames from:
   - the page's `Sources Included` section
   - `Wiki/sources/clipping-registry.md`
3. Open the smallest useful raw file(s) in `Clippings/`.
4. Pull only the specific lines or snippet needed to verify the answer.
5. Keep the final answer grounded in the wiki, using the raw file as verification or precision support.

## Why This Matters
- The wiki is the working memory layer.
- The clipping files remain the source of truth for details that can be flattened by synthesis.
- This avoids both failure modes:
  - re-reading all raw files every time
  - trusting summaries too much when precision matters

## Practical Patterns

### Pattern: exact benchmark recovery
- Use the wiki to find which routing paper matters.
- Use the registry to find the raw clipping.
- Open the raw clipping and pull the specific cost or quality result.

### Pattern: hyperparameter recovery
- Use the post-training page to find the relevant tuning source.
- Reopen the raw clipping only for the exact LoRA, batch, or learning-rate values.

### Pattern: protocol or architecture verification
- Use the MCP or Envoy synthesis pages first.
- Reopen the raw source when a field name, routing mode, or enforcement mechanism needs exact wording.

## Output Discipline
- Do not dump long raw excerpts into the wiki or into answers.
- Pull the smallest useful snippet or paraphrase.
- If the wiki page learned something new from that verification, update the wiki page and log it.

## Related
- [[clippings-ingest-workflow]]
- [[../sources/clipping-registry|Clipping Registry]]
- [[../components/knowledge-wiki|Knowledge Wiki]]
