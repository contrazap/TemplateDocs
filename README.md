# TemplateDocs

Reusable instruction templates for creating and maintaining agent-managed workspaces, plus optional tooling companions.

Canonical repository: https://github.com/contrazap/TemplateDocs

| Document | Applies to |
|---|---|
| `WORKSPACE_TEMPLATE_CORE.md` | Every workspace: shared structure, records (incl. the record size budget), planning, evidence, resume routine, `AGENTS.md` and client entry files (`CLAUDE.md`). Always used with one variant. |
| `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` | Variant — the user implements; the agent plans, coaches, reviews and maintains records. |
| `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` | Variant — the agent implements; the user directs, reviews and learns. |
| `UNREAL_MCP_BRIDGE.md` | Optional tooling companion (Unreal Engine): the MCP bridges giving the agent local editor access — the engine's official Unreal MCP as the primary editor bridge, plus the community pyremote server for the local layer and gaps; client entries for OpenCode and Claude Code; verification and evidence in manual workspaces, editor implementation and visual verification in agentic ones. Appendix F adds the agent-side reference-material pipeline for reference-driven projects. |
| `scripts/` | Helper scripts used by the companion (discovery probe, MCP smoke tests) and the in-editor agent check helpers (`ue_checks.py` — copy to a workspace's `tools/`). |

**Usage.** Provide the core plus the applicable variant to the agent together with the project requirements; provide the applicable tooling companions when the project uses that tooling. The templates stay generic; the companions carry environment-specific setup and the matching workspace-record additions. Generated workspaces record this repository as a reference instead of copying the templates. Shared rules change in the core; role-specific rules in the variant.
