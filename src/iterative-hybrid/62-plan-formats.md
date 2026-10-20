## Plan formats

`docs/plans/README.md` carries these formats, adapted to the project. Plans hold no live status; task checkboxes exist so any session can resume the work.

**`MILESTONE.md`**

```markdown
# M01 — [Title]

🎯 Outcome — [what the user can play, demo or use when this milestone is done]
📦 Scope — ✔ in · ✖ out
✅ Done when — [observable checks, including the user's own playtest or review]

## Features
- F01 — [title] — [one line]
- F02 — [title] — [one line]

## Notes
[Risks, open questions this milestone answers, links to the brief.]

## Outcome
[Filled when the milestone is done: what is now true, what moved to later milestones, brief or convention changes it led to.]
```

**`FEATURE.md`**

```markdown
# M01/F02 — [Title]

🎯 Goal — [what the feature does, one or two lines]
🧭 Design — [key choices, data shapes, interfaces; link the brief or conventions instead of repeating them]
📦 Scope — ✔ in · ✖ out

## Implementation plans
- I01 — [title] — [one line]
- I02 — [title] — [one line; planned later]

## Outcome
[Filled when the feature is done.]
```

**Implementation plan (`I01-<slug>.md`)**

```markdown
# M01/F02/I01 — [Title]
Kind: build | spike · Implementer: agent | user | split · Depends: [IDs or —]

🎯 Goal — [the checkable result]
📚 Context — [links to FEATURE.md, the brief, conventions, related plans; files to read first]
📦 Scope — ✔ in · ✖ out

## Tasks
- [ ] T1 — [title] · files: [paths] · verify: [command or check] → [expected]
- [ ] T2 — …

✅ Done when — [what is true when the plan is complete; the user's check if one is needed]

## Outcome
[Filled at the end: what changed (files, commits), evidence (see *Verification and evidence*), deviations from the plan and why, findings, follow-ups for the user's tracker, proposed convention, brief or skill changes.]
```

**Bug-fix plan (`B01-<slug>.md`)**

```markdown
# M02/B01 — [Title]
Fixes: M01/F02/I02 · Found: YYYY-MM-DD · Implementer: agent | user | split

🐞 Problem — [what happens] · Expected — [what should happen]
🔁 Repro — 1. … 2. … 3. …
🔍 Cause — [filled once found]

## Tasks
- [ ] T1 — [title] · files: [paths] · verify: [command or check] → [expected]
- [ ] T2 — Regression check: [the repro no longer reproduces; the original plan's checks still pass]

## Outcome
[As in an implementation plan.]
```

**Enhancement plan (`E01-<slug>.md`)**

```markdown
# M02/E01 — [Title]
Enhances: M01/F02/I01 · Implementer: agent | user | split

💡 Why — [what is lacking and what prompted it: playtest, feedback, a later feature]
🔧 Change — [what will be different]

## Tasks
- [ ] T1 — [title] · files: [paths] · verify: [command or check] → [expected]

## Outcome
[As in an implementation plan.]
```

Markers: `🎯` goal or outcome, `🧭` design, `📦` scope, `📚` context, `✅` done when, `🐞` problem, `🔁` repro, `🔍` cause, `💡` why, `🔧` change; tasks `[ ]` open, `[x]` done, `[~]` dropped with a reason on the line.
