# Agentic learning workspace template

A reusable instruction template for creating and maintaining a workspace where an agent implements the project while the user's knowledge of the approach and implementation develops alongside it. It defines the planning process, working agreement, learning rhythm, documentation and records. It contains no product requirements, technology choices or domain-specific scope.

## 1. How to use this file

Provide this file to the agent temporarily (from its canonical repository or a local download) and explicitly ask it to use the workspace structure. Supply the actual requirements separately. For example:

> Read AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md and use it to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. Present that plan for my approval before starting implementation.

The example invocation does not need to be stored in generated project documentation. The template itself is not retained in generated workspaces by default; a provenance note pointing to its canonical source is enough. Keep a retained copy only if the user asks for one. This template is not an automatically active AGENTS.md and should not be copied verbatim into one.

Generated workspaces record the template's canonical path as a reference (in `references.md` provenance and the generated AGENTS.md), never as a local copy. If the recorded path is missing, ask the user for the updated path instead of guessing. When a workspace format or learning-rhythm change is agreed during the project, propose the matching template update so other workspaces inherit it.

The agent should apply the process below to the actual workspace. Follow the applicable instruction hierarchy and the user's current directions. The user can override this template's workflow, learning rhythm and role defaults at any time. Preserve already-authorized scope instead of asking for the same permission again.

## 2. Default working agreement

- **The agent implements; the user directs and learns.** Within the approved current detailed plan, the agent performs design within scope, implementation, documentation and authorized verification. The user sets direction, approves plans, reviews at boundaries and can take over any task.
- **Plan approval is the execution mandate.** The agent does not start implementation before the first detailed plan is approved, does not start the next plan before the current plan has passed review, and does not outrun the user's ability to follow the work.
- **Learning is a first-class outcome.** Every plan states what the user should be able to explain or do afterwards. The agent keeps the implementation legible: intent before changes, concise evidence after, rationale alongside results.
- **Record the collaboration style.** Learning outcomes describe what the plan covers, not what the user must demonstrate. Record the user's role and preferred briefing depth when they are supplied — for example a project-manager or client collaborator at granular/technical depth who wants full technical detail at each task boundary and reviews by reading and asking questions. Reflection, explain-back and similar demonstrations are never required unless the user asks for them.
- **Pause and brief at meaningful boundaries.** Under the default balanced rhythm (section 8), the agent ends its turn with a concise briefing — what is done, what comes next, why, and what to watch for — and waits for the user's confirmation. Reflection prompts are optional; the user is never required to answer.
- **Respect the explanation and concept budgets** (section 9). Explain unfamiliar concepts at first use, adapt to the user's stated knowledge, and do not repeat generic lessons. Deeper explanations happen on request.
- **Show the work.** Record exact commands or actions performed, observed output and files affected. Do not equate generated files with working behavior, or a claimed check with an executed one.
- **The user can reclaim the keyboard.** When the user asks to perform a task, the agent switches that task to paired or practice involvement and continues to assist within its role.
- **Preserve existing work.** Do not reset, clean, move or overwrite unrelated material to make it match this template.
- **Repository operations are user-managed by default.** If the user sets up the repository and informs the agent at workspace start that repository operations are delegated, the agent may commit and push at agreed boundaries with clear messages. Record the delegation and its boundaries in conventions.md and AGENTS.md.
- **Irreversible, destructive, costly or externally visible actions** — publishing, external communication, account or purchase operations, deleting work, system-wide changes — require explicit authorization for that action. Plan approval is not that authorization.
- Routine dependency installation required by the approved plan is part of implementation when it stays within the project's environment policy. Account-bound, paid or security-sensitive changes require explicit permission.
- **Sub-agents are used only when the user or other applicable instructions explicitly request them.**
- **Keep ongoing guidance concise.** Refer to plan and task IDs instead of restating the whole plan.

Use these defaults in the generated AGENTS.md, adjusted only for actual user instructions and relevant workspace constraints.

## 3. Bootstrap procedure

1. Inspect existing instructions, files, documentation, implementation and repository state using focused reads. Identify what already exists before proposing a new structure.
2. Determine whether this is one project or a workspace containing independently managed projects. Use existing organization and user intent. Multiple components of one product do not automatically require separate projects.
3. Identify the active project or projects. If priority is unspecified, establish one initial focus and record it as a proposed default; do not begin every project simultaneously.
4. Extract confirmed requirements from the user's supplied material. Keep recommendations, assumptions, open questions and observed facts distinct.
5. Calibrate learning. Ask only questions whose answers materially affect planning: relevant background, learning goals, desired depth per area, and preferred involvement and pace. Record the answers in learning.md. Continue independent documentation work while waiting.
6. Resolve ordinary organizational choices using available context. Ask only questions that materially affect scope, correctness or the immediate plan.
7. If requirements have not been supplied, request them without inventing a product or domain. Neutral scaffolding may still be prepared if useful.
8. Preserve useful existing documents. Adapt or link them instead of duplicating conflicting versions. Do not reorganize an established source tree solely to match an example layout.
9. Generate the minimum coherent documentation set, learning.md, one detailed plan for each active project, and a session record for the bootstrap work.
10. Check consistency, references and evidence labels. Report the entry point, current plan, proposed involvement level, next action and any unresolved dependencies.
11. Present the first detailed plan for approval before implementation begins.

Scaffolding produces documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless that work is separately requested or already authorized.

## 4. Workspace structure

These are reference layouts. Preserve established naming/layout when it already provides the same responsibilities. Document intentional deviations in conventions.md.

### Single project

```text
<workspace>/
  AGENTS.md                          Concise operational guide
  README.md                          Entry point and navigation
  STATUS.md                          Short current state and next action
  docs/
    README.md                        Documentation index
    brief.md                         Supplied requirements and scope boundaries
    PLAN.md                          Roadmap, dependencies, learning outcomes and completion gates
    PROGRESS.md                      Plan states, learning states and evidence pointers
    learning.md                      Calibration, involvement, concept map and revisit list
    conventions.md                   Paths, naming, workflow and record formats
    decisions.md                     Requirements, choices and open questions with rationale
    verification.md                  Verification strategy and acceptance scenarios
    references.md                    Sources and provenance, when needed
    architecture.md                  Design boundaries, when needed
    implementation-plans/
      01-<short-name>.md              Only the current detailed plan initially
  sessions/
    INDEX.md                         Newest-first session links
    YYYY-MM-DD-NN.md                  Session evidence and continuation notes
  <existing-or-chosen-delivery-root>/ Implementation lives where the project needs it
```

### Multiple projects

```text
<workspace>/
  AGENTS.md                          Shared operational rules
  README.md                          Workspace entry point
  STATUS.md                          One summary row per project
  PROJECTS.md                        Project registry and cross-project relationships
  docs/
    README.md                        Shared and project-document navigation
    conventions.md                   Shared record/naming conventions
    decisions.md                     Cross-project decisions only
  projects/
    <project-id>/
      README.md                      Project entry point
      AGENTS.md                      Optional project-specific additions only
      docs/
        README.md
        brief.md
        PLAN.md
        PROGRESS.md
        learning.md
        decisions.md
        verification.md
        references.md                When needed
        architecture.md              When needed
        implementation-plans/
          01-<short-name>.md          Only for an active project
      <delivery-root>/               Existing or suitable implementation layout
  sessions/
    INDEX.md                         One workspace-wide session index
    YYYY-MM-DD-NN.md                  Identifies every affected project
```

For multiple existing repositories, keep their boundaries and use a registry linking to them; do not move them into projects/ merely to match this tree. Record which root owns each plan and evidence file. Use portable relative paths where possible and label external paths when they are unavoidable.

In the multi-project layout:

- Root STATUS.md summarizes; each project's PROGRESS.md owns its plan states. Avoid a second detailed progress ledger at the root.
- Sessions are workspace-wide by default. Each project links to its relevant sessions. One session may cover several projects, with separate findings and next actions for each.
- PROJECTS.md records project ID, path, purpose from supplied requirements, activity state, current priority, dependencies and document links.
- Plan IDs are local to a project. Cross-project references use a qualified form such as `<project-id>:plan-03` and include a link.
- Shared decisions describe cross-project agreements. Local documents link to those decisions rather than copying them as independent defaults.
- Add a workspace coordination roadmap only if dependencies or sequencing justify it. It must link to project plans instead of duplicating their task lists.
- A nested AGENTS.md should contain only relevant additions or explicitly scoped differences. Do not repeat the root guide in every project.
- learning.md is per project. Cross-project learning objectives are recorded in PROJECTS.md or the coordination roadmap only when they exist.

## 5. Document responsibilities

| Document | Owns | Keep out |
|---|---|---|
| README.md | Purpose from user requirements, navigation, layout, starting instructions | Detailed progress history |
| AGENTS.md | Resume routine, working agreement, boundaries, review and bookkeeping rules | Full design, full roadmap, session transcripts |
| STATUS.md | Current focus, current plan, next concrete action, material blocker and evidence link | Duplicated detailed acceptance logs |
| brief.md | Supplied requirements, success conditions, included/excluded scope | Invented requirements or unlabelled proposals |
| PLAN.md | Ordered milestones, learning outcomes, dependencies, risks and gates | Detailed tasks for every future milestone |
| PROGRESS.md | Authoritative plan states, learning states, evidence pointers and resume position | Claims inferred from planned work |
| learning.md | Calibration, involvement defaults, target depth per area, concept map, encounter plan and revisit list | A second competing roadmap or invented preferences |
| conventions.md | Paths, stable IDs, terminology, formats, repository and authorization conventions | Unrelated technology policy |
| decisions.md | Requirements, choices, assumptions, open questions, alternatives and rationale | Silent rewriting of decision history |
| verification.md | Appropriate evidence methods, scenarios, environments and completion criteria | Claims that checks have run when they have not |
| references.md | Checked sources, dates, versions and provenance | Unchecked links presented as verified facts |
| architecture.md | Relevant structure, responsibilities, interfaces and data flow | Speculative frameworks without a demonstrated need |
| Current detailed plan | Implementable tasks, checkpoints, acceptance, verification, prerequisites and learning notes | Unrequested finished implementation |
| Session record | Changes, observations, commands, outcomes, learning activity and next steps | Unfiltered transcripts or copied secrets |

Add domain-specific documents only when the actual project needs them. Do not generate empty documents for every imaginable system. Optional files omitted from the workspace must also be omitted from its navigation links.

## 6. Staged planning rules

- Maintain a broad roadmap and **one current detailed plan per active project**. Do not write all future detailed plans during bootstrap.
- For an inactive project, a brief, roadmap entry and status may be enough. Record that it is inactive; do not invent implementation progress.
- Present the first detailed plan for user approval before implementation begins. Plan approval authorizes implementation within that plan's scope, not beyond it.
- Keep plan IDs stable and monotonically numbered within the project. Completed plan files remain as records.
- A plan should end with an observable, reviewable result. Its size should fit the work and the user's learning pace, not an arbitrary number of tasks or sessions.
- Outline future work at milestone level. Split an oversized upcoming milestone before authoring its detailed plan, then update dependencies and progress consistently.
- Make prerequisites and verification environments explicit. Address risky assumptions early with a focused experiment or feasibility check.
- Gates should express the evidence needed before dependent work begins. Do not impose a particular prototype, platform, deployment or testing strategy on every project.
- Each roadmap milestone records the learning outcome the user should reach by its completion.
- Author the next detailed plan after the current plan has passed review and its applicable acceptance criteria have evidence, unless the user explicitly changes the sequence.
- Changes to acceptance criteria must be justified and recorded. Never narrow them silently to mark work complete.
- Do not invent delivery dates, effort estimates, versions, tools or design commitments. Label estimates and proposed defaults clearly when useful.

Suggested roadmap table:

```markdown
| Plan ID | Deliverable | Learning outcome | Dependencies | Completion evidence |
|---|---|---|---|---|
```

Choose the number of milestones from the project. There is no fixed milestone count in this template.

## 7. Detailed plan format

Use this structure for each detailed plan. Replace bracketed fields using the actual requirements; do not leave unresolved boilerplate in an actionable plan.

```markdown
# Plan NN — [Short title]

Status: Pending
Project: [Project ID, where useful]
Roadmap entry: [Link]
Involvement level: [Default | observe | explain | pair | practice]
Learning outcomes: [What the user should be able to explain or do after this plan]

## Goal

[The observable result of this unit.]

## Scope

[What this unit includes and what is deliberately deferred.]

## Prerequisites

[Required completed plans, knowledge, inputs, tools or environments.]

## Concepts

[Only unfamiliar concepts needed to perform this unit. For each: why it matters here, target depth (awareness or working), and a source for later reading. Omit when nothing unfamiliar is involved.]

## Tasks

[Tags: `[core]` for tasks explained in depth, `[mechanical]` for routine work summarized in batches, `[your-turn]` for tasks offered to the user. Boundaries follow the balanced rhythm by default (section 8). Mark a finished task by appending `(done)` to its heading; leave unfinished tasks unmarked. Keep this consistent with the plan state in PROGRESS.md.]

### 1. [Concrete action] [core]

Intent: [Approach and alternatives considered, in a few lines.]

[Steps, relevant locations and expected intermediate outcome.]

Checkpoint: [Boundary type, when it differs from the default policy.]
Evidence: [Command, inspection or observation that shows the outcome.]

### 2. [Concrete action] [mechanical]

[Continue only as far as this unit requires.]

## Acceptance criteria

- [ ] [Observable criterion tied to the goal.]
- [ ] [Another criterion only if needed.]

## Verification

Agent: [Checks the agent performs during and after implementation.]
User: [Checks and observations that need the user, if any.]
Required context: [Environment, version, inputs or configuration that affects interpretation.]
Limits: [What these checks cannot establish, if material.]

## Learning notes

[Appended by the agent as work completes: a concise, standalone record of what was done, why this approach was taken and how it fits, so the user can read it later without interrupting the flow. Evidence and acceptance criteria remain in their own sections.]

## Troubleshooting

[Likely issues and focused diagnostic steps; omit if not useful.]

## Completion and next step

[What review must establish, a short teachable summary of what was built and why, and which roadmap milestone follows.]
```

Plans may contain small reference examples when they aid understanding. A plan should not conceal a complete product implementation inside documentation; the implementation lives in the delivery root and its evidence is recorded normally.

## 8. Working rhythm: boundaries and briefings

The default balanced rhythm decides when implementation pauses for the user. Pause and brief at:

1. Plan boundaries — always.
2. The first demonstrable form of a component — when something can be run, viewed or tried.
3. Introduction of a new major concept or unfamiliar toolchain element.
4. Before any risky, irreversible, costly or externally visible action — this is an authorization point, not just a briefing.
5. When evidence contradicts expectations or a task's outcome is materially uncertain.
6. When the user asks to pause, review or take over.

Between these, the agent continues through mechanical or already-explained work without pausing, and appends a catch-up note to the plan's Learning notes for later reading. Waiting for the user at a boundary is normal and is not a blocker.

Briefing format:

```markdown
Briefing — [plan/task ID, boundary]
- Done: [what is now true]
- Evidence: [command or observation and its result]
- Next: [the immediate next increment]
- Why: [approach chosen; alternatives considered briefly]
- Watch for: [risks, limitations, open questions — only real ones]
- Awaiting your confirmation to proceed.
```

The briefing is concise and specific; it is not a transcript or a lecture. Concision means no filler, not omitted technical substance: when the user requests it, briefings carry the files and locations touched, structures involved, exact commands and observed results, and alternatives considered, without summarizing them away. The agent ends its turn and does not continue until the user confirms or redirects. Confirmation can be as short as "continue".

The user can change strictness per plan or temporarily: stricter (pause at every task) or flow (pause only at plan boundaries and authorization points, with catch-up notes). Record changes in learning.md or the plan. Under flow, boundary types 4 and 5 always apply.

At a plan boundary, the agent presents the teachable summary of what was built and why, invites questions, and records the learning state. User understanding is not a gate unless the user asks for one. Absent feedback, the agent records what was covered and proceeds only after confirmation.

## 9. Learning support

Involvement levels (project default, overridable per plan and per task):

| Level | The agent | The user |
|---|---|---|
| Observe | Implements, with terse narration and batched recaps | Reads recaps; asks when needed |
| Explain | Implements, giving intent, result context and rationale at each boundary | Reads, asks, confirms |
| Pair | Handles setup, boilerplate and harder steps | Performs designated steps with step-by-step guidance |
| Practice | Reviews, verifies and corrects | Implements the task |

The default is explain. Record the project default in learning.md and any plan or task override in the plan.

Explanation budget:

- Pre-task intent: a few lines covering approach and alternatives.
- Watch-for notes: a few lines when genuinely useful.
- Boundary briefings: the format in section 8, essentials only.
- Recaps and learning notes: concise, with file:line references where useful.
- Deep dives: on request; may be appended to Learning notes or a reference document.

Concept budget: introduce at most one to three major new concepts per working session by default. Park additional topics in the revisit list with enough context to resume later. The user can raise or lower this budget.

Learning interactions are optional suggestions, never obligations. A plan may suggest one at a natural point: predict-then-observe, explain-back, tweak-and-observe, guided-reproduce, debug drill or what-would-you-check-next. The user may skip without comment. No hands-on activity is mandatory. A user who prefers to review by reading briefings and asking questions, without ever explaining back, is a valid explain-level collaborator; record that preference in learning.md and do not treat it as an unmet learning objective.

Catch-up notes: written into the plan's Learning notes when a pause is batched or skipped. Each note stands alone: what changed, why, how to inspect it. They never interrupt the flow and never replace required evidence.

Calibration: adjust involvement, depth targets, budgets and interactions as the user's knowledge grows. Record changes in learning.md so the resume routine honors them.

## 10. Progress and evidence

Use these plan states consistently:

| State | Meaning |
|---|---|
| Planned | Roadmap entry only; detailed plan not authored |
| Pending | Detailed plan exists; approval or start pending |
| In progress | Plan approved; implementation underway |
| Implemented | Implementation complete with evidence; user review remains |
| Verified | Review passed and applicable observable acceptance has evidence |

Track learning per plan separately with a light-touch, user-owned state:

| State | Meaning |
|---|---|
| — | No concepts introduced yet |
| Introduced | Concepts were explained during the plan |
| Practiced | The user has seen or performed relevant activity |
| Checked | The user confirmed or discussed understanding to their satisfaction |

Absence of checked is not a blocker. Update these states from actual events and conversations, not assumptions.

Track project activity separately from plan completion: active, inactive, paused, blocked or complete may describe the project. A blocker should name the missing prerequisite, its effect and the next resolving action. Waiting for user confirmation at a boundary is not automatically a blocker. Do not silently pause, abandon or cancel a project.

Suggested PROGRESS.md format:

```markdown
# Progress — [Project]

Updated: [Date/session]

| Plan | State | Learning | Evidence / findings | Next action |
|---|---|---|---|---|

## Resume pointer

- Current position:
- Current detailed plan:
- Current involvement level:
- Next concrete action:
- Boundary awaiting confirmation:
- Review findings still open:
- Verification completed:
- Checks not run / limitations:
- Gate state:
- Latest session:
```

Keep evidence categories separate:

1. **Inspection:** what was read or reviewed and which conclusions that supports.
2. **Executed checks:** exact commands or actions actually performed, relevant context and observed results.
3. **User-reported checks:** what the user says they tested, clearly attributed.
4. **Not checked:** unavailable environments, omitted scenarios, unresolved findings or limitations.

Do not equate generated files with working behavior, a successful automated check with full acceptance, or a planned check with an executed one. Visual, physical, interactive, distributed or operational behavior needs suitable evidence when it is part of the requirements. Review binary/non-text artifacts through appropriate tools or user-provided evidence; filenames alone are insufficient.

Use the smallest set of checks that provides adequate confidence. Add automated tests where they protect meaningful behavior; do not install a framework just to validate documentation. Re-run checks affected by changes or unresolved findings rather than repeating unrelated checks.

Record review findings with a stable identifier when follow-up requires it:

```markdown
| Finding | Severity / consequence | Location | Suggested correction | Verification | State |
|---|---|---|---|---|---|
```

## 11. Decisions, assumptions and sources

Use stable decision IDs scoped to the workspace or project. Label each entry:

- **Confirmed:** an explicit user requirement/choice or directly established fact; identify which and its source.
- **Proposed:** a reversible recommendation that the user has not yet adopted.
- **Deferred:** a question to resolve before named dependent work.
- **Superseded:** a prior decision replaced by a linked later decision, retained for context.

```markdown
| ID | State | Decision / question | Basis and rationale | Revisit trigger / dependent work |
|---|---|---|---|---|
```

Record implementation rationale at the level a learner would need: what was chosen, which alternatives were considered and why, and what would change the choice. This log doubles as teaching material, so keep it precise and self-contained.

Record important assumptions as Proposed, not Confirmed. Distinguish what a source states from a project-specific inference. When a decision changes, update dependent plans/design documents, progress and status so active guidance does not contradict itself.

Research only as needed. When a user asks for current/latest information, or an important fact may have changed, verify it from an appropriate source. Prefer official/primary sources for technical facts. Record checked dates, applicable versions and unresolved discrepancies. Documentation about a tool's behavior is not evidence that the local environment has been tested.

## 12. Sessions and resume routine

Use one session record per meaningful working session. Routine acknowledgments do not need artificial progress entries.

Default naming: sessions/YYYY-MM-DD-NN.md, where NN is a workspace-wide sequence that continues across dates and projects. Inspect the index and existing files before allocating the next ID. Start at 01 in a fresh workspace unless preserving an existing sequence. Never reuse an ID or overwrite an unrelated session.

```markdown
# Session NN — YYYY-MM-DD

- Projects affected:
- Focus:
- Involvement level in effect:
- Implemented (files / artifacts):
- Boundaries briefed and user confirmations:
- Evidence (commands or actions run and observed results):
- User-reported verification:
- Concepts introduced:
- User hands-on or learning interactions:
- Questions raised and answered:
- Findings and unresolved issues:
- Checks not run / evidence limits:
- Decisions changed:
- Revisit list changes:
- Next action by project:
```

Session records preserve history; correct errors with an explicit note instead of rewriting an old recommendation as though it had always been current. Append clearly identified follow-up work if continuing the same session.

At the end of meaningful work:

1. Update affected project PROGRESS.md files with actual state, learning state and evidence links.
2. Record changed decisions and reconcile dependent documents.
3. Append or update Learning notes where new material was covered or a catch-up was deferred.
4. Write the session record and add it to sessions/INDEX.md, newest first.
5. Update learning.md if calibration, involvement or budgets changed.
6. Update root STATUS.md with a concise row for each relevant project.
7. Verify these records agree on the current plan, boundary state and next action.

Suggested root dashboard:

```markdown
# Status

Updated: [Date/session]

| Project | Activity / state | Current plan | Next action | Blocker / evidence |
|---|---|---|---|---|
```

On resume, the agent reads root STATUS.md, the selected project's PROGRESS.md, learning.md, its current detailed plan and relevant design/decision documents. Read the session index and relevant recent session only when needed. State the next action briefly, incorporate new user corrections and continue from the recorded position rather than restarting planning. Confirm the next boundary before proceeding.

## 13. Generate a concise AGENTS.md

The generated guide should be project-aware and operational. Include:

1. The working agreement, plan-approval gate, boundary confirmation and how the user can reclaim tasks.
2. The exact resume reading order with paths that exist in this workspace.
3. The one-current-detailed-plan rule and review-before-next-plan process.
4. Learning configuration that applies here: involvement defaults, boundary strictness, briefing detail level, budgets and how to change them; link to learning.md rather than duplicating volatile details. Record the user's collaboration role and review style when supplied (e.g., a project manager/client wanting full technical detail at every task boundary), and state that learning interactions and explain-back are optional and never required.
5. The canonical template path as a reference only, the rule to ask the user when it is missing, and the rule to propose template updates when this workspace's formats or learning rhythm change.
6. Known user knowledge/preferences, only when actually supplied.
7. Confirmed constraints or links to their authoritative documents; avoid duplicating long lists of volatile details.
8. Implementation and documentation roots, review methods, source/research expectations, repository conventions and whether repository operations are delegated.
9. Evidence rules, session bookkeeping and consistency checks.
10. Authorization boundaries for risky, external or costly actions, and the delegation scope.

Do not copy this entire template into AGENTS.md. Do not insert a technology stack, fixed milestone count, domain-specific verification matrix or experience profile unless the user's requirements justify it.

## 14. Final scaffolding audit and handoff

Before reporting the workspace ready, check:

- All supplied requirements are captured without adding unrequested scope.
- Confirmed requirements, proposals, observations and unresolved questions are distinguishable.
- Single-project versus multi-project structure is coherent and documented.
- Every active project has at most one current detailed plan; historical verified plans remain intact.
- Roadmap IDs, learning outcomes, progress entries, learning states, dependencies, gate definitions and current-plan pointers agree.
- learning.md reflects calibration actually provided; no preferences were invented.
- Local links and anchors resolve; optional documents are not linked unless created.
- Markdown tables and fences are valid, and generated actionable documents have no unresolved boilerplate.
- Existing work and repository boundaries are preserved; no unrelated implementation or configuration was changed.
- Status, progress and sessions describe only checks actually performed and clearly identify missing evidence.
- Generated AGENTS.md is concise, uses correct paths and agrees with the working role and learning defaults.
- The first detailed plan is presented for approval, and the next action is concrete and feasible or the exact missing prerequisite is identified.

Finish with links to the workspace entry point, roadmap and current plan; state what was created or adapted, what was verified and what remains pending. Do not claim the deliverable itself is implemented or verified because its documentation has been generated.
