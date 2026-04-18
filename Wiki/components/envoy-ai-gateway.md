---
tags: [envoy, gateway, mcp, security, routing, llm-providers]
sources: [Envoy AI Gateway docs, Case for Envoy in Agentic AI Era, Context-aware Security agentgateway]
last_updated: 2026-04-13
---

# Envoy AI Gateway

## Purpose

Answers: "How do I route to multiple LLM providers securely? How does MCP security work at the gateway layer? What does Envoy add that an app-level proxy doesn't?"

---

## What It Is

**Envoy AI Gateway** (aigateway.envoyproxy.io) is an open-source project built on Envoy Proxy that provides a unified, secure, observable layer for LLM/AI traffic. It sits between your application and GenAI providers.

**Key capabilities**:
- Unified routing to 15+ LLM providers (one API to rule them all)
- Automatic failover between providers/models
- Rate limiting and usage policy enforcement
- Upstream authentication (provider API keys, not exposed to callers)
- MCP protocol support with tool-name-aware security
- Token-based rate limiting (not just request counts)
- OpenTelemetry-compatible observability

---

## Supported Providers (out of the box)

Anthropic, AWS Bedrock, Azure OpenAI, Cohere, DeepInfra, DeepSeek, Google Gemini, Grok, Groq, Mistral, OpenAI, SambaNova, Together AI, Vertex AI, Hunyuan, Tetrate Agent Router Service.

---

## Why Envoy (not a simple HTTP proxy)

Traditional proxies treat request bodies as opaque bytes. Agentic protocols (MCP, A2A) put critical policy attributes **inside** the message body:
- MCP: tool name, method, parameters are in the JSON-RPC body
- OpenAI: model name is in the request body

Envoy solves this with **deframing filters** that parse protocol messages and expose structured metadata to the rest of the filter chain. This enables:
- RBAC on tool names: `if agent_identity == "triage-agent" AND tool_name IN [list_issues, get_issue] → allow`
- CEL expressions over parsed message attributes
- ext_authz with full MCP context forwarded to external authorization service

---

## Gateway Modes for MCP

### Passthrough Mode
```
Client → [Envoy] → MCP Server A
                 → MCP Server B
```
- Session stickiness via `Mcp-Session-Id` with encoded server address suffix
- Envoy strips the suffix before forwarding to the actual server
- Primary use: policy enforcement (RBAC, rate limiting, auth) for external MCP servers

### Aggregating Mode
```
Client → [Envoy (single MCP facade)] → MCP Server A (tools 1-5)
                                     → MCP Server B (tools 6-10)
```
- Envoy advertises merged tool/resource catalog to the client
- Client sees one MCP server, gets all tools
- Session management tracks which tools belong to which backend server
- Primary use: simplify agent configuration, unify policy for multiple MCP servers

---

## MCP Security Pattern (RBAC on Tool Names)

```yaml
# Restrict agent to read-only GitHub tools only
envoy.filters.http.rbac:
  rbac:
    rules:
      policies:
        github-issue-reader-policy:
          permissions:
            and_rules:
              - sourced_metadata:  # MCP deframing filter extracts this
                  path: [{key: "method"}]
                  value: {string_match: {exact: "tools/call"}}
              - sourced_metadata:
                  path: [{key: "params"}, {key: "name"}]
                  value:
                    or_match:
                      - {string_match: {exact: "list_issues"}}
                      - {string_match: {exact: "get_issue"}}
          principals:
            - authenticated:
                principal_name:
                  exact: "spiffe://cluster.local/ns/agents/sa/triage-agent"
```

---

## Security Layers (zero-trust stack)

1. **mTLS + SPIFFE** — workload identity at transport layer
2. **RBAC** — protocol-aware allow/deny on tool names, model names, resource paths
3. **ext_authz** — complex policies delegated to external service (receives MCP attributes + peer cert)
4. **CEL expressions** — inline policy logic without external service
5. **Rate limiting** — per-agent, per-model, token-count-aware
6. **Upstream auth** — Envoy holds provider API keys; agents never see them

**User-behind-agent pattern**: Agent never holds user credentials. Envoy injects user delegation tokens at the infrastructure layer — if agent is compromised, it can't misuse or leak the token.

---

## agentgateway (Solo.io alternative)

Solo.io's **agentgateway** (agentgateway.dev) is an AI-native Rust proxy with native MCP and A2A protocol support:

| | Envoy AI Gateway | agentgateway |
|---|---|---|
| Language | C++ (Envoy) | Rust |
| Protocol awareness | Via deframing extensions | Native |
| MCP support | Yes (with filter) | Yes (native) |
| K8s integration | Envoy AI Gateway + kube-agentic-networking | kgateway control plane |
| Memory/CPU | Standard Envoy | Significantly lighter |
| Auth patterns | RBAC, ext_authz, mTLS/SPIFFE | CEL + same patterns |

**Deployment modes for agentgateway**:
- Standalone binary with admin UI
- Kubernetes via kgateway (acts as control plane for agentgateway instances)
- Service mesh waypoint (replaces Envoy sidecar for agentic workloads)

---

## A2A Protocol Support (Envoy)

Envoy is adding support for the **Agent-to-Agent (A2A)** protocol and **AgentCard** discovery:
- AgentCard: JSON document advertising agent capabilities, auth requirements, endpoints
- Can be served statically (direct response) or from a centralized registry (via xDS/ext_proc)
- Enables multi-agent coordination without hardcoded endpoints

---

## Session State for Stateful MCP

MCP Streamable HTTP creates sessions. Envoy manages session stickiness:

```
Client               Envoy               MCP Server
  |                    |                     |
  |--tools/list------->|                     |
  |                    |--tools/list-------->|
  |                    |<---Mcp-Session-Id: abc123
  |<--Mcp-Session-Id: abc123+[envoy_suffix]  |
  |                    |                     |
  |--tools/call------->|  (extracts suffix)  |
  |  (Mcp-Session-Id:  |---routes to server--→
  |   abc123+suffix)   |   that holds abc123 |
```

---

## Deployment Checklist

- [ ] `AIGatewayRoute` CRDs configured for each LLM provider
- [ ] Upstream auth secrets loaded (not hardcoded in config)
- [ ] MCP deframing filter enabled for any MCP server routes
- [ ] RBAC policies defined per agent identity
- [ ] Rate limits set (per-agent + global)
- [ ] Health checks configured for failover
- [ ] OTEL exporter configured for observability

---

## Failure Modes

| Failure | Impact | Mitigation |
|---|---|---|
| Provider API down | All requests to that provider fail | Configure fallback to secondary provider |
| Rate limit exceeded | 429 returned to agent | Queue or shed load; alert on threshold |
| MCP session broken | Agent tools stop working | Session reconnect; retry tool call |
| SPIFFE cert expired | mTLS auth fails | Automate cert renewal (cert-manager) |

---

## Related

- [[../workflows/mcp-agentic-patterns|MCP Agentic Patterns]] — what happens inside the gateway
- [[../workflows/llm-routing-approaches|LLM Routing Approaches]] — semantic routing before the gateway
- [[../sources/envoy-gateway-notes|Envoy Source Notes]] — raw source details
