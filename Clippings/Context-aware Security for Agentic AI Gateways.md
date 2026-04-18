---
title: "Context-aware Security for Agentic AI Gateways"
source: "https://www.solo.io/blog/context-aware-security-ai-gateways"
author:
published: 2025-12-19
created: 2026-04-13
description: "Learn why agentic systems require context-aware gateways to secure and route LLM, MCP, inference, and agent traffic across modern platforms."
tags:
  - "clippings"
---
## "Legacy" proxies

Most network proxies - whether NGINX, HAProxy or even the relatively more modern Envoy Proxy - were all built before the age of AI.

For proxies to be effective in the context of agentic networking flows, they must be context-aware: is the target "backend" workload an MCP server? An agent? Or perhaps some other type of artifact?

In order to be able to implement proper security controls, or to perform any of the functions that proxies are known for (rate limiting, observability, routing), this context-awareness not only matters, it's necessary.

Solo.io created the [agentgateway](https://agentgateway.dev/) project precisely for this reason: to build into a proxy the necessary context-awareness that allows it to properly handle network flows, not only for traditional microservices traffic, but also for modern "agentic" flows.

## AI use cases

AI use cases are categorized along the following lines:

1. **LLM consumption** - In the context of internal applications making calls to LLMs, agentgateway can proxy requests to outbound providers and their models. agentgateway supports a variety of LLM consumption use cases out of the box: credential management, prompt enrichment, prompt guards, rate limiting, model failover, and more. In this capacity, agentgateway acts as an egress gateway: workloads running inside an organization's environment (be it on-prem or in the cloud) makes calls to an external LLM. The proxy is in a position to mediate calls to external LLMs and can add value in many different ways, whether it be to audit outbound requests, enrich prompts, mask content from the LLMs responses, or fail over to another model.
1. **Inference consumption** - Hosting Large Language Models internally on-premises and intelligently routing requests to the correct model. In this capacity, agentgateway acts as a context-aware ingress gateway, controlling and routing traffic to the target models running on premises. agentgateway can make intelligent decisions relating to how to route incoming requests to the appropriate model, taking into account token consumption, session awareness, response times, and model capabilities.
1. **Development of agentic systems** - A variety of agentic artifacts are brought to bear to deploy a system of collaborating actors: agents, agent skills, MCP servers, and LLMs, with a possible mix of on-prem and off-premises actors. In this context, agentgateway can act as a proxy that controls the intelligent routing of traffic, as a way of collecting and emitting telemetry information for observability, and as a policy enforcement point for security. In this capacity, the role of agentgateway more closely matches what we traditionally think of as service mesh traffic.

### Agentic flows - the new kid on the block

The process of interacting with LLMs has evolved significantly over the last twelve months. Today when we interact with an LLM, we may not realize that we do so in the context of agents that mediate the communication with the user and with other actors. The LLM itself becomes one component in a larger system involving multiple actors: the LLMs, agents, and MCP servers.

The agent is not only a service fronting the LLM, but it also acts as a mediator between LLMs and tools. The algorithm goes something like this:

1. The agent informs the LLM of the tools that are at its disposal, how to call them, and how to parse their responses.
2. The LLM can request of the agent that specific tool invocations be performed.
3. The agent in turn will proxy the calls to the tools and relay the responses to the LLM.
4. The LLM is at liberty to repeat the above tool calling process as many times as necessary until it is satisfied it can provide the user an answer to their questions.
5. Ultimately, the LLM prepares an answer that is informed by, and that incorporates the tool call responses, and forwards the reply to the agent.
6. The agent relays the final reply to the end user.

The above is also known as the "agentic loop".

![](https://cdn.prod.website-files.com/6704482c45ef6ead081645ff/6941bf48fbd9c0afe0349853_9cac8261.png)

The agentic loop

In the enterprise, the construction and deployment of specialized agents making calls to tools and to LLMs is becoming commonplace. Enterprise workloads are becoming a mix of the traditional microservices workloads and these new agentic workloads.

## The agentgateway project

Agentgateway was designed to support the above variety of AI scenarios: LLM Consumption, inference consumption, and agentic flows.

The "story" of the genesis of the agentgateway project at Solo.io is worth summarizing. Engineering was initially trying to bolt security controls and other canonical proxy capabilities for agentic use cases on top of Envoy proxy. It quickly became clear that the recipe of programming the Envoy proxy was not going to work for AI scenarios, for a multiplicity of reasons.

For example, in order to provide the ability to specify a sensible security policy for calling MCP tools, we must expose contextual information, such as the name of the tool being invoked. In order to do that, the proxy had to become MCP-protocol aware. The end result was the creation of a new, AI-native, [Rust](https://rust-lang.org/) -based proxy named agentgateway, one that natively understands the MCP and A2A protocols which are used in agentic network communications.

Besides its ability to natively understand this new crop of AI-native protocols, agentgateway is significantly more performant both in terms of memory and CPU resources, in comparison to market alternatives. For more details on this front, see John Howard's [Gateway API benchmarks, part 2](https://github.com/howardjohn/gateway-api-bench/blob/main/README-v2.md).

## Example: MCP authorization

In the context of an agent calling tool via the MCP protocol, we need the ability to make decisions based not only on the caller and their identity, but also on the tool being targeted -- we need a context-aware proxy.

Agentgateway integrates the [Common Expression Language](https://cel.dev/) (CEL) and exposes contextual information which an operator can use to express their desired policy.

See [this MCP authorization example](https://agentgateway.dev/docs/mcp/mcp-authz/) from the project's documentation.

In the example, the expression configures the proxy with an authorization policy that can inspect not only the subject from a JWT token in the request, but also the MCP tool that is being targeted in the call.

## How mesh complements security posture in an agentic context

We're familiar with using [ambient mesh authorization policies](https://ambientmesh.io/docs/security/waypoint-authz/) to enforce requests through a waypoint.

When agentgateway proxies an MCP server (or multiple MCP servers: see [MCP server multiplexing](https://agentgateway.dev/docs/mcp/connect/multiplex/)) for workloads running atop an ambient mesh, these same kinds of authorization policies ensure that no clients can circumvent the agentgateway - that all calls to the tool servers go through the agentgateway.

John Howard's blog post [Your AI workloads still need a service mesh](https://blog.howardjohn.info/posts/ai-mesh/) comes to mind.

## Baking agentgateway into Solo.io's products

Solo.io today is embedding agentgateway into many of its products to unlock not only traditional proxy capabilities, but also all of the new agentic flows that are the focus of so many of today's development efforts.

Agentgateway can be consumed in a variety of ways:

1. **Standalone** - The [documentation on agentgateway.dev](https://agentgateway.dev/docs/) shows you how to download and install the agentgateway binary, and how to program it for a variety of both traditional and agentic use cases. agentgateway is lean and mean, the binary is lightweight, it has lightning-fast performance, and sports a beautiful administrative UI, with a built-in client inspector.
1. **In Kubernetes** - Integration is provided through the open-source CNCF project [kgateway.dev](https://kgateway.dev/docs/agentgateway/latest) whereby kgateway acts as a control plane that allows the configuration of proxies through the Kubernetes Gateway API. Via the GatewayClass agentgateway, kgateway can be made to provision agentgateway instances and program them accordingly for a variety of use cases.
1. **Service mesh** - Solo.io's products now support the ability to use agentgateway (in lieu of Envoy proxy) as the implementation of the waypoint used to provision Layer 7 proxies in front of designated services. [Solo.io](http://solo.io/) often uses the term "Layer 8" with respect to agentgateway because it goes beyond the traditional HTTP layer concerns with its native support for the MCP and A2A protocols (the AI layer).

For enterprise users, Solo.io recently released [Solo Enterprise for agentgateway](https://docs.solo.io/gateway/2.0.x/ai/about/), providing full support for "AI connectivity, security, governance for agents, tools, LLMs, and inference workloads." In addition, [Solo Enterprise for kagent](https://docs.solo.io/kagent-enterprise/) offers a version of Solo's agentic AI solution for Kubernetes that runs on top of a multicluster service mesh with agentgateway "baked in" to secure, observe, and control network communications for agents.

Solo.io has effectively extended its suite of networking products and their capabilities to now encompass AI use cases. Whether it is to control, secure, and observe applications calling out to external LLM providers (egress), routing incoming traffic to hosted LLM inference models intelligently, or working with full-fledged agentic solutions involving agents, MCP servers, and agent skills. Solo.io's new AI-native proxy, agentgateway, was built specifically to enable these use cases.