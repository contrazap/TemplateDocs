# TemplateDocs

Reusable instruction templates for creating and maintaining agent-managed workspaces, plus optional add-ons for specific tooling.

Canonical repository: https://github.com/contrazap/TemplateDocs

## Templates

Each template is self-contained: give the agent one template (plus the add-ons the project uses) and the project requirements. The iterative hybrid template applies add-ons only when asked, later, by creating the needed files in the project.

| Template | Use when |
|---|---|
| `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` | The agent implements and the user learns by building along: every plan is a from-scratch build guide split into step files; for each step the user reads what will happen, replies go, the agent executes exactly that step, and the user reads the resulting code and runs checks against expected output. Structure first, tools when needed, industry-standard tools by default. |
| `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` | The user implements; the agent plans, coaches with support levels, reviews and maintains the records. |
| `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` | Agents implement end to end: roles (orchestrator, implementer, reviewer), optional cheaper worker agents with verification economy, task-card plans, guard rails, needs-you queue; the user approves at milestone gates. |
| `ITERATIVE_HYBRID_WORKSPACE_TEMPLATE.md` | Human-first with agent acceleration, for new or existing projects whose direction evolves as they are built: a project brief and conventions instead of a roadmap; milestone, feature and implementation plans written just in time and handed to an agent or the user per plan; bug-fix and enhancement plans in the current milestone while completed plans stay frozen; an append-only history of the order of work; skills added as the project needs them. Status lives in the user's own tracker, and generated workspaces are fully self-contained. |
| `PRACTICE_TRACK_WORKSPACE_TEMPLATE.md` | The user practises a tool or stack for exposure and practice, not unguided problem solving: every plan is a self-contained small project with complete steps that never fade or rely on earlier plans; tasks sized to the user's sessions; a coverage map of topic clusters (core or later, out-of-scope topics routed to other media); rolling arcs of a few plans with an arc review; a time section with estimates re-scaled from a time log; a toolbox of everything met so far (use it when, built in, nearby, docs). No skill ledger. |

## Add-ons

Optional; each template lists them under *Optional add-ons* with when to use them and what the agent does if one is needed but not provided.

| Add-on | Covers |
|---|---|
| `AGENT_ORCHESTRATION.md` | Autonomous template: Claude Code as orchestrator dispatching task cards to OpenCode workers (DeepSeek); worker agent definition, dispatch wrapper, report format, orchestrator skill, dry-run checklist. |
| `UNREAL_MCP_BRIDGE.md` | Unreal Engine: the MCP bridges giving the agent local editor access (the engine's official Unreal MCP as the primary editor bridge, plus the community pyremote server for the local layer and gaps); client entries for OpenCode and Claude Code; how each template uses them. Appendix F adds the agent-side reference-material pipeline; Appendices H–I add procedures ready to become project skills (material mobile instruction counts, multiplayer PIE checks and captures). |
| `UNREAL_TEST_AUTOMATION.md` | Unreal Engine: headless, agent-runnable checks mapped to the Fast/Standard/Full verification levels: command-line builds, automation and functional tests, two-process network tests, performance captures, screenshot comparisons, packaging. |
| `BLENDER_MCP_BRIDGE.md` | Blender: the `blender-mcp` bridge for interactive scene work, batch `blender -b` scripts for repeatable pipeline steps, and Unreal export conventions (units, orientation, pivots, UCX collision, LODs, Chaos vehicle rigs). |
| `ASSET_GENERATION_PIPELINE.md` | 3D asset source priority (packs → AI 3D → Blender), provenance and licences, AI 3D cleanup steps, and concept/reference image generation for design review packs. |
| `CAPACITOR_ANDROID_APP.md` | Personal Android apps (Capacitor 8 + React/TypeScript, installed directly on a few phones): stack, one-time PC setup, starting a new app, app conventions, signing, and the self-updating release pipeline (web bundles on Firebase Hosting, APKs on GitHub releases); optional sync, reminders and AI modules. Uses `starters/capacitor-android/` and `scripts/new-capacitor-android-app.ps1`. |
| `starters/` | Working starter projects with `__PLACEHOLDERS__`, filled in by the matching `scripts/new-*.ps1`. |
| `scripts/` | Helper scripts used by the add-ons (discovery probe, MCP smoke tests, new-app scaffolders), the in-editor agent check helpers (`ue_checks.py`, copied to a workspace's `tools/`) and `build-templates.ps1`. |

## Maintaining the templates

The five templates are generated. Their text lives in `src/`:

```text
src/shared/              rules the roadmap-based templates (agentic learning, manual, autonomous, practice track) use: template use,
                         shared working rules, bootstrap, structure, planning, records and evidence, decisions,
                         resume and AGENTS.md, audit, add-ons
src/iterative-hybrid/    the iterative hybrid template: own parts only (no roadmap, memory or plan states to share)
src/<template>/          the template's own parts and manifest.txt (output file, token values, part order)
```

1. Edit the parts in `src/`, never the generated files. A rule the roadmap-based templates share goes in `src/shared/`; a difference between templates is either a template's own part or a `{{TOKEN}}` whose value each `manifest.txt` sets.
2. Rebuild: `powershell -File scripts/build-templates.ps1` (Windows PowerShell 5.1 or later).
3. Before committing: `powershell -File scripts/build-templates.ps1 -Check` exits 1 if a generated file is out of date.

Workspaces generated from the roadmap-based templates record this repository and the template file used as references instead of copying the template; iterative hybrid workspaces do not refer back at all. When a workspace agrees a process change, it proposes the matching edit to the parts here.
