## Support levels

Task detail adapts to demonstrated skill, not a fixed global setting:

| Level | Use when | Detail |
|---|---|---|
| L1 Guided | First occurrence of a skill | Exact steps and field values; code deltas with short per-line explanations; intermediate results stated. |
| L2 Supported | One clean repetition completed | Concrete steps and expected result; code described (signature, location, behavior); snippet on request or for a genuinely new API. |
| L3 Independent | Two clean repetitions completed | Goal, constraints and acceptance; snippets only for genuinely new APIs; the agent reviews the result. |

- Record the skill, evidence and current level in the `MEMORY.md` skill ledger. The recorded level drives task detail; task headings carry no level label.
- A clean repetition means the task was completed and its checkpoint passed without correction. If the user struggles or the task introduces a new API, teach that occurrence one level more detailed, then return to the recorded level after a clean repetition.
- For a first occurrence whose deliverable spans many similar units (zones, screens, systems), checkpoint after each unit (build it, look at it, short check) rather than only at the task's end.
- Levels are per skill; a plan may mix them. Adjust remaining task detail when checkpoint evidence warrants; record changes at review.
- Support levels change presentation detail only. Acceptance criteria and verification requirements never change with the level.
