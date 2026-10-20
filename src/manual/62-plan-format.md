## Plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Done|Verified]` · `⬜⬜⬜⬜⬜⬜⬜ n/N` · next → N · roadmap: ../ROADMAP.md

🎯 [Target — the observable result, one or two lines.]

### 1. [Action]
&emsp;&emsp;1.1 [Step]

&emsp;&emsp;1.2 [Step]

💡 [Colocated note — only where a new concept or a genuine trap sits.]

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
- Mark a finished step ✅ leading its line, and a finished task by appending ✅ to its heading once its checkpoint passes.
- Tasks are actions. Use exact steps where the tooling is first-time (see *Support levels*); explanations are colocated at the step that needs them, never a separate study section before the steps.
- Each task closes with a `**Done when:**` statement; the aggregate acceptance list lives in the agent block.
- The send line asks only for evidence the agent cannot produce or inspect itself.
- Known traps and verified environment let the agent answer quickly and cold-start safely.

**Task anatomy**

- **Why (optional):** one line linking the task to the target, only when non-obvious.
- **Steps:** ordered, concrete actions. Exact editor paths, menu names and field values at L1; less hand-holding as the level drops.
- **Code:** task-scoped deltas only: file path, anchor, the lines to add, replace or delete, clearly marked. A complete file only when the task creates that small file. Explain only APIs the user has not met.
- **Done when:** what is true, visible or runnable when the task is complete; add an evidence hint where non-obvious.
