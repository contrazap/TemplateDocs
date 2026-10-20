## AGENTS.md and client entry files

The generated `AGENTS.md` is the single source of agent rules. It contains, concisely and with paths that exist in this project:

1. One line on what the project is, linking `docs/PROJECT_BRIEF.md`.
2. **Read order** at the start of a session: `docs/PROJECT_BRIEF.md` → `docs/CONVENTIONS.md` → `docs/plans/README.md` → the last lines of `docs/plans/HISTORY.md` → the plan being worked on, its feature and milestone.
3. The working agreement (see *Working agreement*) and authorization boundaries, including any repository delegation.
4. How planning works: the hierarchy, IDs, the rules, just-in-time authoring, with a pointer to `docs/plans/README.md` for the formats.
5. Working a plan, hold and resume, and the history rule.
6. Verification levels and evidence, with a pointer to the commands in `docs/CONVENTIONS.md`.
7. When to propose convention, brief and skill changes, and that nothing is added without the user's approval.
8. That project status lives in the user's tracker, not in the repository.

It does not repeat the brief, the conventions or the plan formats, and it does not mention the template.

**Client entry files.** A client that does not read `AGENTS.md` natively gets a thin entry file pointing to it, never a copy. For Claude Code: `CLAUDE.md` containing `@AGENTS.md`, plus client-only notes if any. Create entry files only for the clients the user uses. Tool-server (MCP) configuration is per client and per project (for example `.mcp.json` for Claude Code, `opencode.json` for OpenCode); when more than one client is in use, keep their entries equivalent.
