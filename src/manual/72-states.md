## States and review protocol

Plans: Planned → Pending → In progress → **Done** (the user reports completion; review or required evidence remains) → **Verified**.

Standard review protocol: the user provides run evidence (short clip or screenshots, what was tested, versions); the agent inspects project files, configuration and structure where the domain allows, runs the non-destructive checks it can (type-check, build, lint, tests) on every reported completion, and reviews user-provided evidence of behavior. Errors found this way come back with the fix and a short why, as teaching; the send line never asks for output the agent can produce itself. Binary or non-text artifacts (compiled assets, graphs, levels) need suitable user evidence.

Review replies lead with the verdict per step or task: `✅ N.N passes`, or `❌ N.N: <finding> → <correction>`, one or two lines per finding, then `Next:`. The full finding (location, consequence, verification) goes in the plan's agent notes or the history, not the reply. A pass is `✅ N.N passes` and `Next:`, nothing else; evidence goes in the history. Add one line only for a deviation the user should know about.

Record review findings with a stable identifier when follow-up requires it:

```markdown
| Finding | Severity / consequence | Location | Suggested correction | Verification | State |
|---|---|---|---|---|---|
```
