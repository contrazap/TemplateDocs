## Add-ons on request

The template repository has optional add-ons for specific tooling. They are not used during bootstrap. When the user asks to apply one, read it and create what the project needs in the project itself:

- Configuration files (MCP entries, scripts) in the project, at the paths the add-on gives.
- Rules and verified commands in `CONVENTIONS.md`.
- Repeatable procedures as skills, with the user's approval (see *Skills*).

The add-ons were written for the other templates in the family, whose workspaces keep `MEMORY.md`, tooling notes and a roadmap. Map their instructions to this structure: tooling notes and conventions → `CONVENTIONS.md` or a skill; decisions → the plan's outcome or a convention; plan-level steps → tasks in the current plan. The project does not link back to the add-on.

| Add-on | Use when |
|---|---|
| `UNREAL_MCP_BRIDGE.md` | An Unreal Engine project where agents should inspect or edit the editor |
| `UNREAL_TEST_AUTOMATION.md` | An Unreal Engine project with automated checks at each verification level |
| `BLENDER_MCP_BRIDGE.md` | Blender scene work or batch asset pipelines |
| `ASSET_GENERATION_PIPELINE.md` | 3D assets or reference images are sourced or generated (packs, AI 3D, Blender), with provenance and licences |
| `AGENT_ORCHESTRATION.md` | A cheaper worker agent client carries out implementation plans dispatched by an orchestrating agent |
