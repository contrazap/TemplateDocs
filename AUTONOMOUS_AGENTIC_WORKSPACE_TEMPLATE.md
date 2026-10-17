# Autonomous agentic workspace template

The **autonomous** variant of the workspace template family. Agents implement the project end to end; the user directs, makes taste calls and approves work at milestone gates. Use it together with `WORKSPACE_TEMPLATE_CORE.md`, which holds the shared structure, records, planning, evidence and resume rules. This file adds the working agreement, the roles and orchestrated mode, the plan format (task cards), how verification levels apply, guard rails, the needs-you queue, and the role-specific `AGENTS.md` and audit items. Where this file and the core differ, this file wins.

How it differs from the other variants:

- `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md`: the agent implements, the user learns, and there are approval gates at every plan. The autonomous variant has no learning budget. Gates sit at milestones, and plans inside an approved milestone advance on agent evidence.
- `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md`: the user implements.

Optional companions: `AGENT_ORCHESTRATION.md` (an orchestrator client dispatching task cards to a cheaper worker client), `UNREAL_TEST_AUTOMATION.md` (verification levels for Unreal Engine), `UNREAL_MCP_BRIDGE.md`, `BLENDER_MCP_BRIDGE.md` and `ASSET_GENERATION_PIPELINE.md`.

## 1. How to use this file

Provide this file and the core temporarily, together with the companions the project uses, and supply the requirements separately. For example:

> Read WORKSPACE_TEMPLATE_CORE.md, AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md and the companions <list>, and use them to generate this workspace's documentation and AGENTS.md from the requirements I provide. Preserve existing work. Author only the first detailed plan and present it for approval.

The example invocation does not need to be stored in generated documentation. Retention, provenance and template-update rules: core section 1.

## 2. Working agreement

Shared rules: core section 2. In this variant:

- **Agents implement; the user directs.** Inside an approved milestone, agents design within scope, implement, verify, author the next plan and keep the records. The user approves the roadmap and each milestone, judges results at milestone gates, makes taste calls (look, feel, layout, naming of player-facing things) and handles the items in the needs-you queue (section 9).
- **Milestone approval is the execution mandate.** It covers implementation inside that milestone's scope, routine dependency installs the plans need, and editor or tool lifecycle actions that `AGENTS.md` lists (for example opening and closing the project's editor). It never covers irreversible, destructive, costly or externally visible actions: publishing, pushing (unless delegated), external communication, accounts, purchases, API spend beyond the recorded budget, deleting work, or system-wide changes. Each of those needs explicit authorization.
- **Repository delegation** is recorded in `AGENTS.md` and `MEMORY.md` conventions when the user grants it. A typical delegation lets the orchestrator commit locally once per verified task, while pushing stays with the user.
- **Show the work.** Plans carry a build log, gates carry a briefing, and evidence is recorded honestly (core section 7).
- **The user can step in at any time:** pause, take over a task, change a decision or tighten the gates. Record changes to the cadence in `MEMORY.md`.

## 3. Roles and orchestrated mode

Three roles. The session prompt names the role; `AGENTS.md` defines each one and the default role for each agent client.

| Role | Does | Never |
|---|---|---|
| **Orchestrator** | Runs the resume routine, authors and splits plans, dispatches task cards, verifies results, commits (when delegated), keeps the records, briefs the user at gates | Hands judgment-only work to a worker (below) |
| **Implementer** | Executes exactly one task card: reads the card and the design sections it links, changes the listed files, runs the card's verification, writes a report | Edits records (`ROADMAP.md`, `MEMORY.md`, plan states), commits, pushes, widens scope |
| **Reviewer** | Audits a finished plan or milestone against its acceptance and the design docs; reports findings | Changes code while reviewing |

**Orchestrated mode (default when a worker client is configured).** The implementer is a cheaper worker model in a separate client. The orchestrator stays lean: it reads reports, diffs and test summaries, not worker transcripts. The setup recipe (configs, dispatch wrapper, report format) lives in `AGENT_ORCHESTRATION.md`. Without a worker, the orchestrator implements the cards itself and the same rules apply.

**Verification economy.** Checks are paid once, by whoever is cheapest, unless the claim needs independent judgment:

- The **worker runs the card's verification level**, including expensive checks (full test suites, multi-process tests, packaging, captures). It reports exact commands, exit codes, result summaries and artifact paths.
- The **orchestrator verifies by the cheapest sufficient means.** It reads the report, inspects the diff (stat plus key hunks) and re-runs cheap deterministic checks (build exit code, test-result files). It re-runs an expensive check only when the report is incomplete or inconsistent with the artifacts, or when a spot check is due.
- **The orchestrator verifies these itself; they cannot be delegated:**
  - acceptance judgment against design intent
  - visual and look comparisons against references
  - conformance to architecture and standards (module boundaries, naming, replication or data-flow model)
  - anything that touches permissions, credentials or external services
  - integration across tasks at plan end
  - any claim where the report conflicts with the evidence
  - the evidence for milestone gates
- **Spot checks calibrate trust.** At least once per plan, the orchestrator re-runs one expensive check the worker reported. Record a mismatch in history and re-verify every remaining task of that plan independently.

**Retry and escalation.** A task that fails verification is re-dispatched with the findings attached, up to 3 attempts in total. Then the orchestrator either takes the task itself (marking it `executor: orchestrator`) or marks it ⛔ blocked with a needs-you item.

**Concurrency.** One dispatch at a time by default. Editor-bound and binary-asset work always has a single writer. Parallel workers are allowed only for code-only tasks in separate worktrees, and the orchestrator merges them.

## 4. Bootstrap additions

- Calibration (core step 3.4): record what the user supplied about gate cadence, taste-call areas, willingness to do manual work, API and subscription budgets, and the agent clients in use. Do not invent preferences.
- Verify the worker toolchain inside the first plan, with a dry run of one trivial card through the full loop. Configuration alone is not evidence that the loop works.
- Handoff: present the first detailed plan for approval before implementation begins.

## 5. Planning additions

- **Milestones end in gates.** Each roadmap milestone states its gate: what the user will play, see or judge, and the Full-level evidence that accompanies it.
- **Auto-advance inside a milestone.** This overrides core section 6. Once the current plan is Verified on agent evidence, the orchestrator authors and starts the next plan of the same milestone without waiting, and notes it in the build log and ROADMAP resume block. Crossing a milestone boundary still needs the user's confirmation.
- **Design before build.** Structure and taste decisions (layouts, art direction, UX flows, mission or content structure) are drafted by the orchestrator into a spec or review pack built from reference material. The user approves it before build plans depend on it (core section 6, design specs). Diagrams are generated from the spec's own numbers so they never drift.
- **Cards sized for the worker:** one session, roughly ≤ 10 files, one verification command, exact paths and interfaces, and links to design sections instead of restated content. Cards whose acceptance is judgment-heavy, cross-cutting, or repeatedly failed are marked `executor: orchestrator`.
- **No more than one unverified task.** Implementation never runs ahead of verification by more than one card.
- **Plans are agent-neutral.** Cards name files, commands and outcomes, never client-specific tool names, so any implementer client can execute them.

## 6. Detailed plan format

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Implemented|Verified]` · `⬜⬜⬜⬜ n/N` · next → T<n> · milestone: M<x> · roadmap: ../ROADMAP.md

🎯 [Target — the observable result, one or two lines.]

🧭 Approach — [a few lines for the user: what is built, key choices, what to expect at review.]

📦 Scope — ✔ in · ✖ out.

## Tasks

### T1 — [Title] ⬜
executor: worker · verify: fast|standard|full · depends: —
Goal: [one line]   Design: ../design/<doc>.md#<section>
Files: [paths to create or change]
Interface: [signatures, data shapes or file formats the task must expose]
Steps: 1. … 2. … 3. …
Verify: `[exact command]` → expected: [result]
Done when: [what is true when the task is complete]
Notes: [traps, constraints; omit when none]

📝 Build log — [orchestrator-appended, one entry per verified task: what changed, evidence (level, command, result), commit, deviations.]

📤 Gate / review — [what the user can look at, run or judge, and when.]

---
## 🔧 Orchestrator block
*Bookkeeping — not user reading.*
- **Acceptance** (plan-level; `[x]` only when Verified): […]
- **Verification plan**: [which checks the worker runs, which the orchestrator runs itself, spot check]
- **Environment** verified [date]: […]
- **Record**: [decisions, history, conventions to update at plan end]
```

Format rules (in addition to core section 6):

- The user part (target, approach, scope, build log, gate) stays short and readable without the cards.
- Cards are self-contained. A worker reads the card, the linked design sections and `AGENTS.md`, and nothing else.
- Mark a finished card ✅ in its heading once it is verified, and a blocked one ⛔ with the reason on a `Blocked:` line.
- Only the orchestrator writes the build log, the progress grid and plan states.

## 7. Verification levels

The levels (Fast, Standard, Full) and their evidence lines are defined in core section 7; in this variant they are required. Every card names one level, Standard by default. Full runs at plan end where acceptance needs it and always at milestone gates, followed by the user's manual check. The project's tooling notes give the exact commands; engine companions give recipes (for Unreal: `UNREAL_TEST_AUTOMATION.md`).

## 8. Guard rails

- **Stop and escalate** (⛔ plus a needs-you item, then continue with other unblocked cards) when: the spec is ambiguous or contradicts a design doc; the work needs a taste call; it needs credentials, an account, a purchase or spend; it needs a destructive operation; or 3 attempts have failed.
- **No fabricated evidence.** Verified requires executed checks. "Configured" is not "works" (core section 7).
- **Budgets.** Record API and subscription budgets in `MEMORY.md` conventions. Worker runs have time and step caps. Spend beyond the budget needs authorization.
- **Secrets** live in environment variables or the client's credential store, never in the repository, plans, reports or logs.
- **Records have a single writer:** the orchestrator. Workers report; they never edit records.

## 9. Needs-you queue and briefings

`ROADMAP.md` carries a **📤 Needs you** section. It holds every manual item in one place, and agents keep working on unblocked cards meanwhile:

```markdown
## 📤 Needs you
- [ ] [Item] — why · needed by Plan NN / T<n> · effort ≈ [minutes/hours]
```

Briefing at a milestone gate, at a ⛔ that blocks all remaining work, or when evidence contradicts expectations:

```markdown
Briefing — [milestone / plan, boundary]
- Done: [what is now true]
- Evidence: [key checks and results; links to captures]
- Needs you: [queue items, gate judgment requested]
- Next: [the next plan or milestone]
- Watch for: [real risks, open questions]
```

## 10. States

Plan states (core section 7): Planned → Pending → In progress → **Implemented** (all cards verified; plan-level acceptance pending) → **Verified** (plan acceptance passed on executed checks). A **milestone** is Verified only after its gate: Full-level evidence plus the user's confirmation. Task markers: ⬜ open · ✅ verified · ⛔ blocked.

## 11. AGENTS.md additions

Beyond core section 9, the generated `AGENTS.md` includes:

1. The working agreement: milestone mandate, what it does not cover, repository delegation, and the editor/tool lifecycle actions agents may take.
2. The roles, the default role per agent client, and how a session prompt selects one.
3. Orchestrated mode: dispatch, report location, verification economy (including the orchestrator-only list), retry and escalation, concurrency. Link the companion for configuration.
4. Verification levels, with a pointer to the project's exact commands.
5. Guard rails, budgets, secrets and the single-writer rule for records.
6. The needs-you queue and briefing format.
7. The markers legend: plan states Planned → Pending → In progress → Implemented → Verified; `🎯 🧭 📦 📝 📤 🔧`; tasks `⬜ ✅ ⛔`.

## 12. Audit additions

Beyond core section 10:

- The first plan is presented for approval and includes the worker-loop dry run when a worker client is configured.
- Cards follow the format: executor, level, files, interface, exact verify command, done-when. They link design sections instead of restating them.
- Roadmap milestones state their gates; the needs-you queue is current; the auto-advance and gate rules agree between `AGENTS.md` and `ROADMAP.md`.
- The orchestrator-only verification list is present in `AGENTS.md`, and budgets and secrets handling are recorded.
- No implementer is given write access to records; repository delegation matches what the user granted.
