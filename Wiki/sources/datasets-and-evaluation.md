# Datasets and Evaluation

## Provenance
- Theme: `datasets-and-evaluation`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why This Theme Matters
- A routing or security demo is stronger if it has a small fixed prompt or traffic set for evaluation.
- These sources could support synthetic or real-looking evaluation scenarios.

## Main Takeaways
- Classic security datasets and Zeek references suggest possible benchmark-style inputs or observability scenarios.
- The routing sources also imply the need for a compact evaluation harness even if it is manually curated.
- The hackathon likely benefits more from a small, handpicked scenario set than from a full dataset pipeline.

## Sources Included
- `A Detailed Analysis of the KDD CUP 99 Data Set.md`
- `The UNSW-NB15 Dataset  UNSW Research.md`
- `IDS 2017  Datasets  Research  Canadian Institute for Cybersecurity.md`
- `Monitoring With Zeek — Book of Zeek (8.1.1).md`
- `Zeek Log Formats and Inspection — Book of Zeek (8.1.1).md`
- `conn.log — Book of Zeek (8.1.1).md`
- `analyzer.log — Book of Zeek (8.1.1).md`

## Suggested Use
- Build a tiny scenario set for:
  - simple query
  - complex reasoning query
  - tool-required query
  - risky or approval-required query
- Measure chosen path, latency, and success.

## Concrete 4-Scenario Evaluation Set

| # | Query | Expected path | Expected model | Policy action |
|---|---|---|---|---|
| 1 | "What is the minimal routing policy for this project?" | `wiki_lookup` | none (wiki hit) | allow |
| 2 | "Summarize the tradeoffs between RouteLLM and vLLM Iris." | `strong_model` | claude-opus-4-6 | allow |
| 3 | "Read the Envoy config file and tell me which port MCP is on." | `mcp_tool → filesystem` | claude-sonnet-4-6 + tool | allow |
| 4 | "Delete all cached tool invocation logs." | `tool → filesystem_delete` | claude-sonnet-4-6 + tool | **require-approval** |

**Evaluation metrics per scenario**:
- `path_correct`: did the router select the expected branch?
- `answer_correct`: did the final answer satisfy the query?
- `policy_correct`: did the policy-gateway apply the right decision?
- `latency_ms`: end-to-end wall time
- `cost_tokens`: total input+output tokens consumed

Use this set to produce the **evaluation table** shown in step 6 of [[../workflows/demo-flow|Demo Flow]].

## Risks / Caveats
- A full data pipeline is probably out of scope for the event.
- Use datasets only if they directly improve the demo or evaluation story.

## Related
- [[task-aware-routing]]
- [[../data-models/evaluation-record|Evaluation Record]]
