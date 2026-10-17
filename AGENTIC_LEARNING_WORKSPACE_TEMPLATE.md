# Agentic learning workspace template

The **agentic** variant of the workspace template family: the agent implements the project while the user directs, reviews and learns from reading how it is built — what was implemented, which decisions were made and why, and what was tried along the way. Use it together with `WORKSPACE_TEMPLATE_CORE.md`, which holds the shared structure, records, planning, evidence and resume rules; this file adds the working agreement, approval gate, plan format, working rhythm with briefings and milestone demos, learning support with hands-on offers, and the role-specific `AGENTS.md` and audit items, and wins where the two differ. The other variants: `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` (the user implements, the agent coaches) and `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` (agents implement end to end; the user approves at milestone gates).

## 1. How to use this file

Provide this file and the core temporarily and ask the agent to use them; supply the requirements separately. For example:

> Read WORKSPACE_TEMPLATE_CORE.md and AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md and use them to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. Present that plan for my approval before starting implementation.

The example invocation does not need to be stored in generated project documentation. Retention, provenance and template-update rules: core section 1 (learning-rhythm changes count as process changes).

## 2. Working agreement

Shared rules: core section 2. In this variant:

- **The agent implements; the user directs and learns.** Within an approved plan the agent performs design within scope, implementation and verification. The user sets direction, approves plans, reviews at boundaries and can take over any task.
- **Plan approval is the execution mandate.** No implementation before the first detailed plan is approved; no next plan before the current one has passed review; the agent does not outrun the user's ability to follow the work. Plan approval authorizes implementation within that plan's scope only — it is not authorization for irreversible, destructive, costly or externally visible actions (publishing, external communication, account or purchase operations, deleting work, system-wide changes). Routine dependency installation required by the approved plan is part of implementation.
- **Learning is a first-class outcome.** Every plan's user section explains what is being built and how it works, and every boundary leaves a written briefing: what is done, what was decided and why, what was tried and dropped. The agent keeps the work legible: intent before changes, concise evidence after, rationale alongside results. Explain-back, reflection and similar demonstrations are never required.
- **Show the work.** Record actions actually performed and their observed results.
- **The user can reclaim the keyboard.** When the user asks to perform a task, the agent switches that task to guided involvement and continues to assist.
- **The agent offers hands-on tasks; the user decides.** When doing a task by hand would teach a skill the project keeps needing, or would simply be faster than the agent's tools, the agent offers it together with an alternative (section 7). Declining needs no reason; the agent then does the task.

## 3. Bootstrap additions

- Calibration (core step 3.4), recorded in the `MEMORY.md` learning section: what the user wants to understand, explanation depth, pause mode (section 6) and appetite for hands-on tasks (section 7). Start from the core's default user profile; record only what the user states beyond it.
- Handoff: present the first detailed plan for approval before implementation begins.

## 4. Planning additions

- Roadmap milestones record what the user will be able to see, run or evaluate by their completion; that is what the milestone demo shows (section 6).
- Checklist tasks have IDs (`T1`, `T2`, …) and an owner: the agent by default, the user only for an accepted hands-on offer. Offers are made when the plan is authored, so the user approves them with the plan.
- Where the project defines verification levels (core section 7), each checklist task names one.
- When repository operations are delegated, commit once per completed task as `[P<NN>-T<n>] <title>` and push each commit right away, record-only commits included, so the remote always matches the records. The build log cites the hash, so each change and the decision behind it can be inspected as a diff.
- Items only the user can do — accounts, logins, purchases, installs that need an interactive session, taste calls — go to a **📤 Needs you** section in `ROADMAP.md`, one line each: `- [ ] [Item] — why · needed by Plan NN / T<n> · effort ≈ [minutes/hours]`. The agent continues with unblocked work meanwhile. Optional hands-on offers live in the plan, not in this queue.

## 5. Detailed plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Implemented|Verified]` · `⬜⬜⬜ n/N` · next → T<n> · roadmap: ../ROADMAP.md

🎯 [Target — the observable result, one or two lines.]

🧭 What's being built — [the agent's approach in readable form: what will be implemented, how it works,
key choices and the concepts involved, explained at first use with a link to the glossary entry.
This is the user's learning read.]

📦 Scope — ✔ in · ✖ out.

🙋 Hands-on (optional) — [tasks offered to the user: task · why it is worth doing by hand · effort ≈ … ·
alternative. An accepted task gets its guided steps here. Omit the section when nothing is offered.]

📝 Build log — [appended by the agent as work completes: concise, standalone notes — what changed, why,
how to inspect it (file, command, commit); decisions taken (IDs); approaches tried and dropped, with the
evidence that ruled them out.]

📣 Briefings — [each boundary briefing, appended verbatim and dated (section 6); the last plan of a
milestone ends with the milestone demo.]

📤 Review — Judge: [what the user is asked to judge — behavior, look, feel, whether the explanation holds
up — and what to run or open] · Already verified: [what the agent checked, with evidence].

---
## 🔧 Agent execution
*Execution and bookkeeping — not user reading.*
- **Checklist**: [T1 … Tn — owner (agent | user), verification level where defined, ✅ as they complete]
- **Acceptance & verification**: [criteria; how each is checked; limits]
- **Environment / inspect**: [preconditions verified; what review checks]
- **Record**: [what to log at review — decisions, history, learning updates]
```

Format rules (in addition to core section 6):

- The user part is target, what's being built, scope, hands-on offers, build log, briefings, review — written for understanding and readable without the agent block.
- "What's being built" is the learning content: intent, approach, trade-offs, concepts at first use. A concept's lasting explanation goes into the glossary (core section 5) the first time it appears; later plans link it instead of re-explaining. Deep dives happen on request and may be appended to the build log.
- The build log stands alone: what changed, why, how to inspect. Dead ends are recorded, not erased (core section 8).
- Briefings are the plan's summary layer: a reader who skips the build log still knows what happened, what was decided and why.
- The review separates judgment from verification. The user is asked only for judgments that need no tool, framework or engine expertise; technical correctness is the agent's responsibility and comes with evidence.
- Mark checklist tasks ✅ as they complete.
- The plan is the approval artifact: the first plan is presented for approval; later plans are authored after review and confirmation.

## 6. Working rhythm: boundaries, briefings and demos

Pause and brief at:

1. Plan boundaries — always (first plan: approval before implementation).
2. The first demonstrable form of a component — when something can be run, viewed or tried.
3. Introduction of a new major concept or unfamiliar toolchain element (one the `MEMORY.md` concept list does not mark familiar).
4. Before any risky, irreversible, costly or externally visible action — an authorization point, not just a briefing.
5. When evidence contradicts expectations or an outcome is materially uncertain.
6. When the user asks to pause, review or take over.

Briefing format:

```markdown
Briefing — [plan/task ID, boundary] · [YYYY-MM-DD]
- Done: [what is now true]
- Evidence: [command or observation and its result; level where defined]
- Decisions: [IDs new or changed — choice, why, rejected alternatives; or "none"]
- Tried and dropped: [approach — the evidence that ruled it out; omit when none]
- Next: [the immediate next increment and why this approach]
- Watch for: [real risks, limitations, open questions]
- Hands-on: [a task offered to the user, if any (section 7)]
- Awaiting your confirmation to proceed.
```

The agent presents the briefing and appends it unchanged to the plan's 📣 section. Answers to status check-ins between boundaries are not briefings and are not recorded.

**Milestone demo.** At the end of a milestone's last plan, the boundary briefing is a demo, written so the user can walk through the milestone cold or replay it later:

```markdown
Demo — M<x> [title] · [YYYY-MM-DD]
- Show: [steps to run or open, in order, and what each one should show]
- Built: [the milestone's plans, one line each, linked]
- Decisions: [the milestone's decisions — ID, choice, why, rejected alternatives]
- Tried and dropped: [the dead ends that shaped the result]
- Changed from plan: [deviations from the roadmap or acceptance, with reasons]
- Evidence: [key checks and results; captures linked]
- Concepts: [concepts met in the milestone, glossary-linked]
- Open: [risks, open questions, known limitations]
- Next: [the next milestone and what it will make demonstrable]
```

The demo is stored in that plan's 📣 section and linked from the milestone's row in `ROADMAP.md`.

Between boundaries the agent continues mechanical or already-explained work and appends build-log notes for later reading. Waiting for the user at a boundary is normal, not a blocker. Pause modes: **boundary** (default) pauses at all six points; **flow** pauses only at 1, 4, 5 and 6 — points 2 and 3 are still briefed in writing in the 📣 section, and the next pause summarizes them; **strict** also pauses after every task. Record mode changes in `MEMORY.md`.

## 7. Learning support and hands-on offers

- **Default:** the agent implements and explains at boundaries; the user reads plans and asks questions. The starting point is the core's default user profile — a programmer new to this project's stack. The user can take over any task (the agent guides step by step) or ask for a deep dive before decisions.
- **Explanation budget:** intent before changes (a few lines); boundary briefings in the format above; build-log notes after; deep dives on request.
- **Concept budget:** introduce one to three major new concepts per working session by default; park extras in the `MEMORY.md` revisit list with enough context to resume. The budget paces explanation, not implementation: approved work that relies on a parked concept still proceeds, and the build log names the concept so the user can follow up.
- **Concept record:** the glossary (core section 5) holds each concept's explanation; the `MEMORY.md` concept list records the user's familiarity with each (new · met · familiar), which drives pause point 3 and hands-on offers.
- **Other optional interactions — never obligations:** predict-then-observe, explain-back, guided reproduce, debug drill. A user who reviews by reading and asking questions is fully valid.
- Calibration lives in the `MEMORY.md` learning section (learning profile, concept list, hands-on record); update it as the user's knowledge grows so the resume routine honors it. Decision rationale doubles as teaching material, so keep it precise and self-contained.

**Hands-on offers.** The agent proposes that the user do a task by hand when either holds:

- **Learning leverage:** the task is a core workflow of the stack that later roadmap milestones need again, the user has not done it before, and it is small (about 30 minutes or less).
- **Faster by hand:** the task is interactive and slow or unreliable through the agent's tools — placing and adjusting things visually, tuning values by feel, playtesting, UI work that needs a mouse.

Never offered: mechanical, bulk or boilerplate work; anything the agent does reliably in moments; tasks whose only lesson is generic programming. Items only the user can do are needs-you items, not offers (section 4).

Each offer names the task, why it is worth the user's time, the rough effort and the alternatives:

- **Guided:** the user does it from exact steps in the plan; the agent then reviews it (finding, location, suggested correction, how to check) and records the evidence as user-reported plus agent inspection.
- **Watch, then vary:** the agent does it and records the steps in the build log; the user then makes one small change and observes the effect.
- **Agent does it:** with the usual build-log note.

Offers are made when the plan is authored — one or two per plan by default, as calibrated — or, when discovered mid-plan, in the next briefing; never as an interruption. Step detail graduates with the user's record: the first time, exact steps and values; after one clean repetition, steps and the expected result; after two, goal and acceptance only; after that the agent stops offering that skill unless the user asks. The hands-on record in `MEMORY.md` lists each skill, how often it was done and its current detail.

## 8. States

The variant state (core section 7): **Implemented** — implementation complete with agent evidence; the user's review remains. Progression: Planned → Pending → In progress → Implemented → Verified. In this variant, Pending means the plan awaits approval or start; In progress means the plan is approved and implementation is underway.

## 9. AGENTS.md additions

Beyond core section 9, the generated `AGENTS.md` includes:

1. The plan-approval gate, how the user can reclaim tasks, and hands-on offers: criteria, alternatives, the per-plan default and graduation.
2. Boundary rhythm, pause modes, briefing and milestone-demo formats, and the rule that briefings are recorded in the plan's 📣 section; where to record mode changes.
3. Learning configuration: default explanation depth, concept budget, glossary path and how to change them — link to `MEMORY.md` rather than duplicating volatile details. State that learning interactions and hands-on offers are optional and never required.
4. The needs-you queue in `ROADMAP.md` and, when repository operations are delegated, the per-task commit-and-push convention.
5. The plan markers legend: states Planned → Pending → In progress → Implemented → Verified; `🎯 🧭 📦 🙋 📝 📣 📤 ✅ ⬜ 🔧`.

## 10. Audit additions

Beyond core section 10:

- The first detailed plan is presented for approval before implementation.
- Plans follow the format: user part first (target, what's being built, scope, hands-on offers when any, build log, briefings, review), agent execution below the divider; the user section is readable without the agent notes.
- The review asks the user only for judgments that need no tool expertise; technical claims carry agent evidence.
- Learning calibration starts from the core default and reflects only what was supplied; no prior knowledge or preferences were assumed.
- Every briefing given is recorded in its plan; each completed milestone ends with a demo linked from `ROADMAP.md`.
- Roadmap IDs, plan states, learning notes, gate definitions, the needs-you queue and current-plan pointers agree.
- The next action or next boundary is concrete and feasible.
