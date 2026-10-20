## Bootstrap procedure

1. Inspect existing instructions, files, documentation, implementation and repository state; identify what exists before proposing a structure.
2. Determine whether this is one project or a workspace of independently managed projects; use existing organization and user intent.
3. Extract confirmed requirements from the supplied material; keep proposals, assumptions, open questions and observed facts distinct.
4. Calibrate (see *Bootstrap additions*). Default user profile when nothing else is supplied: comfortable with general programming; no experience with this project's tools, frameworks, engine or conventions. Explain those at first use and skip generic programming lessons. Record only knowledge the user states for this workspace; do not carry it over from elsewhere or invent preferences.
5. Verify what the agent can verify itself (environment, installed tools, filesystem) before authoring plans.
6. Resolve ordinary organizational choices from available context; ask only questions that materially affect scope, correctness or the immediate plan. If requirements are missing, request them without inventing a product or domain; neutral scaffolding may still be prepared.
7. Check which add-ons the project needs (see *Optional add-ons*). Use the ones provided; for a needed add-on that was not provided, name it and ask for it, or proceed without it and state what is missing.
8. Preserve useful existing documents; adapt or link them instead of duplicating conflicting versions.
9. Generate the minimum coherent set: `README.md`, `AGENTS.md`, `docs/ROADMAP.md`, `docs/MEMORY.md`, a domain document only when the project has one (several → `docs/design/` with an index), {{FIRST_PLAN}}, and the agent-client entry files the user's clients need (see *Resume routine, AGENTS.md and client entry files*). No session files, no separate status, conventions, decisions, references or verification documents.
10. Check consistency of links, states and evidence labels; finish with the audit and handoff (see *Final audit and handoff*).

Scaffolding produces documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless that work is separately requested or already authorized.
