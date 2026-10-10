# TemplateDocs

Reusable instruction templates for creating and maintaining agent-managed workspaces, plus optional tooling companions.

Canonical repository: https://github.com/contrazap/TemplateDocs

| Document | Applies to |
|---|---|
| `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` | Workspaces where the user implements the work; the agent plans, coaches, reviews and maintains records. |
| `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` | Workspaces where the agent implements the project; the user directs, reviews and learns. |
| `UNREAL_MCP_BRIDGE.md` | Optional tooling companion (Unreal Engine): an MCP bridge giving the agent local editor access — verification and evidence in manual workspaces, editor implementation and visual verification in agentic ones. |

**Usage.** Provide the applicable template to the agent together with the project requirements; provide the applicable tooling companions when the project uses that tooling. The workspace templates stay generic; the companions carry environment-specific setup and the matching workspace-record additions. Generated workspaces record this repository as a reference instead of copying the templates.
