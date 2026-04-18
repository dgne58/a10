---
title: "The case for Envoy networking in the agentic AI era"
source: "https://cloud.google.com/blog/products/networking/the-case-for-envoy-networking-in-the-agentic-ai-era"
author:
  - "[[Yan Avlasov]]"
  - "[[Erica Hughberg]]"
published: 2026-04-03
created: 2026-04-13
description: "In the world of AI agents, the Envoy networking proxy consistently enforces governance and security across all agentic paths, and at scale."
tags:
  - "clippings"
---
##### Yan Avlasov

Staff Software Engineer, Google

##### Erica Hughberg

Product and Product Marketing Manager, Tetrate

##### Try Nano Banana 2

State-of-the-art image generation and editing

[Try now](https://console.cloud.google.com/vertex-ai/studio/multimodal?model=gemini-3.1-flash-image-preview)

In today's agentic AI environments, the network has a new set of responsibilities.

In a traditional application stack, the network mainly moves requests between services. But as discussed in a recent white paper, [Cloud Infrastructure in the Agent-Native Era](https://services.google.com/fh/files/misc/cloud_infrastructure_in_the_agent_native_era.pdf), in an agentic system the network sits in the middle of model calls, tool invocations, agent-to-agent interactions, and policy decisions that can shape what an agent is allowed to do. The rapid proliferation of agents, often built on diverse frameworks, necessitates a consistent enforcement of governance and security across all agentic paths at scale. To achieve this, the enforcement layer must shift from the application level to the underlying infrastructure. That means the network can no longer operate as a blind transport layer. It has to understand more, enforce better, and adapt faster. This shift is precisely where Envoy comes in.

As a high-performance distributed proxy and universal data plane, Envoy is built for massive scale. Trusted by demanding enterprise environments, including Google Cloud, it supports everything from single-service deployments to complex service meshes using Ingress, Egress, and Sidecar patterns. Because of its deep extensibility, robust policy integration, and operational maturity, Envoy is uniquely suited for an era where protocols change quickly and the cost of weak control is steep. For teams building agentic AI, Envoy is more than a concept: it's a practical, production-ready foundation.

![https://storage.googleapis.com/gweb-cloudblog-publish/images/1_xPxMxF4.max-1800x1800.jpg](https://storage.googleapis.com/gweb-cloudblog-publish/images/1_xPxMxF4.max-1800x1800.jpg)

### Agentic AI changes the networking problem

Agentic workloads still often use HTTP as a transport, but they break some of the assumptions that traditional HTTP intermediaries rely on. Protocols such as [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) and [Agent2agent](https://github.com/google/A2A) (A2A) use [JSON-RPC](https://www.jsonrpc.org/specification) or [gRPC](https://grpc.io/) over HTTP, adding protocol-level phases such as MCP initialization, where client and server exchange their capabilities, on top of standard HTTP request/response semantics. The key aspects of agentic systems that require intermediaries to adapt include:

1. **Diverse enterprise governance imperatives.** The primary challenge is satisfying the wide spectrum of non-negotiable enterprise requirements for safety, security, data privacy, and regulatory compliance. These needs often go beyond standard network policies and require deep integration with internal systems, custom logic, and the ability to rapidly adapt to new organizational rules or external regulations. This demands a highly extensible framework where enterprises can plug in their specific governance models.
2. **Policy attributes live inside message bodies, not headers.** Unlike traditional web traffic where policy inputs like paths and headers are readily accessible, agentic protocols frequently bury critical attributes (e.g., model names, tool calls, resource IDs) deep within JSON-RPC or gRPC payloads. This shift requires intermediaries to possess the ability to parse and understand message contents to apply context-aware policies.
3. **Handling diverse and evolving protocol characteristics.** Agentic protocols are not uniform. Some, like MCP with Streamable HTTP, can introduce stateful interactions requiring session management across distributed proxies (e.g., using `Mcp-Session-Id`). The need to support such varied behaviors, along with future protocol innovations, reinforces the necessity of an inherently adaptable and extensible networking foundation.

These factors mean enterprises need more than just connectivity. The network must now serve as a central point for enforcing the crucial governance needs mentioned earlier. This includes providing capabilities like centralized security, comprehensive auditability, fine-grained policy enforcement, and dynamic guardrails, all while keeping pace with the rapid evolution of protocols and agent behaviors. Put simply, agentic AI transforms the network from a mere transit path into a critical control point.

### Why Envoy fits this shift

Envoy is a strong fit for agentic AI networking for three reasons. Envoy is:

- **Battle-tested.** Enterprises already rely on Envoy in high-scale, security-sensitive environments, making it a credible platform to anchor a new generation of traffic management and policy enforcement.
- **Extensible.** Envoy can be extended through native filters, Rust modules, WebAssembly (Wasm) modules, and [external processing](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter) patterns. That gives platform teams room to adopt new protocols without having to rebuild their networking layer every time the ecosystem changes.
- **Operationally useful today.** Envoy already acts as a gateway, enforcement point, observability layer, and integration surface for control planes. That makes it a practical choice for organizations that need to move now, not after the standards settle.

Building on these core strengths, Envoy has introduced specific architectural advancements to meet the unique demands of agentic networking:

#### 1\. Envoy understands agent traffic

The first requirement for agentic networking is simple: The gateway needs to understand what the agent is actually trying to do.

That’s harder than it sounds. In protocols such as MCP, A2A, and OpenAI-style APIs, important policy signals may live inside the request body. Traditional HTTP proxies are optimized to treat bodies as opaque byte streams. That design is efficient, but it limits what the proxy can enforce. For protocols that use JSON messages, a proxy may need to buffer the entire request body to locate attribute values needed for policy application — especially when those attributes appear at the end of the JSON message. Business logic specific to gen AI protocols, such as rate limiting based on consumed tokens, may also require parsing server responses.

Envoy addresses this by deframing protocol messages carried over HTTP and exposing useful attributes to the rest of the filter chain. The extensibility model for gen AI protocols was guided by two goals:

1. Easy reuse of existing HTTP extensions that work with gen AI protocols out of the box, such as RBAC or tracers.
2. Easy access to deframed messages for gen-AI-specific extensions, so that developers can focus on gen AI business logic without needing to deal with HTTP or JSON envelopes.

Based on these goals, new extensions for gen AI protocols are still built as HTTP extensions and configured in the HTTP filter chain. This provides flexibility to mix HTTP-native business logic, such as OAuth or mTLS authorization, with gen AI protocol logic in a single chain. A deframing extension parses the protocol messages carried by HTTP and provides an ambient context with extracted attributes, or even the entirety of parsed messages, to downstream extensions via well-known filter state and metadata values.

Instead of forcing every policy component to parse JSON envelopes or protocol-specific message formats on its own, Envoy makes those attributes available as structured metadata. Once the gateway has deframed protocol messages, existing Envoy extensions such as [ext\_authz](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter) or RBAC can read protocol properties to evaluate policies using protocol-specific attributes such as tool names for MCP, message attributes for A2A, or model names for OpenAI.

Access logs can include message attributes for enhanced monitoring and auditing. The protocol attributes are also available to the [Common Expression Language](https://cel.dev/) (CEL) runtime, simplifying creation of complex policy expressions in RBAC or composite extensions.

**Buffering and memory management  
**Envoy is designed to use as little memory as possible when proxying HTTP requests. However, parsing agentic protocols may require an arbitrary amount of buffer space, especially when extensions require the entire message to be in memory. The flexibility of allowing extensions to use larger buffers needs to be balanced with adequate protection from memory exhaustion, especially in the presence of untrusted traffic.

To achieve this, Envoy now provides a per-request buffer size limit. Buffers that hold request data are also integrated with the overload manager, enabling a full range of protective actions under memory pressure, such as reducing idle timeouts or resetting requests that consume the most memory for an extended duration. These changes pave the way for Envoy to serve as a gateway and policy-enforcement point for gen AI protocols without compromising its resource efficiency.

#### 2\. Envoy enforces policy on things that matter

Understanding traffic is only useful if the gateway can act on it.

In agentic systems, policy is not just about which service an agent can reach. It’s about which tools an agent can call, which models it can use, what identity it presents, how much it can consume, and what kinds of outputs require additional controls. Those are higher-value decisions than simple layer-4 or path-based controls, and they are exactly the kinds of controls enterprises care about when agents are allowed to take action on their behalf.

Envoy is well-positioned here because it can combine transport-level security with application-aware policy enforcement. Teams can authenticate workloads with mTLS and SPIFFE identities, then enforce protocol-specific rules with RBAC, external authorization, external processing, access logging, and CEL-based policy expressions.

This capability is crucial because it lets platform teams decouple agent development from enforcement. Developers can focus on building useful agents, while operators enforce a consistent zero-trust posture at the network layer, even as tools, models, and protocols continue to change.A prime example of this zero-trust decoupling is the critical "user-behind-agent" scenario, where an AI agent must execute tasks on a human user's behalf. Traditionally, handing user credentials directly to an application introduces severe security risks — if the agent is compromised or manipulated via prompt injection, an attacker could exfiltrate or misuse those credentials. By offloading identity management to Envoy, the proxy can automatically insert user delegation tokens into outbound requests at the infrastructure layer. Because the agent never directly holds the sensitive credential, the risk of a compromised agent misusing or leaking the token is completely neutralized, ensuring actions remain strictly bound to the user's actual permissions.

**Case study: Restricting an agent to specific GitHub MCP tools  
**Consider an agent that triages GitHub issues.

The GitHub MCP server may expose dozens of tools, but the agent may only need a small read-only subset, such as `list_issues`, `get_issue`, and `get_issue_comments`. In most enterprises, that difference matters. A useful agent should not automatically become an unrestricted one.

With Envoy in front of the MCP server, the gateway can verify the agent identity using SPIFFE during the mTLS handshake, parse the MCP message via [the deframing filter](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/http/mcp/v3/mcp.proto#envoy-v3-api-msg-extensions-filters-http-mcp-v3-mcp), extract the requested method and tool name, and enforce a policy that allows only the approved tool calls for that specific agent identity. RBAC uses metadata created by the MCP deframing filter to check the method and tool name in the MCP message:

```
envoy.filters.http.rbac:
```

```
"@type": type.googleapis.com/envoy.extensions.filters.http.rbac.v3.RBACPerRoute
```

```
rbac:
```

```
rules:
```

```
policies:
```

```
github-issue-reader-policy:
```

```
permissions:
```

```
- and_rules:
```

```
rules:
```

```
- sourced_metadata:
```

```
metadata_matcher:
```

```
filter: envoy.http.filters.mcp
```

```
path: [{ key: "method" }]
```

```
value: { string_match: { exact: "tools/call" } }
```

```
- sourced_metadata:
```

```
metadata_matcher:
```

```
filter: envoy.http.filters.mcp
```

```
path: [{ key: "params" }, { key: "name" }]
```

```
value:
```

```
or_match:
```

```
value_matchers:
```

```
- string_match: { exact: "list_issues" }
```

```
- string_match: { exact: "get_issue" }
```

```
- string_match: { exact: "get_issue_comments" }
```

```
principals:
```

```
- authenticated:
```

```
principal_name:
```

```
exact: "spiffe://cluster.local/ns/github-agents/sa/issue-triage-agent"
```

That’s the real value: Policy is enforced centrally, close to the traffic, and in terms that match the agent's actual behavior.

**Beyond static rules: External authorization  
**A complex compliance policy that can’t be expressed using RBAC rules can be implemented in an external authorization service using the [ext\_authz](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter) protocol. Envoy provides MCP message attributes along with HTTP headers in the context of the ext\_authz RPC. It can also forward the agent's SPIFFE identity from the peer certificate:

```
http_filters:
```

```
- name: envoy.filters.http.ext_authz
```

```
typed_config:
```

```
"@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
```

```
grpc_service:
```

```
envoy_grpc:
```

```
cluster_name: auth_service_cluster
```

```
include_peer_certificate: true
```

```
metadata_context_namespaces:
```

```
- envoy.http.filters.mcp
```

This allows external services to make authorization decisions based on the full combination of agent identity, MCP method, tool name, and any other protocol attributes, without the agent or the MCP server needing to be aware of the policy layer.

**Protocol-native error responses  
**When Envoy denies a request, the error should be meaningful to the calling agent. For MCP traffic, Envoy can use `local_reply_config` to map HTTP error codes to appropriate JSON-RPC error responses. For example, a 403 Forbidden can be mapped to a JSON-RPC response with `isError: true` and a human-readable message, ensuring the agent receives a protocol-appropriate denial rather than an opaque HTTP status code.

#### 3\. Envoy supports stateful agent interactions at scale

Not all agent traffic is stateless. Some protocols, including Streamable HTTP for MCP, can rely on session-oriented behavior. That creates a new challenge for intermediaries, especially when traffic flows through multiple gateway instances to achieve scale and resilience. An MCP session effectively binds the agent to the server that established it, and all intermediaries need to know this to direct incoming MCP connections to the correct server.

If a session is established on one backend, later requests in that conversation need to reach the right destination. That sounds straightforward for a single-proxy deployment, but it becomes more complicated in horizontally scaled systems, where multiple Envoy instances may handle different requests from the same agent.

**Passthrough gateway  
**In the simpler passthrough mode, Envoy establishes one upstream connection for each downstream connection. Its primary use is enforcing centralized policies, such as client authorization, RBAC, rate limiting, and authentication, for external MCP servers. The session state transferred between intermediaries needs to include only the address of the server that established the session over the initial HTTP connection, so that all session-related requests are directed to that server.

Session state transfer between different Envoy instances is achieved by appending encoded session state to the MCP session ID provided by the MCP server. Envoy removes the session-state suffix from the session ID before forwarding the request to the destination MCP server. This session stickiness is enabled by configuring Envoy's [`envoy.http.stateful_session.envelope`](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/http/stateful_session/envelope/v3/envelope.proto) extension.

**Aggregating gateway  
**In aggregating mode, Envoy acts as a single MCP server by aggregating the capabilities, tools, and resources of multiple backend MCP servers. In addition to enforcing policies, this simplifies agent configuration and unifies policy application for multiple MCP servers.

Session management in this mode is more complicated because the session state also needs to include mapping from tools and resources to the server addresses and session IDs that advertised them. The session ID that Envoy provides to the agent is created before tools or resources are known, and the mapping has to be established later, after the MCP initialization phases between Envoy and the backend MCP servers are complete.

One approach, currently implemented in Envoy, is to combine the name of a tool or resource with the identifier and session ID of its origin server. The exact tool or resource names are typically not meaningful to the agent and can carry this additional provenance information. If unmodified tool or resource names are desirable, another approach is to use an Envoy instance that does not have the mapping, and then recreate it by issuing a `tools/list` command before calling a specific tool. This trades latency for the complexity of deploying an external global store of MCP sessions, and is currently in planning based on user feedback.

This matters because it moves Envoy beyond simple traffic forwarding. It allows Envoy to serve as a reliable intermediary for real agent workflows, including those spanning multiple requests, tools, and backends.

#### 4\. Envoy supports agent discovery

Envoy is adding support for the A2A protocol and agent discovery via a well-known AgentCard endpoint. AgentCard, a JSON document with agent capabilities, enables discovery and multi-agent coordination by advertising skills, authentication requirements, and service endpoints. The AgentCard can be provisioned statically via direct response configuration or obtained from a centralized agent registry server via xDS or ext\_proc APIs. A more detailed description of A2A implementation and agent discovery will be published in a forthcoming blog post.

#### 5\. Envoy is a complete solution for agentic networking challenges

Building on the same foundation that enabled policy application for MCP protocol in demanding deployments, Envoy is adding support for OpenAI and transcoding of agentic protocols into RESTful HTTP APIs. This transcoding capability simplifies the integration of gen AI agents with existing RESTful applications, with out-of-the-box support for OpenAPI-based applications and custom options via dynamic modules or Wasm extensions. In addition to transcoding, Envoy is being strengthened in critical areas for production readiness, such as advanced policy applications like quota management, comprehensive telemetry adhering to [OpenTelemetry semantic conventions for generative AI systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/), and integrated guardrails for secure agent operation.

**Guardrails for safe agents  
**The next significant area of investment is centralized management and application of guardrails for all agentic traffic. Integrating policy enforcement points with external guardrails presently requires bespoke implementation and this problem area is ripe for standardization.

### Control planes make this operational

The gateway is only part of the story. To achieve this policy management and rollout at scale, a separate control plane is required to dynamically configure the data plane using the xDS protocol, also known as the universal data plane API.

That is where control planes become important. Cloud Service Mesh, alongside open-source projects such as [Envoy AI Gateway](https://aigateway.envoyproxy.io/) and [kube-agentic-networking](https://github.com/kubernetes-sigs/kube-agentic-networking), uses Envoy as the data plane while giving operators higher-level ways to define and manage policy for agentic workloads.

This combination is powerful: Envoy provides the enforcement and extensibility in the traffic path, while control planes provide the operating model teams need to deploy that capability consistently.

### Why this matters now

The shift towards agentic systems and gen AI protocols such as MCP, A2A, and OpenAI necessitates an evolution in network intermediaries. The primary complexities Envoy addresses include:

- **Deep protocol inspection.** Protocol deframing extensions extract policy-relevant attributes (tool names, model names, resource paths) from the body of HTTP requests, enabling precise policy enforcement where traditional proxies would only see an opaque byte stream.
- **Fine-grained policy enforcement.** By exposing these internal attributes, existing Envoy extensions like RBAC and ext\_authz can evaluate policies based on protocol-specific criteria. This allows network operators to enforce a unified, zero-trust security posture, ensuring agents comply with access policies for specific tools or resources.
- **Stateful transport management.** Envoy supports managing session state for the Streamable HTTP transport used by MCP, enabling robust deployments in both passthrough and aggregating gateway modes, even across a fleet of intermediaries.

Agentic AI protocols are still in their early stages, and the protocol landscape will continue to evolve. That’s exactly why the networking layer needs to be adaptable. Enterprises should not have to rebuild their security and traffic infrastructure every time a new agent framework, transport pattern, or tool protocol gains traction. They need a foundation that can absorb change without sacrificing control.

Envoy brings together three qualities that are hard to get in one place: proven production maturity, deep extensibility, and growing protocol awareness for agentic workloads. By leveraging Envoy as an agent gateway, organizations can decouple security and policy enforcement from agent development code.

That makes Envoy more than just a proxy that happens to handle AI traffic. It makes Envoy a future-ready foundation for agentic AI networking.

---

<sup>Special thanks to the additional co-authors of this blog: Boteng Yao, Software Engineer, Google and Tianyu Xia, Software Engineer, Google and Sisira Narayana, Sr Product Manager, Google.</sup>