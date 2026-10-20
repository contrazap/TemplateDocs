# Blender MCP bridge — setup and Unreal export conventions

An optional add-on for workspaces that prepare 3D assets in Blender for Unreal Engine: vehicle rigs, cleanup of AI-generated or pack meshes, collision and LODs. Two ways in:

- **Interactive bridge, `blender-mcp`.** An MCP server (`uvx blender-mcp`) talks to an add-on running inside Blender over a local socket (default port `9876`, configurable via `BLENDER_PORT`). Use it to inspect scenes, take viewport screenshots and make one-off edits.
- **Batch scripts, `blender -b`.** Headless Blender runs Python scripts kept in the repository (`tools/blender/*.py`). Use them for every repeatable pipeline step: export, validation, decimation, LOD generation. They work from any agent client, are reviewable as text and need no running Blender UI. **Prefer batch for the pipeline**, and use the bridge for looking around.

**Status.** Setup steps follow the upstream project (github.com/ahujasid/blender-mcp, PyPI `blender-mcp`). Not yet verified on this machine (Blender 5.2). Upstream Blender 5 support is unconfirmed; a fork reports Blender 5.0.1 working. Each workspace verifies setup in the plan that first needs Blender and records the result here.

## 1. Setup (once per PC)

1. Install **uv** with its official installer (not pip). Confirm `uvx --version`.
2. Install the add-on: run `uvx blender-mcp install-addon`, or install upstream's `addon.py` manually. Then in Blender: *Edit ▸ Preferences ▸ Add-ons* → enable **Blender MCP**.
3. In the 3D viewport sidebar (N), open the **BlenderMCP** tab and start the server.
4. Register the client entry, project-scoped, next to the Unreal bridges:
   - Claude Code `.mcp.json`: `"blender": { "type": "stdio", "command": "uvx", "args": ["blender-mcp"] }`
   - OpenCode `opencode.json`: `"blender": { "type": "local", "command": ["uvx", "blender-mcp"] }` under `mcp.servers`
5. Only one MCP client should connect to the add-on at a time.

**Security.** The add-on executes arbitrary Python sent by the client. Keep it on loopback, run it only when needed, and never expose the port. Its optional asset integrations (Poly Haven, Sketchfab, Hyper3D) contact external services. Leave them off unless a plan needs them and the user has authorized it.

## 2. Batch scripts

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b "<file.blend>" -P tools/blender/<script>.py -- --out "<path>" [args]
```

- Scripts parse arguments after `--`, write their outputs (FBX/glTF and a JSON report) to the given paths, and exit non-zero on failure.
- Seed set: `export_fbx.py` (applies the conventions below), `validate_export.py` (checks those conventions and the budgets, writes a JSON report), `make_lods.py` (decimate steps), `ucx_from_hull.py` (convex collision).

## 3. Export conventions for Unreal

Verify these on the first import of each asset class (does the asset face forward, is it 1:1 scale, are the pivots right?), then record the verified settings in the workspace tooling notes:

- **Units:** metric, unit scale 1.0, modelled in metres. Apply all transforms before export.
- **Orientation:** model vehicles facing **+X**. Export FBX with *Forward = X, Up = Z* and *Apply Scalings = FBX All*. Confirm that the vehicle faces +X in Unreal.
- **Pivots:** static props at the base centre; doors and hinged parts at the hinge; vehicles at the chassis origin, at ground level between the axles.
- **Collision:** `UCX_<MeshName>_NN` convex hulls exported with the mesh. Keep hulls few and simple.
- **LODs:** `<MeshName>_LOD0…n` in one FBX, or Unreal auto-LOD; the target counts come from the project budget. Use Nanite only where the performance doc allows it on the minimum-spec tier.
- **Vehicles (Chaos wheeled):** one skeletal mesh. Root bone at the chassis origin; one bone per wheel (`wheel_fl`, `wheel_fr`, `wheel_ml`, …) at the hub centre, with the wheel geometry skinned 100 % to its bone. Optional suspension or steering visual bones. The physics asset uses simple chassis bodies; wheels need no bodies, because the vehicle simulates wheels itself. Record attachment points (winch, hitch, cargo slots, lights) as named sockets or empties exported as sockets (`SOCKET_<name>` on static meshes).
- **Materials:** one slot per material, with names matching the Unreal master-material instances (`MI_<name>`). Packed textures follow the project convention (for example ORM).
- **Naming:** `SM_` static, `SK_` skeletal, `T_` textures. Source files in `ArtSource/` (Git LFS), exports alongside in `ArtSource/Export/`, never cooked directly.

## 4. Verification checklist

1. `uvx blender-mcp` starts, and the client lists the `blender` server's tools.
2. With the add-on server running, a scene query returns the open file's objects, and a viewport screenshot attaches.
3. `blender -b` runs `validate_export.py` on a sample file and writes its JSON report.
4. An exported test mesh imports into Unreal facing +X at 1:1 scale, with its UCX collision and sockets intact.

## 5. Troubleshooting (seed)

| Symptom | Cause | Fix |
|---|---|---|
| Connection refused | Blender closed, add-on disabled, or server not started | Start Blender, enable the add-on, press start in the BlenderMCP tab |
| Mesh 100× too big or small in Unreal | Unit scale or Apply Scalings mismatch | Unit scale 1.0, Apply Scalings = FBX All; re-export |
| Vehicle faces sideways | Forward axis mismatch | Model +X forward and export Forward = X, or rotate before export |
| Collision missing | Hull names don't match the mesh name | `UCX_<exact mesh name>_01` |
