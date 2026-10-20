## Verification, guard rails and the needs-you queue

**Verification levels** (defined in *Records, states and evidence*) are required in this template. Every card names one level, Standard by default. Full runs at plan end where acceptance needs it and always at milestone gates, followed by the user's manual check. The project's tooling notes give the exact commands; engine add-ons give recipes (for Unreal: `UNREAL_TEST_AUTOMATION.md`).

**Guard rails**

- **Stop and escalate** (⛔ plus a needs-you item, then continue with other unblocked cards) when: the spec is ambiguous or contradicts a design doc; the work needs a taste call; it needs credentials, an account, a purchase or spend; it needs a destructive operation; or 3 attempts have failed.
- **No fabricated evidence.** Verified requires executed checks. "Configured" is not "works".
- **Budgets.** Record API and subscription budgets in `MEMORY.md` conventions. Worker runs have time and step caps. Spend beyond the budget needs authorization.
- **Secrets** live in environment variables or the client's credential store, never in the repository, plans, reports or logs.
- **Records have a single writer:** the orchestrator. Workers report; they never edit records.

**Needs-you queue and briefings.** `ROADMAP.md` carries a **📤 Needs you** section. It holds every manual item in one place, and agents keep working on unblocked cards meanwhile:

```markdown
## 📤 Needs you
- [ ] [Item] — why · needed by Plan NN / T<n> · effort ≈ [minutes/hours]
```

Briefing at a milestone gate, at a ⛔ that blocks all remaining work, or when evidence contradicts expectations:

```markdown
Briefing — [milestone / plan, boundary]
- Done: [what is now true]
- Evidence: [key checks and results; links to captures]
- Needs you: [queue items, gate judgment requested]
- Next: [the next plan or milestone]
- Watch for: [real risks, open questions]
```
