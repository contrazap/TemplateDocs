# Agentic learning workspace template

The **agentic** variant of the workspace template family: the agent implements the project while the user directs, reviews and learns from reading how it is built. Use it together with `WORKSPACE_TEMPLATE_CORE.md`, which holds the shared structure, records, planning, evidence and resume rules; this file adds the working agreement, approval gate, plan format, working rhythm, learning support and the role-specific `AGENTS.md` and audit items, and wins where the two differ. The other variant, `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md`, covers workspaces where the user implements and the agent coaches.

## 1. How to use this file

Provide this file and the core temporarily and ask the agent to use them; supply the requirements separately. For example:

> Read WORKSPACE_TEMPLATE_CORE.md and AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md and use them to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. Present that plan for my approval before starting implementation.

The example invocation does not need to be stored in generated project documentation. Retention, provenance and template-update rules: core section 1 (learning-rhythm changes count as process changes).

## 2. Working agreement

Shared rules: core section 2. In this variant:

- **The agent implements; the user directs and learns.** Within an approved plan the agent performs design within scope, implementation and verification. The user sets direction, approves plans, reviews at boundaries and can take over any task.
- **Plan approval is the execution mandate.** No implementation before the first detailed plan is approved; no next plan before the current one has passed review; the agent does not outrun the user's ability to follow the work. Plan approval authorizes implementation within that plan's scope only — it is not authorization for irreversible, destructive, costly or externally visible actions (publishing, external communication, account or purchase operations, deleting work, system-wide changes). Routine dependency installation required by the approved plan is part of implementation.
- **Learning is a first-class outcome.** Every plan's user section explains what is being built and how it works. The agent keeps the work legible: intent before changes, concise evidence after, rationale alongside results. Explain-back, reflection and similar demonstrations are never required.
- **Show the work.** Record actions actually performed and their observed results.
- **The user can reclaim the keyboard.** When the user asks to perform a task, the agent switches that task to guided involvement and continues to assist.

## 3. Bootstrap additions

- Calibration (core step 3.4): what the user wants to understand, their preferred explanation depth and involvement — recorded in the `MEMORY.md` learning section.
- Handoff: present the first detailed plan for approval before implementation begins.

## 4. Planning additions

- Roadmap milestones record what the user will be able to understand or evaluate by their completion.
- A plan's size also fits the user's learning pace.

## 5. Detailed plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Implemented|Verified]` · `⬜⬜⬜ n/N` · next → N · roadmap: docs/ROADMAP.md

🎯 [Target — the observable result, one or two lines.]

🧭 What's being built — [the agent's approach in readable form: what will be implemented, how it works,
key choices and the concepts involved, explained at first use. This is the user's learning read.]

📦 Scope — ✔ in · ✖ out.

📝 Build log — [appended by the agent as work completes: concise, standalone notes — what changed, why,
how to inspect it. Keeps the user current without interrupting the flow.]

📤 Review — [when and how the user can look at the result: what to run or open; feedback that helps.
Optional hands-on suggestions are never obligations.]

---
## 🔧 Agent execution
*Execution and bookkeeping — not user reading.*
- **Checklist**: [agent tasks with ✅ marks as they complete]
- **Acceptance & verification**: [criteria; how each is checked; limits]
- **Environment / inspect**: [preconditions verified; what review checks]
- **Record**: [what to log at review — decisions, history, learning updates]
```

Format rules (in addition to core section 6):

- The user part is target, what's being built, scope, build log, review ask — written for understanding.
- "What's being built" is the learning content: intent, approach, trade-offs, concepts at first use. Deep dives happen on request and may be appended to the build log.
- The build log is written so it stands alone: what changed, why, how to inspect.
- Mark agent checklist items ✅ as they complete.
- The plan is the approval artifact: the first plan is presented for approval; later plans are authored after review and confirmation.

## 6. Working rhythm: boundaries and briefings

Pause and brief at:

1. Plan boundaries — always (first plan: approval before implementation).
2. The first demonstrable form of a component — when something can be run, viewed or tried.
3. Introduction of a new major concept or unfamiliar toolchain element.
4. Before any risky, irreversible, costly or externally visible action — an authorization point, not just a briefing.
5. When evidence contradicts expectations or an outcome is materially uncertain.
6. When the user asks to pause, review or take over.

Briefing format:

```markdown
Briefing — [plan/task ID, boundary]
- Done: [what is now true]
- Evidence: [command or observation and its result]
- Next: [the immediate next increment]
- Why: [approach chosen; alternatives considered briefly]
- Watch for: [real risks, limitations, open questions]
- Awaiting your confirmation to proceed.
```

Between boundaries the agent continues mechanical or already-explained work and appends build-log notes for later reading. Waiting for the user at a boundary is normal, not a blocker. The user can set stricter (pause every task) or flow (pause at boundaries only) modes; record changes in `MEMORY.md`.

## 7. Learning support

- **Default:** the agent implements and explains at boundaries; the user reads plans and asks questions. The user can take over any task (the agent guides step by step) or ask for a deep dive before decisions.
- **Explanation budget:** intent before changes (a few lines); boundary briefings in the format above; build-log notes after; deep dives on request.
- **Concept budget:** introduce one to three major new concepts per working session by default; park extras in the `MEMORY.md` revisit list with enough context to resume.
- **Optional interactions — never obligations:** predict-then-observe, explain-back, tweak-and-observe, guided reproduce, debug drill. A user who reviews by reading and asking questions is fully valid.
- Calibration lives in the `MEMORY.md` learning section (learning profile and concept list); update it as the user's knowledge grows so the resume routine honors it. Decision rationale doubles as teaching material, so keep it precise and self-contained.

## 8. States

The variant state (core section 7): **Implemented** — implementation complete with evidence; user review remains. Progression: Planned → Pending → In progress → Implemented → Verified. In this variant, Pending means the plan awaits approval or start; In progress means the plan is approved and implementation is underway.

## 9. AGENTS.md additions

Beyond core section 9, the generated `AGENTS.md` includes:

1. The plan-approval gate and how the user can reclaim tasks.
2. Boundary rhythm and briefing format; where to record changes.
3. Learning configuration: default explanation depth, concept budget and how to change them — link to `MEMORY.md` rather than duplicating volatile details. State that learning interactions are optional and never required.
4. The plan markers legend: states Planned → Pending → In progress → Implemented → Verified; `🎯 🧭 📦 📝 📤 ✅ ⬜ 🔧`.

## 10. Audit additions

Beyond core section 10:

- The first detailed plan is presented for approval before implementation.
- Plans follow the format: user part first (target, what's being built, scope, build log, review ask), agent execution below the divider; the user section is readable without the agent notes.
- Learning calibration reflects what was supplied; no preferences were invented.
- Roadmap IDs, plan states, learning notes, gate definitions and current-plan pointers agree.
- The next action or next boundary is concrete and feasible.
