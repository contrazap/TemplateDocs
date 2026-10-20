## Decisions, conventions and sources

All three live in `MEMORY.md`.

- **Decisions:** stable IDs scoped to the workspace or project; states Confirmed, Proposed, Deferred, Superseded. One line each: decision, basis, rejected alternatives (a few words on why each lost), revisit trigger, and a pointer to where the full reasoning sits (plan section or history entry). Never silently rewritten; a superseded decision names its successor. Ratify Proposed decisions once the work they govern is underway. The basis lives in the repository (a history entry or a file in the workspace), not only in an external file.
- **Tried and dropped:** an approach abandoned during the work is recorded where it happened ({{DEAD_END_HOME}}): what was tried, the evidence that ruled it out, what replaced it. A dead end that shaped a decision is also listed among that decision's rejected alternatives.
- **Conventions:** paths, IDs, naming, markers, evidence labels, repository rules (for example which build artifacts to ignore, and an explicit ignore or attribute decision when a new artifact class first appears), compaction rules, supported agent clients. Fetched third-party material keeps a provenance note beside it (source, date, usage) and stays reference-only.
- **References:** checked sources with dates and versions; unchecked items labeled as to-verify. Research prefers official or primary sources; documentation about a tool is not evidence that the local environment was tested.
