## Planning additions

- **Milestones end in gates.** Each roadmap milestone states its gate: what the user will play, see or judge, and the Full-level evidence that accompanies it.
- **Auto-advance inside a milestone.** Once the current plan is Verified on agent evidence, the orchestrator authors and starts the next plan of the same milestone without waiting, and notes it in the build log and the roadmap's resume block. Crossing a milestone boundary still needs the user's confirmation.
- **Design before build.** Structure and taste decisions (layouts, art direction, UX flows, mission or content structure) are drafted by the orchestrator into a spec or review pack built from reference material. The user approves it before build plans depend on it (see *Planning rules*, design specs). Diagrams are generated from the spec's own numbers so they never drift.
- **Cards sized for the worker:** one session, roughly ≤ 10 files, one verification command, exact paths and interfaces, and links to design sections instead of restated content. Cards whose acceptance is judgment-heavy, cross-cutting, or repeatedly failed are marked `executor: orchestrator`.
- **No more than one unverified task.** Implementation never runs ahead of verification by more than one card.
