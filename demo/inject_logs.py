import subprocess
import random

logs = [
    "nginx: service failed to start",
    "mysql daemon failed to respond",
    "unauthorized ssh login attempt detected",
    "apache2 unexpectedly stopped",
    "kernel: oom killer triggered",
    "unknown critical crash"
]

print("🧪 Injecting demo logs into journalctl...\n")
for log in logs:
    subprocess.run(["logger", log])
