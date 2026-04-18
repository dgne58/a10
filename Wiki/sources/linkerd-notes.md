---
title: Linkerd and Istio — Service Mesh Internals
type: source-synthesis
tags: [service-mesh, linkerd, istio, traffic-management, circuit-breaking, rate-limiting, kubernetes, sources]
last_updated: 2026-04-15
---

# Linkerd and Istio — Service Mesh Internals

Synthesis of Linkerd proxy internals and Istio traffic management. Complements [[infrastructure-security|Infrastructure Security]] (which covers service mesh concepts + Zero Trust) and [[envoy-gateway-notes|Envoy Gateway Notes]] (which covers the Envoy proxy used by Istio's data plane).

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included (Batches 13 + 14)
**Linkerd**:
- `Circuit Breaking.md`, `Rate Limiting.md`, `Retries.md`, `Cancellation.md`, `Deadlines.md`
- `Observability.md`, `Proxy Configuration.md`, `Proxy Log Level.md`, `Proxy Metrics.md`
- `Custom Backend Metrics.md`, `Custom Load Balancing Policies.md`, `Custom Name Resolution.md`
- `Benchmarking.md`, `Authentication.md`, `Debugging.md`, `Status Codes.md`, `Compression.md`
- `Architecture.md`, `Multi-cluster communication.md`, `Cluster Configuration.md`
- `Control Plane Port Names.md`, `Service Profiles.md`, `EgressNetwork.md`
- `ExternalWorkload.md`, `GRPCRoute.md`, `HTTPRoute.md`

**Istio**:
- `Traffic Management.md`

---

## 1. Linkerd Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│  Control Plane (linkerd namespace)                          │
│  • destination service — policy + service discovery        │
│  • identity service — TLS CA; issues mTLS certs to proxies  │
│  • proxy injector — admission controller; injects sidecar   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  Data Plane — per-pod sidecar (linkerd-proxy, Rust)         │
│  • Transparent TCP proxy (iptables redirection via init)    │
│  • Outbound proxy: service discovery, LB, circuit breaker,  │
│    retries, timeouts                                        │
│  • Inbound proxy: enforces authorization policy             │
│  • Automatic Prometheus metrics, mTLS, WebSocket            │
└─────────────────────────────────────────────────────────────┘
```

**Linkerd2-proxy** is written in Rust — ultralight, designed for service mesh only (not general-purpose). Compare to Envoy (Istio's proxy): heavier, C++, general-purpose but more extensible.

**Meshed connection roles**:
- **Outbound proxy** (in requesting pod): service discovery, load balancing, circuit breakers, retries, timeouts
- **Inbound proxy** (in target pod): enforces authorization policy

---

## 2. Traffic Reliability Controls

### Circuit Breaking

Endpoint-level circuit breaking (not service-level): the proxy monitors individual pod health.

**Failure accrual**: tracks N consecutive failures → marks endpoint unavailable.

```
Default: 7 consecutive 5xx responses → endpoint tripped
```

**Probation and backoff**:
1. After min-penalty (default 1s): endpoint enters probation
2. One probe request sent to test recovery
3. If probe succeeds → endpoint restored
4. If probe fails → exponential backoff (up to max-penalty, default 1m) + jitter
5. Repeat until recovery

**Key constraint**: Circuit breaking is **incompatible with ServiceProfiles** — ServiceProfile retry/timeout config takes precedence.

**Outbound proxy implements circuit breaking** (client-side behavior): when all endpoints are tripped, return 503 or select another backendRef.

### Rate Limiting

Linkerd rate limiting uses `HTTPLocalRateLimitPolicy` (K8s CRD):

```yaml
spec:
  targetRef: <Server>          # Server resource being protected
  total:
    requestsPerSecond: 100     # Global cap across all callers
  identity:
    requestsPerSecond: 20      # Per-client identity fairness cap
  overrides:                   # Named client exceptions
    - requestsPerSecond: 25
      clientRefs:
        - kind: ServiceAccount
          namespace: emojivoto
          name: special-client
```

**Note**: Default Server `accessPolicy` is `deny`. If no AuthorizationPolicy exists, rate limits can't be applied to a permissive-by-default server without setting `accessPolicy: all-unauthenticated`.

### Retries

Retries are configured via annotations on Services or route resources (HTTPRoute/GRPCRoute):

| Annotation | Scope | Behavior |
|-----------|-------|---------|
| `retry.linkerd.io/http` | Service/HTTPRoute | Comma-separated HTTP status codes to retry (e.g., `"500-504"`, `"5xx"`, `"gateway-error"`) |
| `retry.linkerd.io/grpc` | Service/GRPCRoute | gRPC status codes: `cancelled`, `deadline-exceeded`, `internal`, `resource-exhausted`, `unavailable` |

**Constraints**:
- Request body > 64KiB: **not retried**
- ServiceProfile overrides all retry annotations (same incompatibility as circuit breaking)
- Each retry can go to a different backend (if multiple `backendRef`s)

---

## 3. Istio Traffic Management

Istio uses Envoy as its data plane proxy. Traffic management is configured via Kubernetes CRDs.

### Key Resources

| Resource | Purpose |
|---------|---------|
| **VirtualService** | Route matching rules (path, headers, user identity) → weighted destinations |
| **DestinationRule** | Load balancing policy, circuit breaker config, TLS policy for a service |
| **Gateway** | Ingress/egress Envoy configuration at mesh boundary |
| **ServiceEntry** | Register external services in Istio's registry |
| **Sidecar** | Scope which namespaces an Envoy proxy should be aware of |

### Virtual Services

VirtualServices decouple client-facing hostname from backend versions:
- Header-based routing (user identity, content type)
- Percentage-based canary traffic splits (e.g., 80% → v1, 20% → v2)
- Retry and timeout policies per route
- Fault injection for chaos testing

```yaml
# Example: user "jason" → v2, everyone else → v1
http:
- match:
  - headers: { end-user: { exact: jason } }
  route:
  - destination: { host: reviews, subset: v2 }
- route:
  - destination: { host: reviews, subset: v1 }
```

### Destination Rules

DestinationRules configure what happens after routing decisions:
- **Load balancing**: ROUND_ROBIN, LEAST_CONN, RANDOM, PASSTHROUGH, CONSISTENT_HASH (session affinity)
- **Circuit breaking** (connection pool + outlier detection): max connections, max pending requests, consecutive errors → host ejection
- **Service subsets**: Named groups of endpoints by label (e.g., version: v1 vs version: v2)
- **TLS policy**: DISABLE, SIMPLE (TLS), MUTUAL (mTLS), ISTIO_MUTUAL

### Gateways

Istio Gateways configure Envoy at mesh edges (ingress/egress):
- Specify port, protocol, TLS termination
- Combine with VirtualService for L7 routing rules
- Supports HTTP/HTTPS, TCP, gRPC

---

## 4. HTTPRoute and GRPCRoute (Gateway API)

Kubernetes Gateway API replaces the older Ingress API. Both Istio and Linkerd support it.

**HTTPRoute**:
- Matches on path prefix, method, headers
- Routes to Services with optional weight (traffic split)
- Retry/timeout policies per rule
- Header modification and URL rewriting

**GRPCRoute**:
- Matches on service name and method name (gRPC-specific)
- Weight-based traffic splitting per method
- Retry on specific gRPC status codes

**HTTPLocalRateLimitPolicy** (Linkerd) attaches to a Server, not a route — separate concept from route-level traffic management.

---

## 5. Relevance to This Project

| Capability | Use in Hackathon Project |
|-----------|------------------------|
| **Linkerd circuit breaking** | SLM router: if one routing backend (e.g., Groq) fails consecutively, trip circuit breaker and failover to Bedrock |
| **Linkerd rate limiting** | Inference endpoint: `total.requestsPerSecond` guards against token-cost attacks (LLM10 Denial of Wallet) |
| **Istio VirtualService** | Canary rollout of new routing policy: 10% traffic to new router, 90% to old |
| **DestinationRule circuit breaker** | Outlier detection on LLM backends: eject backend after N 5xx responses |
| **HTTPRoute retries** | Retry transient 503/504 from inference endpoints before returning error to agent |

---

## 6. Istio Security Model

### Identity and Certificate Management

Istio's security model centers on **workload identity** (not IP-based identity):
- Every workload gets a **SPIFFE identity** (X.509 certificate) issued by Istio's built-in CA (istiod)
- Certificates are short-lived, auto-rotated; workloads never need to manage certs manually
- **Secure naming**: maps service account → expected service name; prevents a compromised service from impersonating another

### mTLS by Default

Istio enables mutual TLS automatically between meshed services:
- **STRICT mode**: Only mTLS connections accepted (rejects plaintext)
- **PERMISSIVE mode**: Both plaintext and mTLS accepted (migration phase)
- Each Envoy sidecar acts as a **Policy Enforcement Point (PEP)**

### Authorization Policy

Fine-grained L7 access control via `AuthorizationPolicy` CRDs:
- **Source**: namespace, principal (service account), IP block
- **Operation**: hosts, ports, methods, HTTP paths, gRPC services
- **Condition**: JWT claims, headers, source labels

```yaml
# Only allow "frontend" service to call "backend" via GET /api
spec:
  selector: { matchLabels: { app: backend } }
  rules:
  - from:
    - source: { principals: ["cluster.local/ns/default/sa/frontend"] }
    to:
    - operation: { methods: ["GET"], paths: ["/api/*"] }
```

### Relevance to Agentic Systems

| Istio Security | Agentic Application |
|---------------|---------------------|
| SPIFFE workload identity | Each agent has a cryptographic identity; policy enforced on agent, not on API key |
| AuthorizationPolicy | Restrict which agents can call which MCP tool endpoints |
| mTLS between agents | Prevents man-in-the-middle on agent-to-agent and agent-to-tool traffic |
| Audit logging | Non-repudiation: which agent called which tool at what time |

---

## Related
- [[infrastructure-security|Infrastructure Security]] — service mesh overview, Istio positioning, Zero Trust
- [[envoy-gateway-notes|Envoy Gateway Notes]] — Envoy AI Gateway, Envoy proxy internals
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — LLM routing via Envoy
- [[network-protocols|Network Protocols]] — gRPC, HTTP/2, mTLS specs
- [[owasp-llm-top10|OWASP LLM Top 10 (2025)]] — LLM10 (Unbounded Consumption) = rate limiting target
