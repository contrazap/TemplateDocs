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
