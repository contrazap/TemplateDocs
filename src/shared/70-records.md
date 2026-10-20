## Records, states and evidence

Plan states (the fourth state is described under *States*):

| State | Meaning |
|---|---|
| Planned | Roadmap entry only; plan not authored |
| Pending | Plan exists; approval or start pending |
| In progress | Implementation or correction is underway |
| {{FOURTH_STATE}} | {{FOURTH_STATE_MEANING}} |
| Verified | Review passed and applicable observable acceptance has evidence |

- `ROADMAP.md` owns the roadmap, plan states and the resume pointer. `MEMORY.md` owns decisions, conventions, {{LEARNING_RECORD}}, references and history; history entries are labeled `YYYY-MM-DD-NN` (workspace-wide sequence).
- After meaningful work: update `ROADMAP.md` (states, resume pointer) and `MEMORY.md` (history entry, decisions, learning or skill updates); keep them consistent. No session files.
- On the user's "compact": condense history (recent detailed → older one-liners); never silently remove decisions, evidence labels or learning and skill records. Correct errors by annotation, not silent rewriting.

**Record size budget.** The resume routine reads `ROADMAP.md` and `MEMORY.md` every session, so both must stay readable in one pass:

- `MEMORY.md` targets ≤ ~25 KB. History keeps the current plan's entries (at most ~5) detailed, each ≤ ~5 lines; older entries are one line each (label · what happened · outcome, with pointers to decisions or commits). When the file exceeds the budget, compact proactively and say so in the history entry; the compaction rules above still apply.
- Conventions are rules, one or two lines each. Tool recipes, API quirks, long environment inventories and engine or tool reference material go in the tooling notes (or the applicable add-on) with a one-line pointer in Conventions.
- Tooling notes list a command only after it has been run in the workspace, with the shell it runs in. When the project starts long-running processes (servers, containers, editors), they open with a **Check first** section: how to see what is already running, what "nothing running" looks like, and how to stop it, free a port or reset state.
- `ROADMAP.md`'s resume block is a few lines: position, current plan, next action, gate. No history; that lives in `MEMORY.md`.
- Long-running workspaces may move older one-line history into `docs/history/YYYY-MM.md` at compaction, leaving one pointer line per archived month in `MEMORY.md`. Archived entries are moved verbatim, never rewritten; decisions, conventions and evidence labels stay in `MEMORY.md`.
- Other documents have soft budgets so no file becomes the one large document: `AGENTS.md` ~10 KB (recipes move to tooling notes), `ROADMAP.md` ~10 KB (outcome-level only), each domain or design doc ~15 KB (split by system and update the index), {{PLAN_BUDGET}}.

Evidence categories, kept separate:

1. **Inspection:** what was read or reviewed and what it supports.
2. **Executed checks:** commands or actions actually run, with context and observed results.
3. **User-reported checks:** what the user says they tested, clearly attributed.
4. **Not checked:** missing environments, omitted scenarios, unresolved findings.

Match the check to the claim: use the cheapest check that settles it (targeted inspection before full runs) and escalate only when the scenario requires it. Distinguish "configured correctly" from "actually works": values visible in a tool's UI are evidenced by user screenshots (user-reported), while heavier runtime or session checks are reserved for claims configuration alone cannot settle (constructed state, runtime wiring, integration, feel). Binary or non-text artifacts need suitable evidence; filenames alone are insufficient. Never equate generated files with working behavior, or a planned check with an executed one.

Visual defects (rendering artifacts, misplaced or missing elements): reproduce before fixing, isolate by toggling the suspect element at runtime, and close only on an executed before/after capture where the tooling allows; "it went away" after an unrelated change is not a closure. Parity checks against a reference (template, earlier version) diff the full property set, not a hand-picked list.

**Verification levels** ({{LEVELS_USE}}). The project's tooling notes give the exact commands; engine add-ons give recipes (for Unreal: `UNREAL_TEST_AUTOMATION.md`).

| Level | When | Typical content | Budget |
|---|---|---|---|
| **Fast** | Every change | Build, static and data validation, lint and format checks, unit tests, headless | minutes |
| **Standard** | {{STANDARD_WHEN}} | Fast plus functional or integration tests of the behavior, including networked or multi-process checks where the behavior spans processes | ≤ ~15 min |
| **Full** | Plan end where acceptance needs it; milestone gates and demos | Standard plus multi-client or integration runs, performance budgets, visual captures compared with references, packaging; then the user's manual check | ~1 h + user time |

Evidence lines record the level, command, result and artifact path, using the evidence categories above. A planned check is never reported as an executed one.
