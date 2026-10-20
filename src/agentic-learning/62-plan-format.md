## Plan format

**Plan overview** (`NN-<name>.md`):

```markdown
# Plan NN — [Short title]
`[Planned|Pending|In progress|Implemented|Verified]` · `⬜⬜⬜ n/N` · next → [T<n> — title](NN-<name>/T<n>-<slug>.md) · roadmap: ../ROADMAP.md

🎯 [Target: the observable result of this stage, two or three lines.]

**Starting point:** [what exists before the first step: code, tools, services.]

**How each step works:** read the step → run 📋 Before if present → reply go → the agent runs 🔧 Do and
fills 📝 Record → do 🔍 Read the code and 📤 Check and report → the agent records it and writes the next step.

## Steps
| Step | After it you have | New concepts | State |
|---|---|---|---|
| [T1 — …](NN-<name>/T1-<slug>.md) | … | … | 📖 Ready to read |
| T2 — … | … | … | Outlined |

## Temporary on purpose
| Stopgap | Arrives | Replaced | Why it is fine until then |

## Decisions
| Decision | Why | Rejected | Step |

## Watch for
- [pitfalls that span steps: shells, ports, platform quirks]

## Review
Acceptance ([x] only when Verified): - [ ] …
Judge: [what the user runs or looks at, and judges] · Already verified: [agent evidence per acceptance item]
```

**Step file** (`NN-<name>/T<n>-<slug>.md`):

```markdown
# T<n> — [Title]
`[📖 Ready to read|Executed|✅ Verified]` · [Plan NN](../NN-<name>.md) · previous ← … · next → …

**Where we are:** [state before the step] **After this step:** [what the user will have and know]

## 🧭 New concepts        each explained here and linked to its glossary entry (≤ 3 major ones)
## 📋 Before (you)         only when the step changes the machine or repository state:
                           commands and the output expected now (e.g. a tool list without the tool)
## 🔧 Do (the agent)       exact commands (shell named, every flag explained); files with full content
                           when small and new, diffs for edits, a table for generated files; self-check; commit
## ⚖️ Decisions            choice · why · rejected · revisit when
## 🔍 Read the code (you)  files in order, what each line or setting does and why; ends with 2–3
                           find-it questions answered by reading, answers in a collapsed block
## 📤 Check (you)          state check first; steps naming shell or tool with expected output; before/after
                           comparisons; a break-and-observe experiment with its undo; `git show --stat HEAD`
                           with the full file list, plan records included
## 📝 Record               agent: commands run, results, deviations, evidence level · then the user's
                           results (user-reported) and the commit hash
```

Format rules:

- **Commands** work in every shell the user uses, or the shell is named and the differences called out. Expected output includes normal one-time messages (cache rebuilds, first-run notices) so the user can tell them from errors.
- **🔍 Read the code** covers configuration and generated files, not only source code. The first time a file type appears, every line or setting is explained; later steps cover what changed (`git diff`) and anything new.
- **📤 Check** compares against stated expected output; the user should be able to judge each result without asking. Where cheap, one experiment breaks something on purpose (a wrong version, an unused variable, a missing setting) to show what a rule or tool catches, then undoes it.
- **📋 Before / after** pairs make every state change visible: tool lists, installed packages, running containers, files present, database contents.
- **Concepts** link the glossary (`docs/concepts.md`); a concept's lasting explanation is written there the first time it appears.
- The overview and each step stay readable on their own; records about the step stay in the step's 📝 Record.
- Mark steps ✅ in the overview's table as they are verified; the plan's acceptance stays `[ ]` until the plan is Verified.
