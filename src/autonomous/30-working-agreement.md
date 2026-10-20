## Working agreement

- **Agents implement; the user directs.** Inside an approved milestone, agents design within scope, implement, verify, author the next plan and keep the records. The user approves the roadmap and each milestone, judges results at milestone gates, makes taste calls (look, feel, layout, naming of player-facing things) and handles the items in the needs-you queue (see *Verification, guard rails and the needs-you queue*).
- **Milestone approval is the execution mandate.** It covers implementation inside that milestone's scope, routine dependency installs the plans need, and editor or tool lifecycle actions that `AGENTS.md` lists (for example opening and closing the project's editor). It never covers irreversible, destructive, costly or externally visible actions: publishing, pushing (unless delegated), external communication, accounts, purchases, API spend beyond the recorded budget, deleting work, or system-wide changes. Each of those needs explicit authorization.
- **Repository delegation** is recorded in `AGENTS.md` and `MEMORY.md` conventions when the user grants it. A typical delegation lets the orchestrator commit locally once per verified task, while pushing stays with the user.
- **Show the work.** Plans carry a build log, gates carry a briefing, and evidence is recorded honestly (see *Records, states and evidence*).
- **The user can step in at any time:** pause, take over a task, change a decision or tighten the gates. Record changes to the cadence in `MEMORY.md`.

## Roles and orchestrated mode

Three roles. The session prompt names the role; `AGENTS.md` defines each one and the default role for each agent client.

| Role | Does | Never |
|---|---|---|
| **Orchestrator** | Runs the resume routine, authors and splits plans, dispatches task cards, verifies results, commits (when delegated), keeps the records, briefs the user at gates | Hands judgment-only work to a worker (below) |
| **Implementer** | Executes exactly one task card: reads the card and the design sections it links, changes the listed files, runs the card's verification, writes a report | Edits records (`ROADMAP.md`, `MEMORY.md`, plan states), commits, pushes, widens scope |
| **Reviewer** | Audits a finished plan or milestone against its acceptance and the design docs; reports findings | Changes code while reviewing |

**Orchestrated mode (default when a worker client is configured).** The implementer is a cheaper worker model in a separate client. The orchestrator stays lean: it reads reports, diffs and test summaries, not worker transcripts. The setup recipe (configs, dispatch wrapper, report format) lives in the `AGENT_ORCHESTRATION.md` add-on. Without a worker, the orchestrator implements the cards itself and the same rules apply.

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
