import subprocess
import json
import psutil
import requests
import time
import os
from threading import Thread

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
    if "nginx" in log_line and "failed" in log_line:
        send_alert("[AI] Nginx failed, auto-restarting...")
        restart_service("nginx")
    elif "unauthorized" in log_line and "ssh" in log_line:
        send_alert("[AI] Unauthorized SSH access attempt detected.")
    else:
        log("[~] No rule match.")

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

if __name__ == "__main__":
    log("🔧 Healix is starting...")
    start_monitoring()
