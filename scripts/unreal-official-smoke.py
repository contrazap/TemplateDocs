# unreal-official-smoke.py
import json, urllib.request

URL = "http://127.0.0.1:8000/mcp"

def rpc(payload, session=None):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                 **({"mcp-session-id": session} if session else {})})
    resp = urllib.request.urlopen(req, timeout=30)
    body = resp.read().decode()
    if not body.strip():           # notifications reply 202 with an empty body
        return resp.headers.get("mcp-session-id"), None
    if body.startswith("event:"):  # SSE framing fallback
        body = "\n".join(l[5:].strip() for l in body.splitlines() if l.startswith("data:"))
    return resp.headers.get("mcp-session-id"), json.loads(body)

sid, init = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "0"}}})
print("init:", init.get("result", {}).get("protocolVersion"), "| session:", bool(sid))
rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
_, tools = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
print("tools:", [t["name"] for t in tools["result"]["tools"]])
_, ts = rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "call_tool", "arguments": {"tool_name": "list_toolsets"}}}, sid)
print("toolsets:", ts["result"]["content"][0]["text"][:300])
