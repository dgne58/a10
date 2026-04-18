# Hackathon Build Loop

## Purpose
- Define how Codex, Claude Code, and the wiki should interact during the event.

## Loop
1. Read preload pages.
2. Read the smallest relevant thematic wiki pages.
3. Inspect local code only where the wiki is insufficient.
4. Implement the change.
5. Verify with tests or direct execution where possible.
6. Write back commands, file map updates, and any new contracts or risks.

## Division Of Labor
- Wiki:
  - persistent state, architecture, commands, contracts, demo story
- Codex / Claude:
  - implementation, debugging, focused synthesis, write-back
- MCP / tools:
  - authenticated actions and structured execution

## Session Start Checklist
- read `hot.md`
- read `commands.md`
- confirm repo state
- confirm MCP auth state
- confirm current demo goal

## Failure Modes
- jumping into code without refreshing preload
- splitting memory across chat history instead of the wiki
- deferring wiki updates until “later”

## Related
- [[demo-flow]]
- [[../00-preload/hot|Hot]]
- [[../00-preload/allowed-tools|Allowed Tools]]
