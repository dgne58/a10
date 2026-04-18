---
tags: [openai, agents, sdk, agentic, tools, guardrails, mcp, sources]
last_updated: 2026-04-15
---

# OpenAI Agents SDK

## Provenance
- Theme: `mcp-agentic-workflows`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/OpenAI Agents SDK.md`
- `Clippings/Agents SDK  OpenAI API.md`
- `Clippings/Guardrails - OpenAI Agents SDK.md`
- `Clippings/Function calling  OpenAI API.md`
- `Clippings/Sandbox Agents  OpenAI API.md`
- `Clippings/Agent Builder  OpenAI API.md`
- `Clippings/Sandbox – Codex  OpenAI Developers.md`

---

## Overview

The OpenAI Agents SDK (`openai-agents` Python package) is the production-ready successor to Swarm. It provides a small set of composable primitives for building multi-agent systems without steep learning curves.

Install: `pip install openai-agents`

**Design philosophy**: Few abstractions, Python-first, works out of the box with customizable internals.

---

## Core Primitives

### 1. Agent
An LLM equipped with instructions and tools.

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)
result = Runner.run_sync(agent, "Write a haiku about recursion.")
print(result.final_output)
```

### 2. Handoffs / Agents-as-Tools
Agents can delegate to other agents for specialized tasks:
- **Handoffs**: Transfer conversation control to another agent
- **Agents as tools**: Call another agent as if it were a function tool
- Manager pattern: Orchestrator agent invokes specialists; specialists return results to manager

### 3. Guardrails
Input/output validation running in parallel with or before agent execution.

```python
# Input guardrail blocks before agent runs (blocking mode)
# Output guardrail validates final agent output
# Tool guardrail wraps specific function tools
```

### 4. Function Tools
Any Python function becomes a tool via automatic schema generation + Pydantic validation:

```python
@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: sunny"
```

### 5. Sessions
Persistent memory layer for context within an agent loop.

### 6. Sandbox Agents
Run specialists in real isolated workspaces (container-based):
- Manifest-defined files
- Real shell commands and package installation
- Resumable sandbox sessions
- Snapshot/restore support

### 7. Agent Builder (visual canvas)
- Node-based visual workflow editor for composing multi-step agent flows
- Each node is an agent, tool, or conditional branch
- ChatKit: embeddable chat widget for deploying Agent Builder workflows
- Export to SDK code: visual graph converts to `openai-agents` Python code

---

## Agent Loop

Built-in loop that:
1. Sends request to LLM
2. Receives response (text or tool calls)
3. Executes tool calls if any
4. Feeds tool results back to LLM
5. Repeats until no more tool calls (task complete)

The SDK manages this loop; the Responses API lets you own it manually.

**When to use SDK vs Responses API**:
| Use SDK | Use Responses API |
|---------|-------------------|
| Multi-turn orchestration | Short-lived, single-step |
| Guardrails and human approval | Full control over loop |
| Handoffs and multi-agent | Simple model response |
| Sandbox or resumable execution | Light wrapper |

---

## Guardrails — Detail

### Types
| Type | Scope | When it runs |
|------|-------|-------------|
| Input guardrail | Agent | First agent in chain only |
| Output guardrail | Agent | Last agent in chain only |
| Tool guardrail (input) | Tool | Before tool executes |
| Tool guardrail (output) | Tool | After tool executes |

### Execution Modes (Input Guardrails)
- **Parallel** (default): guardrail runs concurrently with agent — best latency, but agent may consume tokens before failure
- **Blocking** (`run_in_parallel=False`): guardrail completes first — prevents token waste and side effects, ideal for cost optimization

### Mechanism
```python
# 1. Guardrail function receives agent input
# 2. Returns GuardrailFunctionOutput
# 3. If .tripwire_triggered → raises InputGuardrailTripwireTriggered
# 4. Caller handles exception (e.g., return error to user)
```

### Practical pattern: Fast guard model + expensive main agent
Use a cheap/fast model as guardrail to detect malicious/off-topic inputs before invoking expensive model:

```python
input_guardrail = InputGuardrail(
    guardrail_function=detect_malicious_input,  # runs fast/cheap model
    run_in_parallel=False  # block if policy violation
)
agent = Agent(
    instructions="Handle customer requests",
    input_guardrails=[input_guardrail]
)
```

---

## Function Calling (Responses API)

The underlying primitive for tool use, exposed at API level.

### 5-step flow
1. Request: send tools list (JSON schema) + user message
2. Response: model returns `tool_calls` items
3. Execute: application runs the function
4. Submit: send tool results back in next request
5. Final: model returns final text response (or more tool calls)

```python
tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get weather for a city",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
    }
}]

# 5-step loop: request → tool_call → execute → submit → response
```

### Tool search (new in gpt-5.4+)
For apps with many functions or large schemas: defer rarely-used tools and load them only when model determines they are needed. Reduces prompt size and cost.

---

## MCP Integration

The SDK supports MCP servers as first-class tool providers:
- MCP server tools work identically to function tools in the agent loop
- `MCPServerStdio` and `MCPServerSse` server types supported
- Tools from multiple MCP servers automatically available in same agent

---

## Tracing and Observability

- Built-in tracing: visualize and debug agentic flows
- Supports OpenAI evaluation, fine-tuning, and distillation tooling
- Structured trace captures: tool calls, handoffs, guardrail results, intermediate states

---

## Harness / Compute Boundary

The Codex agent architecture defines a clean split between two planes:

```
┌────────────────────────────────────────────────────────────────┐
│  Harness (control plane)                                        │
│  • Agent loop orchestration      • Model API calls             │
│  • Tool routing + handoffs       • Human approval checkpoints  │
│  • Tracing + observability       • Run state management        │
│  • Recovery logic                                              │
└────────────────────────────────────────────────────────────────┘
           ↕ controlled interface (tool calls, outputs)
┌────────────────────────────────────────────────────────────────┐
│  Compute (sandbox execution plane)                              │
│  • File reads + writes           • Shell command execution     │
│  • Package installs              • External process invocation │
│  • Contained by sandboxing layer                               │
└────────────────────────────────────────────────────────────────┘
```

**Platform-native sandboxing** (Codex CLI):
- macOS: `Seatbelt` (App Sandbox profile — system call restriction)
- Linux: `bubblewrap` (unprivileged user namespace isolation)
- Windows: Windows Sandbox (lightweight VM layer)

**Sandboxing vs approval flow** are orthogonal:
- **Sandboxing** contains damage — limits what the compute plane can reach even if a bad action executes
- **Approval flow** prevents unwanted actions — human confirms before compute plane acts on high-risk operations

**Design principle for this project**: Keep the orchestrator (harness) separate from each task agent's execution environment (compute). The orchestrator should never execute untrusted tool outputs directly; route through the compute boundary with appropriate sandboxing.

---

## Human-in-the-Loop

Built-in support for pausing agent execution and requiring human approval before continuing:
- Interruption points can be set on high-risk operations
- Agent can suspend, send approval request, and resume after confirmation
- Pattern aligns with OWASP LLM06 Excessive Agency mitigation

---

## Security Considerations

| Risk | SDK Mechanism |
|------|--------------|
| Excessive agency (LLM06) | Guardrails + human approval on high-risk actions |
| Prompt injection via tools | Tool guardrails on output; input sanitization |
| Unbounded consumption (LLM10) | Rate limiting at application layer (not built-in) |
| Excessive permissions | Principle: grant only needed tools to each agent |

---

## Related
- [[../workflows/mcp-agentic-patterns|MCP Agentic Patterns]] — MCP protocol, tool invocations, agentic loops
- [[../components/orchestrator|Orchestrator]] — loop responsibilities, workflow patterns
- [[../components/tool-surfaces|Tool Surfaces]] — function tools, MCP tools, resources
- [[owasp-llm-top10]] — security risks for LLM agents
- [[mcp-overview]] — MCP source overview
