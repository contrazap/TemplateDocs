# Agentic learning workspace template (build-along)

A self-contained template for agent-managed workspaces in which **the agent implements and the user learns by building along**. Every plan is a from-scratch build guide split into small steps. For each step the user reads what will happen and why, replies **go**, the agent executes exactly that step, and the user reads the resulting code and runs the checks against stated expected output. The project grows the way a real one does: structure first, each tool when it is needed, and refactors when a better option earns its place.

The goal is a working project *and* a user who could set it up again: which tools, which commands, which files and settings, and why. Checks that only test behavior are not enough; every step includes reading the code and configuration it produced.

Other templates in the family: `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` (the user implements; the agent coaches), `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` (agents build end to end; the user approves at milestone gates) and `ITERATIVE_HYBRID_WORKSPACE_TEMPLATE.md` (human-first with agent acceleration; the direction evolves and plans are written just in time).

## How to use this template

Provide this file to the agent (from the canonical repository or a local copy), together with the add-ons the project uses (see *Optional add-ons*), and supply the requirements separately. For example:

> Read AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md and use it to generate or adapt this workspace's documentation and AGENTS.md from the requirements I provide. Preserve existing work. Write the first plan's overview and its first step, ready for me to read.

The example invocation does not need to be stored in generated documentation. To switch an existing workspace to this template, see *Restarting an existing workspace*.
