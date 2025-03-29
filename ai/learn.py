import json
from pathlib import Path

SAMPLES_FILE = Path("ai/log_samples.json")
BUFFER_FILE = Path("ai/learn_buffer.json")

def load_json(path):
    if not path.exists() or path.stat().st_size == 0:
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[!] Warning: {path} is not valid JSON. Resetting it.")
        return []


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def list_actions():
    return [
        "restart_nginx",
        "restart_apache",
        "restart_mysql",
        "kill_memory_hog",
        "alert_admin"
    ]

def review_unmatched_logs():
    buffer = load_json(BUFFER_FILE)
    samples = load_json(SAMPLES_FILE)

    if not buffer:
        print("✅ No unmatched logs to review.")
        return

    print(f"\n🔍 Reviewing {len(buffer)} unmatched logs...\n")

    for entry in buffer:
        print(f"Log: {entry['log']}")
        print(f"AI score: {entry['score']}")
        print("Suggested actions:")
        for i, action in enumerate(list_actions(), start=1):
            print(f"  [{i}] {action}")
        print("  [0] Skip\n")

        choice = input("Your choice (number): ").strip()
        if choice == "0":
            continue
        try:
            index = int(choice) - 1
            if 0 <= index < len(list_actions()):
                action = list_actions()[index]
                print(f"✅ Added: {entry['log']} -> {action}\n")
                samples.append({"log": entry["log"], "action": action})
            else:
                print("Invalid choice, skipping.\n")
        except ValueError:
            print("Invalid input, skipping.\n")

    save_json(SAMPLES_FILE, samples)
    save_json(BUFFER_FILE, [])
    print("🧠 Learning complete! AI rules updated.")
