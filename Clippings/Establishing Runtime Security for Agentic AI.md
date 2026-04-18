---
title: "Establishing Runtime Security for Agentic AI"
source: "https://www.ibm.com/think/insights/agentic-ai-runtime-security"
author:
  - "[[Shalini Harkar]]"
published:
created: 2026-04-13
description: "The shift from Generative AI - generating text to Agentic AI - taking action requires a total rethink of our defense posture. We can no longer treat AI as an isolated sandbox; we must treat it as a participant in our most critical infrastructure."
tags:
  - "clippings"
---
## From autonomy to unpredictability

[Agentic AI](https://www.ibm.com/think/topics/agentic-ai) systems, built on complex agentic architectures, are not just autonomous; their complex functions are also becoming unpredictable in operations, posing new challenges for agentic AI security. The real challenge is that agents are becoming unpredictable in their operation because of context, tools and interactions in ways that you didn’t even design. You are no longer managing static systems. You are now managing dynamic decision loops. And that’s when the risk begins to compound.

## The unpredictable action loop

Agentic AI brings a new model of operation, where control is not fully defined. At run time, the agent’s operation is a continuous cycle of reasoning, deciding, executing and adapting. And each step along the way expands the possibilities.

Therefore, a simple action can rapidly expand into:  

1. Tool orchestration across systems.
2. Dynamic data access, not limited to the initial scope.
3. Emergent decisions.
4. Dynamic creation of tasks or agents.

The cycle doesn’t stop—it compounds. Traditional systems have workflows. Agentic AI creates them. The risk is not an individual action but how decisions build up and change. What was once harmless can change into unintended outcomes—not because it fails, but because it adapts. With real-time context and multi-agent interactions, behavior is fluid and difficult to control. This is the unpredictable action cycle.  
  

## Agentic threats beyond your design

Agentic AI systems introduce a distinct runtime risk profile. Unlike static AI models, risk emerges during execution—when decisions are made, tools are invoked and state evolves dynamically. Key runtime security risks include:

- Agents act with real permissions, like API, database or execution layers. If permissions are too broad or intent is misunderstood, the agents perform the right actions but in the wrong context, like deleting data or initiating transactions. The risk is not from unauthorized access, but from uncontrolled power.
- Agents are constantly consuming information and use that information to decide on what actions to take next. If untrusted data isn’t separated from decision logic, it stops being input and starts driving behavior. The moment observation becomes control, things break.
- As agents become more autonomous, they begin to influence the manner in which the objectives are being pursued. Over time, they begin to drift from their original intent, driven by feedback loops or shortcuts. It looks intelligent, but it’s misalignment in motion.

## A2AS: The HTTPS moment for agentic AI

We can no longer consider AI to be an entity that is contained within its own sandbox. There is a need to totally rethink our defense posture. We must consider it to be a participant within our most critical infrastructure.

The Agentic AI Runtime Security and Self Defense framework—A2AS is like the “HTTPS for the AI world.” It is intended to be a standardized, lightweight and scalable construct that is necessary for this future. We can now create agents that are high performance and “secure by design.”

A2AS is based on five foundational control elements that together allow for secure and predictable agent behavior to be enabled:

- **Behavior certificates**: Define what agent behaviors are permissible.
- **Authenticated prompts**: Validate what is entering an agent.
- **Security boundaries**: Identify what is trustworthy and what is not trustworthy.
- **In-context defenses**: Direct agent behaviors to reject untrustworthy input.
- **Policies**: Enforce business logic.

These elements all come together to allow for a defense-in-depth approach to agentic AI systems. “Security is not an afterthought but is integral to how agents think and behave.”

## Architecting core runtime defenses

The threat landscape has moved beyond simple direct prompt injections toward complex, indirect manipulation and autonomous privilege escalation.  
Securing agentic systems requires controls embedded across four critical layers of execution:

### Perception layer

**Input and context sanitization:** Validating inputs and user context before the agent. This level involves the integration of an identity provider (IdP) like [IBM Verify](https://www.ibm.com/new/product-blog/agentic-ai-meets-identity-security-with-ibm-verify-identity-protection) by using OAuth 2 specifications to securely authenticate the human user before the agentic flow. This method provides the necessary identity context combined with deterministic filters and models for detecting user intent, allowing for the separation of external inputs by using well-defined boundaries to prevent prompt injection.

### Reasoning layer

**Semantic firewalls:** Monitor how the agent thinks, not just what it outputs. Detect manipulation through reasoning patterns and block actions that deviate from intended goals.

### Action layer

- **Execution interceptors:** Limit the abilities of an agent when they interact with external databases or services, and integrate a control plane that addresses two major shifts in security paradigms for agents working with external systems and services.
- **Dynamic credentials:** Eliminate the huge security risk associated with static API keys, by using a system like [Vault](https://www.ibm.com/docs/en/security-qradar/security-qradar-soar/saas?topic=managers-hashicorp-vault) to provide on-demand, dynamic credentials. These credentials are time-based and automatically revoked at the end of their session, in essence, giving true “least privilege access” only when executing.
- **Client-initiated backchannel authentication:** When high-risk operations are being performed, authenticate the user’s action by requiring them to authenticate out-of-band. This authentication is accomplished by stopping the agent’s ‘process’ and sending the user a secure request through their mobile device by using your IdP. This process is done so that if the agent’s ‘logic’ is compromised, they cannot act without user authorization and verification.

### Memory layer

**State protection:** Secure long-term context. Track data provenance, prevent memory poisoning and enable rollback to trusted states when anomalies occur.

## Runtime security unlocks exponential ROI

[Agentic AI security](https://www.ibm.com/think/topics/ai-agent-security) in runtime is not a friction point in the world of agentic AI—it is the primary driver of scale and business value. This is because continuous in-loop security delivers exponential returns through:

- **Accelerated deployment velocity:** Acceleration of AI deployments from a virtual, ‘sandboxed’ environment in which AI is deployed and used only for proofs of concept, to the deployment of AI at scale with verifiable trust in autonomous actions.
- **Hard cost avoidance**: Prevention of AI-driven ‘blast radiuses’ like data exfiltration or compute depletion in milliseconds, thus preventing them from impacting the bottom line.
- **Regulatory confidence:** The ability of autonomous agents to receive the ‘green light’ to process sensitive workloads like complex healthcare datasets or financial transactions through continuous intent-based compliance.
- **Reduced breach impact:** Use of AI-driven semantic gateways to identify logic-based breaches in milliseconds, thus minimizing the financial and reputational damage of a breach.

## Control is what agents follow not what you define

The [IBM X-Force® report](https://www.ibm.com/reports/threat-intelligence), 2026 reveals a 44% spike in AI-accelerated attacks, exposing an existential threat to distributed architectures. As exploits occur at machine speed, static security becomes obsolete. The businesses that will define the next decade will not be the ones with the strongest AI agents; rather, it will be the businesses with the most trusted agents. Autonomy without control is a weakness. Verified autonomy is the strength.

## Author

![Shalini](https://assets.ibm.com/is/image/ibm/shalini-harkar?wid=128)

[Shalini Harkar](https://www.ibm.com/think/author/shalini-harkar)

Lead AI Advocate

[](https://www.ibm.com/think/insights/agentic-ai-runtime-security)

[](mailto:?subject=Agentic%20AI%20Runtime%20Security&body=https://www.ibm.com/think/insights/agentic-ai-runtime-security)[](https://www.linkedin.com/shareArticle?url=https://www.ibm.com/think/insights/agentic-ai-runtime-security&title=Agentic%20AI%20Runtime%20Security)[](https://www.facebook.com/share.php?u=https://www.ibm.com/think/insights/agentic-ai-runtime-security)[](https://x.com/intent/tweet?text=Agentic%20AI%20Runtime%20Security&url=https://www.ibm.com/think/insights/agentic-ai-runtime-security)