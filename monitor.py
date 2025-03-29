import subprocess
import json
from alerts import send_alert
from healer import restart_service, kill_memory_hog
from rules import handle_log
import psutil

CONFIG = json.load(open("config.json"))

def check_services():
    for svc in CONFIG["services"]:
        result = subprocess.run(['systemctl', 'is-active', svc], capture_output=True, text=True)
        if result.stdout.strip() != "active":
            send_alert(f"[!] {svc} is down. Restarting...")
            restart_service(svc)

def check_memory():
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        mem = proc.info['memory_info'].rss / (1024 * 1024)
        if mem > CONFIG["memory_limit_mb"]:
            send_alert(f"[!] {proc.info['name']} using {mem:.2f}MB. Killing it.")
            kill_memory_hog(proc.info['pid'])

def monitor_logs():
    process = subprocess.Popen(['journalctl', '-f'], stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        if any(keyword in line.lower() for keyword in CONFIG["log_keywords"]):
            handle_log(line)

def start_monitoring():
    check_services()
    check_memory()
    monitor_logs()
