---
title: "Agentic AI Governance: How to Approach It"
source: "https://securityboulevard.com/2026/04/agentic-ai-governance-how-to-approach-it/"
author:
  - "[[Rhys Campbell]]"
published: 2026-04-01
created: 2026-04-13
description: "Simulators don’t just teach pilots how to fly the plane; they also teach judgment. When do you escalate? When do you hand off to air traffic control? When do you abort the mission? These are human decisions, trained under pressure, and just as critical as the technical flying itself. The post Agentic AI Governance: How to Approach It appeared first on Strata.io."
tags:
  - "clippings"
---
[LinkedIn](https://securityboulevard.com/#linkedin "LinkedIn") [Reddit](https://securityboulevard.com/#reddit "Reddit") [Email](https://securityboulevard.com/#email "Email")

[Security Bloggers Network](https://securityboulevard.com/category/sbn/)

![SBN](https://securityboulevard.com/wp-content/uploads/2017/09/SBNIcon4_512px.png)

## Key Takeaways

- **AI agents operate in the shadows** Nearly 70% of enterprises already run agents in production, but most operate outside the reach of traditional IAM controls making them invisible, overprivileged, and unmanaged.
- **Your existing IDP won’t save you** Login-time decisions, session-based trust, and single-vendor governance don’t map to agents that are ephemeral, autonomous, and operate across trust boundaries at machine speed.
- **An identity control plane is the architectural answer** A vendor-neutral layer above your identity infrastructure that enforces policy at runtime—regardless of which IDP issued the credentials or which cloud the agent runs in.
- **Strata’s AI Identity Gateway secures every agent tool call** The AI Identity Gateway issues task-specific ephemeral tokens (5-second TTLs) and provides full delegation chain visibility, MCP-native enforcement, and OPA-based authorization—with zero changes to upstream services.
- **The OWASP MCP Top 10 provides a concrete benchmark** Strata’s published self-attestation mapping at docs.strata.io shows exactly which risks the gateway directly addresses and where complementary controls are needed.
- **The regulatory clock is ticking** EU AI Act enforcement begins in August 2026. Organizations that treat agentic identity as a first-class security concern now will be the ones who can continue to deploy agents safely at scale.

There’s a new employee at every company I talk to. It never sleeps, it never asks for permission twice, and nobody in security knows its name.

The cybersecurity industry has a term for this kind of risk: identity dark matter—access that exists outside your governance fabric, powerful, invisible, and unmanaged. For years, that meant orphaned service accounts, stale API keys, and forgotten local admin credentials. Now it means AI agents. Strata and the Cloud Security Alliance (CSA) surveyed 285 IT and security professionals and found that nearly 70% of enterprises are already running AI assistants or agents in production, with another 23% planning deployments this year. Two-thirds are building their agents in-house and within private data center environments. Yet we found that only 18% of respondents were confident their current IAM systems can manage agent identities effectively.

So let me talk to you the way I’d talk to a peer over coffee: the identity infrastructure most of us inherited was never built for this. These agents don’t join or leave through HR. They don’t submit access requests. They’re optimized to finish the job with minimal friction—fewer approvals, fewer prompts, fewer blockers. In identity terms, that means they’ll gravitate toward whatever already works: in-app local accounts, stale service identities, long-lived tokens, bypass auth paths. If it works, it gets reused. And that’s how AI agents become the fastest-growing source of identity dark matter in the enterprise.

## The Numbers Should Scare You

The CSA+Strata survey paints a sobering picture. For all of the organizations that already have agents in production, nearly half are authenticating them with static API keys or username/password combinations. Only 11% have fully implemented runtime authorization policy enforcement.

What makes agentic AI different from previous identity challenges isn’t just scale. It’s behavior. Agents are autonomous systems optimized for efficiency. They don’t understand your org chart or your governance intent; they understand what works. The typical abuse pattern follows a predictable sequence. The agent enumerates what exists, tries whatever is easiest first, locks onto “good enough” access, and then upgrades quietly. And in the process they find over-scoped tokens, stale entitlements, or dormant-but-privileged identities. All at machine speed, across hybrid environments, too fast for humans to spot early enough to control.

Leading industry analysts expect the vast majority of unauthorized agent actions will stem from internal enterprise policy violations. This means misguided AI behavior or information oversharing rather than malicious external attacks. The breach won’t start with a zero-day. It will start with an identity shortcut someone forgot to clean up, then get amplified by agentic automation until it looks like a systemic compromise.

## Why Your Current IDP Won’t Save You

I’ve evaluated the approaches on the market, and they generally fall into two camps. Neither of which fully solves the problem.

The first camp is major identity providers extending their platforms to cover agents as another identity type. They bring scale, but also architectural assumptions from the era of human SSO. Login-time decisions and session-based trust don’t map to entities that spin up for a single task, delegate to sub-agents, cross trust boundaries, and vanish. More critically, native platform controls and vendor safeguards generally do not extend beyond their own cloud or platform borders. When your agent population scales to tens of thousands, per-seat licensing tied to a single vendor becomes a real flexibility problem. Worse, cross-cloud agent interactions remain entirely ungoverned.

The second camp treats agents as another flavor of non-human identity (NHI). Think “souped-up service accounts managed through lifecycle workflows”. Provisioning identities with scoped permissions, assigning human owners, enforcing credential rotation, and decommissioning agents when they’re done is necessary but not sufficient. A dormant agent identity can persist quietly for months, creating exactly the kind of entry point attackers love. You need lifecycle governance, but you also need runtime enforcement alongside it, because the most dangerous moment isn’t when an agent is provisioned or retired. It’s every second in between.

We’ve seen the recent concept of specialized “guardian agents”—supervisory AI solutions that continuously evaluate, monitor, and enforce boundaries on working agents. The concept is sound, but it raises a foundational question: what identity infrastructure do those guardian agents themselves run on? If the answer is the same single-vendor IDP that can’t govern the working agents, you’ve just added a layer of automation to an architectural problem.

## What Changed My Thinking: The Identity Control Plane

After working through these options, I landed on a different architectural approach—and full transparency, it’s what we’re building at Strata with the Maverics platform. But the design principle matters more than the vendor, so take the pattern even if you never talk to us.

You can’t solve agentic identity by bolting features onto any single IDP. You need a layer above your identity infrastructure that enforces policy at runtime, regardless of which provider issued the credentials, which cloud the agent runs in, or which protocol the upstream service expects. This Identity Control Plane is the independent oversight mechanism that analysts like Gartner identify as essential, but implemented at the identity layer, where it can govern every agent interaction consistently across hybrid environments.

## How Strata’s AI Identity Gateway Eliminates Agent Dark Matter

Strata’s AI Identity Gateway operates as a runtime enforcement proxy in the Model Context Protocol (MCP) path. MCP is the emerging standard for how agents discover and invoke tools. The gateway was built from the ground up to be the governance layer that sits above your entire identity infrastructure. Here’s how it directly addresses each dimension of the agentic identity problem.

**Every agent action traces back to a human sponsor.** The AI Identity Gateway implements OAuth 2.0 token exchange with delegation semantics. When an agent calls a tool, the downstream token carries both the agent’s identity and the delegating user’s identity via an “act” claim. If the human changes roles or leaves, the agent’s access changes with them. No orphaned agent identities. No dark matter.

**Per-task ephemeral credentials eliminate privilege drift.** Every tool invocation gets a fresh, minimal-privilege token that expires in seconds—typically a 5-second TTL. A “listUsers” call gets a token with only user:List scope. A “createEmployee” call moments later gets a completely different token with employee:Create scope. No token accumulates permissions, and no token outlives its task. This is implemented through RFC 8693 token exchange, which means the privilege drift that creates identity dark matter is architecturally impossible.

**Vendor-neutral governance across hybrid environments.** The Maverics AI Identity Gateway connects to your existing identity fabric through connectors that abstract protocol details—Entra ID, Active Directory, Okta, PingFed, Keycloak, LDAP directories. Different protocols, different vendors, different eras of technology, all unified behind a single governance layer.

**MCP-native enforcement with zero upstream changes.** The AI Identity Gateway speaks MCP natively, operating as both an MCP Bridge (auto-generating tool catalogs from existing OpenAPI specs so agents can discover and call REST APIs) and an MCP Proxy (adding authentication and authorization to existing MCP server connections). OPA policies evaluate every tool invocation with access to the full MCP context before any request reaches upstream. These include tool name, arguments, agent identity, delegating user. Agents discover available tools through standards-based OAuth discovery (RFC 9470), requiring no pre-configuration.

**Token minting governance as an independent control point.** Beyond inbound OPA policies, the Auth Provider AI Identity Gateway can apply OPA-based token minting policies during token exchange. Even if an inbound policy allows a tool call, the Auth Provider can refuse to mint the token based on agent identity, requested scopes, audience, or delegating user attributes. This dual-layer authorization means governance decisions are enforced at two independent checkpoints.

**Full audit trails that satisfy compliance today.** Every tool invocation is logged with the complete identity context: which agent, which user delegated authority, which tool was invoked, what parameters were passed, and what result was returned. Structured JSON output via OTEL integrates directly with your SIEM. When auditors ask who approved access, who used it, and what data was touched, identity dark matter makes those answers slow or impossible. The gateway makes them immediate.

## Mapping to the OWASP MCP Top 10

The OWASP MCP Top 10 is the first authoritative catalog of security risks specific to Model Context Protocol deployments. Strata’s published mapping at docs.strata.io/guides/ai-identity/owasp-mcp-top-10 shows exactly how the AI Identity Gateway addresses each risk:

The gateway directly addresses token mismanagement (MCP01) through per-tool token exchange with short-lived scoped tokens; insufficient authentication and authorization (MCP07) through multi-layer auth with deny-by-default OPA policies; and lack of audit (MCP08) through complete identity-context logging. It reduces the attack surface for privilege escalation (MCP02), tool poisoning (MCP03), supply chain attacks (MCP04), command injection (MCP05), and shadow MCP servers (MCP09). For risks targeting the AI model layer, including intent flow subversion (MCP06) and context injection (MCP10), the gateway limits blast radius and enables detection, but prevention requires complementary controls at the model and application layers.

That transparency about coverage boundaries matters. The vendors who claim to solve everything are the ones who solve nothing well.

## A Scenario That Makes This Real

A developer clones a trending open-source AI assistant. The AI assistant manages files, automates tasks, sends messages. What they don’t realize is that the system prompt has been poisoned. The agent harvests credentials from config files and API tokens from environment variables, then uses communication tools to propagate itself to colleagues. This is identity dark matter in action: the agent uses whatever works, be it orphaned accounts, over-scoped tokens, stale credentials, as the fastest path to completion.

With traditional controls, this is devastating considering it uses valid credentials, legitimate machine, authorized-looking traffic. With the AI Identity Gateway in the path, harvested credentials are useless because tokens are ephemeral and task-scoped. Lateral movement is neutralized because the gateway evaluates each action against policy in real time, and every action requires a fresh delegation token tied to a specific human sponsor. The dark matter the virus is looking for doesn’t exist.

## From One CISO to Another

Here are the recommendations I’d share with any peer grappling with this right now.

**Treat agents as a distinct identity category.** They’re not faster humans and they’re not smarter scripts. They need authorization at runtime, not just at login.

**Kill long-lived, broad-scope credentials.** Every token should be task-scoped and short-lived. If that feels painful, you need an Identity Control Layer handling it automatically.

**Insist on vendor neutrality.** The agentic ecosystem is multi-cloud, multi-IDP, and multi-framework. Any solution that requires consolidating onto one identity provider is creating, not eliminating, governance blind spots.

**Own agent lifecycle management end-to-end.** Every agent needs a documented human owner, scoped permissions, and explicit decommissioning criteria. Abandoned agent identities carry the same risk profile as an unpatched server.

**Benchmark against the OWASP MCP Top 10.** Map your controls against it and you’ll see where the gaps are.

**Make every agent action auditable.** Every tool invocation should log the agent, the delegating user, the tool, and the result. This isn’t just compliance—it’s your forensic lifeline.

## The Window Is Closing

Seventy percent of organizations expect to manage hundreds of agents within the next year, and the EU AI Act enforcement starts August 2026 with fines up to €35 million. In practice, most AI agent incidents won’t start with a zero-day. Instead, they’ll start with an identity shortcut someone forgot to clean up, then get amplified by automation until it appears to be a systemic breach.

If identity dark matter is the sum of what we can’t see or control, then unmanaged AI agents are its fastest-growing source. At Strata, we’re building the identity infrastructure to eliminate that dark matter. Maverics makes every agent identity visible, governed, and auditable, regardless of which cloud it runs in or which vendor issued its credentials.

The organizations that treat agentic identity as a first-class security concern will deploy agents safely at scale. The rest will learn that speed without governance isn’t innovation. It’s exposure.

*Rhys Campbell is the CISO at Strata Identity, where he builds security programs that enable business growth. Learn more at strata.io and explore the Maverics Agentic Identity Sandbox at maverics.ai/labs.*

The post [Agentic AI Governance: How to Approach It](https://www.strata.io/blog/agentic-identity/agentic-ai-governance-how-to-approach-it/) appeared first on [Strata.io](https://www.strata.io/).

,