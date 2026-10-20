## Skills

`.claude/skills/` holds this project's reusable procedures as Agent Skills. It starts with only a `README.md`; skills are added when the project shows it needs them.

**When to suggest one.** The agent suggests a skill when a multi-step procedure has been done more than once or was hard to work out and will recur. For example: how to verify a feature through the engine editor's MCP bridge after implementing it; how to import and validate a generated 3D model; how to run and read a profiling capture on the target device. The suggestion gives the name, when it would be used and an outline of the steps. A skill is created only when the user approves.

**Rules or procedures.** A rule ("all gameplay state is server-authoritative") goes in `CONVENTIONS.md`. A procedure (the steps to check replication in a two-client session) becomes a skill, with a one-line pointer from `CONVENTIONS.md`.

**Format.** One folder per skill, `.claude/skills/<name>/SKILL.md`, with YAML frontmatter and a markdown body; supporting scripts or examples sit beside it:

```markdown
---
name: <kebab-case-name>
description: <what it does and when to use it, in one or two sentences; agents choose skills from this line>
---

# <Title>

<When to use it, prerequisites, then numbered steps with exact commands and the expected results.>
```

Keep skills specific to this project: real paths, real commands, verified results. Update a skill when its procedure changes; remove one that is no longer used. `.claude/skills/` is where Claude Code reads skills; if another agent client is in use, record in `CONVENTIONS.md` where it reads them and keep one copy of each skill.

Copying a skill to another project or to the template repository happens only when the user asks.

**`.claude/skills/README.md`** says what belongs in the folder, repeats the format above and the rule that skills are added with the user's approval.
