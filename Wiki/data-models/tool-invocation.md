# Tool Invocation

## Purpose
- Normalize direct function calls and MCP-backed tool usage into one auditable structure.

## Producers
- orchestrator
- policy gateway

## Consumers
- tool execution layer
- audit logging
- evaluation harness

## Shape
```json
{
  "invocation_id": "string",
  "tool_type": "function|mcp",
  "tool_name": "string",
  "target_system": "string",
  "reason": "string",
  "input_schema_ref": "string",
  "input_payload": {},
  "approval_mode": "auto|manual|required",
  "status": "planned|running|succeeded|failed|blocked",
  "result_ref": "string"
}
```

## Field Semantics

### `tool_type`
- `function` means app-owned deterministic logic
- `mcp` means server-backed capability reached through MCP

### `reason`
- should explain the branch decision in execution terms
- examples:
  - "wiki lacked exact benchmark figure"
  - "external verification required"
  - "deterministic schema transform preferred over model synthesis"

### `approval_mode`
- `auto`: allowed by policy without human checkpoint
- `manual`: human checkpoint required before execution
- `required`: execution must not proceed until explicit approval state exists

### `result_ref`
- should point to a concrete output, trace artifact, or stored result
- avoids embedding giant tool outputs directly inside every trace envelope

## Lifecycle Position
- This structure belongs after routing and before or during execution.
- One routed request may produce zero, one, or many tool invocations depending on the chosen branch.
- The policy gateway may inspect or enrich this envelope before execution proceeds.

## Validation Rules
- `tool_name` and `tool_type` are required.
- `reason` should explain why this tool is being used instead of a wiki/local answer.
- risky actions should not be `auto` without explicit allowlisting.

## Failure / Compatibility Notes
- Missing rationale makes debugging and judging harder.
- Different MCP providers may require adapter-specific fields outside the common core.

## Related
- [[routed-request]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../components/mcp-control-plane|MCP Control Plane]]
- [[../components/policy-gateway|Policy Gateway]]
