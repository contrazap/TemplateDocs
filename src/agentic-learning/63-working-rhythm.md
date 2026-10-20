## Working rhythm

For every step:

1. The step file is ready; the chat names it and adds only what needs the user now.
2. The user reads it and runs 📋 Before when present, then replies **go** (or asks questions, or takes the step).
3. The agent runs 🔧 Do exactly as written and self-checks (Fast, or Standard when the step has behavior to test).
   - A small fix that keeps the step's intent (a quoting rule, a missing flag): apply it, record it as a Deviation, correct the step text.
   - A problem that changes the step's intent, scope or decisions: stop and report before continuing.
4. The agent fills the 📝 Record, commits, updates the overview's step table and the roadmap's resume block, and reports in a few lines: outcome, deviations, anything needing the user.
5. The user does 🔍 Read the code and 📤 Check and reports results and find-it answers. The agent clarifies anything unclear, records the results as user-reported, marks the step ✅ and writes the next step file.

**Pause points:** after every step. Also before any risky, irreversible, costly or externally visible action (an authorization point), when evidence contradicts expectations, and when the user asks.

**Plan end:** the overview's Review section is filled in: acceptance with evidence, what the user judges, and what the agent already verified. The plan becomes Implemented, then Verified after the user's review. The next plan is authored after the user confirms.

**Milestone demo:** a milestone's last plan ends with a demo in its overview, linked from the milestone's row in `ROADMAP.md`, written so the user can walk through it cold:

```markdown
Demo — M<x> [title] · [YYYY-MM-DD]
- Show: [steps to run or open, in order, and what each one should show]
- Built: [the milestone's plans, one line each, linked]
- Decisions: [IDs, choice, why, rejected alternatives]
- Tried and dropped: [dead ends that shaped the result]
- Changed from plan: [deviations from roadmap or acceptance, with reasons]
- Evidence: [key checks and results; captures linked]
- Concepts: [concepts met, glossary-linked]
- Open: [risks, open questions, limitations]
- Next: [the next milestone and what it will make demonstrable]
```
