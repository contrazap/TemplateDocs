# Unreal test automation — verification levels for agents

An optional add-on for Unreal Engine workspaces. It maps the verification levels (defined in each workspace template under *Records, states and evidence*; required in the autonomous template) onto checks that agents can run **without a human at the editor**: command-line builds, headless automation tests, functional-test maps, multi-process network tests, performance captures, screenshot comparisons and packaging. Editor-driven inspection stays with `UNREAL_MCP_BRIDGE.md`. This file covers the checks that should not need the editor's UI at all.

**Status.** The command shapes below are the standard UE 5.x ones. Each workspace verifies them on its own machine in its first plan, wraps them in `tools/build.ps1`, `tools/test.ps1` and `tools/package.ps1`, and records the verified commands in its tooling notes. Correct this file when a shape turns out wrong.

## 1. Principles

- **Text-first logic is testable logic.** Gameplay rules live in C++ (and data in JSON/CSV) so automation tests can reach them. Blueprints stay thin bindings.
- **Every check writes a result file** (JSON, XML, CSV or PNG) under the project's `Saved/`. The wrapper summarizes it in one line. Reports quote that line and the artifact path.
- **Deterministic by construction:** fixed random seeds, fixed physics timestep in tests, scripted inputs instead of human input, and test maps that contain only what the test needs.
- **Headless first.** `-nullrhi` wherever rendering is irrelevant. Use rendering (`-RenderOffscreen` or a window) only for visual and performance checks.

## 2. Build (Fast)

```powershell
& "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat" <Project>Editor Win64 Development `
  -Project="<abs path>\<Project>.uproject" -WaitMutex -NoHotReloadFromIDE
```

- Building the editor target while the editor has the project open fails on locked DLLs, unless Live Coding is used. Agents close the editor first, or limit themselves to Live Coding-compatible function-body edits during editor sessions.
- Project files: `...\Engine\Build\BatchFiles\Build.bat -projectfiles -project="<uproject>" -game -engine` (or `GenerateProjectFiles.bat`), only when an IDE solution is wanted. Builds do not need it.
- Exit code 0 and no `error` lines are the evidence. Keep the log at `Saved/Logs/Build-*.log`.

## 3. Automation tests (Fast / Standard)

Test kinds:

| Kind | Use for | Notes |
|---|---|---|
| Simple/complex automation tests (`IMPLEMENT_SIMPLE_AUTOMATION_TEST`) and **Automation Specs** (`BEGIN_DEFINE_SPEC`) | Pure logic: gearbox, tuning parsing, cargo slot math, mission state machines | Fast; no world needed, or a transient one |
| **CQTest** (Code Quality Test framework) | C++ tests with fixtures and latent steps | Readable test bodies for agents |
| **Functional tests** (`AFunctionalTest` actors in test maps, for example `/Game/Tests/Maps/FT_*`) | Behavior in a world: drive N metres, winch frees a stuck vehicle, trailer hitches | Standard level; one behavior per map section |
| **Screenshot functional tests** | Visual regressions against approved ground-truth images | Full level; needs rendering |

Name tests by area so filters select them: `<Prefix>.<Area>.<Case>` (for example `VE.Vehicles.Gearbox.ShiftToReverse`).

Run headless:

```powershell
& "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "<abs uproject>" `
  -ExecCmds="Automation RunTests <Filter>; Quit" -TestExit="Automation Test Queue Empty" `
  -ReportExportPath="<abs>\Saved\TestReports\<stamp>" -unattended -nopause -nosplash -nullrhi -NoSound -log
```

- Results: `<ReportExportPath>/index.json` (totals and per-test entries). The wrapper prints `passed / failed / skipped` and the first failure messages.
- Functional tests that need rendering: drop `-nullrhi` and add `-RenderOffscreen` (or `-windowed -ResX=1280 -ResY=720`).
- Test maps must be cooked or listed for the editor run; keep them under one folder and reference them in the functional test filter.

## 4. Network tests (Standard)

The goal is to prove that replicated state matches on server and client, and that late joiners receive it.

- **Two-process local test.** Start a listen server on a test map, start a client that connects, run a scripted scenario, have both processes dump state, then compare:

  ```powershell
  # server (listen) — scenario driven by -ExecCmds or a test GameMode option
  UnrealEditor-Cmd.exe "<uproject>" /Game/Tests/Maps/NT_Basic?listen -game -nullrhi -log -NoSound -unattended `
    -ExecCmds="<scenario commands>" -TestStateDump="<abs>\Saved\NetTests\<stamp>\server.json"
  # client
  UnrealEditor-Cmd.exe "<uproject>" 127.0.0.1 -game -nullrhi -log -NoSound -unattended `
    -TestStateDump="<abs>\Saved\NetTests\<stamp>\client.json"
  ```

  `-TestStateDump` is a **project-defined** argument, not an engine one: a small test subsystem writes the replicated facts under test (transforms within tolerance, cargo slots, mission state, winch attachments) to JSON at scenario end. A script diffs server against client with tolerances.
- **Late join:** start the client after the scenario has changed world state, then compare. This is the join-in-progress check.
- Use the **Null online subsystem** (direct IP) for automated tests, so they never depend on the online backend. Test the online-service path (EOS sessions and P2P) separately, at Full level.
- **Gauntlet** (`RunUAT.bat RunUnreal -project=<uproject> -test=<GauntletTestName> -build=editor`) orchestrates multi-process client/server tests with timeouts and log collection. Adopt it when the two-process scripts grow beyond a few scenarios.

## 5. Performance (Full)

- **Scripted captures:** a test map or the real map with a deterministic camera path or drive route per zone. Run with the target device profile and scalability level, and record with the CSV profiler (`-csvprofile` or console `csvprofile start` / `csvprofile stop`). Output lands in `Saved/Profiling/CSV/*.csv`. Compare frame time (game, render, GPU) per zone against the budgets in the project's performance doc.
- **Unreal Insights** traces (`-trace=default,gpu -tracefile=<path>`) are for diagnosis, not for routine checks.
- Target hardware runs (for example a handheld via Proton) are user-assisted. The agent prepares the build, the capture command and the budget table; the user runs it and returns the CSV.

## 6. Visual checks (Full)

- Approved reference captures live in `docs/refs/<topic>/`. Screenshot functional tests compare against ground-truth images with a tolerance. Refresh the ground truth deliberately, never automatically.
- Agent-viewable captures: `HighResShot` from scripted runs, or the bridge helpers (`UNREAL_MCP_BRIDGE.md`, Appendix G). Evidence is the before/after pair plus the reference, never the agent's description alone.

## 7. Packaging (Full)

```powershell
& "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="<abs uproject>" `
  -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<abs builds dir>" -unattended -utf8output
```

- Evidence: exit code 0, the archive exists, and a smoke run of the packaged executable (`-ExecCmds="<smoke>" -log`, with a timed `Quit`) writes the expected log line.
- Packaging needs the editor closed.

## 8. Mapping to levels (default)

| Level | Unreal checks |
|---|---|
| Fast | Build · data validation (JSON schema, asset naming/validation commandlet) · spec/unit tests (`-nullrhi`) |
| Standard | Fast · functional tests for the card's behavior · two-process network check when replicated state changed |
| Full | Standard · late-join and multi-client runs · performance captures vs budgets · screenshot comparisons · package + packaged smoke run · user-assisted target-hardware run at gates |

## 9. Workspace integration

- `tools/test.ps1 -Tier fast|standard|full [-Filter <prefix>]` wraps sections 2–7 and prints one summary line per check plus artifact paths, for the worker report or the plan's build log.
- Record verified command shapes, timings and quirks in the project's tooling notes. Record the test-name prefix and test-map folder in `MEMORY.md` conventions.
