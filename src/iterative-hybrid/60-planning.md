## Planning

### Hierarchy and types

| Level | Is | Written |
|---|---|---|
| **Milestone** (`M`) | An outcome the user can play, demo or use, for example "first level playable on Windows" | At the start of the milestone, with the user |
| **Feature** (`F`) | One system or capability inside a milestone; a folder of implementation plans | When the milestone starts, or just before the feature starts |
| **Implementation plan** (`I`) | One chunk of work handed over to an implementer, ending in something checkable | Just before it is worked on, against the code as it stands |
| **Bug-fix plan** (`B`) | A fix to completed work, from this milestone or an earlier one | When the bug is taken on |
| **Enhancement plan** (`E`) | A change to completed work that improves or extends it | When the enhancement is taken on |

A small feature may need only one implementation plan, but it still gets a `FEATURE.md` so every feature reads the same way. A bug or enhancement too large for one handover becomes a feature folder with implementation plans instead of a single `B` or `E` file.

**Spikes** answer one open question before work builds on an assumption (for example: can the target device hold the frame budget; does the networking approach work across platforms). A spike is an implementation plan whose header says `Kind: spike`; its result is a finding, not merged code. The finding goes into the plan's outcome and becomes a brief or conventions proposal. Spike code stays on its branch; building the real thing is a new plan. When the brief has high-risk open questions, propose spikes for them in the first milestone.

### IDs and paths

- Two-digit numbers within the parent: `M00`, `M01` at the top; `F01`, `B01`, `E01` inside a milestone; `I01` inside a feature. Each type numbers on its own.
- Folder and file names add a short kebab-case slug: `M01-first-level-playable/F02-weapons/I01-weapon-framework.md`.
- The full reference is the path of IDs: `M01/F02/I01`, `M02/B01`. Use it in plans, history, commit messages and the user's tracker.
- IDs are never reused or renumbered. A plan that is dropped keeps its file, with the reason in its outcome.

### Rules

1. **Completed plans are frozen.** Once a plan is done, its file and everything under a completed milestone stay unchanged. Later changes are new plans that name what they change (`Fixes: M01/F02/I02`, `Enhances: M01/F02/I01`); searching for an ID finds every later change to it.
2. **New work goes into the current milestone,** wherever the bug or enhancement came from. A milestone is the window of time in which its work was done. The current milestone is the latest one started and not done in `HISTORY.md`. Between milestones, ask the user to start the next one before planning new work; a completed milestone is never reopened.
3. **A plan still in progress is not frozen.** A bug found in it becomes another task in that plan; only completed work gets a `B` or `E` plan.
4. **One plan at a time per implementer** is in progress. Starting another means putting the first on hold in `HISTORY.md`.
5. **Plan just in time.** Do not write future milestones, features or implementation plans in detail; the user's tracker holds the backlog. Before authoring, verify what can be verified (the code, the environment, the tools).
6. **Size for one handover.** An implementation plan is completed and verified in one session or a few, and ends in something the user can check. Split it before authoring when it would not.
7. **Plans are agent-neutral.** They name files, commands and outcomes, not client-specific tool names, so any agent client, or the user, can carry them out.
8. **Never narrow scope or acceptance silently.** A change to what a plan delivers is agreed with the user and noted in the plan.
