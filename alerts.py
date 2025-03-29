import requests
import json

CONFIG = json.load(open("config.json"))

def send_alert(message):
    print(f"[ALERT] {message}")
    if CONFIG["discord_webhook"]:
        requests.post(CONFIG["discord_webhook"], json={"content": message})
