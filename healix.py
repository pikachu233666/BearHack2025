import argparse
import os
import subprocess
from ai.learn import review_unmatched_logs
from ai.ai_matcher import retrain_model
from demo.inject_logs import inject_logs
from monitor import start_monitoring

RESET_PATH = "ai/learn_buffer.json"

def run_monitor():
    print("🔍 Starting Healix monitor...\n")
    start_monitoring()

def learn_and_reload():
    print("📘 Reviewing unmatched logs...")
    review_unmatched_logs()
    print("\n🔁 Reloading AI model with new data...")
    retrain_model()
    print("✅ Healix AI ruleset updated!\n")

def start_dashboard():
    print("📊 Launching dashboard...")
    subprocess.run(["streamlit", "run", "ui/dashboard.py"])

def inject_demo_logs():
    print("🧪 Injecting demo logs...")
    inject_logs()

def reset_logs():
    with open(RESET_PATH, "w") as f:
        f.write("[]")
    print("🧹 learn_buffer.json reset!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🛠️ Healix CLI")
    parser.add_argument("command", choices=["run", "learn", "dashboard", "inject", "reset"], help="Command to run")

    args = parser.parse_args()

    if args.command == "run":
        run_monitor()
    elif args.command == "learn":
        learn_and_reload()
    elif args.command == "dashboard":
        start_dashboard()
    elif args.command == "inject":
        inject_demo_logs()
    elif args.command == "reset":
        reset_logs()
