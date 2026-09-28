# Project workspace template

A reusable instruction template for creating and maintaining a single-project or multi-project workspace. It defines the planning process, agent role, documentation and records. It contains no product requirements, technology choices or domain-specific scope.

## 1. How to use this file

Copy this file into a workspace and explicitly ask the agent to use it. Supply the actual requirements separately. For example:

> Read PROJECT_WORKSPACE_TEMPLATE.md and use it to generate or adapt this workspace's documentation and AGENTS.md. Use the requirements I provide separately. Preserve existing work and create only the first detailed plan for each active project. This request is for documentation, not implementation.

The example invocation does not need to be stored in generated project documentation. This template is not an automatically active AGENTS.md and should not be copied verbatim into one.

The agent should apply the process below to the actual workspace. Follow the applicable instruction hierarchy and the user's current directions. The user can override this template's workflow and role defaults. Preserve already-authorized scope instead of asking for the same permission again.

## 2. Default working agreement

- **The user implements.** The agent plans, explains relevant concepts, reviews work, performs authorized verification and maintains records.
- Creating documentation does not authorize creating or rewriting the product, application, assets, implementation configuration or other deliverables described by that documentation.
- If the user requests implementation or fixes, carry out that authorized work and record the changed role/scope when it affects future sessions. Do not repeatedly ask to make edits already requested.
- Explain unfamiliar domain/tool concepts when first needed. Adapt to the user's stated knowledge; do not assume a particular experience level or repeat generic programming lessons unnecessarily.
- Keep ongoing guidance concise. Refer to plan and task IDs instead of restating the whole plan.
- Reviews give concrete findings, locations, consequences, suggested corrections and a way to verify the correction. The user makes corrections unless the agent has been asked to edit.
- Documentation changes and targeted, non-destructive verification are normal agent responsibilities. Installation, publication, external communication and repository operations must stay within the user's authorization.
- Git initialization, remotes, identity settings and commits/pushes are user-managed by default. Do not treat scaffolding permission as permission for these operations.
- Preserve existing work. Do not reset, clean, move or overwrite unrelated material to make it match the template.
- This template does not authorize sub-agents. Delegate only when the user or other applicable instructions explicitly request it.

Use these defaults in the generated AGENTS.md, adjusted only for actual user instructions and relevant workspace constraints.

## 3. Bootstrap procedure

1. Inspect existing instructions, files, documentation, implementation and repository state using focused reads. Identify what already exists before proposing a new structure.
2. Determine whether this is one project or a workspace containing independently managed projects. Use existing organization and user intent. Multiple components of one product do not automatically require separate projects.
3. Identify the active project or projects. If priority is unspecified, establish one initial focus and record it as a proposed default; do not begin every project simultaneously.
4. Extract confirmed requirements from the user's supplied material. Keep recommendations, assumptions, open questions and observed facts distinct.
5. Resolve ordinary organizational choices using available context. Ask only questions whose answers materially affect scope, correctness or the immediate plan. Continue independent documentation work while waiting.
6. If requirements have not been supplied, request them without inventing a product or domain. Neutral scaffolding may still be prepared if useful.
7. Preserve useful existing documents. Adapt or link them instead of duplicating conflicting versions. Do not reorganize an established source tree solely to match an example layout.
8. Generate the minimum coherent documentation set, one detailed plan for each active project, and a session record for the bootstrap work.
9. Check consistency, references and evidence labels. Report the entry point, current plan, next action and any unresolved dependencies.

Scaffolding should normally produce documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless that work is separately requested or already authorized.

## 4. Workspace structure

These are reference layouts. Preserve established naming/layout when it already provides the same responsibilities. Document intentional deviations in conventions.md.

### Single project

```text
<workspace>/
  PROJECT_WORKSPACE_TEMPLATE.md       Optional retained copy of this template
  AGENTS.md                          Concise operational guide
  README.md                          Entry point and navigation
  STATUS.md                          Short current state and next action
  docs/
    README.md                        Documentation index
    brief.md                         Supplied requirements and scope boundaries
    PLAN.md                          Roadmap, dependencies and completion gates
    PROGRESS.md                      Plan states and evidence pointers
    conventions.md                   Paths, naming, workflow and record formats
    decisions.md                     Requirements, choices and open questions
    verification.md                  Verification strategy and acceptance scenarios
    references.md                    Sources and provenance, when needed
    architecture.md                  Design boundaries, when needed
    curriculum.md                    Learning sequence, when useful
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
        decisions.md
        verification.md
        references.md                When needed
        architecture.md              When needed
        curriculum.md                When useful
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

## 5. Document responsibilities

| Document | Owns | Keep out |
|---|---|---|
| README.md | Purpose from user requirements, navigation, layout, starting instructions | Detailed progress history |
| AGENTS.md | Resume routine, agent role, boundaries, review and bookkeeping rules | Full design, full roadmap, session transcripts |
| STATUS.md | Current focus, current plan, next concrete action, material blocker and evidence link | Duplicated detailed acceptance logs |
| brief.md | Supplied requirements, success conditions, included/excluded scope | Invented requirements or unlabelled proposals |
| PLAN.md | Ordered milestones, dependencies, risks and gates | Detailed tasks for every future milestone |
| PROGRESS.md | Authoritative plan states, evidence pointers and resume position | Claims inferred from planned work |
| conventions.md | Paths, stable IDs, terminology, formats and repository conventions | Unrelated technology policy |
| decisions.md | Requirements, choices, assumptions, open questions and rationale | Silent rewriting of decision history |
| verification.md | Appropriate evidence methods, scenarios, environments and completion criteria | Claims that checks have run when they have not |
| references.md | Checked sources, dates, versions and provenance | Unchecked links presented as verified facts |
| architecture.md | Relevant structure, responsibilities, interfaces and data flow | Speculative frameworks without a demonstrated need |
| curriculum.md | Concepts learned through the planned work | A second competing roadmap |
| Current detailed plan | Implementable tasks, acceptance, verification and prerequisites | Unrequested finished implementation |
| Session record | Changes, observations, commands, outcomes and next steps | Unfiltered transcripts or copied secrets |

Add domain-specific documents only when the actual project needs them. Do not generate empty documents for every imaginable system. Optional files omitted from the workspace must also be omitted from its navigation links.

## 6. Staged planning rules

- Maintain a broad roadmap and **one current detailed plan per active project**. Do not write all future detailed plans during bootstrap.
- For an inactive project, a brief, roadmap and status may be enough. Record that it is inactive; do not invent implementation progress.
- Keep plan IDs stable and monotonically numbered within the project. Completed plan files remain as records.
- A plan should end with an observable, reviewable result. Its size should fit the user's learning needs and the complexity of the work, not an arbitrary number of tasks or sessions.
- Outline future work at milestone level. Split an oversized upcoming milestone before authoring its detailed plan, then update dependencies and progress consistently.
- Make prerequisites and verification environments explicit. Address risky assumptions early with a focused experiment or feasibility check.
- Gates should express the evidence needed before dependent work begins. Do not impose a particular prototype, platform, deployment or testing strategy on every project.
- When the user reports completion, review the implementation and evidence. Keep unresolved findings attached to the current plan.
- Author the next detailed plan after the current plan has passed review and its applicable acceptance criteria have evidence, unless the user explicitly changes the sequence.
- Changes to acceptance criteria must be justified and recorded. Never narrow them silently to mark work complete.
- Do not invent delivery dates, effort estimates, versions, tools or design commitments. Label estimates and proposed defaults clearly when useful.

Suggested roadmap table:

```markdown
| Plan ID | Deliverable | Dependencies | Completion evidence |
|---|---|---|---|
```

Choose the number of milestones from the project. There is no fixed milestone count in this template.

## 7. Detailed plan format

Use this structure for each detailed plan. Replace bracketed fields using the actual requirements; do not leave unresolved boilerplate in an actionable plan.

```markdown
# Plan NN — [Short title]

Status: Pending
Project: [Project ID, where useful]
Roadmap entry: [Link]

## Goal

[The observable result of this unit.]

## Scope

[What this unit includes and what is deliberately deferred.]

## Prerequisites

[Required completed plans, knowledge, inputs, tools or environments.]

## Concepts

[Only unfamiliar concepts needed to perform this unit; omit if unnecessary.]

## Tasks

[Mark a finished task by appending ✅ to its heading; leave unfinished tasks unmarked. Keep this consistent with the plan state in PROGRESS.md.]

### 1. [Concrete action]

[Steps, relevant locations and expected intermediate outcome.]

### 2. [Concrete action]

[Continue only as far as this unit requires.]

## Acceptance criteria

- [ ] [Observable criterion tied to the goal.]
- [ ] [Another criterion only if needed.]

## Verification

User: [Checks and evidence the user must provide.]
Agent: [Inspection or commands the agent should perform within authorization.]
Required context: [Environment, version, inputs or configuration that affects interpretation.]
Limits: [What these checks cannot establish, if material.]

## Troubleshooting

[Likely issues and focused diagnostic steps; omit if not useful.]

## Completion and next step

[What review must establish, and which roadmap milestone follows.]
```

Plans may contain small reference examples when they aid understanding. Under the default coaching agreement, they should not conceal a complete product implementation inside documentation.

## 8. Progress and evidence

Use these plan states consistently:

| State | Meaning |
|---|---|
| Planned | Roadmap entry only; detailed plan not authored |
| Pending | Detailed plan exists; implementation has not started |
| In progress | Implementation or correction is underway |
| Done | User reports completion; review or required evidence remains |
| Verified | Review passed and applicable observable acceptance has evidence |

Track project activity separately from plan completion: active, inactive, paused, blocked or complete may describe the project. A blocker should name the missing prerequisite, its effect and the next resolving action. Waiting for the user to implement a pending plan is not automatically a blocker. Do not silently pause, abandon or cancel a project.

Suggested PROGRESS.md format:

```markdown
# Progress — [Project]

Updated: [Date/session]

| Plan | State | Evidence / findings | Next action |
|---|---|---|---|

## Resume pointer

- Current position:
- Current detailed plan:
- Next concrete action:
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

## 9. Decisions, assumptions and sources

Use stable decision IDs scoped to the workspace or project. Label each entry:

- **Confirmed:** an explicit user requirement/choice or directly established fact; identify which and its source.
- **Proposed:** a reversible recommendation that the user has not yet adopted.
- **Deferred:** a question to resolve before named dependent work.
- **Superseded:** a prior decision replaced by a linked later decision, retained for context.

```markdown
| ID | State | Decision / question | Basis and rationale | Revisit trigger / dependent work |
|---|---|---|---|---|
```

Record important assumptions as Proposed, not Confirmed. Distinguish what a source states from a project-specific inference. When a decision changes, update dependent plans/design documents, progress and status so active guidance does not contradict itself.

Research only as needed. When a user asks for current/latest information, or an important fact may have changed, verify it from an appropriate source. Prefer official/primary sources for technical facts. Record checked dates, applicable versions and unresolved discrepancies. Documentation about a tool's behavior is not evidence that the local environment has been tested.

## 10. Sessions and resume routine

Use one session record per meaningful working session. Routine acknowledgments do not need artificial progress entries.

Default naming: sessions/YYYY-MM-DD-NN.md, where NN is a workspace-wide sequence that continues across dates and projects. Inspect the index and existing files before allocating the next ID. Start at 01 in a fresh workspace unless preserving an existing sequence. Never reuse an ID or overwrite an unrelated session.

```markdown
# Session NN — YYYY-MM-DD

- Projects affected:
- Focus:
- Changed:
- Reviewed / commands or actions actually run:
- User-reported verification:
- Findings and unresolved issues:
- Checks not run / evidence limits:
- Decisions changed:
- Next action by project:
```

Session records preserve history; correct errors with an explicit note instead of rewriting an old recommendation as though it had always been current. Append clearly identified follow-up work if continuing the same session.

At the end of meaningful work:

1. Update affected project PROGRESS.md files with actual state and evidence links.
2. Record changed decisions and reconcile dependent documents.
3. Write the session record and add it to sessions/INDEX.md, newest first.
4. Update root STATUS.md with a concise row for each relevant project.
5. Verify these records agree on the current plan, gate state and next action.

Suggested root dashboard:

```markdown
# Status

Updated: [Date/session]

| Project | Activity / state | Current plan | Next action | Blocker / evidence |
|---|---|---|---|---|
```

On resume, the agent reads root STATUS.md, the selected project's PROGRESS.md, its current detailed plan and relevant design/decision documents. Read the session index and relevant recent session only when needed. State the next action briefly, incorporate new user corrections and continue from the recorded position rather than restarting planning.

## 11. Generate a concise AGENTS.md

The generated guide should be project-aware and operational. Include:

1. The user/agent working agreement and how authorized implementation requests change it.
2. The exact resume reading order with paths that exist in this workspace.
3. The one-current-detailed-plan rule and review-before-next-plan process.
4. Known user knowledge/preferences, only when actually supplied.
5. Confirmed constraints or links to their authoritative documents; avoid duplicating long lists of volatile details.
6. Implementation and documentation roots, review methods, source/research expectations and repository conventions that apply here.
7. Evidence rules, session bookkeeping and consistency checks.
8. Scope of repository/external actions and delegation, following the working agreement.

Do not copy this entire template into AGENTS.md. Do not insert a technology stack, fixed milestone count, domain-specific verification matrix or experience profile unless the user's requirements justify it.

## 12. Final scaffolding audit and handoff

Before reporting the workspace ready, check:

- All supplied requirements are captured without adding unrequested scope.
- Confirmed requirements, proposals, observations and unresolved questions are distinguishable.
- Single-project versus multi-project structure is coherent and documented.
- Every active project has at most one current detailed plan; historical verified plans remain intact.
- Roadmap IDs, progress entries, dependencies, gate definitions and current-plan pointers agree.
- Local links and anchors resolve; optional documents are not linked unless created.
- Markdown tables and fences are valid, and generated actionable documents have no unresolved boilerplate.
- Existing work and repository boundaries are preserved; no unrelated implementation or configuration was changed.
- Status, progress and sessions describe only checks actually performed and clearly identify missing evidence.
- Generated AGENTS.md is concise, uses correct paths and agrees with the working role.
- The next action is concrete and feasible, or the exact missing prerequisite is identified.

Finish with links to the workspace entry point, roadmap and current plan; state what was created or adapted, what was verified and what remains pending. Do not claim the product itself is implemented or verified because its documentation has been generated.
