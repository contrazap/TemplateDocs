## Workspace structure

```text
<project>/
  AGENTS.md                          How agents work here; read order; boundaries
  CLAUDE.md                          Client entry file: @AGENTS.md (one per client in use)
  docs/
    PROJECT_BRIEF.md                 North star, pillars, constraints, non-goals, open questions
    CONVENTIONS.md                   Patterns and rules agents must follow; grows as patterns settle
    plans/
      README.md                      Plan hierarchy, IDs, types, rules and formats
      HISTORY.md                     Append-only: start / hold / resume / done, in real order
      M00-<slug>/                    Milestone (completed ones are frozen)
        MILESTONE.md
        F01-<slug>/                  Feature
          FEATURE.md
          I01-<slug>.md              Implementation plan: one handover
        B01-<slug>.md                Bug-fix plan (may fix work from an earlier milestone)
        E01-<slug>.md                Enhancement plan
  .claude/
    skills/
      README.md                      What belongs here and how to add a skill; starts empty otherwise
  <code>/                            Wherever the project needs it
```

Preserve an existing project's layout; place `docs/` and `.claude/` beside it and record intentional deviations in `docs/CONVENTIONS.md`. For a workspace of several independent projects, repeat `docs/` per project (for example under `projects/<id>/`) and keep one root `AGENTS.md`; nested `AGENTS.md` files hold only additions.

### Document responsibilities

| Document | Owns | Keep out |
|---|---|---|
| `AGENTS.md` | Working agreement, read order, boundaries, how planning, history, conventions and skills work here | Brief content, conventions, plans, status |
| Client entry files | A pointer to `AGENTS.md`; client-only notes | A copy of `AGENTS.md` |
| `PROJECT_BRIEF.md` | What the project is trying to achieve and why | Status, plans, implementation detail |
| `CONVENTIONS.md` | Rules and patterns agents must follow, verified commands | Status, history, tutorials, long procedures (those become skills) |
| `plans/README.md` | Plan hierarchy, IDs, types, rules, formats | Plan content |
| `plans/HISTORY.md` | The order in which work started, paused, resumed and finished | Status commentary, reasoning (that stays in the plans) |
| Plans | What was planned, how it was verified, what was delivered | Live status (the user's tracker owns it) |
| `.claude/skills/` | Reusable procedures for this project | Rules (those go in `CONVENTIONS.md`) |

Each fact has one home; other documents link to it. Do not generate empty or speculative documents. Soft size budgets: `AGENTS.md` ~8 KB, `PROJECT_BRIEF.md` ~10 KB, `CONVENTIONS.md` ~15 KB (move procedures to skills before splitting), each plan ~15 KB (split before it grows past that).
