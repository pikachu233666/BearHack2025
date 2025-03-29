# demo/inject_logs.py

import subprocess

def inject_logs():
    logs = [
        "nginx: service failed to start",
        "mysql daemon failed to respond",
        "unauthorized ssh login attempt detected",
        "apache2 unexpectedly stopped",
        "kernel: oom killer triggered",
        "unknown critical crash"
    ]

    for log in logs:
        subprocess.run(["logger", log])
