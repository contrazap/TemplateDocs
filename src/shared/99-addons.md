## Optional add-ons

Add-ons are separate files in the template repository for specific tooling. They supplement this template and never change its working agreement. Use one when the project involves its area; record the ones used in `MEMORY.md` references.

| Add-on | Use when | If needed but not provided |
|---|---|---|
| `UNREAL_MCP_BRIDGE.md` | An Unreal Engine project where the agent should inspect or edit the editor (MCP bridges, reference-material pipeline) | Ask for it; without it, editor work becomes user steps with screenshot evidence |
| `UNREAL_TEST_AUTOMATION.md` | An Unreal Engine project with automated checks (builds, automation and functional tests, captures, packaging per verification level) | Ask for it; without it, define the commands in the tooling notes as they are verified |
| `BLENDER_MCP_BRIDGE.md` | Blender scene work or batch asset pipelines, Unreal export conventions | Ask for it; without it, Blender work becomes user steps |
| `ASSET_GENERATION_PIPELINE.md` | 3D assets or concept and reference images are sourced or generated (packs, AI 3D, Blender; provenance and licences) | Ask for it; without it, record sources and licences by hand |
| `AGENT_ORCHESTRATION.md` | The autonomous template with a cheaper worker client (dispatch, report format, dry run) | The orchestrator implements the cards itself |

Helper scripts used by the add-ons live in the template repository's `scripts/` folder.
