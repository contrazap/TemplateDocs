## Planning additions

- **Plans are stages of natural growth.** Each plan ends with something the user can run and judge, and brings in the tools that stage needs (for example: an API with data in memory → a real database → a web client → accounts). Roadmap milestones say what the user will be able to see, run or evaluate.
- **A plan is an overview plus one file per step**: `implementation-plans/NN-<name>.md` and `implementation-plans/NN-<name>/T<n>-<slug>.md`.
- **Steps are written one ahead.** The overview lists all steps; only the next step has a file. The agent writes it while the user checks the current one, folding in what that step taught.
- **Verify before writing a step.** Run the step's commands, templates and checks in a scratch location first, so every expected output in the step comes from a real run. Check the current versions of the tools and packages the step installs.
- **Step size:** about 10–20 minutes of reading and checking, at most three major new concepts. Split a step that exceeds either.
- **Temporary on purpose:** the overview lists the plan's stopgaps (what, arrives, replaced in, why it is fine until then); stopgaps that span plans are listed in `ROADMAP.md`.
- **Needs you:** items only the user can do or decide (accounts, logins, purchases, interactive installs, taste calls, open decisions) go to a **📤 Needs you** section in `ROADMAP.md`, one line each: `- [ ] [Item] — why · needed by Plan NN / T<n> · effort ≈ …`. The agent continues with unblocked work meanwhile.
- **Repository delegation:** when granted, commit once per step as `[P<NN>-T<n>] <title>` (record-only commits `[P<NN>] …`) and push each commit right away; the step's Record cites the hash.
