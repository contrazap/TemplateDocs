## Working a plan

1. **Plan.** The agent reads `PROJECT_BRIEF.md`, `CONVENTIONS.md`, the parent milestone and feature, related completed plans and the code involved; asks what it needs; drafts the plan. The user refines and approves it.
2. **Hand over.** The user names the implementer in the plan header. An agent starts in a fresh session when the planning conversation was long; the plan must carry everything the work needs.
3. **Start.** Append a `start` line to `HISTORY.md`.
4. **Implement.** Follow the tasks in order, verify each one, tick it, and keep notes for the outcome. Stop and ask the user when: the plan is ambiguous or contradicts the brief or conventions; the work needs a taste call; scope would change; it needs credentials, an account, spend or a destructive action; or the same check has failed three times.
5. **Review.** The user reviews, plays or uses the result. Fixes found now are new tasks in the same plan.
6. **Wrap up.** Fill the outcome; append a `done` line to `HISTORY.md`; propose any convention, brief or skill changes and apply the ones the user approves. When the last plan of a feature or milestone is done, fill its outcome and append its `done` line too.

**Hold and resume.** To switch to other work, note in the plan where it stopped (an unticked task with a short note), append a `hold` line with the reason, and start the other work. To resume, append `resume` and continue from the first unticked task after rereading the plan and anything changed since the hold.
