# Policy Gateway

## Overview
- Enforce security, identity, approvals, and observability at runtime.
- Prevent the system from becoming an unbounded execution layer.
- Provide a place where runtime trust decisions become explicit rather than being hidden inside prompts.

## Trust Zones

The gateway is easiest to reason about if the system is divided into trust zones:

| Zone | Typical contents | Default posture |
| --- | --- | --- |
| Local memory zone | wiki pages, trace artifacts, preload docs | mostly trusted but protected from silent corruption |
| App-owned execution zone | internal deterministic tools and local code | allow narrow, auditable operations |
| MCP / connector zone | external servers and reusable integrations | trust only per server and per capability |
| Public model / SaaS zone | external LLMs, public tools, browser-like surfaces | assume data egress and stronger controls |

This framing helps clarify why wiki writes, local file writes, and external API calls should not all share the same approval posture.

## Inputs
- requested action
- caller or task identity
- target tool, resource, or service
- context and risk metadata
- optional human approval state

## Outputs
- allow, deny, or require-approval decision
- audit record
- rate-limit, routing, or failover consequence

## Runtime Security Model

### Perception layer
- validates input structure and origin
- mitigates prompt injection and untrusted payload blending

### Reasoning layer
- checks whether the intended action still matches the declared task
- useful for blocking goal drift

### Action layer
- enforces capability boundaries
- where allowlists, dynamic credentials, and approval paths matter most

### Memory layer
- protects long-lived state such as the wiki, traces, and stored context
- prevents silent poisoning or undocumented writes

These layers come directly from the runtime-security material and are useful because they map cleanly to engineering controls.

## A2AS And Related Control Ideas
- behavior certificates: predeclare permissible behavior envelopes
- authenticated prompts: distinguish trusted from untrusted instructions
- security boundaries: separate internal from external capability sets
- in-context defenses: still useful, but insufficient alone
- policies: actual enforceable business logic at runtime

## How It Works In This Project

### Low-risk actions
- wiki reads
- local introspection
- read-only filesystem or resource access

### Medium-risk actions
- wiki writes
- local file writes
- updates to project memory

### High-risk actions
- external API calls with side effects
- publish, delete, transfer, or mutation operations
- actions using delegated identity
- data egress to public model surfaces

### Suggested behavior
- low-risk: allow
- medium-risk: allow plus log, or gated by scope
- high-risk: explicit human approval or deny by default

## Dynamic Credentials
- Prefer task-scoped or short-lived credentials over static API keys.
- This limits blast radius and aligns with the source material on runtime control.

## Delegation And User Identity
- In many agentic systems, the question is not only "which tool can the agent call?"
- It is also "on whose behalf is that action being performed?"
- That makes delegated user identity and approval traces central to the security story.

## Evaluation Order

A useful evaluation order for this gateway is:
1. identify caller and delegated user scope
2. classify requested action
3. determine target trust zone
4. inspect payload for sensitive-data restrictions if relevant
5. allow, deny, or require approval
6. emit audit event with the final decision

This ordering keeps DLP and identity from being treated as optional post-processing.

## DLP Integration

DLP belongs in the gateway because data flow and action flow are coupled in agent systems.

### Typical triggers
- paste or upload into public LLM
- sending internal wiki or source material to an external MCP server
- tool output that includes secrets, PII, credentials, or regulated records

### Typical controls
- block
- redact
- require approval
- route to safer internal path instead

Routing and policy interact here: a branch may be technically possible but still disallowed because its data-flow properties are unsafe.

## Relationship To Network Enforcement
- Application-level policy decides whether the system should attempt an action.
- Infrastructure-level enforcement such as [[envoy-ai-gateway]] can:
  - verify workload identity
  - enforce RBAC on tool names or provider paths
  - apply rate limiting
  - emit telemetry

These layers are complementary, not substitutes.

## Minimal Hackathon Policy Shape

```python
POLICY = {
    "wiki_read": {"risk": "low", "approval": "none"},
    "wiki_write": {"risk": "medium", "approval": "auto"},
    "filesystem_read": {"risk": "low", "approval": "none"},
    "filesystem_write": {"risk": "medium", "approval": "auto"},
    "external_api": {"risk": "high", "approval": "manual"},
}
```

The point is not this exact dictionary. The point is that the logic is explicit and demonstrable.

## What Good Evidence Looks Like
- trace shows which rule fired
- approval event is visible
- blocked action is explainable
- delegated identity is explicit
- outbound data restrictions are inspectable

## Failure Modes
- policy exists only as prose, not as executable or inspectable logic
- broad long-lived credentials undermine all higher-level controls
- no audit trail exists for tool calls and writes
- destructive paths lack approval gates
- data-flow controls are missing even when action controls exist

## Related Topics
- [[mcp-control-plane]]
- [[envoy-ai-gateway]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../sources/security-networking-and-governance|Security, Networking, and Governance]]
- [[../sources/agentic-security-notes|Agentic Security Notes]]
- [[../00-preload/fallback-plans|Fallback Plans]]
