## States and review protocol

Plans: Planned → Pending → In progress → **Done** (the user reports every task complete; the plan-end review remains) → **Verified**.

- During a plan the user works through the tasks and reports each one done (for example `3 done`). The agent marks it ✅ without a full review, and looks into a task mid-plan only when the user asks or a **Done when:** check fails.
- **Plan-end review:** the user sends the 📤 evidence and the hours spent. The agent inspects the project's files, configuration and structure, runs the non-destructive checks it can (build, tests, lint, editor read-backs where a bridge is set up) and reviews the user's evidence of behaviour. Errors come back as fix steps in the plan, with the fix and a short why; the plan is Verified when they pass.
- At Verified: record the hours in the time log, update the roadmap (state, hours spent, resume block) and the coverage map, add the plan to the **Built in** line of the toolbox entries it used, and add a one-line history entry.
- Review replies lead with the verdict: `✅ Plan NN passes`, or `❌ N.N: <finding> → <correction>`, one or two lines per finding, then `Next:`. The full finding goes in the plan's agent notes, not the reply.
- When the last plan of an arc is Verified, hold the arc review (see *Arcs, coverage and time*) before writing the next plan.
