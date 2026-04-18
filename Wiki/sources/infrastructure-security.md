---
tags: [security, zero-trust, opa, service-mesh, istio, ztna, kubernetes, sandboxing, sources]
last_updated: 2026-04-15
---

# Infrastructure Security

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/What is a service mesh.md`
- `Clippings/What is Istio.md`
- `Clippings/Why choose Istio.md`
- `Clippings/Sidecar or ambient.md`
- `Clippings/Open Policy Agent (OPA)  Open Policy Agent.md`
- `Clippings/What is a Zero Trust network.md`
- `Clippings/What is Zero Trust Network Access (ZTNA).md`
- `Clippings/What is CASB  Cloud access security brokers.md`
- `Clippings/Cloud Native Security and Kubernetes.md`
- `Clippings/Kubernetes Security - OWASP Cheat Sheet Series.md`
- `Clippings/Pod Security Standards.md`
- `Clippings/Pod Security Standards 1.md`
- `Clippings/What is gVisor - gVisor.md`
- `Clippings/Introduction to gVisor security - gVisor.md`
- `Clippings/Firecracker.md`
- `Clippings/firecrackerdocsdesign.md at main.md`

---

## Service Mesh

### What is a service mesh?
A service mesh adds **observability, security, and reliability** to microservices by inserting these features at the platform layer rather than the application layer.

Implemented as a set of network proxies deployed alongside services (sidecar pattern).

Components:
- **Data plane**: The proxies themselves (Envoy, in Istio's case)
- **Control plane**: Central config manager (istiod in Istio)

### What a service mesh provides

| Capability | Mechanism |
|-----------|-----------|
| Mutual TLS (mTLS) | Automatic encryption + identity validation between services |
| Load balancing | Latency-aware, weighted, failover, canary |
| Traffic management | Routing rules, retries, circuit breaking, fault injection |
| Observability | Metrics, traces, access logs for all traffic — no app changes |
| Policy enforcement | Rate limits, quotas, access control |
| Service discovery | Dynamic endpoint registration from Kubernetes |

### Why it matters for agentic AI
Agents make many service-to-service calls (tool invocations, MCP servers). A service mesh:
- Provides mTLS identity for every agent-to-tool call
- Enables rate limiting on tool calls per agent
- Creates observability traces spanning agent ↔ tool ↔ external API
- Enforces least-privilege access at network level

### Istio

Open-source service mesh on Kubernetes. Two data plane modes:
| Mode | Description | Best for |
|------|-------------|---------|
| **Sidecar mode** | Envoy proxy injected into each pod | Per-workload fine-grained control |
| **Ambient mode** | Per-node L4 proxy + optional per-namespace L7 proxy | Lower overhead, simpler ops |

**Sidecar advantages**: per-pod policies, isolation, full L7 visibility  
**Ambient advantages**: no proxy per pod → lower memory, faster startup, no injection complexity

Key Istio capabilities:
- mTLS auto-enabled between services (SPIFFE/X.509 identities)
- VirtualService, DestinationRule for traffic routing
- AuthorizationPolicy for RBAC on service calls
- Integration with external auth (JWT, OIDC)

---

## Open Policy Agent (OPA)

### What is OPA?
OPA is a **general-purpose policy engine** that decouples policy decision-making from policy enforcement.

**Pattern**: Service queries OPA → OPA evaluates policy + data → returns decision (any JSON, not just allow/deny)

```
Service → OPA: {"user": "alice", "action": "read", "resource": "db"}
OPA → Service: {"allow": true}
```

### Rego policy language
OPA policies are written in Rego (declarative, logic-based):

```rego
package example

default allow := false

allow if {
    input.user == "admin"
}

allow if {
    input.action == "read"
    input.user in data.authorized_users
}
```

### Where OPA is used
- Kubernetes admission control (gatekeeper)
- API gateway policy (integrate with Envoy ext_authz)
- CI/CD pipeline checks
- Microservice authorization
- Terraform/infrastructure as code policy enforcement

### OPA + Envoy Integration
OPA can serve as the `ext_authz` backend for Envoy:
1. Request arrives at Envoy
2. Envoy calls OPA (gRPC ext_authz API)
3. OPA evaluates policy (user identity, request path, method, headers)
4. Envoy allows or denies based on OPA decision

This enables declarative, code-driven policy for LLM gateway/routing decisions.

---

## Zero Trust and ZTNA

### Zero Trust model
"Never trust, always verify." Assumes threats exist both inside and outside the network perimeter.

**Traditional (castle-and-moat)**: Trust everything inside the network boundary → once inside, access to all resources  
**Zero Trust**: Every user, device, and request must be explicitly verified before accessing any resource

### Zero Trust Network Access (ZTNA)
Technology that implements the Zero Trust model for network access.

Key properties:
1. **Least-privilege access**: Only grant access to the specific resource requested
2. **Micro-segmentation**: Resources are invisible (unlisted) to unauthorized entities
3. **Continuous verification**: Re-verify and re-authorize periodically, not just at login
4. **Application layer**: ZTNA operates at L7 (application), not L3 (network like VPN)

### ZTNA vs VPN

| Aspect | VPN | ZTNA |
|--------|-----|------|
| Access scope | Full network (castle-and-moat) | Specific application only |
| OSI layer | L3 (IPsec) | L7 (application) |
| Visibility | All internal resources visible | Other resources hidden |
| Lateral movement | Easy for attacker | Blocked by design |
| Security model | Perimeter-based | Identity-based, continuous |

### Relevance to agentic systems
- Agents should access only what they need (ZTNA principle = least privilege)
- Agent identity (SPIFFE/mTLS) + OPA policy + ZTNA-style access controls form a coherent security architecture
- Connection to [[../components/policy-gateway|Policy Gateway]]: policy gateway implements ZTNA principles at the application/API level

### CASB (Cloud Access Security Broker)
Intermediary between cloud users and cloud services that enforces security policies:
- Visibility into cloud service usage
- Data loss prevention (DLP)
- Compliance enforcement
- Threat protection

Relevant for multi-cloud agent deployments where agents call different cloud-hosted tools.

---

## Kubernetes Security

### Pod Security Standards
Three profiles enforced at namespace level:

| Profile | Description |
|---------|-------------|
| **Privileged** | Unrestricted (for system pods) |
| **Baseline** | Minimal restrictions; prevents known privilege escalations |
| **Restricted** | Hardened; defense-in-depth for security-sensitive workloads |

Enforced via `pod-security.kubernetes.io/enforce: restricted` namespace label.

Key restrictions in `restricted` profile:
- No privileged containers
- No `hostPath` volume mounts
- No `hostPID`/`hostNetwork`
- Non-root user required (`runAsNonRoot: true`)
- Drop all capabilities; add only what's needed
- Seccomp profile required

### OWASP Kubernetes Top 10
1. Insecure workload configs
2. Supply chain vulnerabilities
3. Overly permissive RBAC
4. Lack of centralized policy enforcement
5. Inadequate logging and monitoring
6. Broken authentication
7. Missing network segmentation
8. Secrets management failures
9. Misconfigured cluster components
10. Outdated/vulnerable components

---

## Sandboxing Technologies

### gVisor (Google)
A user-space kernel that intercepts and handles system calls, providing a sandboxing layer between containers and the host kernel.

**How it works**:
- Containers run with gVisor's "Sentry" (user-space kernel) instead of directly on host kernel
- Sentry intercepts syscalls and implements kernel ABI in user space
- Reduces attack surface: even if container escapes, attacker reaches Sentry (user-space), not host kernel

**Use case**: Running untrusted code (e.g., code generated by agent) in isolation.

**Performance**: ~10-30% overhead vs. native; acceptable for most LLM workloads where inference dominates.

### Firecracker (AWS)
A lightweight virtual machine monitor (VMM) designed for secure multi-tenant workloads.

**How it works**:
- Each workload runs in a micro-VM (not container)
- Minimal device model: only virtio-net, virtio-block, serial, button
- Fast startup: ~125ms to boot a micro-VM
- Used in production by AWS Lambda and AWS Fargate

**Security model**: Hardware VM isolation — stronger than container isolation. Each tenant/agent gets their own micro-VM.

**Use case for agentic systems**: When agents need real filesystem operations or code execution. Firecracker provides isolation comparable to VMs with container-like density.

### gVisor vs Firecracker vs Standard Containers

| Technology | Isolation | Overhead | Use case |
|-----------|-----------|----------|---------|
| Container (runc) | Linux namespaces/cgroups | ~minimal | Trusted workloads |
| gVisor (runsc) | User-space kernel | ~10-30% | Moderate isolation |
| Firecracker micro-VM | Full VM isolation | ~5-10% for compute | High isolation per tenant |
| Traditional VM | Full hypervisor | ~15-20% | Strongest isolation |

### WASI (WebAssembly System Interface)
Sandboxed execution of WebAssembly modules with restricted capabilities:
- Run untrusted code with explicit capability grants (file access, network, etc.)
- Language-agnostic bytecode format
- Lower overhead than VM isolation

---

## Security Architecture for Agentic Systems

Combining all layers:

```
Internet
  ↓
[ZTNA / Edge Security]     ← Identity, device trust
  ↓
[Envoy AI Gateway]         ← SPIFFE mTLS, RBAC, rate limiting
  ↓
[OPA Policy Engine]        ← Declarative authorization decisions
  ↓
[Service Mesh (Istio)]     ← Service-to-service mTLS, traffic control
  ↓
[Agent Runtime]            ← Guardrails, human-in-loop (LLM06)
  ↓
[Tool Execution]           ← Sandboxed (gVisor/Firecracker for code execution)
  ↓
[KV / Storage]             ← Encrypted, access-controlled
```

Each layer provides defense in depth. Failure at any one layer doesn't compromise the whole stack.

---

## Related
- [[agentic-security-notes]] — runtime security layers, dynamic credentials
- [[owasp-llm-top10]] — application-level LLM vulnerabilities
- [[adversarial-ml]] — ML-specific attack taxonomy
- [[../components/policy-gateway|Policy Gateway]] — policy enforcement design
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — gateway layer
- [[security-networking-and-governance]] — source hub
