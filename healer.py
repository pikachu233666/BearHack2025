import subprocess
import json
import psutil
import requests
import time
import os
from threading import Thread
from ai.ai_matcher import match_log
from healer import *
from alerts import send_alert

CONFIG = json.load(open("config.json"))
LOG_FILE = "logs/healix.log"

os.makedirs("logs", exist_ok=True)
open(LOG_FILE, "a").close()

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} | {msg}\n")

def send_alert(message):
    log(f"[ALERT] {message}")
    if CONFIG.get("discord_webhook"):
        requests.post(CONFIG["discord_webhook"], json={"content": message})

def restart_service(service):
    subprocess.run(['systemctl', 'restart', service])
    log(f"[✔] Restarted {service}")

def kill_memory_hog(pid):
    subprocess.run(['kill', '-9', str(pid)])
    log(f"[✔] Killed process {pid}")

def restore_config(service):
    backup_path = f'logs/{service}.bak'
    config_path = f'/etc/{service}/{service}.conf'
    if os.path.exists(backup_path):
        subprocess.run(['cp', backup_path, config_path])
        restart_service(service)
        log(f"[✔] Restored config for {service}")


def rule_engine(log_line):
    action, score = match_log(log_line.lower())

    if action != "unknown" and hasattr(globals()["__builtins__"], action) is False:
        try:
            func = globals().get(action)
            if callable(func):
                send_alert(f"[AI] Action: `{action}` (confidence: {score:.2f})")
                func()
            else:
                send_alert(f"[AI] No handler for action: {action}")
        except Exception as e:
            send_alert(f"[ERROR] Exception during healing: {str(e)}")
    else:
        send_alert(f"[AI] No confident match for: {log_line.strip()} ({score:.2f})")

def check_services():
    for svc in CONFIG["services"]:
        result = subprocess.run(['systemctl', 'is-active', svc], capture_output=True, text=True)
        if result.stdout.strip() != "active":
            send_alert(f"[!] {svc} is down. Restarting...")
            restart_service(svc)

def check_memory():
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            mem = proc.info['memory_info'].rss / (1024 * 1024)
            if mem > CONFIG["memory_limit_mb"]:
                send_alert(f"[!] {proc.info['name']} using {mem:.2f}MB. Killing it.")
                kill_memory_hog(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def monitor_logs():
    process = subprocess.Popen(['journalctl', '-f'], stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        if any(keyword in line.lower() for keyword in CONFIG["log_keywords"]):
            rule_engine(line)

def start_monitoring():
    Thread(target=monitor_logs, daemon=True).start()
    while True:
        check_services()
        check_memory()
        time.sleep(10)

def restart_mysql():
    restart_service("mysql")

def restart_apache():
    restart_service("apache2")

def restart_docker():
    restart_service("docker")

def restart_journal():
    restart_service("systemd-journald")

def restart_network():
    restart_service("NetworkManager")

def restart_firewalld():
    restart_service("firewalld")

def restart_generic():
    print("[~] Generic restart: No specific service. Skipping actual restart.")

def cleanup_disk():
    subprocess.run(["rm", "-rf", "/tmp/*"])
    print("[✔] Cleaned up temporary files to recover disk space")

def kill_high_cpu():
    import psutil
    max_cpu = 0
    target = None
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if proc.info['cpu_percent'] > max_cpu:
            max_cpu = proc.info['cpu_percent']
            target = proc
    if target:
        psutil.Process(target.info['pid']).kill()
        print(f"[✔] Killed high CPU process: {target.info['name']} ({max_cpu:.2f}%)")


if __name__ == "__main__":
    log("🔧 Healix is starting...")
    start_monitoring()
