# Manual implementation workspace template

The **manual** variant of the workspace template family: the user implements the work while the agent plans, coaches, reviews and maintains records. Use it together with `WORKSPACE_TEMPLATE_CORE.md`, which holds the shared structure, records, planning, evidence and resume rules; this file adds the working agreement, plan format, support levels, review protocol and the role-specific `AGENTS.md` and audit items, and wins where the two differ. The other variant, `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md`, covers workspaces where the agent implements.

## 1. How to use this file

Provide this file and the core temporarily and ask the agent to use them; supply the requirements separately. For example:

> Read WORKSPACE_TEMPLATE_CORE.md and MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md and use them to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. This request is for documentation, not implementation.

The example invocation does not need to be stored in generated project documentation. Retention, provenance and template-update rules: core section 1.

## 2. Working agreement

Shared rules: core section 2. In this variant:

- **The user implements.** The agent plans, explains concepts when first needed, reviews work, performs authorized verification and maintains the records, including the skill ledger.
- Creating or rewriting project code, assets, levels or configuration requires an explicit user request; documentation and non-destructive checks are normal agent work.
- Explain unfamiliar domain/tool concepts at first use and adapt to the user's stated knowledge; do not repeat generic lessons the user's background covers.
- Reviews give finding, location, consequence, suggested correction and a way to verify. The user applies corrections unless the agent has been asked to edit.

## 3. Bootstrap additions

- Calibration (core step 3.4): seed the `MEMORY.md` skill ledger from what the user supplied; unknown skills start at L1.
- Verification (core step 3.5) exists so plans carry only user actions.
- Handoff: report the entry point, current plan and next action.

## 4. Detailed plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Done|Verified]` · `⬜⬜⬜⬜⬜⬜⬜ n/N` · next → N · roadmap: docs/ROADMAP.md

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

Format rules (in addition to core section 6):

- The user part is target, tasks, send line. Plans contain only user actions.
- Tasks are numbered `1`, `2`, …; steps are numbered `1.1`, `1.2`, … under their task, each on its own line indented with `&emsp;&emsp;` — Markdown lists cannot express `1.1`.
- Mark a finished step ✅ leading its line, and a finished task by appending ✅ to its heading once its checkpoint passes.
- Tasks are actions. Use exact steps where the tooling is first-time (support levels, section 5); explanations are colocated at the step that needs them — never a separate study section before the steps.
- Each task closes with a `**Done when:**` statement; the aggregate acceptance list lives in the agent block.
- The send line asks only for evidence the agent cannot produce or inspect itself.
- Known traps and verified environment let the agent answer quickly and cold-start safely.

### Task anatomy

- **Why (optional):** one line linking the task to the target, only when non-obvious.
- **Steps:** ordered, concrete actions. Exact editor paths, menu names and field values at L1; less hand-holding as the level drops.
- **Code:** task-scoped deltas only — file path, anchor, the lines to add/replace/delete, clearly marked. A complete file only when the task creates that small file. Explain only APIs the user has not met.
- **Done when:** what is true, visible or runnable when the task is complete; add an evidence hint where non-obvious.

## 5. Support levels and graduated coaching

Task detail adapts to demonstrated skill, not a fixed global setting:

| Level | Use when | Detail |
|---|---|---|
| L1 Guided | First occurrence of a skill | Exact steps and field values; code deltas with short per-line explanations; intermediate results stated. |
| L2 Supported | One clean repetition completed | Concrete steps and expected result; code described (signature, location, behavior); snippet on request or for a genuinely new API. |
| L3 Independent | Two clean repetitions completed | Goal, constraints and acceptance; snippets only for genuinely new APIs; the agent reviews the result. |

- Record the skill, evidence and current level in the `MEMORY.md` skill ledger. The recorded level drives task detail; task headings carry no level label.
- A clean repetition means the task was completed and its checkpoint passed without correction. If the user struggles or the task introduces a new API, teach that occurrence one level more detailed, then return to the recorded level after a clean repetition.
- For a first occurrence whose deliverable spans many similar units (zones, screens, systems), checkpoint after each unit — build it, look at it, short check — rather than only at the task's end.
- Levels are per skill; a plan may mix them. Adjust remaining task detail when checkpoint evidence warrants; record changes at review.
- Support levels change presentation detail only. Acceptance criteria and verification requirements never change with the level.

## 6. States and review protocol

The variant state (core section 7): **Done** — the user reports completion; review or required evidence remains. Progression: Planned → Pending → In progress → Done → Verified.

Standard review protocol: the user provides run evidence (short clip or screenshots, what was tested, versions); the agent inspects project files, configuration and structure where the domain allows, and reviews user-provided evidence of behavior. Binary or non-text artifacts (compiled assets, graphs, levels) need suitable user evidence.

Record review findings with a stable identifier when follow-up requires it:

```markdown
| Finding | Severity / consequence | Location | Suggested correction | Verification | State |
|---|---|---|---|---|---|
```

## 7. AGENTS.md additions

Beyond core section 9, the generated `AGENTS.md` includes:

1. How authorized implementation requests change the working agreement.
2. Coaching: support levels, ledger location, how detail adapts.
3. The review protocol and evidence categories.
4. The plan markers legend: states Planned → Pending → In progress → Done → Verified; `🎯 💡 ✅ ⬜ 📤 🔧`; `**Done when:**` checkpoints.

## 8. Audit additions

Beyond core section 10:

- The current plan is one coherent slice; the next plan is gated on review plus user confirmation.
- Plans follow the format: target, tasks, send line, agent notes below the divider; explanations are colocated, not study sections; plans contain only user actions.
- Task detail matches the recorded support levels; headings carry no level label; acceptance criteria are unchanged by level.
