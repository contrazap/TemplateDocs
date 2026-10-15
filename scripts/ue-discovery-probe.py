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
