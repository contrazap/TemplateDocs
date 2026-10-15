"""Agent verification helpers, run inside the Unreal Editor via the pyremote bridge (`ue_exec_python`).

Read-only by design: nothing here saves assets or levels. PIE helpers act on a throwaway play world.
Loader snippet (one `ue_exec_python` call; finds the workspace `tools/` above the project dir). Once loaded,
later calls in the same editor session need only `import ue_checks`:

    import sys, os, importlib, unreal
    d = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()).rstrip("/")
    while not os.path.isfile(os.path.join(d, "tools", "ue_checks.py")) and os.path.dirname(d) != d: d = os.path.dirname(d)
    t = os.path.join(d, "tools"); sys.path.insert(0, t) if t not in sys.path else None
    import ue_checks; importlib.reload(ue_checks)
    result = ue_checks.pie_start()

Runtime visual check (3 calls + viewing the PNG):
    1. pie_start()                          — real PIE (player pawn possessed), not Simulate
    2. pie_shot("name", pitch=-60, hide=[]) — aim, optionally hide components, request a capture
    3. pie_stop()                           — end PIE, report which captures were written
    then view Saved/Screenshots/Checks/<name>.png with the client's image reader
    (or pyremote `ue_screenshot` while PIE still runs, if the client cannot read images).
Blueprint parity: bp_diff(path_a, path_b) — full reflected-property diff of the two component trees.
"""
import os
import re

import unreal

SHOT_DIR = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()), "Screenshots", "Checks")
_shots = []


def _les():
    return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def _pie_world():
    return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()


def pie_start():
    """Request a standard PIE session (current play settings). Returns before BeginPlay; pie_shot waits for the pawn."""
    if _les().is_in_play_in_editor():
        return {"started": False, "note": "PIE already running"}
    del _shots[:]
    _les().editor_request_begin_play()
    return {"requested": True, "next": "pie_shot(...) — retry if it reports no pawn yet"}


def pie_shot(name, pitch=None, yaw=None, hide=(), width=1280, height=720):
    """Aim the local player, optionally hide components (by name, this PIE only), and request a viewport capture.

    The PNG is written on a later frame — pie_stop() reports whether it exists.
    """
    world = _pie_world()
    pc = unreal.GameplayStatics.get_player_controller(world, 0) if world else None
    pawn = pc.get_controlled_pawn() if pc else None
    if not pawn:
        return {"ok": False, "note": "no PIE pawn yet — PIE still starting; call again"}
    rot = pc.get_control_rotation()
    if pitch is not None:
        rot.pitch = pitch
    if yaw is not None:
        rot.yaw = yaw
    pc.set_control_rotation(rot)
    hidden = []
    for comp in pawn.get_components_by_class(unreal.PrimitiveComponent):
        if comp.get_name() in hide:
            comp.set_visibility(False, True)
            hidden.append(comp.get_name())
    os.makedirs(SHOT_DIR, exist_ok=True)
    path = os.path.join(SHOT_DIR, name if name.lower().endswith(".png") else name + ".png")
    if os.path.exists(path):
        os.remove(path)
    unreal.AutomationLibrary.take_high_res_screenshot(width, height, path)
    _shots.append(path)
    return {"ok": True, "pawn": pawn.get_class().get_name(), "pitch": rot.pitch, "yaw": rot.yaw,
            "hidden": hidden, "missing_hide": [h for h in hide if h not in hidden], "file": path}


def pie_stop():
    """End PIE and report the captures requested in this session (written or not)."""
    running = _les().is_in_play_in_editor()
    if running:
        _les().editor_request_end_play()
    shots = [{"file": p, "written": os.path.exists(p)} for p in _shots]
    return {"stopped": running, "shots": shots,
            "note": "unwritten capture: the editor window must be in the foreground; rerun"
            if any(not s["written"] for s in shots) else None}


# --- Blueprint parity diff -------------------------------------------------

_ADDR = re.compile(r"\s*\(0x[0-9A-Fa-f]+\)")
_SKIP = {"creation_method", "ucs_serialization_index", "ucs_modified_properties", "component_tags",
         "asset_user_data", "asset_user_data_editor_only", "on_component_activated", "on_component_deactivated"}


_NUM = re.compile(r"-?\d+\.\d+(?:[eE][-+]?\d+)?")
_SELF = re.compile(r"/[^\s'\"]*\.Default__\w+_C:")


def _num(m):
    s = "%.2f" % round(float(m.group(0)), 2)  # 2-decimal tolerance: 89.9999 == 90, 2.7938 == 2.79
    return "0.00" if s == "-0.00" else s


def _val(v):
    s = v.get_path_name() if isinstance(v, unreal.Object) else _ADDR.sub("", str(v))
    return _NUM.sub(_num, _SELF.sub("self:", s))  # own subobjects compare as self:<name>


def _fields(obj):
    for n in dir(obj):
        if n.startswith("_") or n in _SKIP:
            continue
        try:
            v = obj.get_editor_property(n)
        except Exception:
            continue
        if not callable(v):
            yield n, v


def _props(obj):
    """Reflected properties as comparable strings; structs flattened one level (body_instance.mass_scale)."""
    out = {}
    for n, v in _fields(obj):
        if isinstance(v, unreal.StructBase):
            sub = dict((n + "." + f, _val(fv)) for f, fv in _fields(v))
            if sub:
                out.update(sub)
                continue
        out[n] = _val(v)
    return out


def _components(bp):
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    comps = {}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if isinstance(o, unreal.ActorComponent):
            comps[o.get_name().replace("_GEN_VARIABLE", "")] = o
    return comps


def _pair(ca, cb):
    """Match components by name, then leftover ones by class when that class is unique on both sides."""
    pairs = [(n, ca[n], cb[n]) for n in ca if n in cb]
    la = {n: o for n, o in ca.items() if n not in cb}
    lb = {n: o for n, o in cb.items() if n not in ca}
    for na, oa in list(la.items()):
        cls = oa.get_class()
        same_a = [n for n, o in la.items() if o.get_class() == cls]
        same_b = [n for n, o in lb.items() if o.get_class() == cls]
        if len(same_a) == 1 and len(same_b) == 1:
            nb = same_b[0]
            pairs.append(("%s~%s" % (na, nb), oa, lb.pop(nb)))
            la.pop(na)
    return pairs, sorted(la), sorted(lb)


def bp_diff(path_a, path_b, include_cdo=True):
    """Diff every reflected editor property of two Blueprints' components (and class defaults).

    Returns {"diff": {component: {prop: [a, b]}}, "only_a": [...], "only_b": [...]}.
    Inherited native components (CharacterMesh0, CharacterMovement…) are included.
    """
    ba, bb = unreal.load_asset(path_a), unreal.load_asset(path_b)
    if not ba or not bb:
        return {"error": "asset not found", "a": bool(ba), "b": bool(bb)}
    pairs, only_a, only_b = _pair(_components(ba), _components(bb))
    if include_cdo:
        cdo = lambda bp: unreal.get_default_object(unreal.load_object(None, bp.generated_class().get_path_name()))
        pairs.append(("<class defaults>", cdo(ba), cdo(bb)))
    diff = {}
    for label, oa, ob in pairs:
        pa, pb = _props(oa), _props(ob)
        d = {k: [pa.get(k), pb.get(k)] for k in sorted(set(pa) | set(pb)) if pa.get(k) != pb.get(k)}
        if d:
            diff[label] = d
    return {"diff": diff, "only_a": only_a, "only_b": only_b}
