## Planning rules

- Maintain a broad roadmap and **one current plan**. Do not write future plans during bootstrap.
- Author the next plan only after the current one has passed review with evidence; {{NEXT_PLAN_GATE}}.
- Verify what is verifiable before authoring (environment, filesystem, installed tools).
- A plan ends in an observable, reviewable result; its size fits the work and the user's pace.
- Split a milestone before authoring its plan when: acceptance depends on later milestones · independent systems share only a final proof · several risky unknowns need early checks · no reviewable result appears within each group of work · a first-contact slice (what the next plans immediately depend on) separates cleanly from a completion slice that can wait until those plans need it.
- Design decisions the user may not be able to judge (layout, composition, structure) are drafted by the agent into a spec built from the reference material and corrected by the user; build steps then link that spec so the user judges concrete options instead of inventing.
- Keep plan IDs stable; a split after authoring keeps the number with letter suffixes (`03a`, `03b`), and any divergence between run order and numeric order is stated explicitly (for example under the roadmap table). Completed plan files remain as records.
- Mark finished items ✅ as they complete; acceptance criteria stay `[ ]` until the plan is Verified, then mark `[x]`.
- Changes to acceptance criteria must be justified and recorded. Never narrow them silently.
- Keep future roadmap entries outcome-level; treat their internals as provisional.
- Label estimates as rough and provisional; never invent delivery dates or commitments.
- Fold the previous plan's recorded learnings into the next plan.

Plan-format rules for every plan (*Plan format* gives the full format):

- Plan content that describes or recreates something visual (a build step, an approach description, a record note) links the reference or generated diagram that shows it (relative path, for example `../refs/<topic>/…`) so the picture sits beside the text.
- The plan header line carries the state, a progress grid (`⬜`/`✅`), the next item and the roadmap link.
- Plans are agent-neutral: they name files, commands and outcomes, not client-specific tool names, so any supported agent client can execute them.
- Each fact has one home: design docs (what/why), plans (how/now), the glossary (concepts), `MEMORY.md` (decisions, history), `ROADMAP.md` (where we are). Other documents link to it (`../design/<doc>.md#<section>`) instead of repeating it.
