# TemplateDocs

Reusable instruction templates for creating and maintaining agent-managed workspaces, plus optional tooling companions.

Canonical repository: https://github.com/contrazap/TemplateDocs

| Document | Applies to |
|---|---|
| `WORKSPACE_TEMPLATE_CORE.md` | Every workspace: shared structure, records (incl. size budgets and the history archive), default user profile, planning, evidence and verification levels, decisions with rejected alternatives and dead ends, optional concept glossary, resume routine, `AGENTS.md` and client entry files (`CLAUDE.md`). Always used with one variant. |
| `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` | Variant — the user implements; the agent plans, coaches, reviews and maintains records. |
| `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` | Variant — the agent implements; the user directs, reviews and learns: plan approval gate, boundary briefings and milestone demos recorded in the plans, review split into user judgment and agent-verified evidence, hands-on offers for tasks worth doing by hand. |
| `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` | Variant — agents implement end to end; roles (orchestrator, implementer, reviewer), orchestrated mode with cheaper worker agents and verification economy, task-card plans, verification levels, guard rails, needs-you queue; the user approves at milestone gates. |
| `AGENT_ORCHESTRATION.md` | Optional tooling companion (autonomous variant): Claude Code as orchestrator dispatching task cards to OpenCode workers (DeepSeek); worker agent definition, dispatch wrapper, report format, orchestrator skill, dry-run checklist. |
| `UNREAL_MCP_BRIDGE.md` | Optional tooling companion (Unreal Engine): the MCP bridges giving the agent local editor access — the engine's official Unreal MCP as the primary editor bridge, plus the community pyremote server for the local layer and gaps; client entries for OpenCode and Claude Code; verification and evidence in manual workspaces, editor implementation and visual verification in agentic ones. Appendix F adds the agent-side reference-material pipeline for reference-driven projects. |
| `UNREAL_TEST_AUTOMATION.md` | Optional tooling companion (Unreal Engine): headless, agent-runnable checks mapped to the Fast/Standard/Full verification levels (core) — command-line builds, automation and functional tests, two-process network tests, performance captures, screenshot comparisons, packaging. |
| `BLENDER_MCP_BRIDGE.md` | Optional tooling companion (Blender): the `blender-mcp` bridge for interactive scene work, batch `blender -b` scripts for repeatable pipeline steps, and Unreal export conventions (units, orientation, pivots, UCX collision, LODs, Chaos vehicle rigs). |
| `ASSET_GENERATION_PIPELINE.md` | Optional tooling companion: 3D asset source priority (packs → AI 3D → Blender), provenance and licences, AI 3D cleanup steps, and concept/reference image generation for design review packs. |
| `scripts/` | Helper scripts used by the companions (discovery probe, MCP smoke tests) and the in-editor agent check helpers (`ue_checks.py` — copy to a workspace's `tools/`). |

**Usage.** Provide the core plus the applicable variant to the agent together with the project requirements; provide the applicable tooling companions when the project uses that tooling. The templates stay generic; the companions carry environment-specific setup and the matching workspace-record additions. Generated workspaces record this repository as a reference instead of copying the templates. Shared rules change in the core; role-specific rules in the variant.
