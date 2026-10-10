# Agentic learning workspace template

A reusable instruction template for creating and maintaining a workspace where the agent implements the project while the user directs, reviews and learns from reading how it is built. It defines the workspace structure, working agreement, learning rhythm, records and plan format. It contains no product requirements or domain-specific content. A companion template (`MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md`) covers workspaces where the user implements and the agent coaches. Optional tooling companions may ship alongside this template — documents covering extra tooling for specific environments (for example, a bridge giving the agent direct access to a project's editor). Provide the applicable companions when the project uses that tooling; they supplement, and do not change, the working agreement.

## 1. How to use this file

Provide this file to the agent temporarily (from its canonical repository or a local download) and explicitly ask it to use the workspace structure. Supply the actual requirements separately. For example:

> Read AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md and use it to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. Present that plan for my approval before starting implementation.

The example invocation does not need to be stored in generated project documentation. The template itself is not retained in generated workspaces by default; a provenance note pointing to its canonical source is enough. Keep a retained copy only if the user asks for one. This template is not an automatically active AGENTS.md and should not be copied verbatim into one.

Generated workspaces record the template's canonical path as a reference (in `docs/MEMORY.md` references and the generated AGENTS.md), never as a local copy. If the recorded path is missing, ask the user for the updated path instead of guessing. When a workspace format or learning-rhythm change is agreed during the project, propose the matching template update so other workspaces inherit it.

The agent applies the process below to the actual workspace, following the applicable instruction hierarchy and the user's current directions. The user can override the workflow, learning rhythm and role defaults at any time. Preserve already-authorized scope instead of asking for the same permission again.

## 2. Default working agreement

- **The agent implements; the user directs and learns.** Within an approved plan the agent performs design within scope, implementation and verification. The user sets direction, approves plans, reviews at boundaries and can take over any task.
- **Plan approval is the execution mandate.** No implementation before the first detailed plan is approved; no next plan before the current one has passed review; the agent does not outrun the user's ability to follow the work.
- **Learning is a first-class outcome.** Every plan's user section explains what is being built and how it works. The agent keeps the work legible: intent before changes, concise evidence after, rationale alongside results. Explain-back, reflection and similar demonstrations are never required.
- **Show the work.** Record actions actually performed and their observed results. Do not equate generated files with working behavior, or a claimed check with an executed one.
- **The user can reclaim the keyboard.** When the user asks to perform a task, the agent switches that task to guided involvement and continues to assist.
- **Preserve existing work.** Do not reset, clean, move or overwrite unrelated material.
- **Repository operations are user-managed by default.** If the user delegates them, record the delegation and its boundaries in `MEMORY.md` conventions and `AGENTS.md`.
- **Irreversible, destructive, costly or externally visible actions** — publishing, external communication, account or purchase operations, deleting work, system-wide changes — require explicit authorization for that action; plan approval is not that authorization. Routine dependency installation required by the approved plan is part of implementation.
- **No sub-agents unless the user or applicable instructions explicitly request them.**
- Keep ongoing guidance concise; answer status check-ins with the current position and next action as pointers.
- The user can stop and resume at any point: the records must stand alone.

## 3. Bootstrap procedure

1. Inspect existing instructions, files, documentation, implementation and repository state; identify what exists before proposing a structure.
2. Determine whether this is one project or a workspace of independently managed projects; use existing organization and user intent.
3. Extract confirmed requirements from the supplied material; keep proposals, assumptions, open questions and observed facts distinct.
4. Calibrate learning: what the user wants to understand, their preferred explanation depth and involvement — recorded in the `MEMORY.md` learning section. Do not invent preferences.
5. Verify what the agent can verify itself — environment, installed tools, filesystem — before authoring plans.
6. Ask only questions that materially affect scope, correctness or the immediate plan; request missing requirements without inventing a product or domain.
7. Preserve useful existing documents; adapt or link them instead of duplicating conflicting versions.
8. Generate the minimum coherent set: `README.md`, `AGENTS.md`, `docs/ROADMAP.md`, `docs/MEMORY.md`, a domain document only when the project has one, and the first detailed plan.
9. Check consistency of links, states and evidence labels; present the first plan for approval before implementation begins.

Scaffolding produces documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless separately requested or already authorized.

## 4. Workspace structure

The same lean file set as the manual variant applies; the difference is the working agreement, the learning rhythm and the plan split between a user-readable build description and an agent execution block.

### Single project

```text
<workspace>/
  README.md                Entry point: purpose, layout, how the workspace works
  AGENTS.md                Agent operating rules, resume routine, boundary rhythm, review protocol
  docs/
    ROADMAP.md             Roadmap, plan states, resume pointer; gates and notes as needed
    MEMORY.md              Decisions, conventions, learning profile, references, history
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
| AGENTS.md | Working agreement, approval gate, boundary rhythm, resume routine, records maintenance | Roadmap, design, transcripts |
| ROADMAP.md | Ordered milestones, plan states, resume pointer, gates, provisional estimates | Detailed tasks for future milestones |
| MEMORY.md | Decisions, conventions, learning profile and concept list, references, history | A second competing roadmap; invented preferences |
| Domain document(s) | Project-specific concept or design that plans refer to | Progress claims |
| Current detailed plan | User part: target, what's being built, scope, build log, review ask. Agent part: execution checklist, acceptance and verification, environment, records | Bookkeeping above the divider |
| Completed plan files | Record of what was planned and delivered | Rewritten history |

Add domain-specific documents only when the actual project needs them. Do not generate empty documents. Optional files omitted from the workspace must also be omitted from navigation links.

## 6. Staged planning rules

- Maintain a broad roadmap and **one current detailed plan**. Do not write future detailed plans during bootstrap.
- Present the first detailed plan for user approval before implementation begins. Plan approval authorizes implementation within that plan's scope, not beyond it.
- Author the next plan only after the current one has passed review and the user confirms.
- Verify what is verifiable before authoring (environment, filesystem, installed tools).
- A plan ends in an observable, result the user can review; its size fits the work and the user's learning pace.
- Split a milestone before authoring its detailed plan when: acceptance depends on later milestones · independent systems share only a final proof · several risky unknowns need early checks · no reviewable result appears within each task group.
- Keep plan IDs stable and monotonically numbered. Completed plan files remain as records.
- Roadmap milestones record what the user will be able to understand or evaluate by their completion.
- Mark the agent checklist items ✅ as they complete; acceptance criteria stay `[ ]` until the plan is Verified, then mark `[x]`.
- Changes to acceptance criteria must be justified and recorded. Never narrow them silently.
- Label estimates as rough and provisional; never invent delivery dates or commitments.
- Fold the previous plan's learnings into the next plan.

## 7. Detailed plan format

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

Format rules:

- The user part comes first and is written for understanding — no bookkeeping. Everything after the divider is agent execution and can be skipped.
- "What's being built" is the learning content: intent, approach, trade-offs, concepts at first use. Deep dives happen on request and may be appended to the build log.
- The build log is written so it stands alone: what changed, why, how to inspect.
- The plan is the approval artifact: the first plan is presented for approval; later plans are authored after review and confirmation.

## 8. Working rhythm: boundaries and briefings

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

## 9. Learning support

- **Default:** the agent implements and explains at boundaries; the user reads plans and asks questions. The user can take over any task (the agent guides step by step) or ask for a deep dive before decisions.
- **Explanation budget:** intent before changes (a few lines); boundary briefings in the format above; build-log notes after; deep dives on request.
- **Concept budget:** introduce one to three major new concepts per working session by default; park extras in the `MEMORY.md` revisit list with enough context to resume.
- **Optional interactions — never obligations:** predict-then-observe, explain-back, tweak-and-observe, guided reproduce, debug drill. A user who reviews by reading and asking questions is fully valid.
- Calibration lives in the `MEMORY.md` learning section; update it as the user's knowledge grows so the resume routine honors it.

## 10. Progress, records and evidence

Plan states:

| State | Meaning |
|---|---|
| Planned | Roadmap entry only; detailed plan not authored |
| Pending | Detailed plan exists; approval or start pending |
| In progress | Plan approved; implementation underway |
| Implemented | Implementation complete with evidence; user review remains |
| Verified | Review passed and applicable observable acceptance has evidence |

- `ROADMAP.md` owns roadmap, plan states and the resume pointer. `MEMORY.md` owns decisions, conventions, the learning profile and concept list, references and history; history entries are labeled `YYYY-MM-DD-NN`.
- Records and compaction are agent-maintained; the user can inspect them. On "compact": condense history; never silently remove decisions, evidence labels or learning records. Correct errors by annotation.
- Evidence categories, kept separate: inspection · executed checks · user-reported checks · not checked. The agent verifies what it can and clearly attributes user observations. Binary or non-text artifacts need suitable evidence — filenames alone are insufficient.
- Match the check to the claim: use the cheapest check that settles it — targeted inspection before full runs — and escalate only when the scenario requires it.
- After meaningful work: update `ROADMAP.md` (states, resume pointer) and `MEMORY.md` (history entry, decisions, learning updates); keep them consistent. No session files.

## 11. Decisions, conventions and sources

All three live in `MEMORY.md`.

- **Decisions:** stable IDs; states Confirmed, Proposed, Deferred, Superseded. One line each with basis and revisit trigger; never silently rewritten. The rationale doubles as teaching material, so keep it precise and self-contained.
- **Conventions:** paths, IDs, naming, markers, evidence labels, repository rules, compaction rules.
- **References:** checked sources with dates and versions; unchecked items labeled as to-verify. Research prefers official/primary sources; documentation about a tool is not evidence that the local environment was tested.

## 12. Resume routine and AGENTS.md

Resume routine: `docs/ROADMAP.md` (roadmap, states, resume pointer) → `docs/MEMORY.md` (decisions, conventions, learning profile, recent history) → the current detailed plan → domain document when design context matters. State the next action as a plan/task pointer and the next boundary; continue from the recorded position.

The generated `AGENTS.md` should include:

1. The working agreement, plan-approval gate and how the user can reclaim tasks.
2. The exact resume reading order with paths that exist in this workspace.
3. Planning rules: one current detailed plan, on-demand authoring, review-before-next-plan.
4. Boundary rhythm and briefing format; where to record changes.
5. Learning configuration: default explanation depth, concept budget and how to change them — link to `MEMORY.md` rather than duplicating volatile details. State that learning interactions are optional and never required.
6. Authorization boundaries for risky, external or costly actions; repository delegation if any.
7. Records maintenance and compaction rules.
8. The plan markers legend (states, `🎯 🧭 📦 📝 📤 ✅ ⬜ 🔧`).
9. Implementation and documentation roots, repository conventions.
10. Known user knowledge and preferences, only when actually supplied.
11. The canonical template path as a reference only, the rule to ask the user when it is missing, and the rule to propose template updates when formats or the learning rhythm change.

Do not copy this entire template into `AGENTS.md`. Do not insert a technology stack, fixed milestone count, domain-specific verification matrix or experience profile unless the user's requirements justify it.

## 13. Final scaffolding audit and handoff

Before reporting the workspace ready, check:

- All supplied requirements are captured without adding unrequested scope; proposals, observations and open questions are distinguishable.
- Single-project versus multi-project structure is coherent and documented.
- Every active project has at most one current detailed plan; completed plans remain intact.
- The first detailed plan is presented for approval before implementation.
- Plans follow the format: user part first (target, what's being built, scope, build log, review ask), agent execution below the divider; the user section is readable without the agent notes.
- Learning calibration reflects what was supplied; no preferences were invented.
- Roadmap IDs, plan states, learning notes, gate definitions and current-plan pointers agree.
- Completed checklist items are ✅; acceptance is `[x]` only for Verified plans.
- Records live only in `ROADMAP.md` and `MEMORY.md`; no stray status, session or duplicate documents.
- The environment the agent can verify was verified before authoring plans.
- Links resolve, tables and fences are valid, and actionable documents have no unresolved boilerplate.
- Evidence labels are honest: only checks actually performed; missing evidence is identified.
- The generated `AGENTS.md` is concise, uses correct paths and agrees with the working role.
- The next action or next boundary is concrete and feasible, or the exact missing prerequisite is identified.

Finish with links to the workspace entry point, roadmap and current plan; state what was created or adapted, what was verified and what remains pending. Do not claim the deliverable is implemented or verified because its documentation has been generated.
