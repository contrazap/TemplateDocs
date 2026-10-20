## Plan format

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

Format rules:

- The user part comes first and carries no bookkeeping; everything after the `---` divider is agent material and can be skipped by the user.
- The user part (target, approach, scope, build log, gate) stays short and readable without the cards.
- Cards are self-contained. A worker reads the card, the linked design sections and `AGENTS.md`, and nothing else.
- Mark a finished card ✅ in its heading once it is verified, and a blocked one ⛔ with the reason on a `Blocked:` line.
- Only the orchestrator writes the build log, the progress grid and plan states.
