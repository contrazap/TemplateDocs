# Unreal MCP bridge — setup and workspace integration

An optional tooling companion for Unreal Engine workspaces created from `MANUAL_IMPLEMENTATION_WORKSPACE_TEMPLATE.md` or `AGENTIC_LEARNING_WORKSPACE_TEMPLATE.md`. It documents the Unreal MCP bridge: an MCP server that lets the agent inspect and drive a running Unreal Editor over a local connection (engine and project status, asset and level queries, actor inspection, screenshots returned to the agent, Play-In-Editor control) plus process-level tools that open, close, build and package projects without the editor.

**Scope and modes.** The bridge gives the agent local access to the editor and to the engine's process tools. In manual workspaces it is a verification and evidence instrument — the user implements, the bridge observes, and it reduces what the user must capture by hand. In agentic workspaces it is also an implementation tool: editor work happens through it, within approved plans and the template's authorization rules, and screenshots make that work visible. In both modes, gameplay feel, difficulty and visual judgment still require user evidence.

This file is not retained in generated workspaces by default; record its canonical source as a reference instead (same rule as the templates).

## 1. What it is

- One machine-level setup drives whichever Unreal Editor instance is running on the PC (the server auto-detects it; `UE_MCP_PROJECT` disambiguates when several editors are open). Each Unreal project needs a two-step enablement (section 4).
- Verified stack (2026-10-10, Windows 11): OpenCode V2 (2.0.26) · `unreal-engine-mcp` 0.10.0 — PyPI, MIT, github.com/FFZackFair92/unreal-engine-mcp, developed against UE 5.8 — · Unreal Engine 5.8.3. Transport: the engine's built-in Python remote execution ("pyremote"); the Remote Control API is not required.
- Process level (works without the editor): find engine installs, create projects from a spec, open and close the editor, compile C++, package the game.
- Editor level (editor must be running): engine, project and level status; asset and actor queries and edits; level, material, Blueprint, behavior-tree and audio operations; Play-In-Editor control; viewport screenshots returned to the agent as images; arbitrary in-editor Python for checks or scripted edits (conventions and 5.8 traps: Appendix D).
- Verified in practice (2026-10-10, setup session plus the first project-verification session): editor discovery, engine/project status and capabilities, editor open/close, viewport screenshots (returned to the agent as images), the Python escape hatch, actor and asset queries, Blueprint graph dumps (`ue_bp_list_graphs`, `ue_bp_graph_info` — node/pin/connection reads that make editor logic reviewable), skeleton inspection, and Play-In-Editor start/stop with read-only in-session inspection (Appendix C). Build/package and the remaining edit APIs come from the server's documented surface — re-verify the ones a project relies on.
- Usage discipline: issue editor-layer calls one at a time. A concurrent burst can time out even on a healthy editor (five parallel calls against a freshly started editor all hit the ~180 s timeout; the same calls succeed when issued sequentially).
- Probe before acting: `ue_editor_status`/`ue_status` report whether an editor is reachable — if none is running, do not blind-call editor tools and do not auto-open the editor: ask first, because startup takes minutes.
- Checks are cheapest-first: prefer the lightest check that settles the question (files and config on disk, then process state, then editor read-backs) and escalate to session or screenshot checks only when the scenario requires them.
- On UE 5.8 the server reports `blueprint_graph_authoring` available; older engines fall back to a C++-parent pattern (see the server repository).
- Capability limits to plan around (server-documented): Niagara emitter stacks and EQS are not scriptable; a landscape must already exist (it cannot be created from Python); UMG layout needs an existing root widget; compiling C++ needs the editor closed (Live Coding covers function-body changes only) and packaging always needs the editor closed.

## 2. Where to start

Check whether this machine is already set up:

1. The isolated environment exists: `%LOCALAPPDATA%\opencode-mcp\unreal-engine-mcp\Scripts\python.exe`.
2. The OpenCode global config has the server: `%USERPROFILE%\.config\opencode\opencode.json` → `mcp.servers.unreal`.
3. With an enabled project open in the editor, the discovery probe (Appendix A) finds the node.

If all three hold, skip section 3. Otherwise do section 3, then the per-project steps (4–5) and verify (6).

## 3. Machine setup (once per PC)

Prerequisites: Python 3.10–3.13 on PATH; OpenCode V2; Unreal Engine installed via the Epic Games Launcher (installs are auto-detected; otherwise see `UE_MCP_ENGINE_DIRS` in the server README).

**3.1 Create the isolated environment** — keeps the server's pinned `mcp` 1.x dependency away from other Python work:

```powershell
python -m venv "$env:LOCALAPPDATA\opencode-mcp\unreal-engine-mcp"
```

**3.2 Install the server** — pin the version that was verified; upgrade deliberately later (section 8):

```powershell
& "$env:LOCALAPPDATA\opencode-mcp\unreal-engine-mcp\Scripts\python.exe" -m pip install unreal-engine-mcp==0.10.0
```

**3.3 Register it with OpenCode** — user-level, so every project on the PC can use it:

```powershell
opencode mcp add unreal --global -- "$env:LOCALAPPDATA\opencode-mcp\unreal-engine-mcp\Scripts\python.exe" -m unreal_mcp.server
```

**3.4 Add the discovery environment variable** to the generated entry in `%USERPROFILE%\.config\opencode\opencode.json` — final shape:

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

Notes: the global config shape is OpenCode V2 (`mcp.servers`); OpenCode V1 placed server names directly under `mcp`. Tools appear to the agent as `tools.<server>.<tool>` (Code Mode groups them under the server name). New sessions pick the server up automatically; an existing session reconnects when the config content changes. Keep the setup local: loopback discovery only, nothing published — the in-editor Python channel executes arbitrary code, so do not tunnel or expose it beyond this machine.

## 4. Project enable (once per Unreal project)

Two editor-only settings (packaged games are unaffected). Restart the editor after changing them. Use the editor route or the file route — they write the same entries.

**4.1 Enable the plugin.** Editor: *Edit ▸ Plugins* → search "Python" → **Python Editor Script Plugin** → restart when prompted. File route — add to the `Plugins` array of the `.uproject`:

```json
{ "Name": "PythonScriptPlugin", "Enabled": true }
```

**4.2 Allow remote execution.** Editor: *Edit ▸ Project Settings* → search "Python" → check **Enable Remote Execution** → restart. File route — append to `Config/DefaultEngine.ini`:

```ini
; MCP bridge (unreal-engine-mcp): allow Python remote execution from the local machine
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
```

After enabling on a new project, run one package to reconfirm packaging is unaffected (expected: the plugin is editor-only and is skipped).

## 5. Workspace integration (records)

For a workspace generated from the template family, fold the bridge into its records when the user asks for it. Adapt IDs and dates; keep evidence labels honest — record what was actually verified on this machine. Suggested entries:

- `AGENTS.md` (repository specifics, one line — use the variant matching the workspace's working agreement):
  - Manual: `- MCP: OpenCode's `unreal` server (user-level; see `docs/MEMORY.md` environment) is the agent's verification/evidence instrument for the editor — the working agreement is unchanged: the user implements, the agent observes and verifies.`
  - Agentic: `- MCP: OpenCode's `unreal` server (user-level; see `docs/MEMORY.md` environment) is the agent's editor tool — editor work happens through it within approved plans, and its screenshots and status outputs are part of the work record.`
- `MEMORY.md` — decision row: `Unreal MCP bridge adopted for this workspace (user-level `unreal` server in OpenCode; per-project enable = PythonScriptPlugin + bRemoteExecution; loopback multicast bind required on this machine) — manual: verification/evidence only, the user implements; agentic: editor implementation and visual verification within approved plans.`
- `MEMORY.md` — conventions bullet: `MCP (unreal bridge): what the agent may change follows the applicable working agreement (manual: observe only; agentic: within approved plans). Editor-layer tools need the editor open; the local layer (open/close/build/package) does not. Checks are cheapest-first and probe before acting (`ue_editor_status`/`ue_status`); if the editor is closed, ask before opening — never blind-call or auto-open. Screenshots need the editor window focused and rendering — retry with the same filename to attach the image (captures fail while the editor is in the background). Run `ue_save_all` before `ue_editor_close` (clean close can fall back to process termination). Issue editor calls one at a time — a concurrent burst can time out. Read-only runtime inspection: `ue_start_pie` runs the *Simulate* mode (no game pawn) — spawn into the throwaway world, inspect, then stop; assets and levels stay untouched (Appendix C).`
- `MEMORY.md` — environment block: server environment path and package version; OpenCode global config path and the `UE_MCP_MULTICAST_BIND` requirement; which projects have the enable applied; what was verified and when.
- `MEMORY.md` — references row: `unreal-engine-mcp — github.com/FFZackFair92/unreal-engine-mcp (PyPI: unreal-engine-mcp) | <date checked> | version, license, engine compatibility, tool count.`

The records are the same in both modes — in agentic workspaces, performed editor actions are recorded like other executed work, screenshots included.

## 6. Verification checklist

Run after setup and after any upgrade; record the results in the workspace history.

1. **Server launches:** the environment's python runs `-m unreal_mcp.server` without import errors, and the OpenCode config lists the server.
2. **Editor ready:** the project is open; the editor log shows `Python enabled` and no load errors for `PythonScriptPlugin`.
3. **Discovery:** Appendix A finds one node whose `engine_version` matches the installed engine.
4. **Session:** in OpenCode, the server is connected and reports tools; `ue_status` returns the expected engine version, project file, current level, actor count, `transport: "pyremote"` and capabilities.
5. **Vision:** with the editor window focused, `ue_screenshot` (retry with the same filename) attaches the image; it matches the editor viewport.
6. **Lifecycle:** `ue_save_all` then `ue_editor_close` leaves no editor process behind; `ue_editor_open` brings the editor back and `ue_editor_status` reaches `bridge_ready`.
7. **In-session inspection (optional):** `ue_start_pie` reaches a running session; the Appendix C recipe can summon, inspect and destroy an actor inside it; `ue_stop_pie` ends it with no leftovers.

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "No editor found" / errors about `127.0.0.1:30010` | Plugin or checkbox missing; editor not restarted; multicast bind mismatch; VPN or firewall swallowing multicast | Re-check section 4; align the bind per section 3; confirm with the probe; fallback: `UE_MCP_TRANSPORT=remotecontrol` (see the server README and SECURITY.md) |
| Tools missing from a session | Server process stopped or connection dropped | Content change in the global config triggers a reconnect, or start a new session; do not manage server processes manually — killing them removes the tools until reconnection |
| `ue_exec_python` returns `null` | The snippet's value was not assigned to the `result` variable (`print()` output is not captured) | Assign the value to be returned to `result`; conventions in Appendix D |
| Several editor calls made at once all time out | The calls were issued concurrently, possibly against a busy or just-started editor | Re-issue them one at a time — the editor is usually fine |
| `opencode mcp list` reports `failed: exited with code 255` | The CLI's own probe teardown is reported as a failure even when the server serves sessions fine | Ignore; verify via a session or the probe instead |
| `ue_screenshot` returns `captured: false` | The editor window is not in the foreground — viewport rendering pauses in the background, so the deferred capture never completes (nor does `HighResShot` write) | Refocus the editor window, then retry with the same filename to attach the image |
| `ue_editor_close` fell back to "process terminated" | The clean close path is unavailable in some setups (e.g., pyremote-only) — observed even with `ue_save_all` returning `saved: true` and no dirty assets | Expected; the fallback exits cleanly (confirm with `ue_editor_status`: `running: false`, no orphans). Run `ue_save_all` first anyway; the close path may auto-save dirty assets — review unexpected binary diffs (e.g., level files) before committing |
| Discovery worked earlier, tool calls now fail | Editor closed or crashed | Confirm with `ue_editor_status`/`ue_status`; if closed, ask before reopening (`ue_editor_open` — deliberate, takes minutes) |
| Packaging fails after the enable | Plugin not treated as editor-only | Check the failure; keep the plugin entry editor-only — do not disable the bridge wholesale |

## 8. Maintenance

- **Server upgrades:** `pip install --upgrade unreal-engine-mcp` in the environment, then re-run section 6; re-pin deliberately.
- **Engine upgrades:** check the server's version-compatibility table before upgrading UE; the plugin enable and loopback bind carry over unchanged. The Appendix D notes are version-bound — re-verify them after an engine upgrade.
- **OpenCode upgrades:** the config shape can change between majors (V1 vs V2); re-check the MCP panel if a server stops connecting.
- **Document maintenance:** when the setup process changes during a project, update this file (it is the template family's shared reference) and keep the companion references in the two templates in sync.

## Appendix A — discovery probe

Standard library only; run with any Python 3.10+ (works without OpenCode). Finds every editor publishing Python remote execution on this machine. Adjust `ENGINE_PY` to the installed engine version.

```python
# ue-discovery-probe.py
import sys, time

ENGINE_PY = r"C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python"
sys.path.insert(0, ENGINE_PY)

import remote_execution as re

config = re.RemoteExecutionConfig()  # defaults: 239.0.0.1:6766 · bind 127.0.0.1 · TTL 0 (this host only)
session = re.RemoteExecution(config)
session.start()

deadline = time.time() + 6
nodes = []
while time.time() < deadline and not nodes:
    nodes = session.remote_nodes
    time.sleep(0.5)

print("FOUND:", nodes if nodes else "none")
session.stop()
```

## Appendix B — MCP stdio smoke test

Handshake, tool count and `ue_status` without OpenCode — useful to separate server problems from client problems.

```python
# mcp-smoke.py
import json, os, queue, subprocess, threading, time

PY = os.path.expandvars(r"%LOCALAPPDATA%\opencode-mcp\unreal-engine-mcp\Scripts\python.exe")
env = dict(os.environ, UE_MCP_MULTICAST_BIND="127.0.0.1")

proc = subprocess.Popen([PY, "-m", "unreal_mcp.server"], stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1, env=env)
inbox = queue.Queue()
threading.Thread(target=lambda: [inbox.put(l) for l in proc.stdout], daemon=True).start()

def send(obj): proc.stdin.write(json.dumps(obj) + "\n"); proc.stdin.flush()
def wait(want, timeout=120):
    end = time.time() + timeout
    while time.time() < end:
        try: line = inbox.get(timeout=1)
        except queue.Empty: continue
        msg = json.loads(line)
        if msg.get("id") == want: return msg
    return None

send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "0"}}})
print("init:", "ok" if wait(1) else "FAILED")
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
r = wait(2); print("tools:", len(r["result"]["tools"]) if r else "FAILED")
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ue_status", "arguments": {}}})
r = wait(3); print("ue_status:", json.dumps(r)[:400] if r else "FAILED")
proc.terminate()
```

## Appendix C — read-only in-session inspection

Some things exist only while a game session runs: a pawn's constructed component hierarchy, attachment sockets, live transforms, animation state. Blueprint construction scripts do not run in the asset (Appendix D), so read them from a live instance instead.

Recipe — nothing is saved; assets and levels are untouched:

1. Start the session: `ue_start_pie`. In this server version it starts the **Simulate** mode — a throwaway world with no possessed pawn. Editor Python reaches it via `unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()` (poll briefly if the session is still starting).
2. Spawn the Blueprint to inspect into that world. The `GameplayStatics` spawn helpers are not bound in this build; the reliable route is the console: `unreal.SystemLibrary.execute_console_command(world, 'summon /Game/Path/BP_Thing.BP_Thing_C')`, then fetch the instance with `unreal.GameplayStatics.get_all_actors_of_class(world, cls)`.
3. Read what you need — `get_components_by_class(unreal.SceneComponent)` returns the full constructed tree; per component: `get_attach_parent()`, `get_attach_socket_name()` (a bone name works as a socket), `get_world_location()`, `get_socket_location('<bone>')`.
4. Destroy the instance (`destroy_actor`) and stop the session (`ue_stop_pie`).
5. If a snippet raises, the tool returns the traceback but the session keeps running — stop it explicitly.

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

## Appendix D — UE 5.8 in-editor Python notes

Verified on 5.8.3 (2026-10-10); re-verify after engine upgrades (Maintenance).

**Escape-hatch conventions.** `ue_exec_python` returns the snippet's `result` variable — assign the value you want back (`print()` is not captured). The snippet runs with the `unreal` module and the server's own `mcp_*` helpers available; exceptions return a traceback and leave any running session alive.

**Reading Blueprints — prefer live instances.**
- Components added in a Blueprint's construction script (SCS) do not appear in `get_components_by_class` on the generated class's default object — construction does not run on CDOs; the attach/socket chain cannot be read that way.
- `SubobjectDataSubsystem.k2_gather_subobject_data_for_blueprint()` returns handles, but the data fields (parent handle, etc.) are Python-protected and `SCS_Node` objects come back as untyped objects — `component_template` and attach/variable names cannot be read. Do not build tooling on this path.
- Use the Appendix C recipe instead; a live instance exposes everything: parents, sockets/bones, world transforms, per-component flags.
- Static reads that do work: class defaults via `unreal.get_default_object(bp.generated_class())` (movement settings, camera classes, property values), subobject templates via `unreal.load_object(outer, name)` (names carry generated suffixes like `_GEN_VARIABLE` / `__CCE3C0B4`). Caveat: component *transform* values can be constructor-set and read as zeroes on default subobjects — read placements from a live instance.

**Enhanced Input.** Read a mapping context as `get_editor_property('default_key_mappings').mappings` — the plain `mappings` property reads empty on 5.8. A mapping's key is an `FKey` whose name reads via `export_text()` (e.g. `Gamepad_Left2D`, `Mouse2D`); `to_dict()`/`to_tuple()` return empty. Modifier objects read normally via `get_editor_property` (including `InputModifierNegate`'s X/Y/Z flags).

**Binding names.** `unreal.SystemLibrary` is the Python name (no `Kismet` prefix) — `unreal.KismetSystemLibrary` does not exist. A skeleton's `sockets` property is protected — use the `ue_skeleton_info` tool; a skeleton may have no sockets at all (attach points can be pure bones, and the editor's parent-socket picker accepts them).

**Session control.** `unreal.LevelEditorSubsystem` carries `editor_play_simulate`, `editor_request_end_play` and `is_in_play_in_editor`; the running world comes from `unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()`. In this server version `ue_start_pie` maps to Simulate (no possessed pawn).

---

*First authored 2026-10-10 from a verified setup (Windows 11 · OpenCode 2.0.26 · unreal-engine-mcp 0.10.0 · Unreal Engine 5.8.3); extended 2026-10-10 with in-session verification learnings (Appendices C–D, verified-list refresh, usage discipline) and the checks discipline (probe-before-acting, cheapest-first, ask before opening; screenshot focus). When the setup process changes, update this file and the repository index (`README.md`) together.*
