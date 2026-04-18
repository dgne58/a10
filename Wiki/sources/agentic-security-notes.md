---
tags: [security, agentic, idp, runtime, sources]
last_updated: 2026-04-13
---

# Agentic Security Notes

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why these matter

Track 2 explicitly includes "identity, security, infrastructure, and execution layers (IDP, Envoy, MCP, and beyond)." These sources define the security posture for agentic systems.

---

## Establishing Runtime Security for Agentic AI (IBM, 2026)

**Core thesis**: Agentic AI is no longer an isolated sandbox — it's a participant in critical infrastructure. The threat is not individual bad actions but compound decision loops that drift from intent.

### Four Security Layers

| Layer | Defense | Implementation |
|---|---|---|
| **Perception** | Input/context sanitization | IdP (OAuth2) for user identity before agentic flow; deterministic filters for intent; prompt injection prevention |
| **Reasoning** | Semantic firewalls | Monitor how the agent thinks; block actions deviating from intended goal |
| **Action** | Execution interceptors + dynamic credentials | Control plane limits agent capabilities; Vault for time-based credentials (auto-revoked); backchannel auth for high-risk ops |
| **Memory** | State protection | Track data provenance; prevent memory poisoning; enable rollback to trusted states |

### A2AS Framework (Agentic AI Runtime Security)

Five control elements:
1. **Behavior certificates** — define permissible agent behaviors
2. **Authenticated prompts** — validate what enters an agent
3. **Security boundaries** — separate trusted from untrusted
4. **In-context defenses** — direct agent to reject untrusted input
5. **Policies** — enforce business logic

### Key Pattern: Dynamic Credentials

Instead of static API keys baked into agent config:
- Use Vault to issue on-demand, time-limited, auto-revoking credentials
- Agents get credentials only for the duration of their task
- If agent is compromised, credentials expire and can't be reused

### Key Pattern: Client-Initiated Backchannel Authentication

For high-risk operations (delete, write, transfer):
1. Agent suspends its execution loop
2. Sends out-of-band authentication request to human via IdP (mobile push)
3. Human approves/denies
4. Agent resumes only with explicit human authorization
- If agent logic is compromised: attacker still can't proceed without human approval

**Source**: `Clippings/Establishing Runtime Security for Agentic AI.md`

---

## Agentic AI Governance (2025)

- Focus on governance frameworks for agentic systems in enterprises.
- Key: log all agent decisions and tool calls for auditability.
- Principle of least privilege: agents should only have the permissions they need for the current task.
- **Source**: `Clippings/Agentic AI Governance How to Approach It.md`

---

## Connection to Envoy/MCP Security

| Security concern | Mechanism |
|---|---|
| Agent identity (who is this agent?) | SPIFFE/mTLS at Envoy layer |
| Tool authorization (what can this agent call?) | RBAC on MCP tool names at Envoy |
| User identity delegation (who is the human?) | IdP OAuth2 → Envoy injects delegation token |
| Dynamic credentials | Vault integration in action layer |
| Audit trail | OTEL telemetry via Envoy + structured agent logs |

---

## Prompt Injection Defense Pattern

Threat: malicious content in tool results hijacks agent's next action.

Defenses:
1. **Separate external input from decision logic** (perception layer sanitization)
2. **Semantic firewall** monitors reasoning step for goal drift
3. **Constrained tool permissions** — agent can't take more damage than its permission scope
4. **Human-in-the-loop** for high-risk consequences

---

## Related

- [[envoy-gateway-notes]] — network layer security implementation
- [[mcp-overview]] — MCP protocol; security of tool calls
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — RBAC, ext_authz, SPIFFE/mTLS details
