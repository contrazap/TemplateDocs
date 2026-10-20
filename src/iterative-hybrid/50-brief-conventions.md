## Project brief and conventions

**`PROJECT_BRIEF.md`** states the direction, not the roadmap:

- **North star:** one or two sentences on what the project is.
- **Pillars:** three to five qualities every decision is weighed against.
- **Platforms and constraints:** targets, engine or stack, performance budgets, hard limits.
- **Non-goals:** what the project deliberately does not do.
- **Open questions:** ranked by risk, each with what would answer it. Answered questions move out: the answer becomes a pillar, a constraint or a convention, with a pointer to the plan that settled it.

The brief changes as the project does. After a plan whose results bear on the direction (a playtest, a spike, user feedback), the agent proposes the edit and the user approves it.

**`CONVENTIONS.md`** holds what agents must follow so they do not drift from the project's patterns. Group it by topic, for example:

- Layout and naming: folders, files, assets, IDs.
- Architecture rules: module boundaries, data flow, authority and replication models, patterns to use and to avoid.
- Code and asset standards: style, formats, budgets (polygon counts, texture sizes, frame time).
- Verification: the commands for each verification level, each listed only after it has been run here, with the shell it runs in. When the project starts long-running processes (servers, containers, editors), a **Check first** entry says how to see what is running and how to stop it or free a port.
- Repository rules: what is ignored, delegated git operations, branch naming.
- Secrets: where they live (environment variables or a credential store, never the repository or the plans).
- Agent clients in use and where each reads its skills.

Each rule takes one or two lines. A multi-step procedure becomes a skill with a one-line pointer here (see *Skills*). Rules are added when a pattern settles, usually at a plan's wrap-up; the agent proposes them and the user approves. A rule that is replaced is updated in place, and the plan that changed it is named on the rule's line.
