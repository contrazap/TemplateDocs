## Plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Done|Verified]` · `⬜⬜⬜⬜⬜⬜⬜ n/N` · next → N · roadmap: ../ROADMAP.md

🎯 [Target — the observable result, one or two lines.]

### 1. [Action] ✅
&emsp;&emsp;✅ 1.1 [Step, finished]

&emsp;&emsp;✅ 1.2 [Step, finished]

💡 How [concept] works here:
- [How it applies to this project, naming the files, assets or steps involved.]
- [Why it is built this way, or the trap it avoids.]

Background: [Concept](../concepts.md#concept).

**Done when:** [what is true when this task is complete.]

### 2. [Action]
…

📤 When done: [the evidence only the user can provide.]

---
## 🔧 Agent notes
*Bookkeeping and review only — not implementation reading.*
- **Acceptance** (checked at review; marked when Verified): [criteria]
- **Known traps**: [short list]
- **Scope guard**: [what this plan deliberately does not include]
- **Environment** verified [date]: [facts the agent checked itself]
- **Inspect**: [files, configs, structure to check at review]
- **Limits**: [what cannot be verified from files]
- **Record**: [what to log at review — decisions, layout outcomes, ledger updates]
```

Format rules:

- The user part comes first and carries no bookkeeping; everything after the `---` divider is agent material and can be skipped by the user.
- The user part is target, tasks, send line. Plans contain only user actions.
- Tasks are numbered `1`, `2`, …; steps are numbered `1.1`, `1.2`, … under their task, each on its own line indented with `&emsp;&emsp;` (Markdown lists cannot express `1.1`).
- When a task's checkpoint passes review, mark each of its steps ✅ at the start of the step line, before the number (`&emsp;&emsp;✅ 1.1 ...`), and append ✅ to the task heading (`### 1. [Action] ✅`). Steps have no checkpoint of their own; a step reviewed on its own is marked when it passes.
- Tasks are actions. Use exact steps where the tooling is first-time (see *Support levels*); explanations are colocated at the step that needs them, never a separate study section before the steps.
- A `💡` tip sits only where a new concept or a genuine trap does, and says only what the concept glossary can't: how the concept works in this project and why it is built this way. A lead line, two or three plain bullets naming the files, assets or steps involved, then `Background:` links to the glossary entries. It never repeats a glossary definition and avoids metaphors; without a glossary, the bullets still stay project-specific.
- Each task closes with a `**Done when:**` statement; the aggregate acceptance list lives in the agent block.
- The send line asks only for evidence the agent cannot produce or inspect itself.
- Known traps and verified environment let the agent answer quickly and cold-start safely.
- Order steps for live feedback: wire up loading first (imports, script or asset references, routes, a running server or watcher), then add content, so every save shows a visible or checkable result. Snippets stay whole; the step tells the user to type a section at a time and save as they go. No step leaves the build broken for a later step to fix.
- Everything the user types (code, markup, commands, values) uses only characters on a standard keyboard: `-` not `—`, straight quotes not curly ones, `...` not `…`. Prose may use other characters.
- Type and lint errors are watched in the editor (underlines, Problems panel); plans don't keep a type-checker watch running, and the user starts one when they want it. Where the tool chain has a test runner with a watch mode, a step starts it before the code it tests, so failures show on save instead of only at the end.
- Every step builds the project or practises a skill on the ledger; no steps that exist only for ceremony or bookkeeping.

**Task anatomy**

- **Why (optional):** one line linking the task to the target, only when non-obvious.
- **Steps:** ordered, concrete actions. Exact editor paths, menu names and field values at L1; less hand-holding as the level drops.
- **Code:** task-scoped deltas only: file path, anchor, the lines to add, replace or delete, clearly marked. A complete file only when the task creates that small file. Explain only APIs the user has not met.
- **Done when:** what is true, visible or runnable when the task is complete; add an evidence hint where non-obvious.
