# Allowed Tools

## Principle
- Use the cheapest reliable source of truth first.

## Local Reads
- Wiki markdown pages: first stop for project understanding, commands, contracts, risks, and demo flow.
- Local source files: second stop when implementation detail or verification is needed.

## MCP Servers
- Filesystem/search MCP: use for large-repo navigation or richer search once the codebase grows.
- External service MCP: use only after authentication has been tested and documented.
- Any MCP used in the demo should have a dry-run command/result recorded here before the hackathon.

## Priority Tool Order For This Project
1. preload wiki pages
2. thematic wiki pages
3. local source files
4. search MCP / filesystem MCP
5. authenticated external MCP servers
6. web

## Skills
- Use skills for repeated execution patterns or specialized workflows.
- Do not treat skills as project memory.

## Likely Tool Roles
- wiki pages: project memory and working context
- local code search: implementation verification
- function tools: deterministic application-side actions
- MCP servers: authenticated access to systems and structured capability surfaces
- web: only for missing or time-sensitive external facts

## Web
- Allowed for official docs, current API behavior, package references, or hackathon requirements not already captured locally.
- Not allowed as the default first step for codebase questions.

## Decision Guide
| Need | Preferred tool |
| --- | --- |
| project orientation | preload pages |
| command lookup | `commands.md` |
| route/schema lookup | `api-routes-and-schemas.md` |
| current state | `hot.md` |
| implementation detail | local source search |
| large-scale code/wiki search | search MCP |
| authenticated external action | relevant MCP server |
| current external fact | web |

## Demo Rule
- During the hackathon, default to showing that the agent can answer from the wiki or local code before it reaches for the internet.
