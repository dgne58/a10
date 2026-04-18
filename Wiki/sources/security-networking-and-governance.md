# Security, Networking, and Governance

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Overview
- Agentic systems become risky at runtime, not only at prompt time.
- This theme supports the governance and control story around the demo.
- The major shared idea across the sources is that agent traffic is no longer just ordinary application traffic; policy-relevant attributes often sit inside protocol payloads and execution loops.

## Core Risk Model
- Agents operate across trust boundaries.
- They can:
  - invoke tools
  - traverse multiple systems
  - accumulate state
  - act with credentials
- The central danger is not merely "bad output text." It is unintended or poorly governed action.

## Trust Boundaries

The corpus becomes easier to operationalize when its controls are grouped by trust boundary:

| Boundary | Example crossing | Why it matters |
| --- | --- | --- |
| user -> app | raw prompt enters system | prompt injection and identity ambiguity begin here |
| app -> model | prompt and context leave the app boundary | data leakage and hallucination risk |
| app -> MCP / external system | tool call reaches a separate capability owner | auth, approval, and data egress concerns |
| agent -> agent | delegated or nested execution | attribution and scope attenuation become hard |
| runtime -> memory | result or artifact is written back | persistence and poisoning risks |

This boundary view helps explain why prompts alone are not enough: the risky transitions happen between systems and identities, not just inside one message.

## Security Layers Emerging From The Sources

### Identity
- Which workload or agent is making the request?
- Which user, if any, is delegated behind the agent?

### Authorization
- Which tools, resources, or actions may that identity invoke?
- What requires approval or denial?

### Observability
- What happened, in what order, with what rationale and outcome?

### Runtime containment
- How do credentials expire?
- How is blast radius bounded if an agent or prompt path goes wrong?

## Why Networking Matters
- Traditional proxies often inspect headers and paths but not domain-specific semantics buried in message bodies.
- Agentic protocols and model APIs frequently encode the most important policy attributes inside payloads:
  - MCP tool names and parameters
  - model name choices
  - agent-to-agent capability metadata

This is why the gateway sources emphasize protocol awareness and deframing.

## Governance Patterns Supported By The Corpus

### Least privilege
- Agents should only receive the minimum capability set for the current task.

### Short-lived credentials
- Runtime-issued or task-scoped credentials reduce blast radius.

### Approval for high-risk actions
- A human checkpoint is acceptable and often desirable for destructive or externally visible steps.

### Auditability
- Decision logs and tool-call traces are part of the product, not just operations overhead.

### Data loss prevention
- Runtime governance is not only "who may call which tool."
- It also includes controlling which data may leave a trusted environment, especially into public AI systems, SaaS tools, chat surfaces, and browser-based agent flows.

### Workload identity
- The system should be able to distinguish:
  - human user identity
  - orchestrator / service identity
  - agent identity
  - tool-server identity
- This is especially important when an agent acts on behalf of a user instead of as the user.

## Identity And Delegation For Agents

The new access-management whitepaper adds a more concrete identity model for agents:

- Existing OAuth 2.1 patterns work reasonably well for simple synchronous agent scenarios inside one trust domain.
- The hard cases are:
  - cross-domain agent execution
  - asynchronous agents acting after the original user is gone
  - agents acting for multiple humans at once
  - recursive delegation from agent to sub-agent
  - browser / computer-use agents that bypass ordinary API-centric consent models

### Strategic implications
- Avoid treating an agent as an indistinguishable impersonation of a human user.
- Prefer explicit delegated authority with:
  - task-scoped permissions
  - attributable agent identity
  - clear "on-behalf-of" semantics
- Expect identity fragmentation if every vendor invents its own agent auth pattern.

### Hackathon minimum
- Distinguish:
  - end user identity
  - orchestrator / worker identity
  - tool or MCP server identity
- Record the delegated scope in traces when a tool call is made on behalf of a user.

## Runtime Control Stack

One helpful synthesis across the sources is a stacked control model:

### Input controls
- input normalization
- prompt separation
- trusted / untrusted data labeling

### Capability controls
- tool allowlists
- server exposure boundaries
- delegated scope enforcement

### Data-flow controls
- DLP
- redaction
- outbound-channel restrictions

### Action controls
- approval
- deny rules
- rate limits
- scoped credentials

### Evidence controls
- audit traces
- provenance
- evaluation and review records

Each layer catches a different failure mode. Removing any one layer creates a predictable hole.

## DLP As A Runtime Control

Data loss prevention (DLP) is a direct match for agentic systems because prompts and tool outputs often carry confidential material.

### Threats DLP helps reduce
- insider data exfiltration
- accidental disclosure through copy/paste or file upload
- external theft after compromise
- confidential data being pasted into public LLMs

### Detection mechanisms
| Mechanism | Use |
| --- | --- |
| fingerprinting / exact match | detect known protected files |
| keyword matching | block known sensitive phrases |
| pattern matching | catch structured secrets, PII, account numbers |
| file hash matching | identify protected binary or document copies |

### Relevance to this repo
- A policy gateway for AI or MCP traffic should be able to express outbound data controls, not just inbound auth checks.
- "Do not paste production secrets into external tools" is not a policy unless enforcement exists.
- DLP is one of the cleanest ways to show that the system governs both actions and data flow.

## Hackathon Interpretation
- The project does not need enterprise-complete governance.
- It does need to show that tool execution is constrained and observable.
- A credible minimum is:
  - per-tool allowlist or policy metadata
  - audit log
  - one manual-approval branch for high-risk actions
  - clear statement of trust boundaries

## Practical Design Patterns

### Explicit on-behalf-of semantics
- Never let the system quietly collapse agent identity into user identity.
- Trace should show both actor and delegated principal when they differ.

### Default-deny on destructive externals
- publish, delete, transfer, or irreversible mutation should not be the default path

### DLP before public model egress
- the cheapest strong control is often preventing sensitive data from leaving the trust boundary in the first place

### Short-lived credentials plus logs
- strong control is a combination of limited blast radius and post-hoc accountability

## Constraints And Failure Modes
- security scope can swallow the entire hackathon if left unconstrained
- a purely narrated policy story is weak if no runtime evidence exists
- long-lived broad credentials undermine the whole security thesis
- policy only in prompts is not sufficient

## Sources Included
- `Context-aware Security for Agentic AI Gateways.md`
- `The case for Envoy networking in the agentic AI era.md`
- `Establishing Runtime Security for Agentic AI.md`
- `Agentic AI Governance How to Approach It.md`
- `Envoy AI Gateway.md`
- `Envoy AI Gateway 1.md`
- `Supported AI Providers  Envoy AI Gateway.md`
- `What Is Envoy Proxy Concepts, Architecture & Use Cases  Solo.io.md`
- `Load Balancing Solutions for Availability & Security.md`
- `What is data loss prevention (DLP).md`
- `PDF to Markdown 1.md` (AI agents + identity / authorization whitepaper extract)

## Related Topics
- [[agentic-security-notes]]
- [[a10-product-notes]]
- [[envoy-gateway-notes]]
- [[infrastructure-security]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../components/policy-gateway|Policy Gateway]]
- [[../components/envoy-ai-gateway|Envoy AI Gateway]]
- [[../components/mcp-control-plane|MCP Control Plane]]
