# Agent orchestration — Claude Code orchestrator, OpenCode workers

An optional add-on for autonomous workspaces (`AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md`, *Roles and orchestrated mode*). One orchestrator client plans, dispatches task cards, verifies and records. A cheaper worker model, running in a second client, implements one card per dispatch. This file gives the recommended pairing, the configuration shapes, the dispatch wrapper and the report format.

**Status.** The building blocks were checked on 2026-10-16 (versions below). **The full loop is not yet verified.** Each workspace's first plan runs a dry run (section 8) and records the result. Update this file with what the dry run teaches.

## 1. The pairing and why

| Part | Choice | Why |
|---|---|---|
| Orchestrator | **Claude Code** (Opus-class model on a Claude subscription) | Planning, judgment and review quality; skills and background shell jobs for dispatch |
| Worker | **OpenCode** running `deepseek/deepseek-flash` (DeepSeek V4.1 Flash) | Low cost per token; DeepSeek lists OpenCode as an official partner with full V4.1-Flash support; reads `AGENTS.md` natively; Unreal MCP bridges already verified in OpenCode (`UNREAL_MCP_BRIDGE.md`) |

Rejected alternative: a second Claude Code pointed at DeepSeek's Anthropic-compatible endpoint (`ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic`). It works mechanically, but there are three problems:

- Claude Code's own subagents can only run Claude models.
- Anthropic states it does not support Claude Code with non-Claude models, so updates may break it.
- If only the base URL is set, the saved claude.ai login stays the active credential and is sent to the third-party endpoint. Avoid that configuration.

Verified building blocks (2026-10-16, Windows 11):

- OpenCode `v2.0.30`. `opencode auth list` shows the DeepSeek credential stored. `opencode models` lists `deepseek/deepseek-flash` and `deepseek/deepseek-v4-pro`.
- Claude Code `2.1.301`.
- OpenCode V2 `run` flags: `--model/-m provider/model#variant`, `--agent`, `--format default|json`, `--title`, `--session/-s`, `--continue/-c`, `--file/-f`, `--auto` (auto-approve permissions not explicitly denied), `--standalone` (private server instead of the background service), `--server <url>`. It runs in the current directory.

## 2. Worker agent definition (OpenCode)

A project agent file `.opencode/agents/implementer.md`. The file name is the agent name. Frontmatter holds options, and the body is the agent's system prompt. Permission rules match parsed commands with `*` and `?` globs, and **the last matching rule wins**, so the catch-all comes first.

```markdown
---
description: Implements exactly one task card and writes a report. Never edits records or commits.
mode: primary
model: deepseek/deepseek-flash
steps: 120
permission:
  "*": allow
  edit: allow
  webfetch: allow
  bash:
    "*": allow
    "git push*": deny
    "git commit*": deny
    "git reset --hard*": deny
    "git clean*": deny
    "git checkout -- *": deny
    "rm -rf *": deny
    "Remove-Item * -Recurse*": deny
  external_directory:
    "*": deny
    "C:/Program Files/Epic Games/UE_5.8/**": allow
---
You are the implementer for this workspace. Follow the Implementer section of AGENTS.md.
Execute only the task card named in the prompt. Read the card, the design sections it links and AGENTS.md;
read other files only as the card requires. Run the card's Verify command(s) exactly. Write the report JSON
to the path given in the prompt, then stop. Do not edit docs/ROADMAP.md, docs/MEMORY.md, plan states or
build logs; do not commit. If the card is ambiguous or blocked, stop and report status "blocked" with the question.
```

Adjust `external_directory` to the engine and tool paths the project's workers must read. Keep MCP entries in the project's `opencode.json` (`UNREAL_MCP_BRIDGE.md`) so workers reach the same bridges as the orchestrator.

## 3. Dispatch wrapper

`tools/agents/run-worker.ps1` (Windows PowerShell) gives the orchestrator one stable command, so that client permissions can allow exactly this script. It:

1. Takes `-Plan NN -Task T<n> [-Attempt k] [-NotesFile path] [-TimeoutMin 45]`.
2. Builds the prompt: role line, plan path and task ID, report path `.agents/reports/P<NN>-T<n>-a<k>.json`, and the notes from previous attempts.
3. Runs `opencode run --agent implementer -m deepseek/deepseek-flash --auto --format json --title "P<NN>-T<n>-a<k>" "<prompt>"` from the repository root. It tees the JSON event stream to `.agents/runs/P<NN>-T<n>-a<k>.jsonl` and kills the process tree after the timeout.
4. Exits 0 when the report exists and parses, 2 when the report is missing (treated as failed), and 3 on timeout. It prints only a one-line summary to stdout: the orchestrator reads the report file, not the stream.

`.agents/` is git-ignored. The orchestrator copies the evidence that matters into the plan's build log.

## 4. Report format

```json
{
  "task": "P01-T3",
  "attempt": 1,
  "status": "done | blocked | failed",
  "summary": "one or two sentences",
  "files_changed": ["Game/Source/..."],
  "checks": [
    {"level": "standard", "command": "tools/test.ps1 -Tier standard -Filter VE.Vehicles", "exit_code": 0,
     "result": "12 passed, 0 failed", "artifact": "Game/Saved/TestReports/20261016-1412/index.json"}
  ],
  "deviations": ["what differs from the card and why"],
  "questions": ["for blocked status"],
  "followups": ["suggested, not done"]
}
```

## 5. Orchestrator skill (Claude Code)

A project skill `.claude/skills/orchestrate/SKILL.md` holds the loop, so that "orchestrate plan NN" starts it in any session:

1. Run the resume routine. Pick the next ⬜ card whose dependencies are ✅.
2. `executor: orchestrator` → implement it directly. Otherwise dispatch it with the wrapper as a **background** shell job and wait for the completion notification (no polling).
3. Read the report. Verify per the template's verification economy: report vs diff vs cheap re-runs; run orchestrator-only checks yourself; run the plan's spot check.
4. Pass → commit `[P<NN>-T<n>] <title>` (when delegated), mark ✅, append the build-log entry, update the ROADMAP resume block. Fail → re-dispatch with findings (≤ 3 attempts), then take the card over or mark it ⛔ with a needs-you item.
5. Continue until the plan is Implemented, then run its acceptance. Auto-advance inside the milestone. Stop at a milestone gate, or at a ⛔ that blocks all remaining cards, and brief the user.

Project permissions (`.claude/settings.json`) allow the wrapper and the read-only git commands. Push stays denied unless delegated:

```json
{
  "permissions": {
    "allow": [
      "PowerShell(powershell -NoProfile -File tools/agents/run-worker.ps1 *)",
      "Bash(powershell -NoProfile -File tools/agents/run-worker.ps1 *)",
      "Bash(git status*)", "Bash(git diff*)", "Bash(git log*)", "Bash(git add *)", "Bash(git commit *)"
    ],
    "deny": ["Bash(git push*)", "PowerShell(git push*)"]
  }
}
```

The permission-rule syntax is client-version specific. Confirm the rules match during the dry run and record the working shape.

## 6. Context and cost economy

- The orchestrator's subscription limits are the bottleneck. The orchestrator never reads worker transcripts or large files to "check". It reads the report, `git diff --stat`, the key hunks and the test-result files.
- Workers do the exploration. Cards point them at exact files and design sections, so they don't have to search the whole tree.
- Update records once per card, not per step. Write the MEMORY history entry once per plan.
- Record the worker spend per plan (DeepSeek usage dashboard or `opencode stats`) in the plan's build log, so cost trends stay visible.

## 7. Parallel workers (later, optional)

Only for code-only cards with no shared files: `git worktree add ../wt-P<NN>-T<n>`, then run the wrapper with the worktree as the working directory. The orchestrator merges and verifies on the main tree. Editor-bound or binary-asset cards never run in parallel.

## 8. Dry-run checklist (first plan of each workspace)

1. `opencode run --agent implementer -m deepseek/deepseek-flash --format json "reply with OK"` returns events and exits 0.
2. A permission deny bites: the worker is asked to run `git push --dry-run` and the call is refused.
3. A trivial card (for example "add a script that prints the project version, plus its check") goes through the wrapper. The report parses, the files changed match the diff, and the check passes when re-run by the orchestrator.
4. The orchestrator commits, updates the build log and resume block, and leaves no stray records written by the worker.
5. MCP: the worker lists the project's MCP servers (`opencode mcp list` or a session check), when the card needs them.

Record results with dates in the workspace history, and fold any corrections into this file.

## 9. Troubleshooting (seed)

| Symptom | Likely cause | Fix |
|---|---|---|
| Worker edits records or commits | Agent prompt or permissions not loaded | Check that `--agent implementer` is passed and the file is at `.opencode/agents/implementer.md`; check that the deny rules come after `"*"` |
| Wrapper times out with no report | Worker looped or waited on a prompt | Lower `steps`, keep `--auto`, read the tail of `.agents/runs/*.jsonl` |
| Report claims pass; orchestrator re-run fails | Stale build, wrong working directory, or optimistic report | Re-dispatch with the failing output; count it as a spot-check mismatch (variant section 3) |
| Orchestrator context fills quickly | Reading streams or whole files | Read only the report, the diff stat and the hunks; move details to the build log |
