## Verification and evidence

Every task names how it is verified, using the cheapest check that settles the claim. Three levels; `CONVENTIONS.md` gives the project's exact commands:

| Level | When | Typical content |
|---|---|---|
| **Fast** | Every change | Build, lint and format, static and data validation, unit tests |
| **Standard** | Behavior changes | Fast plus functional or integration tests, including networked or multi-process checks when the behavior spans processes, and checks through an editor or tool bridge where one is set up |
| **Full** | End of a milestone, demos, platform targets | Standard plus multi-client runs, performance budgets on target hardware, visual captures, packaging; then the user's own check |

Outcome evidence keeps these apart:

1. **Executed:** commands or actions actually run, with the result and any artifact path.
2. **Inspected:** what was read or reviewed and what it supports.
3. **User-reported:** what the user says they checked, attributed to them.
4. **Not checked:** what could not be checked, and why.

- A planned check is never reported as executed. Generated or configured is not the same as working.
- Feel, look and layout are judged by the user; the agent supplies captures and measurements, not the verdict.
- Visual defects: reproduce first, then fix, and close on a before and after capture where the tooling allows.
