## Workspace structure

Preserve established naming and layout when they already provide the same responsibilities; record intentional deviations in `MEMORY.md` conventions.

### Single project

```text
<workspace>/
  README.md                Entry point: purpose, layout, how the workspace works
  AGENTS.md                Agent operating rules, resume routine, role-specific protocol
  CLAUDE.md                Optional client entry file: a pointer to AGENTS.md
  docs/
    ROADMAP.md             Roadmap, plan states, resume pointer; gates and notes as needed
    MEMORY.md              Decisions, conventions, {{LEARNING_RECORD}}, references, history
    history/YYYY-MM.md     Optional: archived history moved out of MEMORY at compaction
    <domain>.md            Project-specific concept or design document(s), as needed
    design/                Optional, when there are several domain docs: README.md index + one doc per system
    concepts.md            Optional: glossary of the project's tool, framework and engine concepts
    tooling-notes.md       Optional: tool recipes and environment reference too long for MEMORY
    tooling/               Optional, when several tools need notes: one file per tool instead of tooling-notes.md
    implementation-plans/
      {{PLAN_FILES}}
    refs/                  Optional reference library: captures, fetched sets (+ `_sources.md` provenance), generated diagrams
  <delivery-root>/         Implementation lives where the project needs it
```

### Multiple projects

Repeat the `docs/` set per project (for example under `projects/<id>/`), keep the workspace-level `README.md` and `AGENTS.md`, and add a small registry (`PROJECTS.md` or a roadmap section) with one row per project: path, purpose, activity state, current plan link. Enforce one current plan per project. IDs and records are project-scoped; cross-project references use a qualified form such as `<project-id>:plan-03`. Nested `AGENTS.md` files contain only additions, never a copy of the root guide.

### Document responsibilities

| Document | Owns | Keep out |
|---|---|---|
| README.md | Purpose, layout, how the workspace works, where to start; a pointer to `ROADMAP.md` for the current position | Progress state and history (they drift; `ROADMAP.md` owns them) |
| AGENTS.md | Working agreement, resume routine, planning rules, role-specific protocol, records maintenance | Roadmap, design, transcripts |
| Client entry files (`CLAUDE.md` …) | A pointer to `AGENTS.md`; client-only notes | A copy of `AGENTS.md` |
| ROADMAP.md | Ordered milestones, plan states, resume pointer, gates, provisional estimates | Detailed tasks for future milestones; history |
| MEMORY.md | Decisions, conventions, {{LEARNING_RECORD}}, references, recent history | A second competing roadmap; invented preferences; long tool recipes |
| History archive (optional) | Older history entries moved out of MEMORY at compaction, one file per month | Decisions or conventions (those stay in MEMORY) |
| Tooling notes (optional) | Tool recipes, API quirks, environment reference material, verified commands | Decisions, progress |
| Domain document(s) | Project-specific concept or design that plans refer to: the *what and why*; with several, a `design/README.md` index (one line per doc) | Progress claims; plan steps |
| Concept glossary (optional) | The project's tool, framework and engine concepts, each explained once and linked from plans; created when the first concept is explained | Progress; decisions; generic programming lessons |
| Current plan | {{PLAN_DOC_OWNS}} | {{PLAN_DOC_KEEP_OUT}} |
| Completed plan files | Record of what was planned and delivered | Rewritten history |

Add domain-specific documents only when the actual project needs them. Do not generate empty documents. Optional files omitted from the workspace must also be omitted from navigation links.
