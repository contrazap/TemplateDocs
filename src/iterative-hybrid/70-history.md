## History

`docs/plans/HISTORY.md` is the record of the order in which work happened, including work paused for something else and resumed later. The user's tracker keeps live status; this file is only the record.

```text
# History
Append-only. One line per event, oldest first: date · event · plan ID · note.

2026-11-02  start   M02          Stealth AI
2026-11-02  start   M02/F01      Guard perception
2026-11-02  start   M02/F01/I01  Sight cone
2026-11-04  done    M02/F01/I01
2026-11-04  start   M02/F01/I02  Hearing
2026-11-05  hold    M02/F01/I02  Waiting on recoil fix
2026-11-05  start   M02/B01      Rifle recoil desync (fixes M01/F02/I02)
2026-11-06  done    M02/B01
2026-11-06  resume  M02/F01/I02
```

- Events: `start`, `hold`, `resume`, `done`, `dropped` (with the reason in the note).
- The agent appends a line when work it is doing changes state, and when the user reports their own work changing state. The user can also append lines by hand.
- Never edit or delete a line. A mistake is corrected by a new `note` line naming the line it corrects.
- Notes are a few words; reasoning stays in the plan.
