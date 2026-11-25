## Arcs, coverage and time

**Coverage map.** A table in `ROADMAP.md` with one row per topic cluster (a group of related features, not a project): cluster · what it includes · scope (`core` or `later`) · arc · status (`—`, `planned`, or `covered` with links to the plans that covered it). Clusters the user practised before the workspace are listed with the status `before`, so arcs spend their time on what is new. Out-of-scope topics are listed once below the table with where the user learns them instead. A new interest becomes a new row; the agent proposes its scope and the user decides.

**Core and value.** A cluster is `core` when most projects of the kind the user wants to build need it, or when the user's stated target needs it; everything else is `later`. The core is sized so that its estimate fits a period the user agrees is worth spending, stated in the roadmap. Growing the core needs the user's agreement at an arc review.

**Arcs.** The core is covered in arcs of about four or five plans with a common theme, ordered by the user's goal: what the target needs soonest, and what later arcs build on. Each plan introduces one cluster (two at most) and uses earlier ones again with complete steps. Only the current plan is written; the current arc's other plans are one-line outcomes, and later arcs stay one-line themes until they start. Where the track has a distributable build (a packaged game, a deployed app), the arc's last plan or its review produces one.

**Arc review** at the end of every arc, short and with the user: update the coverage map; compare the hours spent with the estimates and re-estimate the remaining core; record new interests as rows; confirm, reorder or drop the next arc; then write its first plan. The user can end the core early at any arc review.

**Session-sized tasks.** Each task fits one of the user's usual sessions and ends at a natural stopping point with something visible, runnable or testable. A plan is a handful of tasks, and its estimate is stated in sessions.

**Self-contained plans.** A plan never depends on the user remembering another plan. Anything built before is written out again in full when a plan needs it, and a plan starts from a clean project, starter or template, not from an earlier plan's files. Shared raw files (sounds, images, data) may be reused by path, with the import steps written out.

**Time.** `ROADMAP.md` carries a time section:

- The budget: sessions per week, session length, and the share of planned sessions that realistically happen (80% until the time log shows otherwise), giving realistic hours per week.
- Per arc: plans, estimated hours as a range, hours spent, and calendar weeks at the realistic weekly hours; a core total with cumulative weeks, so the user can see where stopping early would land.
- Estimates are rough and provisional: plan hours are its sessions times the session length plus about 10% for review fixes; an arc adds an allowance for its review and any arc-end build.
- The time log in `MEMORY.md` records each plan's estimate and actual hours, reported by the user at the plan's end. At each arc review, scale the remaining estimates by the ratio of actual to estimated hours so far, and say so in the roadmap. Never state delivery dates.
