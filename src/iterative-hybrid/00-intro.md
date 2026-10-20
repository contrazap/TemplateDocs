# Iterative hybrid workspace template

A self-contained template for project workspaces that are **human-first with agent acceleration**: the user directs, and agents research, analyze and implement where they are strong, while the user does by hand what they do better (taste, feel, level design, art direction) or wants to own. The direction is known in general but not in detail; it evolves as the project is built, played or used. Plans are written just in time, one handover-sized chunk at a time, and completed plans are kept as a frozen record of what was built and fixed.

Project status, priorities and backlog live in the user's own tracker (for example Trello or Notion). The workspace holds what agents need to work without deviating: the project brief, the conventions, the plans and an append-only history of the order in which the work happened.

Other templates in the family: `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` (agents build end to end against an approved roadmap), `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` (the user implements; the agent coaches) and `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` (the agent implements step by step while the user builds along and learns).

## How to use this template

Provide this file to the agent and describe the project: what it is trying to achieve, the platforms and constraints, and whether it is new or existing. For example:

> Read ITERATIVE_HYBRID_WORKSPACE_TEMPLATE.md and use it to set up this project's workspace. Here is what I am trying to achieve: <description>. Preserve existing work. Do not write any plans yet.

**The generated workspace is self-contained.** It never refers to this template or its repository: no provenance note, no links, no copied template text. Everything agents need is written into the project's own files. When the user later asks to bring in material from the template repository (an add-on such as an engine bridge setup, or a stored skill), the agent creates the needed files in the project (see *Add-ons on request*) and the project still does not link back.

The example invocation does not need to be stored in generated documentation.
