## Resume routine, AGENTS.md and client entry files

Resume routine: `docs/ROADMAP.md` (roadmap, states, resume pointer) → `docs/MEMORY.md` (decisions, conventions, {{LEARNING_RECORD}}, recent history) → {{CURRENT_PLAN_READ}} → domain documents when design context matters → tooling notes when tool work is next. State the next action as a plan pointer and continue from the recorded position; do not restart planning.

The generated `AGENTS.md` includes, beyond the items in *AGENTS.md additions*:

1. The working agreement and how the user changes it.
2. The exact resume reading order with paths that exist in this workspace, domain documents named.
3. Planning rules: one current plan, on-demand authoring, verify-before-authoring, review gate before the next plan.
4. Authorization boundaries for risky, external or costly actions; repository delegation if any.
5. Records maintenance, compaction rules and the record size budget.
6. The plan markers legend.
7. Implementation and documentation roots, repository conventions.
8. The user profile: the default (see *Bootstrap procedure*) plus knowledge and preferences actually supplied.
9. The canonical template file and the add-ons used, as references only; the rule to ask the user when a path is missing; the rule to propose template updates when formats change.

Do not copy the template into `AGENTS.md`. Do not insert a technology stack, fixed milestone count, domain-specific verification matrix or experience profile unless the user's requirements justify it.

**Client entry files.** `AGENTS.md` is the single source of agent rules. A client that does not read `AGENTS.md` natively gets a thin entry file that points to it, never a copy. For Claude Code: a root `CLAUDE.md` whose content is `@AGENTS.md` (the import loads the file), plus client-only notes when there are any. Create entry files only for clients the user actually uses, and record the supported clients in `MEMORY.md` conventions. Tool-server (MCP) configuration is per client and per project (for example OpenCode `opencode.json`, Claude Code `.mcp.json`); when more than one client is supported, keep their entries equivalent. The add-ons give the shapes.
