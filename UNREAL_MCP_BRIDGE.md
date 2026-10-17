# Unreal MCP bridge — setup and workspace integration

An optional tooling companion for Unreal Engine workspaces created from the workspace template family (`WORKSPACE_TEMPLATE_CORE.md` + a variant). It documents the Unreal MCP bridges: local connections that let the agent inspect and drive a running Unreal Editor (engine, project and level status; asset, actor, Blueprint and property queries and edits; Play-In-Editor control; screenshots returned to the agent), plus process-level tools that open, close, build and package projects without the editor.

**Two bridges, one machine.** As of UE 5.8 the engine ships the **official Unreal MCP** (plugin `ModelContextProtocol`, friendly name "Unreal MCP") — the primary editor bridge: it runs inside the editor process and serves MCP over local HTTP (section 4). The third-party **community server** (`unreal-engine-mcp`, pyremote) is retained as the fallback where the official one has no reach: the local layer (open/close/build/package while the editor is closed), arbitrary in-editor Python, and screenshots returned to the agent as viewable images (section 3, project enable in section 5). Use the official bridge first; reach for the community one for those gaps.

**Scope and modes.** The bridges give the agent local access to the editor and to the engine's process tools. In manual workspaces they are a verification and evidence instrument — the user implements, the bridges observe, and they reduce what the user must capture by hand. In agentic workspaces they are also implementation tools: editor work happens through them, within approved plans and the template's authorization rules, and screenshots make that work visible. In both modes, gameplay feel, difficulty and visual judgment still require user evidence.

**Agent clients.** The bridges are plain MCP servers; only the client entry differs per agent client. Entries are given for **OpenCode** (`opencode.json`, verified on this setup) and **Claude Code** (`.mcp.json`, shape per the Claude Code MCP docs) — sections 3.3 and 4.3. Register them in every client the workspace supports, project-scoped, with equivalent entries. Tool names differ per client (OpenCode `tools.<server>.<tool>`; Claude Code `mcp__<server>__<tool>`); this file uses the bare tool names.

This file is not retained in generated workspaces by default; record its canonical source as a reference instead (same rule as the templates). The helper scripts live in this repository's `scripts/` folder.

## 1. What it is

|  | Official Unreal MCP | Community server (unreal-engine-mcp) |
|---|---|---|
| Runs | inside the editor process (engine plugins) | separate local process; talks to the editor over Python remote execution ("pyremote") |
| Reach | editor only — no server while the editor is closed | local layer (open/close/build/package) + editor layer |
| Transport | HTTP (streamable HTTP / SSE) on `127.0.0.1:8000/mcp` | multicast discovery (239.0.0.1:6766) + pyremote on loopback |
| Setup | engine plugins enabled per project + auto-start ini + client entry | venv + server install + client entry + per-project plugin + checkbox |
| Version binding | ships with the engine (the engine pin applies) | independent package — pin deliberately |
| Role | primary editor bridge | fallback for the gaps |

- Verified stack (2026-10-11, Windows 11): OpenCode V2 (2.0.26) · Unreal Engine 5.8.3 · official Unreal MCP (engine plugins `ModelContextProtocol` + `AllToolsets`; 52 toolsets registered in tool-search mode) · `unreal-engine-mcp` 0.10.0 — PyPI, MIT, github.com/FFZackFair92/unreal-engine-mcp, developed against UE 5.8. Measured per-call round trip on both bridges: ~330 ms — the floor is the client↔editor pipeline, not the transport; choose by capability and call economy, not latency.
- Official capabilities (5.8): typed toolsets — actors/components (spawn, transform, add/remove, tags), assets (find/load/save/move), Blueprints (compile, default objects, graph DSL), object properties (`list_properties` → `get_properties` / `set_properties`, reflected names — works on CDO subobjects such as `.../BP_X.Default__BP_X_C.Comp`), PIE (`StartPIE` with `options {bSimulate, playMode, warmupSeconds}` / `StopPIE`), viewport capture, logs, CVars, automation tests. Tool discovery is two-hop by default (`list_toolsets` → `describe_toolset` → `call_tool`); execution is serialized on the game thread.
- Community capabilities (editor must be running): engine, project and level status; asset and actor queries; Blueprint graph dumps (`ue_bp_list_graphs`, `ue_bp_graph_info` — node/pin/connection reads that make editor logic reviewable); skeleton inspection; Play-In-Editor start/stop with read-only in-session inspection (Appendix C); viewport screenshots returned as images; arbitrary in-editor Python (conventions and 5.8 traps: Appendix D). Process level (works without the editor): find engine installs, create projects from a spec, open and close the editor, compile C++, package the game.
- Verified in practice (2026-10-10/11): both bridges end to end — editor discovery, status, open/close and packaging (community); plugin enable, auto-start, port bind, MCP handshake and `tools/list`, typed property read/write on Blueprints, PIE start/stop and capture (official); screenshots and Python inspection (community); a full asset fix (shadow bug) driven through the official bridge with per-step verification.
- Usage discipline: issue editor-layer calls one at a time. A concurrent burst can time out even on a healthy editor (five parallel calls against a freshly started editor all hit the ~180 s timeout; the same calls succeed when issued sequentially). Both bridges serialize on the game thread.
- Probe before acting: editor-layer tools need a reachable editor — the official bridge needs its HTTP server listening (port bound), the community one `ue_editor_status`/`ue_status`. If none is running, do not blind-call editor tools and do not auto-open the editor: ask first, because startup takes minutes.
- Checks are cheapest-first: prefer the lightest check that settles the question (files and config on disk, then process state, then editor read-backs) and escalate to session or screenshot checks only when the scenario requires them. Values visible in the editor UI are evidenced by user screenshots (user-reported) — no session to read what a panel already shows; reserve sessions (Appendix C) for what the UI cannot show (constructed component trees, world transforms, cross-asset A/B, runtime wiring) or for claims that can fail despite correct configuration.
- On UE 5.8 the community server reports `blueprint_graph_authoring` available; older engines fall back to a C++-parent pattern (see the server repository).
- Capability limits to plan around. Official: no Python escape hatch; no local layer (the editor must be running); captures return base64 PNGs (1–3 MB — not inline-viewable; use the community screenshot route for viewable images); tool-search mode hides individual tool schemas until described. Community: Niagara emitter stacks and EQS are not scriptable; a landscape must already exist (it cannot be created from Python); UMG layout needs an existing root widget; compiling C++ needs the editor closed (Live Coding covers function-body changes only) and packaging always needs the editor closed.

**Working economics (why Unreal agent loops are heavier than text-first engines).** In Godot the agent works on text files and runs the engine headless; in Unreal the artifacts that matter are binary and editor-bound — expect roughly an order of magnitude more time per verified change. The structural causes, and the practice they imply:

- **Binary assets** (`.uasset`/`.umap`): no read/write/diff; edits only through the editor; git diffs of assets are unreviewable → verification goes through editor read-backs or user screenshots, and text-adjacent surfaces win when there is a choice (ini/configs, DataTable CSV/JSON, `.uplugin`).
- **No headless authoring**: the editor is a GUI process (startup in minutes, captures need focus and rendering, PIE has warmup) → keep the editor open during work sessions; reserve sessions for runtime-only facts (the cheapest-first ladder above); never auto-open.
- **Bridge economics**: ~330 ms per serialized round trip, one operation per call → batch reads into a single script call and let the typed official tools resolve names instead of guessing.
- **Hidden state**: SCS vs CDO, ownership-based rendering, tick options, PIE vs editor worlds → match the evidence to the claim ("configured correctly" ≠ "works"); the recipes in sections 6–8 and Appendices C–E exist so each discovery is paid once.

## 2. Where to start

Check both bridges:

1. Official: the project's `.uproject` lists `ModelContextProtocol` + `AllToolsets`; `Config/DefaultEditorPerProjectUserSettings.ini` contains `bAutoStartServer=True`; each supported client's project config (`opencode.json`, `.mcp.json`) has the `unreal-official` entry; with the editor running, the smoke test (Appendix E) answers.
2. Community: the isolated environment exists (`%LOCALAPPDATA%\opencode-mcp\unreal-engine-mcp\Scripts\python.exe` — the folder name is historical; any client uses it); each client's project config lists `unreal`; with an enabled project open, the discovery probe (Appendix A) finds the node.

If both hold, skip ahead to verification (section 7). Otherwise: official → section 4; community → sections 3 and 5.

## 3. Community server — machine setup (once per PC)

The official bridge needs no machine setup — it ships with the engine and loads with the editor; its client entry is written during project setup (section 4.3). The community server needs the steps below.

Prerequisites: Python 3.10–3.13 on PATH; an MCP client (OpenCode V2 and/or Claude Code); Unreal Engine installed via the Epic Games Launcher (installs are auto-detected; otherwise see `UE_MCP_ENGINE_DIRS` in the server README).

**3.1 Create the isolated environment** — keeps the server's pinned `mcp` 1.x dependency away from other Python work:

```powershell
python -m venv "$env:LOCALAPPDATA\opencode-mcp\unreal-engine-mcp"
```

**3.2 Install the server** — pin the version that was verified; upgrade deliberately later (section 9):

```powershell
& "$env:LOCALAPPDATA\opencode-mcp\unreal-engine-mcp\Scripts\python.exe" -m pip install unreal-engine-mcp==0.10.0
```

**3.3 Register it with the client** — in the Unreal project's own config, so the bridges load only where an editor can answer. OpenCode (run from the repository root; the CLI writes `opencode.json` there; finish with 3.4):

```powershell
opencode mcp add unreal -- "$env:LOCALAPPDATA\opencode-mcp\unreal-engine-mcp\Scripts\python.exe" -m unreal_mcp.server
```

Why project-scoped: registered globally, `unreal-official` reports a connection failure in every other project on the PC, and the community server adds its full tool catalog to every session there — observed 2026-10-14 with both entries in `%USERPROFILE%\.config\opencode\opencode.json`, and fixed by moving them into the Unreal repo's `opencode.json`. A global entry also works when the user prefers it; the trade is that noise.

**3.4 Add the discovery environment variable** to the generated entry in the Unreal project's `opencode.json` — final shape:

```jsonc
{
  "mcp": {
    "servers": {
      "unreal": {
        "type": "local",
        "command": [
          "C:\\Users\\<user>\\AppData\\Local\\opencode-mcp\\unreal-engine-mcp\\Scripts\\python.exe",
          "-m",
          "unreal_mcp.server"
        ],
        "environment": {
          "UE_MCP_MULTICAST_BIND": "127.0.0.1"
        }
      }
    }
  }
}
```

Why the bind matters: Unreal's Python plugin joins the discovery multicast (239.0.0.1:6766, TTL 0) on **loopback** by default. The server's default bind (all adapters) sends discovery out the default network adapter, which never reaches a loopback-bound editor — discovery fails with "no editor found" even though the editor is running. Matching both sides to loopback fixes it and also sidesteps multi-adapter machines (VPN, WSL, Hyper-V). If a project instead sets the editor's "Multicast Bind Address" to `0.0.0.0`, the server's default bind works — either side may be aligned, but the loopback pairing is the recorded standard.

Notes: the config shape is OpenCode V2 (`mcp.servers`); OpenCode V1 placed server names directly under `mcp`. Project files are discovered from the workspace directory upward — a repo-root `opencode.json` covers sessions opened in subfolders — and a project entry replaces a global entry with the same name. Tools appear to the agent as `tools.<server>.<tool>` (Code Mode groups them under the server name). New sessions pick the server up automatically; an existing session reconnects when the config content changes — this applies to both bridges. Keep the setup local: loopback discovery only, nothing published — the in-editor Python channel executes arbitrary code, so do not tunnel or expose it beyond this machine. On Windows with a restricted PowerShell execution policy, run the OpenCode CLI as `cmd /c "opencode …"` — the `.ps1` shim is otherwise blocked.

**3.5 Claude Code entry** — a repo-root `.mcp.json` (project scope; checked into the repository and shared). It carries both bridges; `${LOCALAPPDATA}` is expanded by Claude Code, so the file holds no user-specific path (forward slashes avoid JSON escaping):

```json
{
  "mcpServers": {
    "unreal": {
      "type": "stdio",
      "command": "${LOCALAPPDATA}/opencode-mcp/unreal-engine-mcp/Scripts/python.exe",
      "args": ["-m", "unreal_mcp.server"],
      "env": { "UE_MCP_MULTICAST_BIND": "127.0.0.1" }
    },
    "unreal-official": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

CLI equivalent from the repository root: `claude mcp add --scope project unreal --env UE_MCP_MULTICAST_BIND=127.0.0.1 -- <python.exe> -m unreal_mcp.server` and `claude mcp add --scope project --transport http unreal-official http://127.0.0.1:8000/mcp`. Claude Code loads project-scoped servers only after a one-time approval per machine: until then `claude mcp list` shows "Pending approval" and a session has no Unreal tools. Approve with `/mcp` in a session (or at the startup prompt); the choice is stored in the git-ignored `.claude/settings.local.json` (`enabledMcpjsonServers`) and the tools load without a restart (verified 2026-10-15). Claude Code reads `CLAUDE.md`, not `AGENTS.md` — the workspace's `CLAUDE.md` imports it (`@AGENTS.md`; core section 9).

## 4. Official Unreal MCP — setup (primary)

**4.1 Enable the plugins.** Editor: *Edit ▸ Plugins* → enable **Unreal MCP** and **All Toolsets**, restart when prompted. `Toolset Registry` (the dependency that actually holds the toolsets) and `EngineAssetDefinitions` auto-enable. `All Toolsets` is the aggregate; enable individual toolsets instead when you want a narrow surface. File route — add to the `Plugins` array of the `.uproject`:

```json
{ "Name": "ModelContextProtocol", "Enabled": true, "TargetAllowList": ["Editor"] },
{ "Name": "AllToolsets", "Enabled": true, "TargetAllowList": ["Editor"] }
```

`TargetAllowList: ["Editor"]` keeps both plugins out of packaged builds (they are marked `NoRedist` and experimental — editor usage only; packaging stays unaffected).

**4.2 Auto-start the server.** Editor: *Edit ▸ Editor Preferences ▸ General ▸ Model Context Protocol* → **Auto Start Server** (port `8000`, URL path `/mcp` by default; change them if they conflict with another local service). File route — append to `Config/DefaultEditorPerProjectUserSettings.ini`:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
```

On demand instead: leave auto-start off and run `ModelContextProtocol.StartServer` (optional port argument) in the editor console. Related commands: `ModelContextProtocol.StopServer`, `…RefreshTools` (re-poll the registry after authoring tools), `…GenerateClientConfig <Client|All>`. Tool-search mode (`bEnableToolSearch`, default on) is what exposes the three meta-tools — keep it on; it keeps `tools/list` small.

**4.3 Client config.** The plugin writes client configs for Claude Code, Cursor, VS Code, Gemini and Codex (`ModelContextProtocol.GenerateClientConfig <Client|All>` — it merges existing JSON configs; the Codex TOML is write-once). OpenCode is not among them — add the entry by hand to `mcp.servers` in the Unreal project's `opencode.json` (the same file that carries the community entry):

```jsonc
"unreal-official": {
  "type": "remote",
  "url": "http://127.0.0.1:8000/mcp",
  "oauth": false,
  "codemode": true
}
```

`oauth: false` skips the OAuth discovery attempt (the server has no authentication layer — loopback only). `codemode` groups the tools under the server in OpenCode V2 Code Mode; drop it to expose them directly. Claude Code: the `unreal-official` entry in `.mcp.json` (section 3.5) — or let the plugin generate it (`ModelContextProtocol.GenerateClientConfig ClaudeCode`) and compare the result with 3.5.

**4.4 Restart and verify.** Plugins load at editor startup; the server binds with it. Run the verification checklist (section 7). Note: the server exists only while the editor runs — the client shows a connection failure while it is closed (expected; the community bridge covers that gap where its local layer has reach).

## 5. Community server — project enable (once per Unreal project)

Two editor-only settings (packaged games are unaffected). Restart the editor after changing them. Use the editor route or the file route — they write the same entries.

**5.1 Enable the plugin.** Editor: *Edit ▸ Plugins* → search "Python" → **Python Editor Script Plugin** → restart when prompted. File route — add to the `Plugins` array of the `.uproject`:

```json
{ "Name": "PythonScriptPlugin", "Enabled": true }
```

**5.2 Allow remote execution.** Editor: *Edit ▸ Project Settings* → search "Python" → check **Enable Remote Execution** → restart. File route — append to `Config/DefaultEngine.ini`:

```ini
; MCP bridge (community server): allow Python remote execution from the local machine
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
```

After enabling on a new project, run one package to reconfirm packaging is unaffected (expected: the plugin is editor-only and is skipped).

## 6. Workspace integration (records)

For a workspace generated from the template family, fold the bridges into its records when the user asks for it. Adapt IDs and dates; keep evidence labels honest — record what was actually verified on this machine. Suggested entries:

- `AGENTS.md` (repository specifics, one line — use the variant matching the workspace's working agreement):
  - Manual: `- MCP: the official Unreal MCP (`unreal-official`, the editor's built-in ModelContextProtocol server, http://127.0.0.1:8000/mcp) is the primary editor bridge; the community pyremote server (`unreal`) covers the local layer (open/close/build/package while the editor is closed) and gaps (Python escape hatch, viewable screenshots). The working agreement is unchanged: the user implements, the agent observes and verifies; checks run cheapest-first and the agent asks before opening a closed editor — never auto-opens.`
  - Agentic: `- MCP: editor work goes through the official Unreal MCP (`unreal-official`) within approved plans; the community server (`unreal`) covers the local layer and gaps (Python, viewable screenshots). Its captures and status outputs are part of the work record.`
  - Autonomous (`AUTONOMOUS_AGENTIC_WORKSPACE_TEMPLATE.md`): as agentic, plus — the approved milestone may authorize editor open/close (record it in `AGENTS.md`; the "ask before opening" rule then applies only outside that authorization); exactly one agent drives the editor at a time (the orchestrator dispatches editor-bound cards one by one); headless checks (`UNREAL_TEST_AUTOMATION.md`) are preferred over editor sessions whenever they settle the claim.
- `MEMORY.md` — decision rows: `Official Unreal MCP (ModelContextProtocol + AllToolsets plugins; editor HTTP server at 127.0.0.1:8000/mcp) adopted as the primary agent bridge — manual: verification/evidence only, the user implements; agentic: editor implementation within approved plans.` and `Community server (unreal-engine-mcp, pyremote) retained as fallback for the local layer (editor open/close, build/package while the editor is closed) and gaps (Python exec, viewable screenshots).`
- `MEMORY.md` — conventions bullet (config): `MCP entries are project-scoped in this repository — opencode.json (OpenCode) and/or .mcp.json (Claude Code), both bridges, kept equivalent; the user's global configs carry none, so other projects on the machine load no Unreal servers.`
- Record size: the long operational bullets below are tool recipes — put them in the workspace's `docs/tooling-notes.md` with a one-line pointer in `MEMORY.md` conventions (core section 7, record size budget).
- `MEMORY.md` — conventions bullet (community): `MCP (community bridge): what the agent may change follows the applicable working agreement (manual: observe only; agentic: within approved plans). Editor-layer tools need the editor open; the local layer (open/close/build/package) does not. Screenshots need the editor window focused and rendering — retry with the same filename to attach the image (captures fail while the editor is in the background). Run `ue_save_all` before `ue_editor_close` (clean close can fall back to process termination). Issue editor calls one at a time — a concurrent burst can time out. Read-only runtime inspection: `ue_start_pie` runs the *Simulate* mode (no game pawn) — spawn into the throwaway world, inspect, then stop; assets and levels stay untouched (Appendix C).`
- `MEMORY.md` — conventions bullet (official): `Official MCP (unreal-official): editor-layer only — no server while the editor is closed (local layer stays on the community bridge); calls serialize on the game thread; discovery is two-hop (list_toolsets → describe_toolset → call_tool; pass toolset_name + the short tool_name); object refs are {"refPath": "<object path>"} (CDO subobjects like .../BP_X.Default__BP_X_C.Comp resolve); property names are the reflected camelCase keys from ObjectTools.list_properties — never guess them; CaptureViewport returns 1–3 MB base64 — for viewable captures use the community ue_screenshot trigger → same-filename check; StartPIE takes options {bSimulate, playMode, warmupSeconds}; StopPIE can ECONNRESET while the session tears down — verify or retry; aiming the PIE pawn is done via the community bridge (set_control_rotation; pawn property reads are protected in 5.8); a config-content edit hot-reloads MCP servers in a running session.`
- `MEMORY.md` — environment block: per bridge — official: plugin entries and the auto-start ini key, the client entry, toolset count and what was verified/when; community: environment path and package version, config path and the `UE_MCP_MULTICAST_BIND` requirement, which projects have the enable applied, verified dates.
- `MEMORY.md` — references rows: `Unreal MCP (official) — dev.epicgames.com "Unreal MCP in Unreal Editor" documentation; engine plugins at Engine/Plugins/Experimental/ModelContextProtocol and .../Experimental/Toolsets | <date checked> | verified toolset count, transport, config shapes.` and `unreal-engine-mcp — github.com/FFZackFair92/unreal-engine-mcp (PyPI: unreal-engine-mcp) | <date checked> | version, license, engine compatibility, tool count.`
- Plan-writing rule: quote every value exactly as the editor's UI shows it so the user can type it without translating — e.g. UE rotators are displayed as X/Y/Z (rotation about X/Y/Z = Roll/Pitch/Yaw), so write panel-ready numbers, not the classic Pitch/Yaw/Roll order.
- `MEMORY.md` — conventions bullet (reference material, for reference-driven projects): `Reference library docs/refs/<topic>/ — user captures at the root (NN_what.png), agent-fetched sets under web/ with a _sources.md provenance note (source, date, captions, usage), generated diagrams as named images. Build steps link the picture that shows them (../refs/…). Third-party material is reference-only; repository inclusion is the user's decision. Tooling: Appendix F.`

The records are the same in both modes — in agentic workspaces, performed editor actions are recorded like other executed work, screenshots included.

## 7. Verification checklist

Run after setup and after any upgrade; record the results in the workspace history.

1. **Community server launches:** the environment's python runs `-m unreal_mcp.server` without import errors, and each supported client's project config lists the server.
2. **Official server up:** the editor log shows `LogModelContextProtocol: Tool search enabled: registered 3 meta-tools (<N> toolsets discoverable)`, and the port is bound to the editor process (`netstat -ano | findstr :8000`).
3. **Official handshake:** the smoke test (Appendix E) negotiates a protocol version, `tools/list` returns the three meta-tools and `list_toolsets` returns the toolsets.
4. **Editor ready:** the project is open; the editor log shows `Python enabled` (community) and no load errors for the enabled plugins.
5. **Session:** the client shows both servers connected (OpenCode MCP panel; Claude Code `/mcp`); the official tools group under `unreal-official`; one typed read works (e.g. `ObjectTools.get_properties` on a component); the community `ue_status` returns the expected engine version, project file, current level, actor count, `transport: "pyremote"` and capabilities.
6. **Vision:** with the editor window focused, the community `ue_screenshot` (retry with the same filename) attaches the image; it matches the editor viewport.
7. **Lifecycle:** `ue_save_all` then `ue_editor_close` leaves no editor process behind; `ue_editor_open` brings the editor back and `ue_editor_status` reaches `bridge_ready`; in-session inspection works (Appendix C).

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "No editor found" / errors about `127.0.0.1:30010` (community) | Plugin or checkbox missing; editor not restarted; multicast bind mismatch; VPN or firewall swallowing multicast | Re-check section 5; align the bind per section 3; confirm with the probe; fallback: `UE_MCP_TRANSPORT=remotecontrol` (see the server README and SECURITY.md) |
| Official server not listening | Plugins not enabled/loaded, the ini file not read, or a port conflict | Re-check section 4; look for the startup log line; `netstat -ano \| findstr :8000`; change the port in Editor Preferences if it is taken |
| `StartPIE` says "A play session is already running" | A previous PIE session was not stopped (e.g. its stop call errored) | Run `StopPIE`, then retry |
| `StopPIE` fails with a connection reset | The editor tears the session down while the request is in flight | Treat the stop as likely done; confirm and retry if needed |
| Official capture params rejected ("needs a default value") | Schema quirk: optional-looking parameters must still be passed | Supply them explicitly (`captureTransform: null`, a full `annotations` object) |
| A Blueprint asset is rejected as "not a valid Actor" | Some component tools require live instances | Spawn the class into the level (SceneTools), read the instance, remove it — or use the documented asset-level tools |
| Property write fails / unknown property | Reflected property names cannot be guessed | `ObjectTools.list_properties` first, then `get_properties`/`set_properties` with those exact keys |
| Huge inline base64 from `CaptureViewport` | Captures return PNG base64 (1–3 MB) | Use the community `ue_screenshot` route for viewable captures |
| Claude Code: no Unreal tools; `claude mcp list` shows "Pending approval" | Project-scoped `.mcp.json` servers are not approved on this machine yet | Run `/mcp` in the session and approve both (section 3.5) |
| Tools missing from a session | Server process stopped or connection dropped | Content change in the config (global or project) triggers a reconnect, or start a new session; do not manage server processes manually — killing them removes the tools until reconnection |
| Unrelated projects show `unreal-official` failed or list Unreal tools | Both entries were registered in the user's global config, but the bridges only have reach around the editor project | Move both entries into the Unreal project's config — `opencode.json` (sections 3.3–3.4, 4.3) or `.mcp.json` (3.5) |
| `ue_exec_python` returns `null` | The snippet's value was not assigned to the `result` variable (`print()` output is not captured) | Assign the value to be returned to `result`; conventions in Appendix D |
| Several editor calls made at once all time out | The calls were issued concurrently, possibly against a busy or just-started editor | Re-issue them one at a time — the editor is usually fine |
| `opencode mcp list` reports `failed: exited with code 255` | The CLI's own probe teardown is reported as a failure even when the server serves sessions fine | Ignore; verify via a session or the probe instead |
| `opencode mcp list` shows no servers (or another project's) for a repo that has a project config | The CLI queries the shared background service, whose config resolves for the service's own location | Check per-directory resolution instead: `opencode debug config` run in the repo or `/mcps` in the TUI opened there |
| `ue_screenshot` returns `captured: false` | The editor window is not in the foreground — viewport rendering pauses in the background, so the deferred capture never completes (nor does `HighResShot` write) | Refocus the editor window, then retry with the same filename to attach the image |
| `ue_editor_close` fell back to "process terminated" | The clean close path is unavailable in some setups (e.g., pyremote-only) — observed even with `ue_save_all` returning `saved: true` and no dirty assets | Expected; the fallback exits cleanly (confirm with `ue_editor_status`: `running: false`, no orphans). Run `ue_save_all` first anyway; the close path may auto-save dirty assets — review unexpected binary diffs (e.g., level files) before committing |
| Discovery worked earlier, tool calls now fail | Editor closed or crashed | Confirm with `ue_editor_status`/`ue_status`; if closed, ask before reopening (`ue_editor_open` — deliberate, takes minutes) |
| Packaging fails after the enables | A plugin not treated as editor-only | Check the failing plugin's `TargetAllowList`; keep the bridge plugins editor-only — do not disable the bridges wholesale |

## 9. Maintenance

- **Official MCP:** ships with the engine — after an engine upgrade, re-verify section 7 and the toolset list (`ModelContextProtocol.RefreshTools` re-polls the registry; the plugin names, console commands and settings keys are the stable identifiers; schemas and data formats are experimental and may change).
- **Community server upgrades:** `pip install --upgrade unreal-engine-mcp` in the environment, then re-run section 7; re-pin deliberately.
- **Engine upgrades:** check the community server's version-compatibility table before upgrading UE; the plugin enable, loopback bind and official-MCP entries carry over. The Appendix D notes are version-bound — re-verify them after an engine upgrade.
- **Client upgrades:** the config shape can change between majors (OpenCode V1 vs V2); re-check the client's MCP view (`/mcps` in OpenCode, `/mcp` in Claude Code) if a server stops connecting.
- **Document maintenance:** when the setup process changes during a project, update this file (it is the template family's shared reference) and keep the companion references in the two templates in sync.

## Appendix A — discovery probe (community)

Standard library only; run with any Python 3.10+ (works without an MCP client). Finds every editor publishing Python remote execution on this machine. Adjust `ENGINE_PY` to the installed engine version.

Script: [`scripts/ue-discovery-probe.py`](scripts/ue-discovery-probe.py) — prints `FOUND: [...]` or `FOUND: none`.

## Appendix B — MCP stdio smoke test (community)

Handshake, tool count and `ue_status` without an MCP client — useful to separate server problems from client problems.

Script: [`scripts/mcp-smoke.py`](scripts/mcp-smoke.py) — prints `init`, the tool count and the start of the `ue_status` reply. Adjust `PY` if the environment lives elsewhere.

## Appendix C — read-only in-session inspection (community)

Some things exist only while a game session runs: a pawn's constructed component hierarchy, attachment sockets, live transforms, animation state. Blueprint construction scripts do not run in the asset (Appendix D), so read them from a live instance instead.

Recipe — nothing is saved; assets and levels are untouched:

1. Start the session: `ue_start_pie`. In this server version it starts the **Simulate** mode — a throwaway world with no possessed pawn. Editor Python reaches it via `unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()` (poll briefly if the session is still starting).
2. Spawn the Blueprint to inspect into that world. The `GameplayStatics` spawn helpers are not bound in this build; the reliable route is the console: `unreal.SystemLibrary.execute_console_command(world, 'summon /Game/Path/BP_Thing.BP_Thing_C')`, then fetch the instance with `unreal.GameplayStatics.get_all_actors_of_class(world, cls)`.
3. Read what you need — `get_components_by_class(unreal.SceneComponent)` returns the full constructed tree; per component: `get_attach_parent()`, `get_attach_socket_name()` (a bone name works as a socket), `get_world_location()`, `get_socket_location('<bone>')`.
4. Destroy the instance (`destroy_actor`) and stop the session (`ue_stop_pie`).
5. If a snippet raises, the tool returns the traceback but the session keeps running — stop it explicitly.

For visual runtime checks, prefer the check helpers (Appendix G — real PIE, aimed captures, runtime hide A/B; community bridge only). Manual route: the official bridge starts a real, possessed PIE session (`EditorAppToolset.StartPIE`, `options {bSimulate: false, playMode: "PlayMode_InViewPort", warmupSeconds: N}`) and `StopPIE` ends it; to capture what the player sees from an arbitrary look angle, aim the possessed pawn through the community bridge (`PlayerController.set_control_rotation`) and take the community `ue_screenshot` (trigger → same-filename check) — the official `CaptureViewport` also renders, but returns its image as base64 too heavy to hand back inline.

Compact example:

```python
import unreal, time
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()  # poll with time.sleep if the session just started
cls = unreal.load_class(None, '/Game/Path/BP_Thing.BP_Thing_C')
unreal.SystemLibrary.execute_console_command(world, 'summon /Game/Path/BP_Thing.BP_Thing_C')
time.sleep(2)
actor = unreal.GameplayStatics.get_all_actors_of_class(world, cls)[0]
for c in actor.get_components_by_class(unreal.SceneComponent):
    parent = c.get_attach_parent()
    print(c.get_name(), '->', parent.get_name() if parent else '(root)', '| socket:', c.get_attach_socket_name())
actor.destroy_actor()
result = 'inspection done'
```

This route resolved a first-person camera's attach chain on UE 5.8 when the static APIs were blocked.

## Appendix D — UE 5.8 in-editor Python notes (community)

Verified on 5.8.3 (2026-10-10/11); re-verify after engine upgrades (Maintenance).

**Escape-hatch conventions.** `ue_exec_python` returns the snippet's `result` variable — assign the value you want back (`print()` is not captured). The snippet runs with the `unreal` module and the server's own `mcp_*` helpers available; exceptions return a traceback and leave any running session alive.

**Reading Blueprints — prefer live instances.**
- Components added in a Blueprint's construction script (SCS) do not appear in `get_components_by_class` on the generated class's default object — construction does not run on CDOs; the attach/socket chain cannot be read that way.
- `SubobjectDataSubsystem.k2_gather_subobject_data_for_blueprint()` returns handles whose data fields (parent handle, etc.) are Python-protected and whose `SCS_Node` objects come back untyped — attach parents and variable names cannot be read this way. The component *templates* are reachable, though: `SubobjectDataBlueprintFunctionLibrary.get_object(…get_data(handle))` returns each component (inherited native ones included) with readable and writable properties — the basis of `bp_diff` (Appendix G; verified 2026-10-15). Edits made there persist after compile + save.
- Use the Appendix C recipe instead; a live instance exposes everything: parents, sockets/bones, world transforms, per-component flags.
- Static reads that do work: class defaults via `unreal.get_default_object(bp.generated_class())` (movement settings, camera classes, property values), subobject templates via `unreal.load_object(outer, name)` (names carry generated suffixes like `_GEN_VARIABLE` / `__CCE3C0B4`). Caveat: component *transform* values can be constructor-set and read as zeroes on default subobjects — read placements from a live instance.
- Where possible, prefer the official bridge's typed property tools (`ObjectTools.list_properties` → `get_properties` / `set_properties`) over hand-built Python reads — they resolve reflected names and CDO subobjects (`.../BP_X.Default__BP_X_C.Comp`) for you.

**Enhanced Input.** Read a mapping context as `get_editor_property('default_key_mappings').mappings` — the plain `mappings` property reads empty on 5.8. A mapping's key is an `FKey` whose name reads via `export_text()` (e.g. `Gamepad_Left2D`, `Mouse2D`); `to_dict()`/`to_tuple()` return empty. Modifier objects read normally via `get_editor_property` (including `InputModifierNegate`'s X/Y/Z flags).

**Binding names.** `unreal.SystemLibrary` is the Python name (no `Kismet` prefix) — `unreal.KismetSystemLibrary` does not exist. A skeleton's `sockets` property is protected — use the `ue_skeleton_info` tool; a skeleton may have no sockets at all (attach points can be pure bones, and the editor's parent-socket picker accepts them). A `BlueprintGeneratedClass` exposes no superclass getter (`get_super_class`/`get_super_struct` unbound) — check inheritance with `isinstance` on a summoned instance.

**Collections and controller reads.** `unreal.GameplayStatics.get_all_actors_of_class` returns an unreal Array — `isinstance(x, list)` is False; use `len()` / indexing. A `PlayerController`'s `pawn` property is Python-protected (reads raise): to aim a possessed pawn, call `set_control_rotation` on the controller (the pawn's yaw follows it for characters with `Use Controller Rotation Yaw`).

**Session control.** `unreal.LevelEditorSubsystem` carries `editor_play_simulate`, `editor_request_end_play` and `is_in_play_in_editor`; the running world comes from `unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()`. In this server version `ue_start_pie` maps to Simulate (no possessed pawn); `LevelEditorSubsystem.editor_request_begin_play()` starts a real, possessed PIE from Python (verified 2026-10-15). `unreal.AutomationLibrary.take_high_res_screenshot(w, h, path)` captures the PIE view to a file on the next frame.

## Appendix E — official server smoke test

Standard library only; run with any Python 3.10+ against a running editor. Verifies the official server without an MCP client: handshake, the meta-tools and the toolset list.

Script: [`scripts/unreal-official-smoke.py`](scripts/unreal-official-smoke.py) — prints the negotiated protocol version, the meta-tools and the start of the toolset list.

## Appendix F — reference material pipeline (agent-side)

Reference-driven projects (recreating a level, UI or asset from source material) need the agent to fetch, convert, compose and generate images. All of it runs on a stock Windows machine with Windows PowerShell — no ImageMagick, Pillow or ffmpeg required.

**Finding and fetching.**
- Sites behind Cloudflare (most wikis, including Fandom) block plain HTTP clients with a challenge page — use the site's API instead. MediaWiki: `…/api.php?action=query&list=allimages&aiprefix=<prefix>&ailimit=200&format=json` lists files; `action=query&titles=File:<name>&prop=imageinfo&iiprop=url|size` resolves direct URLs. The HTML page fails; the API passes.
- Guide/portal pages often serve responsive image sets — the `<picture>` element names the real files (typically `<name>-medium.webp` for desktop); fetch those, never the thumbnails.
- Download with `Invoke-WebRequest -Uri <url> -OutFile <path> -UseBasicParsing`.

**Converting and composing (WPF imaging in Windows PowerShell).**
- Decode anything the OS has a codec for (webp included) and re-encode: `System.Windows.Media.Imaging.BitmapImage` (`CacheOption = OnLoad`) → `PngBitmapEncoder` / `JpegBitmapEncoder` (`QualityLevel = 85` turns 1024×576 screenshots from ~430 KB PNG into ~60 KB JPEG).
- Contact sheet: draw the decoded frames into a `DrawingVisual` (`DrawImage` per cell, `FormattedText` for labels), render with `RenderTargetBitmap`, encode once.
- PowerShell trap: inline arithmetic inside `New-Object Type($a, $b + $c)` can parse as extra arguments ("Cannot find an overload … argument count 4") — assign compound values to variables first.

**Generating diagrams.**
- Deterministic diagrams (plan views, coordinate grids, zone maps) are drawn from the project's own numbers, so they stay true to the spec and are cheap to redraw — use them instead of AI-generated imagery for build work. `System.Drawing` (GDI+) covers grids, rectangles and labels; save PNG or JPEG. Scale grids to the project's real dimensions, label a datum and the cell size, and mark the image as a template in its corner.
- Keep generator scripts in one place so a diagram can be re-drawn when its numbers change.

**Storing and using.**
- One library per topic under `docs/refs/<topic>/`: user captures at the root (`NN_what.png`), agent-fetched sets in a `web/` subfolder with a `_sources.md` beside them (source URLs with dates, cleaned captions, usage note), generated diagrams as named images.
- Plans wrap the pictures into the build steps (relative `../refs/…` links render in most viewers and repositories). Open frames at full size — previews hide detail. Portals' frames carry watermarks and HUD; the user's own captures stay primary where they exist.
- Third-party material is reference-only — never shipped with the project; whether the repository carries it is the user's decision (and an explicit ignore/attribute decision, e.g. plain binary images next to LFS-tracked assets).

## Appendix G — agent check helpers (in-editor, community bridge)

Script: [`scripts/ue_checks.py`](scripts/ue_checks.py) — copy it into the workspace's `tools/` and record it in the workspace's tooling notes. Read-only: nothing is saved; PIE helpers act on a throwaway play world. It is imported into the editor through `ue_exec_python` (loader snippet in its docstring, once per editor session — it locates `tools/` above the project directory), so it works the same from any agent client and model.

- **Runtime visual check:** `pie_start()` → `pie_shot("name", pitch=…, yaw=…, hide=[component names])` per angle or variant → `pie_stop()` (reports which captures were written) → view `Saved/Screenshots/Checks/<name>.png` with the client's image reader (or the community `ue_screenshot` while PIE runs, for clients that cannot read image files). An A/B isolation is two shots, with and without `hide`. About 4 calls for two angles, against ~6 for the manual two-bridge route in Appendix C; the editor must be in the foreground.
- **Blueprint parity:** `bp_diff(path_a, path_b)` — every reflected property of both component trees (inherited native components included) and the class defaults; structs flattened one level, 2-decimal tolerance, own-subobject paths normalized; returns only the differing keys plus unmatched components. Use it whenever a project Blueprint is compared with a template or reference — a hand-picked property list missed UE 5.6+ First Person Rendering (`FirstPersonPrimitiveType` on both meshes, the camera's first-person FOV/scale) and let a view artifact persist (2026-10-15).

Verified on UE 5.8.3 from a Claude Code session (2026-10-15); it depends only on `ue_exec_python`, which every client configured per section 3 exposes.

---

*First authored 2026-10-10 from a verified setup (Windows 11 · OpenCode 2.0.26 · unreal-engine-mcp 0.10.0 · Unreal Engine 5.8.3); extended 2026-10-10 with in-session verification learnings (Appendices C–D, verified-list refresh, usage discipline), the checks discipline (probe-before-acting, cheapest-first, ask before opening; screenshot focus) and the evidence-economy rule (panel values evidenced by screenshots; sessions reserved for construction/runtime facts) with panel-ready plan values. Extended 2026-10-11 with the official Unreal MCP — two-bridge structure and capability table, official setup (plugins, auto-start, client config) and operational notes, verification checklists, troubleshooting rows and Appendix E (verified against the live server). Extended 2026-10-12 with the reference-material pipeline (Appendix F — fetching, conversion, contact sheets, generated diagrams) and the matching record snippet in section 6. Extended 2026-10-14 with project-scoped client entries — both bridges in the Unreal project's `opencode.json` instead of the user's global config (sections 2–4, 6–8) — after the global-entry failure mode was hit in a non-Unreal project, and with the `opencode mcp list` location note. Restructured 2026-10-15: client-neutral framing with a Claude Code entry (`.mcp.json`, section 3.5 — config resolution verified with `claude mcp list`; a live session connection not yet verified) next to the verified OpenCode entries; the appendix scripts moved to `scripts/`; record-size pointer in section 6. Extended 2026-10-15 (later) after a live Claude Code session: approval step and troubleshooting row, Python-started real PIE and component-template access (Appendix D corrections), and the agent check helpers (Appendix G, `scripts/ue_checks.py`). When the setup process changes, update this file and the repository index (`README.md`) together.*
