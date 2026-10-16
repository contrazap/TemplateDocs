# Workspace template — core

The shared part of the workspace template family: structure, records, planning, evidence and resume rules that every agent-managed workspace uses, whoever implements. It contains no product requirements or domain-specific content. Always use it together with exactly one **variant**, which sets the working role and everything that depends on it:

- `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` — the user implements; the agent plans, coaches, reviews and maintains records.
- `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md` — the agent implements; the user directs, reviews and learns.
- `AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md` — agents implement end to end, optionally an orchestrator dispatching to cheaper worker agents; the user directs and approves at milestone gates.

Where a variant says something different from this file, the variant wins. Optional tooling companions (for example, a bridge giving the agent direct access to a project's editor) supplement both and do not change the working agreement.

## 1. How to use the template family

Provide this file and the applicable variant to the agent temporarily (from the canonical repository or a local download), explicitly ask it to use the workspace structure, and supply the actual requirements separately. Each variant gives an example invocation.

- The templates are not retained in generated workspaces by default; a provenance note pointing to the canonical source is enough. Keep a retained copy only if the user asks for one. A template is not an automatically active `AGENTS.md` and is never copied verbatim into one.
- Generated workspaces record the canonical path (core + variant) as a reference in `docs/MEMORY.md` references and in the generated `AGENTS.md` — once each, never as a local copy. If the recorded path is missing, ask the user for the updated path instead of guessing.
- When a workspace format or process change is agreed during a project, propose the matching template update so other workspaces inherit it: to this file when it applies to both roles, to the variant when it is role-specific.
- The agent applies the process to the actual workspace, following the applicable instruction hierarchy and the user's current directions. The user can override the workflow and role defaults at any time. Preserve already-authorized scope instead of asking for the same permission again.

## 2. Shared working rules

The variant states the working role; these rules hold in both.

- Records (`ROADMAP.md` states, `MEMORY.md` history, decisions, conventions, the variant's skill or learning record) and their compaction are agent-maintained; the user can inspect them at any time.
- Keep guidance concise: answer status check-ins ("what's next", "current status") with the current position and next action as pointers; keep steps and values in the plan and repeat them only when asked.
- Git, tool installs, publishing and external communication are user-managed unless explicitly delegated or requested; record a delegation and its boundaries in `MEMORY.md` conventions and `AGENTS.md`. Once source control is set up, individual commit/push operations are not tracked in the records — check the repository state directly when needed.
- Irreversible, destructive, costly or externally visible actions require explicit authorization for that action.
- Preserve existing work; do not reset, clean, move or overwrite unrelated material.
- No sub-agents unless the user or applicable instructions explicitly request them.
- The user can stop and resume at any point: the records must stand alone.

## 3. Bootstrap procedure

1. Inspect existing instructions, files, documentation, implementation and repository state; identify what exists before proposing a structure.
2. Determine whether this is one project or a workspace of independently managed projects; use existing organization and user intent.
3. Extract confirmed requirements from the supplied material; keep proposals, assumptions, open questions and observed facts distinct.
4. Apply the variant's calibration step (support levels or learning profile). Do not invent preferences.
5. Verify what the agent can verify itself — environment, installed tools, filesystem — before authoring plans.
6. Resolve ordinary organizational choices from available context; ask only questions that materially affect scope, correctness or the immediate plan. If requirements are missing, request them without inventing a product or domain; neutral scaffolding may still be prepared.
7. Preserve useful existing documents; adapt or link them instead of duplicating conflicting versions.
8. Generate the minimum coherent set: `README.md`, `AGENTS.md`, `docs/ROADMAP.md`, `docs/MEMORY.md`, a domain document only when the project has one (several → `docs/design/` with an index), the first detailed plan, and the agent-client entry files the user's clients need (section 9). No session files, no separate status, conventions, decisions, references or verification documents.
9. Check consistency of links, states and evidence labels; finish with the variant's handoff (section 10).

Scaffolding produces documentation only. Do not create product files, install dependencies, contact external services or initialize source control unless that work is separately requested or already authorized.

## 4. Workspace structure

Preserve established naming and layout when they already provide the same responsibilities; record intentional deviations in `MEMORY.md` conventions.

### Single project

```text
<workspace>/
  README.md                Entry point: purpose, layout, how the workspace works
  AGENTS.md                Agent operating rules, resume routine, role-specific protocol
  CLAUDE.md                Optional client entry file — a pointer to AGENTS.md (section 9)
  docs/
    ROADMAP.md             Roadmap, plan states, resume pointer; gates and notes as needed
    MEMORY.md              Decisions, conventions, skill ledger or learning profile, references, history
    history/YYYY-MM.md     Optional: archived history moved out of MEMORY at compaction (section 7)
    <domain>.md            Project-specific concept or design document(s), as needed
    design/                Optional, when there are several domain docs: README.md index + one doc per system
    tooling-notes.md       Optional: tool recipes and environment reference too long for MEMORY (section 7)
    tooling/               Optional, when several tools need recipes: one file per tool instead of tooling-notes.md
    implementation-plans/
      NN-<name>.md         One current detailed plan; completed plans remain as records
    refs/                  Optional reference library: captures, fetched sets (+ `_sources.md` provenance), generated diagrams
  <delivery-root>/         Implementation lives where the project needs it
```

### Multiple projects

Repeat the `docs/` set per project (for example under `projects/<id>/`), keep the workspace-level `README.md` and `AGENTS.md`, and add a small registry (`PROJECTS.md` or a roadmap section) with one row per project: path, purpose, activity state, current plan link. Enforce one current detailed plan per project. IDs and records are project-scoped; cross-project references use a qualified form such as `<project-id>:plan-03`. Nested `AGENTS.md` files contain only additions, never a copy of the root guide.

## 5. Document responsibilities

| Document | Owns | Keep out |
|---|---|---|
| README.md | Purpose, layout, how the workspace works, where to start — a pointer to `ROADMAP.md` for the current position | Progress state and history (they drift; `ROADMAP.md` owns them) |
| AGENTS.md | Working agreement, resume routine, planning rules, role-specific protocol, records maintenance | Roadmap, design, transcripts |
| Client entry files (`CLAUDE.md` …) | A pointer to `AGENTS.md`; client-only notes | A copy of `AGENTS.md` |
| ROADMAP.md | Ordered milestones, plan states, resume pointer, gates, provisional estimates | Detailed tasks for future milestones; history |
| MEMORY.md | Decisions, conventions, the variant's skill ledger or learning profile, references, recent history | A second competing roadmap; invented preferences; long tool recipes |
| History archive (optional) | Older history entries moved out of MEMORY at compaction, one file per month | Decisions or conventions (those stay in MEMORY) |
| Tooling notes (optional) | Tool recipes, API quirks, environment reference material | Decisions, progress |
| Domain document(s) | Project-specific concept or design that plans refer to — the *what and why*; with several, a `design/README.md` index (one line per doc) | Progress claims; plan steps |
| Current detailed plan | User part first, agent part below the divider — content per the variant's plan format | Bookkeeping above the divider |
| Completed plan files | Record of what was planned and delivered | Rewritten history |

Add domain-specific documents only when the actual project needs them. Do not generate empty documents. Optional files omitted from the workspace must also be omitted from navigation links.

## 6. Staged planning rules

- Maintain a broad roadmap and **one current detailed plan**. Do not write future detailed plans during bootstrap.
- Author the next plan only after the current one has passed review with evidence and the user confirms.
- Verify what is verifiable before authoring (environment, filesystem, installed tools).
- A plan ends in an observable, reviewable result; its size fits the work and the user's pace.
- Split a milestone before authoring its detailed plan when: acceptance depends on later milestones · independent systems share only a final proof · several risky unknowns need early checks · no reviewable result appears within each task group · a first-contact slice (what the next plans immediately depend on) separates cleanly from a completion slice that can wait until those plans need it.
- Design decisions the user may not be able to judge (layout, composition, structure) are drafted by the agent into a spec built from the reference material and corrected by the user; build steps then link that spec so the user judges concrete options instead of inventing.
- Keep plan IDs stable; a split after authoring keeps the number with letter suffixes (`03a`, `03b`), and any divergence between run order and numeric order is stated explicitly (for example under the roadmap table). Completed plan files remain as records.
- Mark finished items ✅ as they complete; acceptance criteria stay `[ ]` until the plan is Verified, then mark `[x]`.
- Changes to acceptance criteria must be justified and recorded. Never narrow them silently.
- Keep future roadmap entries outcome-level; treat their internals as provisional.
- Label estimates as rough and provisional; never invent delivery dates or commitments.
- Fold the previous plan's recorded learnings into the next plan.

Shared plan-format rules (the variant gives the full format):

- The user part comes first and carries no bookkeeping; everything after the `---` divider is agent material and can be skipped by the user.
- Build steps that recreate something visual link the reference or generated diagram that shows it (relative path, for example `../refs/<topic>/…`) so the picture sits inside the step.
- The plan header line carries the state, a progress grid (`⬜`/`✅`), the next item and the roadmap link.
- Plans are agent-neutral: they name files, commands and outcomes, not client-specific tool names, so any supported agent client can execute them.
- Each fact has one home — design docs (what/why), plans (how/now), `MEMORY.md` (decisions, history), `ROADMAP.md` (where we are); other documents link to it (`../design/<doc>.md#<section>`) instead of repeating it.

## 7. Records, states and evidence

Plan states (the fourth state is variant-specific):

| State | Meaning |
|---|---|
| Planned | Roadmap entry only; detailed plan not authored |
| Pending | Detailed plan exists; approval or start pending |
| In progress | Implementation or correction is underway |
| Done (manual) / Implemented (agentic) | See the variant |
| Verified | Review passed and applicable observable acceptance has evidence |

- `ROADMAP.md` owns roadmap, plan states and the resume pointer. `MEMORY.md` owns decisions, conventions, the skill ledger or learning profile, references and history; history entries are labeled `YYYY-MM-DD-NN` (workspace-wide sequence).
- After meaningful work: update `ROADMAP.md` (states, resume pointer) and `MEMORY.md` (history entry, decisions, skill or learning updates); keep them consistent. No session files.
- On the user's "compact": condense history (recent detailed → older one-liners); never silently remove decisions, evidence labels or skill/learning records. Correct errors by annotation, not silent rewriting.

**Record size budget.** The resume routine reads `ROADMAP.md` and `MEMORY.md` every session, so both must stay readable in one pass:

- `MEMORY.md` targets ≤ ~25 KB. History keeps the current plan's entries (at most ~5) detailed, each ≤ ~5 lines; older entries are one line each (label — what happened — outcome, with pointers to decisions or commits). When the file exceeds the budget, compact proactively and say so in the history entry; the compaction rules above still apply.
- Conventions are rules, one or two lines each. Tool recipes, API quirks, long environment inventories and engine/tool reference material go in `docs/tooling-notes.md` (or the applicable companion) with a one-line pointer in Conventions.
- `ROADMAP.md`'s resume block is a few lines: position, current plan, next action, gate. No history — that lives in `MEMORY.md`.
- Long-running workspaces may move older one-line history into `docs/history/YYYY-MM.md` at compaction, leaving one pointer line per archived month in `MEMORY.md`. Archived entries are moved verbatim — never rewritten — and decisions, conventions and evidence labels stay in `MEMORY.md`.
- Other documents have soft budgets so no file becomes the one large document: `AGENTS.md` ~10 KB (recipes move to tooling notes), `ROADMAP.md` ~10 KB (outcome-level only), each domain/design doc ~15 KB (split by system and update the index), each plan ~20 KB (split with letter suffixes, section 6).

Evidence categories, kept separate:

1. **Inspection:** what was read or reviewed and what it supports.
2. **Executed checks:** commands or actions actually run, with context and observed results.
3. **User-reported checks:** what the user says they tested, clearly attributed.
4. **Not checked:** missing environments, omitted scenarios, unresolved findings.

Match the check to the claim: use the cheapest check that settles it — targeted inspection before full runs — and escalate only when the scenario requires it. Distinguish "configured correctly" from "actually works": values visible in the tool's UI are evidenced by user screenshots (user-reported), while heavier runtime or session checks are reserved for claims configuration alone cannot settle — constructed state, runtime wiring, integration, feel. Binary or non-text artifacts need suitable evidence — filenames alone are insufficient. Never equate generated files with working behavior, or a planned check with an executed one.

Visual defects (rendering artifacts, misplaced or missing elements): reproduce before fixing, isolate by toggling the suspect element at runtime, and close only on an executed before/after capture where the tooling allows — "it went away" after an unrelated change is not a closure. Parity checks against a reference (template, earlier version) diff the full property set, not a hand-picked list.

## 8. Decisions, conventions and sources

All three live in `MEMORY.md`.

- **Decisions:** stable IDs scoped to the workspace or project; states Confirmed, Proposed, Deferred, Superseded. One line each: decision, basis, revisit trigger. Never silently rewritten; a superseded decision names its successor. Ratify Proposed decisions once the work they govern is underway. The basis lives in the repository (a history entry or a file in the workspace), not only in an external file.
- **Conventions:** paths, IDs, naming, markers, evidence labels, repository rules (for example which build artifacts to ignore, and an explicit ignore/attribute decision when a new artifact class first appears), compaction rules, supported agent clients; fetched third-party material keeps a provenance note beside it (source, date, usage) and stays reference-only.
- **References:** checked sources with dates and versions; unchecked items labeled as to-verify. Research prefers official/primary sources; documentation about a tool is not evidence that the local environment was tested.

## 9. Resume routine, AGENTS.md and client entry files

Resume routine: `docs/ROADMAP.md` (roadmap, states, resume pointer) → `docs/MEMORY.md` (decisions, conventions, skill ledger or learning profile, recent history) → the current detailed plan → domain documents when design context matters → tooling notes when tool work is next. State the next action as a plan/task pointer and continue from the recorded position; do not restart planning.

The generated `AGENTS.md` includes, beyond the variant's additions:

1. The working agreement (variant) and how the user changes it.
2. The exact resume reading order with paths that exist in this workspace, domain documents named.
3. Planning rules: one current detailed plan, on-demand authoring, verify-before-authoring, review gate before the next plan.
4. Authorization boundaries for risky, external or costly actions; repository delegation if any.
5. Records maintenance, compaction rules and the record size budget.
6. The plan markers legend (variant).
7. Implementation and documentation roots, repository conventions.
8. Known user knowledge and preferences, only when actually supplied.
9. The canonical template path (core + variant) as a reference only, the rule to ask the user when it is missing, and the rule to propose template updates when formats change.

Do not copy the templates into `AGENTS.md`. Do not insert a technology stack, fixed milestone count, domain-specific verification matrix or experience profile unless the user's requirements justify it.

**Client entry files.** `AGENTS.md` is the single source of agent rules. A client that does not read `AGENTS.md` natively gets a thin entry file that points to it, never a copy — Claude Code: a root `CLAUDE.md` whose content is `@AGENTS.md` (the import loads the file), plus client-only notes when there are any. Create entry files only for clients the user actually uses, and record the supported clients in `MEMORY.md` conventions. Tool-server (MCP) configuration is per client and per project (for example OpenCode `opencode.json`, Claude Code `.mcp.json`); when more than one client is supported, keep their entries equivalent — tooling companions give the shapes.

## 10. Final scaffolding audit and handoff

Before reporting the workspace ready, check (plus the variant's additions):

- All supplied requirements are captured without adding unrequested scope; proposals, observations and open questions are distinguishable.
- Single-project versus multi-project structure is coherent and documented.
- Every active project has at most one current detailed plan; completed plans remain intact; future milestones stay outcome-level.
- Completed items are ✅; acceptance is `[x]` only for Verified plans; states agree with `ROADMAP.md`.
- Records live only in `ROADMAP.md` and `MEMORY.md` (plus optional tooling notes and history archive); no stray status, session or duplicate documents; records and documents are within their size budgets.
- The README holds no progress state; the roadmap's resume block is current.
- The environment the agent can verify was verified before authoring plans.
- Links resolve, tables and fences are valid, and actionable documents have no unresolved boilerplate.
- Evidence labels are honest: only checks actually performed; missing evidence is identified.
- The generated `AGENTS.md` is concise, uses correct paths and agrees with the working role; client entry files point to it.
- The next action is concrete and feasible, or the exact missing prerequisite is identified.

Finish with links to the workspace entry point, roadmap and current plan; state what was created or adapted, what was verified and what remains pending. Do not claim the deliverable is implemented or verified because its documentation has been generated.
