---
tags: [envoy, gateway, security, agentic, threading, sources]
last_updated: 2026-04-15
---

# Envoy Gateway Notes

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why these matter

Envoy is the security and traffic management layer for agentic AI. Critical for the hackathon's IDP + security orchestration angle.

---

## Envoy AI Gateway (aigateway.envoyproxy.io, 2024/2025)

- Open-source project built on Envoy Proxy for LLM/AI traffic management.
- **Core goals**: resilient connectivity, observability, enterprise security, extensibility.
- **MCP support added**: Full spec compliance, OAuth authentication, zero-friction deployment.
- Control plane can scale to 2,000 AIGatewayRoute resources (benchmarked).
- 15+ supported LLM providers out of the box.
- **Source**: `Clippings/Envoy AI Gateway.md`, `Clippings/Envoy AI Gateway 1.md`
- [[../components/envoy-ai-gateway|→ Full component page]]

---

## The Case for Envoy Networking in the Agentic AI Era (Google, April 2026)

- **Core thesis**: Agentic protocols (MCP, A2A) bury policy attributes inside JSON-RPC/gRPC message bodies. Traditional proxies can't enforce policy on what they can't see.
- **Envoy's answer**: Deframing filters parse protocol messages and expose structured metadata to the filter chain.
- **Three capabilities added**:
  1. Agent traffic understanding (deframing MCP/A2A/OpenAI messages)
  2. Fine-grained policy enforcement (RBAC on tool names, ext_authz with full MCP context, CEL)
  3. Stateful session management for MCP Streamable HTTP
- **A2A support**: AgentCard discovery; agent registry via xDS.
- **OpenAI transcoding**: Convert agentic protocols ↔ RESTful HTTP APIs (Wasm/dynamic modules).
- **Key quote**: "Decouple agent development from enforcement. Developers build agents; operators enforce zero-trust at the network layer."
- **Source**: `Clippings/The case for Envoy networking in the agentic AI era.md`

---

## Context-Aware Security for Agentic AI Gateways (Solo.io, Dec 2025)

- **Problem**: Traditional proxies (NGINX, HAProxy, even basic Envoy) are not AI-context-aware.
- **agentgateway**: Solo.io's Rust-based AI-native proxy. Understands MCP and A2A natively.
- **Three AI scenarios handled**:
  1. LLM consumption (egress: apps calling external LLMs)
  2. Inference consumption (ingress: routing to self-hosted models)
  3. Agentic flows (mesh: agents, tools, MCP servers communicating internally)
- **CEL-based authorization**: Policy can check both caller identity AND the specific tool being invoked.
- **Deployment**: Standalone binary, Kubernetes (kgateway), service mesh waypoint.
- **Source**: `Clippings/Context-aware Security for Agentic AI Gateways.md`

---

## Supported AI Providers (Envoy AI Gateway)

Full list: Anthropic, AWS Bedrock, Azure OpenAI, Cohere, DeepInfra, DeepSeek, Google Gemini, Grok, Groq, Hunyuan, Mistral, OpenAI, SambaNova, Tetrate Agent Router Service, Together AI, Vertex AI.

- **Source**: `Clippings/Supported AI Providers Envoy AI Gateway.md`

---

## Key Differences: Envoy AI Gateway vs agentgateway

- **Envoy AI Gateway**: Community project on top of proven Envoy; Kubernetes-native; uses xDS control plane.
- **agentgateway**: Purpose-built for AI; Rust, lighter; native protocol understanding without filters; part of Solo.io enterprise stack.
- Both support MCP, both integrate with Kubernetes.
- For hackathon: use Envoy AI Gateway if you want the broader community ecosystem; use agentgateway if you prioritize MCP-native simplicity and performance.

---

## Envoy Proxy Internals (v1.38)

### Core Architecture
- **Out-of-process**: Self-contained sidecar alongside every service; language-agnostic
- **Filter chain architecture**: L3/L4 filters (TCP/UDP) + HTTP L7 filters — composable pipeline
- **Protocols**: HTTP/1.1, HTTP/2 (first-class), HTTP/3 (alpha), gRPC, Redis, MongoDB, Postgres
- **xDS dynamic configuration**: Real-time updates to listeners, clusters, routes, and secrets via gRPC streaming API

### Threading Model (single-process, multi-threaded)

```
┌──────────────────────────────────────────────────────┐
│  Main Thread                                          │
│  • xDS config updates    • Stats flushing             │
│  • Admin interface       • Signal handling            │
└──────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────┐
│  Worker Threads (N = hardware thread count)          │
│  • Accept connections    • HTTP request processing   │
│  • Filter chain execution • Upstream dispatch        │
│  Each thread: Event::Dispatcher loop (libevent)      │
└──────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────┐
│  File Flusher Thread                                  │
│  • Async access log writes (avoids blocking workers) │
└──────────────────────────────────────────────────────┘
```

**Key design decisions**:
- Connection pinned to a single worker thread for its lifetime → no locking on the hot path
- Worker threads are **share-nothing** by default; TLS (Thread Local Storage) used for config state
- Config updates: Main thread posts closures to all workers (one-way push, no cross-worker locks)
- **io_uring** (Linux): Per-worker ring; completion events wired into Dispatcher via eventfd
- **Connection balancing**: Kernel balances by default (sufficient for most workloads); Envoy-level balancing available for long-lived HTTP/2 connections

### Listener and Filter Chain

A **Listener** is an entry point for connections. Listeners contain:
1. **Listener filters** — read metadata before routing (e.g., TLS inspector, HTTP inspector, PROXY protocol)
2. **Network (L3/L4) filter chains** — match on TLS SNI, ALPN, source IP → apply TCP/UDP filters
3. **HTTP Connection Manager** — L7 filter for HTTP; contains HTTP filter chain

**HTTP filter chain evaluation order**:
```
Request in
  → JWT/OAuth verification
  → RBAC policy check
  → Rate limit check
  → Router (picks upstream cluster)
  → ext_authz call (if configured)
  → Upstream connection
Response out ← (filters evaluated in reverse)
```

### Observability
- **Statistics**: Per-connection, per-cluster, per-filter counters/gauges/histograms; statsd/OTel sinks
- **Access logging**: Async (file flusher thread); format configurable; streamed to stdout or file
- **Distributed tracing**: Pluggable (Zipkin, Jaeger, AWS X-Ray, OTLP); trace IDs propagated through filter chain
- **Admin interface**: `/stats`, `/clusters`, `/listeners`, `/config_dump` endpoints on local port

### WebAssembly Extensions (Proxy-Wasm)

Envoy (and Istio) supports dynamic extensions via **WebAssembly plugins** using the Proxy-Wasm ABI:

**Why Wasm for extensions**:
- **Isolation**: Crash in one plugin doesn't affect other plugins or Envoy
- **Efficiency**: Low latency / memory overhead vs. gRPC-based ext_proc
- **Portability**: Can be written in C++, Rust, Go, AssemblyScript
- **Dynamic configuration**: Plugins configured via Istio CRDs, hot-reloaded

**Wasmtime security properties** (relevant when Wasm modules run untrusted code):
- Callstack inaccessible to wasm code → traditional stack-smashing impossible
- Memory accesses bounds-checked → no buffer overruns into Envoy memory
- All host interactions via explicit imports → no raw syscall access
- Capability-based filesystem (WASI) → code only accesses explicitly granted files
- Guard regions precede linear memory → prevents accidental sign-extension bugs
- Memory zeroed after instance destruction → prevents cross-tenant data leakage
- Spectre mitigations: `br_table` and `call_indirect` bounds checks mitigated

**Proxy-Wasm plugin capabilities** in Istio:
- HTTP filter chain — modify headers, trailers, body
- Call out to gRPC or HTTP services from plugin code
- Emit custom metrics + log entries
- Can be canaried (deploy as log-only before enforcing)

**Hackathon use**: Proxy-Wasm plugins could implement custom LLM routing logic at the Envoy layer — e.g., a Wasm filter that reads the model name from request body and routes to a specific backend cluster.

### Additional Sources Included (batch 13)
- `What is Envoy — envoy 1.38.0-dev-550d57 documentation.md`
- `Listeners — envoy 1.38.0-dev-550d57 documentation.md`
- `Listener filters — envoy 1.38.0-dev-550d57 documentation.md`
- `Terminology — envoy 1.38.0-dev-550d57 documentation.md`
- `Threading model — envoy 1.38.0-dev-550d57 documentation.md`
