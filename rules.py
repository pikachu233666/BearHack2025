from ai.ai_matcher import match_log
from healer import restart_service, kill_memory_hog
from alerts import send_alert

def handle_log(log_line):
    action, score, confidence = match_log(log_line)

    if action == "restart_nginx":
        send_alert(f"[AI 🤖] ({confidence}) Restarting nginx – score: {score:.2f}")
        restart_service("nginx")

    elif action == "restart_apache":
        send_alert(f"[AI 🤖] ({confidence}) Restarting apache2 – score: {score:.2f}")
        restart_service("apache2")

    elif action == "restart_mysql":
        send_alert(f"[AI 🤖] ({confidence}) Restarting mysql – score: {score:.2f}")
        restart_service("mysql")

    elif action == "kill_memory_hog":
        send_alert(f"[AI 🤖] ({confidence}) Killing memory hog – score: {score:.2f}")
        # Trigger your memory scan (or handle in monitor)

    elif action == "alert_admin":
        send_alert(f"[AI 🤖] ALERT: {log_line} (score: {score:.2f})")

    elif action == "unknown":
        send_alert(f"[AI 🤖] No confident match for: '{log_line.strip()}' (score: {score:.2f})")
