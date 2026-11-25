## Plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Done|Verified]` · `⬜⬜⬜⬜⬜ n/N` · next → N.N · arc A · roadmap: ../ROADMAP.md

🎯 [Target — the observable result, one or two lines.]
🆕 New: [the cluster(s) this plan introduces] · Also used: [earlier features this plan uses again, written out in full]
⏱️ Estimate: [n sessions, about h–h hours]

### 1. [Action] · ~1 session
&emsp;&emsp;1.1 [Step: exact path, field values and names; the expected result where it is not obvious]

&emsp;&emsp;1.2 [Step]

💡 How [concept] works here:
- [How it works in this plan, naming the files, assets or steps involved, and why it is built this way.]
- Use it when: [the situations in other projects where this is the tool to reach for.]
- Nearby: [related feature] ([when you would pick it instead]) · [related feature] ([when])

Background: [Concept](../toolbox.md#concept).

**Done when:** [what is true when this task is complete.]

### 2. [Action] · ~1 session
…

📤 When done: [the evidence only the user can provide] and the hours spent.

---
## 🔧 Agent notes
*Bookkeeping and review only — not implementation reading.*
- **Acceptance** (checked at the plan-end review; marked when Verified): [criteria]
- **Known traps**: [short list]
- **Scope guard**: [what this plan deliberately does not include]
- **Environment** verified [date]: [facts the agent checked itself]
- **Review**: [what to inspect at the plan-end review, and the limits of what can be checked]
```

Format rules:

- The user part comes first and carries no bookkeeping; everything after the `---` divider is agent material and can be skipped by the user.
- The user part is target, new and also-used line, estimate, tasks, send line. Plans contain only user actions.
- Tasks are numbered `1`, `2`, …; steps are numbered `1.1`, `1.2`, … under their task, each on its own line indented with `&emsp;&emsp;` (Markdown lists cannot express `1.1`). Each task heading carries its session estimate.
- When the user reports a task done, mark each of its steps ✅ at the start of the step line, before the number (`&emsp;&emsp;✅ 1.1 ...`), append ✅ to the task heading (`### 1. [Action] · ~1 session ✅`), and update the header grid and `next →` in the same pass. Fix steps from the plan-end review are added under the task they belong to, and that task loses its ✅ until they pass.
- Steps are complete every time (see *Step detail*). Explanations are colocated at the step that needs them, never a separate study section before the steps.
- A `💡` tip sits where a new concept or a genuine trap does. Its first bullets say how the concept works in this plan and why it is built this way; then come two fixed bullets: **Use it when** (the situations in other projects where this is the tool to reach for, so the user recognises them later) and **Nearby** (two or three related features this plan does not use, one line each on when one would pick it instead). It ends with `Background:` links to the toolbox. No definitions repeated from the toolbox, no metaphors.
- Each task closes with a `**Done when:**` statement the user can check themselves; the aggregate acceptance list lives in the agent block.
- The send line asks only for evidence the agent cannot produce or inspect itself, plus the hours spent.
- Break it on purpose: where a new concept has a failure that is easy to show, add a short `Try it:` step. The user makes one deliberate change, sees what happens and where it shows, then undoes it. One or two per plan.
- Order steps for live feedback: wire up loading first (references, routes, a running server or watcher), then add content, so every save shows a visible or checkable result. No step leaves the project broken for a later step to fix.
- Everything the user types (code, markup, commands, values) uses only characters on a standard keyboard: `-` not `—`, straight quotes not curly ones, `...` not `…`. Prose may use other characters.
- Every step builds the plan's project or practises one of its features; no steps that exist only for ceremony or bookkeeping.

**Toolbox.** `docs/toolbox.md` is the workspace's concept glossary and the user's index of what exists. Each concept a plan introduces gets one entry, written with the plan: what it is (two or three lines), **Use it when**, **Built in** (links to the plans and tasks that used it), **Nearby** (related features and when to pick each) and **Docs** (a link to the official documentation, checked when written). Later plans link the entry instead of explaining the concept again, and add themselves to **Built in** when they are Verified.
