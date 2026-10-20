# Autonomous agentic workspace template

A self-contained template for agent-managed workspaces in which **agents implement the project end to end**; the user directs, makes taste calls and approves work at milestone gates. There is no learning budget: gates sit at milestones, and plans inside an approved milestone advance on agent evidence.

Other templates in the family: `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` (the agent implements step by step while the user builds along and learns) and `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` (the user implements; the agent coaches).

## How to use this template

Provide this file to the agent (from the canonical repository or a local copy), together with the add-ons the project uses (see *Optional add-ons*; `AGENT_ORCHESTRATION.md` when a worker client is configured), and supply the requirements separately. For example:

> Read AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md and the add-ons <list>, and use them to generate this workspace's documentation and AGENTS.md from the requirements I provide. Preserve existing work. Author only the first detailed plan and present it for approval.

The example invocation does not need to be stored in generated documentation.
