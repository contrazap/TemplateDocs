## Bootstrap procedure

1. Inspect what exists: instructions, documentation, code, assets and repository state. For an existing project, identify its layout, stack and the patterns its code already follows before proposing anything.
2. Take the project description from the user. Keep confirmed requirements, assumptions, proposals and open questions distinct. Ask only questions that materially affect the brief or the conventions; do not invent a product, features or preferences.
3. Verify what the agent can verify itself: installed tools and versions, the build, the filesystem. Record only commands that were actually run.
4. Generate the minimum set (see *Workspace structure*): `AGENTS.md`, a client entry file for each agent client the user uses (for Claude Code, `CLAUDE.md` containing `@AGENTS.md`), `docs/PROJECT_BRIEF.md`, `docs/CONVENTIONS.md`, `docs/plans/README.md`, `docs/plans/HISTORY.md` (header only) and `.claude/skills/README.md`.
5. For an existing project, write the patterns observed in the code into `docs/CONVENTIONS.md`, each marked *observed*, and ask the user to confirm or correct them. Keep the project's existing README; it gets no status or plan content.
6. Do not write plans during bootstrap. Offer to draft the first milestone, starting from the brief's riskiest open questions.
7. Finish with the audit (see *Final audit and handoff*).

Scaffolding produces documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless that work is separately requested.
