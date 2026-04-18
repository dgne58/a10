# Sandbox Execution Plane

## Overview
- This page separates orchestrator-owned control flow from the mutable compute boundary where agent-directed code and file work happen.
- It exists because multiple sources converge on the same pattern: keep the harness, approvals, tracing, and policy outside the sandbox when possible.
- In this wiki, "sandbox execution plane" means the live workspace where an agent can read and write files, run commands, expose ports, install packages, and resume stateful work.

## Why This Matters
- Prompt context alone is a weak substitute for a real workspace when the task depends on documents, generated artifacts, or resumable state.
- Combining orchestration and execution inside one container is convenient for prototypes, but it blurs trust boundaries.
- A separate sandbox layer makes it easier to explain where code runs, where secrets live, where approvals happen, and which state is durable.

## Control Plane vs Compute Plane

| Layer | What it owns | Typical risks |
| --- | --- | --- |
| Harness or control plane | agent loop, model calls, tool routing, handoffs, approvals, tracing, recovery, audit, run state | over-broad authority, hidden policy, weak auditability |
| Sandbox execution plane | filesystem mutations, shell commands, package installs, ports, previews, provider-specific workspace state | prompt-directed code execution, secret leakage, artifact poisoning |

The most important design rule from the batch is: keep control-plane trust separate from compute-plane mutability unless the prototype is intentionally accepting that shortcut.

## Workspace Contract
- A manifest is the desired starting workspace contract for a fresh session.
- It should define files, repos, mounts, startup environment, and output directories.
- Relative workspace paths matter because portability across local, Docker, and hosted providers depends on avoiding absolute or escaping paths.
- The manifest is not the same thing as the live workspace. A run may start from a fresh workspace, a resumed live session, serialized state, or a snapshot restored by the provider.

## Capability Model
- Sandbox-native capabilities shape what the agent can do inside the execution plane.
- The batch sources repeatedly center these capability types:
  - shell execution
  - filesystem editing
  - skills materialization
  - compaction or context trimming
  - memory persistence across runs

## Security And Secrets
- Secrets should be runtime configuration, not prompt content.
- Mount credentials and environment values should be scoped to what the sandbox session actually needs.
- Persisted state should avoid carrying forward tokens, generated mount config, or private files unless there is an explicit reason to preserve them.
- Artifact review matters because private inputs can leak into generated outputs even when raw credentials are not exposed.

## When To Use A Sandbox
- the task depends on a directory of documents, not a single prompt
- the agent must create files another system will inspect later
- the workflow needs commands, packages, or scripts
- the product needs previews on exposed ports
- work pauses for review and resumes in the same workspace

## When Not To Use A Sandbox
- the task is short-lived and mainly returns text
- there is no meaningful file, command, or resumable-state requirement
- a single hosted shell or deterministic function tool is enough

## Design Implications For This Project
- A future coding or document-analysis agent should likely run in a sandboxed execution plane, while the wiki-first orchestrator stays outside it.
- The router should choose the sandbox path only when the task truly requires workspace semantics.
- The [[policy-gateway]] should decide whether a sandbox path is permitted and which capabilities, mounts, and credentials it receives.
- The [[orchestrator]] should treat sandbox sessions as execution targets, not as replacements for the overall loop.

## Failure Modes
- running the harness inside the sandbox by default and losing a clean trust boundary
- persisting secrets or provider-specific state into snapshots and artifacts
- using sandboxing for tasks that only needed a normal model call
- confusing manifest defaults with the effective live workspace state
- exposing shell or filesystem capabilities without matching policy and audit coverage

## Related
- [[orchestrator]]
- [[policy-gateway]]
- [[tool-surfaces]]
- [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]
- [[../sources/security-networking-and-governance|Security, Networking, and Governance]]
