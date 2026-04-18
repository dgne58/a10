# Tool Surfaces

## Overview
- This page centralizes a concept that appears repeatedly across routing, orchestration, and MCP pages.
- The system has multiple capability surfaces:
  - direct function tools
  - MCP tools
  - MCP resources
  - MCP prompts
  - model providers

## Why This Page Exists
- Several pages discussed "function tools vs MCP" or "tools vs context" separately.
- This page makes the distinction explicit so those pages can stay focused.

## Capability Types

| Surface | Ownership | Typical use | Discovery model |
| --- | --- | --- | --- |
| Function tool | application-owned | deterministic internal action | static |
| MCP tool | server-owned | externalized reusable action | dynamic |
| MCP resource | server-owned | read-only context surface | dynamic |
| MCP prompt | server-owned | next-step instruction or template | dynamic |
| Model provider | external or self-hosted | generative reasoning or synthesis | configured |

## Function Tools
- Best for app-owned, deterministic actions.
- Examples:
  - local validation
  - schema transformation
  - internal evaluation calculation
  - writing a trace artifact in a controlled format

Advantages:
- easy to reason about
- strong ownership boundary
- easier testing

Limitations:
- not reusable outside the app unless re-exposed
- discovery is usually static

## MCP Tools
- Best for reusable externalized capabilities.
- Examples:
  - GitHub access
  - filesystem server
  - fetch or web retrieval
  - organization-specific internal systems

Advantages:
- protocol-level discovery
- reusable across clients
- clear server boundary

Limitations:
- auth complexity
- runtime reliability depends on the server
- too many exposed tools degrade routing quality

## MCP Resources
- Best for large or structured read-only context.
- Examples:
  - configs
  - project state
  - knowledge artifacts

Why resources matter:
- they reduce the need to cram large context blobs into model prompts
- they are often a cleaner fit than "tool returning a giant text blob"

## MCP Prompts
- Underused but important.
- Best for parameterized next-step instructions or prompt chaining.
- They let a server influence workflow structure without hardcoding every branch in the client.

## Relationship To Routing
- The router should not only choose between model tiers.
- It should often choose between:
  - answer from wiki
  - call a function tool
  - use an MCP tool or resource
  - escalate to a stronger model

## Relationship To The Execution Lifecycle

- tool surfaces sit after route selection and before response assembly
- they are where abstract branch choice becomes a concrete invocation
- they therefore inherit both:
  - routing constraints
  - policy constraints

This is why tool-surface design affects not only integration convenience but also explainability and safety.

## Design Guidance For This Vault
- prefer function tools for app-owned deterministic logic
- prefer MCP for reusable or external capabilities
- prefer resources for large read-only context
- keep the total exposed tool set narrow enough that routing remains explainable

## Related Topics
- [[mcp-control-plane]]
- [[orchestrator]]
- [[router]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]
