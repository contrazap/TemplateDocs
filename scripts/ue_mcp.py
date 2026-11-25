"""Official Unreal MCP client: discover tool schemas, validate arguments, then call.

Solves the common failure of guessing tool names and property names. Every call goes through
the editor's own `describe_toolset` schema, and arguments are checked against it before the
request is sent, so a typo fails locally with a suggestion instead of in the editor.

Usage (from the workspace root, editor open):

    python tools/ue_mcp.py refresh                     # cache every toolset and schema
    python tools/ue_mcp.py toolsets                    # toolset names and tool counts
    python tools/ue_mcp.py find graph                  # search tool names and descriptions
    python tools/ue_mcp.py schema ObjectTools.get_properties
    python tools/ue_mcp.py props /Game/X/X.BP_X.Default__BP_X_C   # property names, no guessing
    python tools/ue_mcp.py call ObjectTools.get_properties --args '{"instance": {...}, "properties": [...]}'
    python tools/ue_mcp.py snapshot                    # rewrite docs/mcp-tools.md

`call` validates argument names (top level and nested objects), required names and value types
against the schema; unknown names get a "did you mean" suggestion. Pass --no-validate to skip.
`--args` takes inline JSON or `@path` to read it from a file.

The cache lives in tools/.cache/official-toolsets.json (git-ignored) and is rebuilt by
`refresh`; `docs/mcp-tools.md` is generated from it and is the readable index. `toolsets`,
`find`, `schema` and `snapshot` read the cache without the editor once it exists. A toolset
missing from the cache triggers one automatic refresh; a tool missing from a cached toolset
only gets suggestions (run `refresh` after an engine upgrade). If the editor answers that the
toolset or tool name does not exist, nothing ran, so the call is refreshed and sent once more;
any other tool error is reported and never re-sent.

Exit codes: 0 ok, 1 `find` matched nothing, 2 validation error, 3 bridge/transport error,
4 the editor ran the tool and it reported an error.
Exit 2 means nothing was sent; exit 4 means the editor rejected the call. `call` catches a bad
`refPath` before sending (2, via `get_properties`' property check), while `props` sends it and
reports the editor's rejection (4). Exit 3 is only a transport failure: if the connection drops
after the request went out, the editor may still have done the work, so read the state before
re-sending anything that changes something.
"""
from __future__ import annotations

import argparse
import atexit
import difflib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

URL = os.environ.get("UE_MCP_URL", "http://127.0.0.1:8000/mcp")
PROTOCOL = "2025-11-25"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", ".cache", "official-toolsets.json")
DOC = os.path.join(ROOT, "docs", "mcp-tools.md")


class BridgeError(RuntimeError):
    pass


class ValidationError(RuntimeError):
    pass


class ToolError(RuntimeError):
    """The editor ran (or tried to run) the tool and answered with isError."""


# The editor's answers when the name itself is wrong: nothing was executed, so a retry is safe.
_NAME_NOT_FOUND = re.compile(r"^(Unknown tool \S+|Toolset '[^']*' not found)")


class Bridge:
    """Minimal Streamable HTTP client for the in-editor MCP server. Connects on first use."""

    def __init__(self, url: str = URL, timeout: float = 120.0) -> None:
        self.url = url
        self.timeout = timeout
        self.session: str | None = None
        self._id = 0
        self._opened = False

    def _post(self, payload: dict, method: str = "POST") -> tuple[dict | None, dict]:
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(self.url, data=body, method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        if self.session:
            req.add_header("Mcp-Session-Id", self.session)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                self.session = resp.headers.get("Mcp-Session-Id", self.session)
                raw = resp.read().decode("utf-8", "replace")
                want = payload.get("id") if isinstance(payload, dict) else None
                return _decode(raw, want), dict(resp.headers)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            raise BridgeError(f"HTTP {exc.code} from {self.url}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BridgeError(
                f"{self.url} is unreachable ({exc.reason}). Is the editor running with the MCP server started?"
            ) from exc
        except OSError as exc:
            # A reset during the reply (ConnectionResetError / RemoteDisconnected) or a timeout
            # arrives as a bare OSError, not a URLError: report it instead of a traceback.
            raise BridgeError(
                f"{self.url}: connection failed ({type(exc).__name__}: {exc}). "
                "Is the editor running with the MCP server started?"
            ) from exc

    def _rpc(self, method: str, params: dict) -> dict:
        self._open()
        self._id += 1
        result, _ = self._post({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params})
        if result is None:
            raise BridgeError(f"empty response to {method}")
        if "error" in result:
            raise BridgeError(f"{method}: {result['error'].get('message', result['error'])}")
        return result.get("result", {})

    def _open(self) -> None:
        if self._opened:
            return
        self._opened = True
        result, _ = self._post(
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL,
                    "capabilities": {},
                    "clientInfo": {"name": "ue_mcp.py", "version": "1.0"},
                },
            }
        )
        if not result or "error" in result:
            raise BridgeError(f"MCP handshake failed: {result}")
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        atexit.register(self.close)

    def close(self) -> None:
        """End the server-side session (Streamable HTTP DELETE); best effort."""
        if not self.session:
            return
        try:
            self._post(None, method="DELETE")
        except BridgeError:
            pass
        self.session = None

    # -- public API ---------------------------------------------------------
    def _tool(self, name: str, arguments: dict) -> str:
        result = self._rpc("tools/call", {"name": name, "arguments": arguments})
        text = _content_text(result)
        if result.get("isError"):
            raise ToolError(text)
        return text

    def meta(self, name: str, **arguments) -> str:
        return self._tool(name, arguments)

    def describe(self, toolset: str) -> dict:
        return json.loads(self.meta("describe_toolset", toolset_name=toolset))

    def call(self, toolset: str, tool: str, arguments: dict | None = None):
        text = self._tool("call_tool", {"toolset_name": toolset, "tool_name": tool, "arguments": arguments or {}})
        return _parse_or_text(text)


def _decode(raw: str, want_id=None) -> dict | None:
    """The server answers JSON or a text/event-stream body; pick the response to our request id."""
    if not raw.strip():
        return None
    if raw.lstrip().startswith("{"):
        return json.loads(raw)
    messages = []
    for line in raw.splitlines():
        if line.startswith("data:"):
            chunk = line[5:].strip()
            if chunk and chunk != "[DONE]":
                messages.append(json.loads(chunk))
    for message in messages:
        if want_id is not None and message.get("id") == want_id:
            return message
    responses = [m for m in messages if "result" in m or "error" in m]
    return (responses or messages or [None])[-1]


def _content_text(result: dict) -> str:
    content = result.get("content") or []
    for item in content:
        if item.get("type") == "text":
            return item.get("text", "")
    return json.dumps(result)


def _parse_or_text(text: str):
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return text


# ---------------------------------------------------------------------------
# schema cache
# ---------------------------------------------------------------------------
def load_cache() -> dict | None:
    if not os.path.isfile(CACHE):
        return None
    with open(CACHE, encoding="utf-8") as handle:
        return json.load(handle)


def save_cache(data: dict) -> None:
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=1, sort_keys=True)


def refresh(bridge: Bridge) -> dict:
    listing = bridge.meta("list_toolsets")
    names = re.findall(r"^- ([A-Za-z0-9_]+\.[A-Za-z0-9_.]+):", listing, flags=re.MULTILINE)
    toolsets: dict[str, dict] = {}
    for name in names:
        info = bridge.describe(name)
        tools = {}
        for entry in info.get("tools", []):
            full = entry["name"]
            short = full.rsplit(".", 1)[-1]
            tools[short] = {
                "description": entry.get("description", ""),
                "inputSchema": entry.get("inputSchema") or {},
            }
        toolsets[name] = {"description": info.get("description", ""), "tools": tools}
    data = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": bridge.url,
        "toolsets": toolsets,
    }
    save_cache(data)
    return data


def ensure_cache(bridge: Bridge) -> dict:
    return load_cache() or refresh(bridge)


_REFRESHED = False


class UnknownToolset(ValidationError):
    pass


def resolve(bridge: Bridge, dotted: str) -> tuple[dict, str, str, dict]:
    """Look a tool up in the cache. Only an unknown toolset refreshes (once per run); an unknown
    tool in a known toolset is almost always a typo, so it gets suggestions without a refresh."""
    global _REFRESHED
    data = ensure_cache(bridge)
    try:
        toolset, tool, spec = lookup(data, dotted)
        return data, toolset, tool, spec
    except UnknownToolset:
        if _REFRESHED:
            raise
        print("toolset not in the cached schema - refreshing from the editor", file=sys.stderr)
        _REFRESHED = True
        data = refresh(bridge)
        toolset, tool, spec = lookup(data, dotted)
        return data, toolset, tool, spec


def lookup(data: dict, dotted: str) -> tuple[str, str, dict]:
    """Resolve 'ObjectTools.get_properties' or 'editor_toolset...BlueprintTools.list_graphs'."""
    if "." not in dotted:
        raise ValidationError(f"'{dotted}' needs the form <toolset>.<tool>, e.g. ObjectTools.get_properties")
    toolset_part, tool = dotted.rsplit(".", 1)
    matches = [name for name in data["toolsets"] if name == toolset_part or name.endswith("." + toolset_part)]
    if not matches:
        short = {name.rsplit(".", 1)[-1]: name for name in data["toolsets"]}
        near = difflib.get_close_matches(toolset_part.rsplit(".", 1)[-1], list(short), n=3, cutoff=0.4)
        raise UnknownToolset(
            f"unknown toolset '{toolset_part}'. Near matches: {near or 'none'} - run 'toolsets' to list them."
        )
    if len(matches) > 1 and toolset_part not in matches:
        raise ValidationError(f"'{toolset_part}' is ambiguous: {matches}. Use the full toolset name.")
    toolset = toolset_part if toolset_part in matches else matches[0]
    tools = data["toolsets"][toolset]["tools"]
    if tool not in tools:
        near = difflib.get_close_matches(tool, list(tools), n=3, cutoff=0.4)
        raise ValidationError(
            f"unknown tool '{tool}' in {toolset}. Near matches: {near or 'none'}"
            " (run 'refresh' if the engine was upgraded)"
        )
    return toolset, tool, tools[tool]


_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "null": lambda v: v is None,
}


def validate(schema: dict, arguments: dict) -> list[str]:
    """Return a list of human-readable problems; empty means the call is safe to send."""
    problems: list[str] = []
    props = schema.get("properties", {})
    required = schema.get("required", [])

    for key in arguments:
        if key not in props:
            near = difflib.get_close_matches(key, list(props), n=2, cutoff=0.4)
            problems.append(f"unknown argument '{key}'" + (f" - did you mean {near}?" if near else ""))
    for key in required:
        if key not in arguments:
            problems.append(f"missing required argument '{key}'")

    for key, value in arguments.items():
        spec = props.get(key) or {}
        expected = spec.get("type")
        if not expected:
            continue  # anyOf/oneOf shapes: leave to the server
        checker = _TYPE_CHECKS.get(expected)
        if checker and value is not None and not checker(value):
            problems.append(f"'{key}' should be {expected}, got {type(value).__name__}")
        if expected == "object" and isinstance(value, dict) and "properties" in spec:
            nested_required = spec.get("required", [])
            for name in nested_required:
                if name not in value:
                    problems.append(f"'{key}.{name}' is required by the schema")
            for name in value:
                if name not in spec.get("properties", {}):
                    near = difflib.get_close_matches(name, list(spec.get("properties", {})), n=2, cutoff=0.4)
                    problems.append(f"unknown '{key}.{name}'" + (f" - did you mean {near}?" if near else ""))
    return problems


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------
def cmd_refresh(args: argparse.Namespace) -> int:
    data = refresh(Bridge())
    total = sum(len(t["tools"]) for t in data["toolsets"].values())
    print(f"cached {len(data['toolsets'])} toolsets, {total} tools -> {os.path.relpath(CACHE, ROOT)}")
    return 0


def cmd_toolsets(args: argparse.Namespace) -> int:
    data = ensure_cache(Bridge())
    for name, entry in sorted(data["toolsets"].items()):
        print(f"{name}  ({len(entry['tools'])} tools)")
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    data = ensure_cache(Bridge())
    needle = args.text.lower()
    hits = 0
    for name, entry in sorted(data["toolsets"].items()):
        for tool, spec in sorted(entry["tools"].items()):
            hay = f"{name}.{tool} {spec.get('description', '')}".lower()
            if needle in hay:
                hits += 1
                first = (spec.get("description") or "").strip().splitlines()[0] if spec.get("description") else ""
                print(f"{name.rsplit('.', 1)[-1]}.{tool}  -  {first[:110]}")
    if not hits:
        print(f"no tool matches '{args.text}'")
        return 1
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    _, toolset, tool, spec = resolve(Bridge(), args.tool)
    print(f"{toolset}.{tool}\n")
    print((spec.get("description") or "").strip())
    print("\ninputSchema:")
    print(json.dumps(spec.get("inputSchema", {}), indent=2))
    return 0


def cmd_props(args: argparse.Namespace) -> int:
    bridge = Bridge()
    _, toolset, tool, _ = resolve(bridge, "ObjectTools.list_properties")
    result = bridge.call(toolset, tool, {"instance": {"refPath": args.ref_path}})
    props = _parse_or_text(result.get("returnValue", result)) if isinstance(result, dict) else result
    if isinstance(props, dict):
        names = sorted(props)
        for name in names:
            title = (props[name] or {}).get("title") or (props[name] or {}).get("type") or ""
            print(f"{name}  ({title})")
        print(f"\n{len(names)} properties. Pass exact names to get_properties, one or two at a time.")
    else:
        print(props, file=sys.stderr)
        return 2
    return 0


def check_property_names(bridge, data: dict, toolset: str, tool: str, arguments: dict) -> list[str]:
    """For get_properties, verify the names against the object instead of trusting them."""
    if tool != "get_properties":
        return []
    instance = arguments.get("instance")
    names = arguments.get("properties")
    if not isinstance(instance, dict) or not isinstance(names, list):
        return []
    ref_path = instance.get("refPath")
    if not ref_path:
        return []
    lt, ltool, _ = lookup(data, "ObjectTools.list_properties")
    try:
        listing = bridge.call(lt, ltool, {"instance": {"refPath": ref_path}})
    except ToolError as exc:
        return [f"instance: {exc}"]  # bad refPath: get_properties would fail the same way
    except BridgeError:
        return []
    known = _parse_or_text(listing.get("returnValue")) if isinstance(listing, dict) else None
    if not isinstance(known, dict):
        return []  # object or class the tool cannot describe: leave it to the server
    problems: list[str] = []
    for name in names:
        if name not in known:
            near = difflib.get_close_matches(str(name), list(known), n=3, cutoff=0.4)
            problems.append(f"unknown property '{name}'" + (f" - did you mean {near}?" if near else ""))
    return problems


def read_arguments(text: str) -> dict:
    """Inline JSON, or @path to read it from a file."""
    source = "--args"
    if text.startswith("@"):
        source = text[1:]
        try:
            with open(source, encoding="utf-8-sig") as handle:
                text = handle.read()
        except OSError as exc:
            raise ValidationError(f"cannot read {source}: {exc.strerror}") from exc
    try:
        arguments = json.loads(text) if text.strip() else {}
    except ValueError as exc:
        raise ValidationError(f"{source} is not valid JSON: {exc}") from exc
    if not isinstance(arguments, dict):
        raise ValidationError(f"{source} must be a JSON object, got {type(arguments).__name__}")
    return arguments


def cmd_call(args: argparse.Namespace) -> int:
    arguments = read_arguments(args.args)
    bridge = Bridge()
    data, toolset, tool, spec = resolve(bridge, args.tool)
    if not args.no_validate:
        problems = validate(spec.get("inputSchema", {}), arguments)
        problems += check_property_names(bridge, data, toolset, tool, arguments)
        if problems:
            for problem in problems:
                print(f"invalid: {problem}", file=sys.stderr)
            print(f"\nnot sent. See 'schema {args.tool}' for the full shape.", file=sys.stderr)
            return 2
    global _REFRESHED
    try:
        result = bridge.call(toolset, tool, arguments)
    except ToolError as exc:
        # Only a wrong toolset/tool name is retried: the editor ran nothing, so re-sending is safe.
        if _REFRESHED or not _NAME_NOT_FOUND.match(str(exc)):
            raise
        print("the editor does not know that name - refreshing the schemas and retrying once", file=sys.stderr)
        _REFRESHED = True
        data = refresh(bridge)
        toolset, tool, spec = lookup(data, args.tool)
        result = bridge.call(toolset, tool, arguments)
    print(json.dumps(result, indent=2) if not isinstance(result, str) else result)
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    data = ensure_cache(Bridge())
    out = args.out or DOC
    total = sum(len(t["tools"]) for t in data["toolsets"].values())
    lines = [
        "# MCP tools - official Unreal MCP",
        "",
        f"Generated by `python tools/ue_mcp.py snapshot` on {data['generated']} from `{data['url']}`.",
        "Do not edit by hand: refresh after an engine upgrade, then review the diff.",
        f"{len(data['toolsets'])} toolsets, {total} tools. Arguments in brackets are required; the full JSON",
        "schema is in `tools/.cache/official-toolsets.json` or `python tools/ue_mcp.py schema <toolset>.<tool>`.",
        "",
        "Rules that keep calls correct: describe a toolset before its first use, pass argument names from its",
        "schema, and for object properties call `ObjectTools.list_properties` first (`python tools/ue_mcp.py props <path>`).",
        "",
    ]
    for name, entry in sorted(data["toolsets"].items()):
        lines.append(f"## {name}")
        description = " ".join((entry.get("description") or "").split())
        if description:
            lines.append(description[:300])
        lines.append("")
        for tool, spec in sorted(entry["tools"].items()):
            summary = " ".join((spec.get("description") or "").split())
            summary = summary.split(" Args:")[0].split(" Args: ")[0].strip()
            if len(summary) > 70:
                summary = summary[:67] + "..."
            required = (spec.get("inputSchema") or {}).get("required") or []
            args_text = f" [{', '.join(required)}]" if required else ""
            lines.append(f"- `{tool}`{args_text} - {summary}")
        lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")
    print(f"wrote {os.path.relpath(out, ROOT)} ({len(lines)} lines, {total} tools)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Discover, validate and call the official Unreal MCP.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("refresh", help="rebuild the schema cache from the running editor").set_defaults(func=cmd_refresh)
    sub.add_parser("toolsets", help="list toolsets and tool counts").set_defaults(func=cmd_toolsets)

    find = sub.add_parser("find", help="search tool names and descriptions")
    find.add_argument("text")
    find.set_defaults(func=cmd_find)

    schema = sub.add_parser("schema", help="print one tool's full input schema")
    schema.add_argument("tool", help="<toolset>.<tool>, e.g. ObjectTools.get_properties")
    schema.set_defaults(func=cmd_schema)

    props = sub.add_parser("props", help="list an object's property names (never guess them)")
    props.add_argument("ref_path")
    props.set_defaults(func=cmd_props)

    call = sub.add_parser("call", help="validate and call a tool")
    call.add_argument("tool")
    call.add_argument("--args", default="{}", help="JSON object, or @path to read it from a file")
    call.add_argument("--no-validate", action="store_true")
    call.set_defaults(func=cmd_call)

    snap = sub.add_parser("snapshot", help="rewrite docs/mcp-tools.md from the cache")
    snap.add_argument("--out", default=None)
    snap.set_defaults(func=cmd_snapshot)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ToolError as exc:
        print(f"tool error: {exc}", file=sys.stderr)
        return 4
    except BridgeError as exc:
        print(f"bridge error: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
