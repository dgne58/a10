# Demo Flow

## Purpose
- Provide a stable live-demo path with clear fallback branches.
- Give judges a visible trace of routing, tool use, and policy enforcement.

## Core Narrative
- "We do not just call a model. We decide how to handle the task."
- "We do not just expose tools. We control and observe their use."
- "We do not just rely on chat history. We maintain persistent project memory."

## Demo Script

### Step 1 - User request enters
- What to show: a typed query arrives at the API or UI.
- Input example: "Summarize the routing strategy and verify one local fact from the project."
- Trace to emit: `{ "step": "receive", "query": "...", "session_id": "demo-001" }`

### Step 2 - Router classifies the task
- Component: [[../components/router|Router]]
- What to show: router log with task category and selected path.

```json
{
  "task_category": "wiki_lookup + verification",
  "selected_path": "wiki_first -> local_tool",
  "rationale": "known topic plus one file-backed fact",
  "cost_tier": "cheap"
}
```

### Step 3 - Orchestrator consults the wiki
- Component: [[../components/orchestrator|Orchestrator]]
- What to show: a wiki hit from a relevant page such as `hot.md`, `project-map.md`, or a component page.

```text
[WIKI HIT] Found relevant page
           Action: inject as context, skip external search
```

This demonstrates local-first context rather than immediate internet use.

### Step 4 - Tool or MCP-backed action
- Component: [[../components/mcp-control-plane|MCP Control Plane]]
- What to show: a local tool or MCP call against a file or system that actually exists in the demo environment.

```json
{
  "tool": "filesystem/read_file",
  "path": "./path-that-exists-in-demo",
  "result": "Local fact verified from file or config.",
  "policy_check": "passed"
}
```

This demonstrates grounded verification instead of guesswork.

### Step 5 - Policy gateway check
- Component: [[../components/policy-gateway|Policy Gateway]]
- What to show: policy decision log for the tool action.

```text
[POLICY] tool=filesystem/read_file risk=low approval=none -> ALLOW
[AUDIT] action=filesystem_read caller=orchestrator ts=2026-04-13T10:30:01Z
```

If a write operation is part of the demo, show the approval branch instead.

### Step 6 - Final answer plus trace
- What to show: synthesized answer plus end-to-end trace.

```text
Answer: "The system uses a tiered routing policy: wiki first, then a cheaper or specialized
path for narrow tasks, then tool or MCP execution for system actions, and a stronger
general path for the remaining cases. The verification step was grounded in a local read."

Trace:
  receive -> route -> wiki_hit -> tool_call -> policy -> synthesize -> respond
```

### Step 7 - Optional write-back
- What to show: orchestrator writes a useful finding into `hot.md` or another narrow page.

```text
[WIKI WRITE] Updated a current-state page with the verified fact.
[AUDIT] wiki_write source=demo-session-001 ts=2026-04-13T10:30:05Z
```

## Fallback Branches

| Failure | Fallback |
| --- | --- |
| Learned router unavailable | Switch to transparent rules-based router |
| MCP server unavailable | Switch to local stub or pre-recorded output |
| Multi-agent instability | Collapse to a single orchestrator path |
| External provider latency | Use offline trace or prior captured run |
| Wiki page missing | Acknowledge the gap and escalate to a stronger path |

## Artifacts To Show
- Routing trace JSON
- Wiki hit log
- Tool invocation log
- Policy decision log
- Execution summary trace
- Optional evaluation table comparing `wiki_first` vs `direct_model`

## Timing Guide

| Step | Target time |
| --- | --- |
| Steps 1-2 | 5-10 sec |
| Step 3 | 5 sec |
| Step 4 | 10-15 sec |
| Step 5 | instant |
| Step 6 | 10-20 sec |
| Step 7 | 5 sec |
| Total | about 60 sec |

## Related
- [[../00-preload/judging-demo-narrative|Judging and Demo Narrative]]
- [[../00-preload/fallback-plans|Fallback Plans]]
- [[../components/router|Router]]
- [[../components/orchestrator|Orchestrator]]
- [[../components/policy-gateway|Policy Gateway]]
- [[../components/mcp-control-plane|MCP Control Plane]]
