# Practice track workspace template

A self-contained template for agent-managed workspaces in which **the user practises a tool or technology stack by implementing fully guided plans**. The aim is exposure and practice, not independence through fading guidance: every plan is a small, self-contained project built from complete steps, so the user meets each feature hands-on, remembers that it exists and where it helps, and looks the details up when a real need arises. Working things out without steps is deliberately out of scope; the user does that in separate projects of their own.

A workspace covers one track, such as a game engine or a web stack. It works through a bounded **core** of topic clusters chosen for their value to the user's goal, planned one **arc** (a few plans) at a time, with time estimates checked against the hours actually spent. Topics that complete text steps teach poorly, such as art, modelling or level design, stay out of the plans.

Other templates in the family: `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` (the user implements; the agent coaches with fading support levels), `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` (the agent implements step by step while the user builds along and learns), `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` (agents build end to end; the user approves at milestone gates) and `ITERATIVE_HYBRID_WORKSPACE_TEMPLATE.md` (human-first with agent acceleration; the direction evolves and plans are written just in time).

## How to use this template

Provide this file to the agent (from the canonical repository or a local copy), together with the add-ons the track uses (see *Optional add-ons*), and describe the track: the tool or stack, the goal the practice serves, what the user already knows, and the time available (sessions per week, their usual length and days). For example:

> Read PRACTICE_TRACK_WORKSPACE_TEMPLATE.md and use it to scaffold a practice workspace for <tool or stack>. Goal: <what the practice is for>. I practise <sessions> a week, about <length> each. I already know <…>. Create the roadmap with its first arc and only the first detailed plan.

The example invocation does not need to be stored in generated documentation.
