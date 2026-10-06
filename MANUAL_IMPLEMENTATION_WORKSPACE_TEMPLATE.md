# Manual implementation workspace template

A reusable instruction template for creating and maintaining a workspace where the user implements the work while the agent plans, coaches, reviews and maintains records. It defines the workspace structure, working agreement, records and plan format. It contains no product requirements or domain-specific content. A companion template (`AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md`) covers workspaces where the agent implements while the user directs and learns.

## 1. How to use this file

Provide this file to the agent temporarily (from its canonical repository or a local download) and explicitly ask it to use the workspace structure. Supply the actual requirements separately. For example:

> Read MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md and use it to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. This request is for documentation, not implementation.

The example invocation does not need to be stored in generated project documentation. The template itself is not retained in generated workspaces by default; a provenance note pointing to its canonical source is enough. Keep a retained copy only if the user asks for one. This template is not an automatically active AGENTS.md and should not be copied verbatim into one.

Generated workspaces record the template's canonical path as a reference (in `docs/MEMORY.md` references and the generated AGENTS.md), never as a local copy. If the recorded path is missing, ask the user for the updated path instead of guessing. When a workspace format or process change is agreed during the project, propose the matching template update so other workspaces inherit it.

The agent applies the process below to the actual workspace, following the applicable instruction hierarchy and the user's current directions. The user can override the workflow and role defaults. Preserve already-authorized scope instead of asking for the same permission again.

## 2. Default working agreement

- **The user implements.** The agent plans, explains concepts when first needed, reviews work, performs authorized verification and maintains the records.
- Records (`ROADMAP.md` states, `MEMORY.md` history, decisions, skill ledger) and their compaction are agent-maintained by default; the user can inspect them at any time.
- Creating or rewriting project code, assets, levels or configuration requires an explicit user request; documentation and non-destructive checks are normal agent work.
- Explain unfamiliar domain/tool concepts at first use and adapt to the user's stated knowledge; do not repeat generic lessons the user's background covers.
- Keep guidance concise: answer status check-ins ("what's next", "current status") with the current position and next action as pointers; keep steps and values in the plan and repeat them only when asked.
- Reviews give finding, location, consequence, suggested correction and a way to verify. The user applies corrections unless the agent has been asked to edit.
- Git, tool installs, publishing and external communication are user-managed unless explicitly delegated or requested.
- Preserve existing work; do not reset, clean, move or overwrite unrelated material.
- No sub-agents unless the user or applicable instructions explicitly request them.
- The user can stop and resume at any point: the records must stand alone.

## 3. Bootstrap procedure

1. Inspect existing instructions, files, documentation, implementation and repository state; identify what exists before proposing a structure.
2. Determine whether this is one project or a workspace of independently managed projects; use existing organization and user intent.
3. Extract confirmed requirements from the supplied material; keep proposals, assumptions, open questions and observed facts distinct.
4. Verify what the agent can verify itself — environment, installed tools, filesystem — so plans carry only user actions.
5. Resolve ordinary organizational choices from available context; ask only questions that materially affect scope, correctness or the immediate plan.
6. If requirements are missing, request them without inventing a product or domain; neutral scaffolding may still be prepared.
7. Preserve useful existing documents; adapt or link them instead of duplicating conflicting versions.
8. Generate the minimum coherent set: `README.md`, `AGENTS.md`, `docs/ROADMAP.md`, `docs/MEMORY.md`, a domain document only when the project has one, and the first detailed plan. No session files, no separate status, brief, conventions, decisions, references or verification documents.
9. Check consistency of links, states and evidence labels; report the entry point, current plan and next action.

Scaffolding produces documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless that work is separately requested or already authorized.

## 4. Workspace structure

Preserve established naming/layout when it already provides the same responsibilities; record intentional deviations in `MEMORY.md` conventions.

### Single project

```text
<workspace>/
  README.md                Entry point: purpose, layout, how the workspace works
  AGENTS.md                Agent operating rules, resume routine, review protocol
  docs/
    ROADMAP.md             Roadmap, plan states, resume pointer; gates and notes as needed
    MEMORY.md              Decisions, conventions, skill ledger, references, history
    <domain>.md            Project-specific concept or design document(s), as needed
    implementation-plans/
      NN-<name>.md         One current detailed plan; completed plans remain as records
    refs/                  Optional reference images (created when generated)
  <delivery-root>/         Implementation lives where the project needs it
```

### Multiple projects

Repeat the `docs/` set per project (for example under `projects/<id>/`), keep the workspace-level `README.md` and `AGENTS.md`, and add a small registry (`PROJECTS.md` or a roadmap section) with one row per project: path, purpose, activity state, current plan link. Enforce one current detailed plan per project. IDs and records are project-scoped; cross-project references use a qualified form such as `<project-id>:plan-03`. Nested `AGENTS.md` files contain only additions, never a copy of the root guide.

## 5. Document responsibilities

| Document | Owns | Keep out |
|---|---|---|
| README.md | Purpose, layout, how the workspace works, where to start | Progress history |
| AGENTS.md | Working agreement, resume routine, planning rules, review protocol, records maintenance | Roadmap, design, transcripts |
| ROADMAP.md | Ordered milestones, plan states, resume pointer, gates, provisional estimates | Detailed tasks for future milestones |
| MEMORY.md | Decisions, conventions, skill ledger, references, history (session entries) | A second competing roadmap; invented preferences |
| Domain document(s) | Project-specific concept or design that the plan refers to | Progress claims |
| Current detailed plan | User part: target, tasks, send line. Agent part: acceptance, known traps, scope guard, environment, inspection, limits, record | Unrequested finished implementation |
| Completed plan files | Record of what was planned and delivered | Rewritten history |

Add domain-specific documents only when the actual project needs them. Do not generate empty documents. Optional files omitted from the workspace must also be omitted from navigation links.

## 6. Staged planning rules

- Maintain a broad roadmap and **one current detailed plan**. Do not write future detailed plans during bootstrap.
- Author the next plan only after the current one is reviewed with evidence and the user confirms.
- Verify what is verifiable before authoring (environment, filesystem, installed tools). Plans contain only user actions.
- A plan ends in an observable, reviewable result; its size fits the work and the user's learning pace.
- Split a milestone before authoring its detailed plan when: acceptance depends on later milestones · independent systems share only a final proof · several risky unknowns need early checks · no meaningful result is runnable or inspectable within each task group.
- Keep plan IDs stable and monotonically numbered. Completed plan files remain as records.
- Mark a finished step with ✅ leading its line, and a finished task by appending ✅ to its heading once its checkpoint passes; acceptance criteria stay `[ ]` until the plan is Verified, then mark `[x]`.
- Changes to acceptance criteria must be justified and recorded. Never narrow them silently.
- Keep future roadmap entries outcome-level; treat their internals as provisional.
- Label estimates as rough and provisional; never invent delivery dates or commitments.
- Fold the previous plan's recorded learnings into the next plan.

## 7. Detailed plan format

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

Format rules:

- The user part comes first: target, tasks, send line. Everything after the divider is agent bookkeeping and can be skipped once implementation is done.
- Tasks are numbered `1`, `2`, …; steps are numbered `1.1`, `1.2`, … under their task, each on its own line indented with `&emsp;&emsp;` — Markdown lists cannot express `1.1`.
- Tasks are actions. Use exact steps where the tooling is first-time (support levels, section 8); explanations are colocated at the step that needs them — never a separate study section before the steps.
- Each task closes with a `**Done when:**` statement; the aggregate acceptance list lives in the agent block.
- The send line asks only for evidence the agent cannot produce or inspect itself.
- Known traps and verified environment let the agent answer quickly and cold-start safely.

### Task anatomy

- **Why (optional):** one line linking the task to the target, only when non-obvious.
- **Steps:** ordered, concrete actions. Exact editor paths, menu names and field values at L1; less hand-holding as the level drops.
- **Code:** task-scoped deltas only — file path, anchor, the lines to add/replace/delete, clearly marked. A complete file only when the task creates that small file. Explain only APIs the user has not met.
- **Done when:** what is true, visible or runnable when the task is complete; add an evidence hint where non-obvious.

## 8. Support levels and graduated coaching

Task detail adapts to demonstrated skill, not a fixed global setting:

| Level | Use when | Detail |
|---|---|---|
| L1 Guided | First occurrence of a skill | Exact steps and field values; code deltas with short per-line explanations; intermediate results stated. |
| L2 Supported | One clean repetition completed | Concrete steps and expected result; code described (signature, location, behavior); snippet on request or for a genuinely new API. |
| L3 Independent | Two clean repetitions completed | Goal, constraints and acceptance; snippets only for genuinely new APIs; the agent reviews the result. |

- Record the skill, evidence and current level in the `MEMORY.md` skill ledger. The recorded level drives task detail; task headings carry no level label.
- A clean repetition means the task was completed and its checkpoint passed without correction. If the user struggles or the task introduces a new API, teach that occurrence one level more detailed, then return to the recorded level after a clean repetition.
- Levels are per skill; a plan may mix them. Adjust remaining task detail when checkpoint evidence warrants; record changes at review.
- Support levels change presentation detail only. Acceptance criteria and verification requirements never change with the level.

## 9. Progress, records and evidence

Plan states:

| State | Meaning |
|---|---|
| Planned | Roadmap entry only; detailed plan not authored |
| Pending | Detailed plan exists; implementation has not started |
| In progress | Implementation or correction is underway |
| Done | User reports completion; review or required evidence remains |
| Verified | Review passed and applicable observable acceptance has evidence |

- `ROADMAP.md` owns roadmap, plan states and the resume pointer. `MEMORY.md` owns decisions, conventions, the skill ledger, references and history; history entries are labeled `YYYY-MM-DD-NN` (workspace-wide sequence).
- After meaningful work: update `ROADMAP.md` (states, resume pointer) and `MEMORY.md` (history entry, decisions, ledger); keep them consistent. No session files.
- On the user's "compact": condense history (recent detailed → older one-liners); never silently remove decisions, evidence labels or skill levels. Correct errors by annotation, not silent rewriting.

Evidence categories, kept separate:

1. **Inspection:** what was read or reviewed and what it supports.
2. **Executed checks:** commands or actions actually run, with context and observed results.
3. **User-reported checks:** what the user says they tested, clearly attributed.
4. **Not checked:** missing environments, omitted scenarios, unresolved findings.

Standard review protocol: the user provides run evidence (short clip or screenshots, what was tested, versions); the agent inspects `.uproject`-style project files, configuration and structure where the domain allows, and reviews user-provided evidence of behavior. Binary or non-text artifacts (compiled assets, graphs, levels) need suitable user evidence — filenames alone are insufficient. Never equate generated files with working behavior or a planned check with an executed one.

Record review findings with a stable identifier when follow-up requires it:

```markdown
| Finding | Severity / consequence | Location | Suggested correction | Verification | State |
|---|---|---|---|---|---|
```

## 10. Decisions, conventions and sources

All three live in `MEMORY.md`.

- **Decisions:** stable IDs scoped to the workspace or project; states Confirmed, Proposed, Deferred, Superseded. One line each: decision, basis, revisit trigger. Never silently rewritten.
- **Conventions:** paths, IDs, naming, markers, support levels, evidence labels, repository rules (for example which build artifacts to ignore) and compaction rules.
- **References:** checked sources with dates and versions; unchecked items are labeled as to-verify. Research prefers official/primary sources; documentation about a tool's behavior is not evidence that the local environment was tested.

## 11. Resume routine and AGENTS.md

Resume routine: `docs/ROADMAP.md` (roadmap, states, resume pointer) → `docs/MEMORY.md` (decisions, conventions, ledger, recent history) → the current detailed plan → domain document when design context matters. State the next action as a plan/task pointer and continue from the recorded position; do not restart planning.

The generated `AGENTS.md` should include:

1. The working agreement and how authorized implementation requests change it.
2. The exact resume reading order with paths that exist in this workspace.
3. Planning rules: one current detailed plan, on-demand authoring, verify-before-authoring, review gate before the next plan.
4. Coaching: support levels, ledger location, how detail adapts.
5. The review protocol and evidence categories.
6. Records maintenance and compaction rules.
7. The plan markers legend (states, `🎯 💡 ✅ ⬜ 📤 🔧`, `**Done when:**` checkpoints).
8. Implementation and documentation roots, repository conventions.
9. Known user knowledge and preferences, only when actually supplied.
10. The canonical template path as a reference only, the rule to ask the user when it is missing, and the rule to propose template updates when workspace formats change.

Do not copy this entire template into `AGENTS.md`. Do not insert a technology stack, fixed milestone count, domain-specific verification matrix or experience profile unless the user's requirements justify it.

## 12. Final scaffolding audit and handoff

Before reporting the workspace ready, check:

- All supplied requirements are captured without adding unrequested scope; proposals, observations and open questions are distinguishable.
- Single-project versus multi-project structure is coherent and documented.
- Every active project has at most one current detailed plan; completed plans remain intact.
- The current plan is one coherent slice; future milestones stay outcome-level; the next plan is gated on review plus user confirmation.
- Plans follow the format: user part first (target, tasks, send line), agent notes below the divider; explanations are colocated, not study sections.
- Task detail matches the recorded support levels; headings carry no level label; acceptance criteria are unchanged by level.
- Completed steps and tasks are marked ✅; acceptance is `[x]` only for Verified plans; states agree with `ROADMAP.md`.
- Records live only in `ROADMAP.md` and `MEMORY.md`; no stray status, session or duplicate documents.
- The environment the agent can verify was verified; plans contain only user actions.
- Links resolve, tables and fences are valid, and actionable documents have no unresolved boilerplate.
- Evidence labels are honest: only checks actually performed; missing evidence is identified.
- The generated `AGENTS.md` is concise, uses correct paths and agrees with the working role.
- The next action is concrete and feasible, or the exact missing prerequisite is identified.

Finish with links to the workspace entry point, roadmap and current plan; state what was created or adapted, what was verified and what remains pending. Do not claim the product is implemented or verified because its documentation has been generated.
