# 🛠️ Healix – Self-Healing Linux System

Healix is an AI-assisted automation framework that keeps your Linux system healthy by monitoring logs, services, resources, and auto-healing issues in real-time. Designed for hackathons, devops, cybersecurity, and system automation.

## ✨ Features

- 🔍 Real-time monitoring of logs and services
- 🔁 Auto-restart failed services (nginx, MySQL, SSH, etc.)
- 💀 Kills memory or CPU hogs
- 🔐 Detects unauthorized SSH attempts
- 🧹 Cleans disk when full
- 📡 Discord alerts
- 🤖 AI-based log understanding using TF-IDF (no LLMs)
- 🧪 CLI-powered for easy testing and extensions
- 📊 Streamlit dashboard (optional)

## ⚙️ 1. Setup

### Clone the repo

```bash
git clone https://github.com/pikachu233666/Healix.git
cd healix
```
### Create virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
If you don’t have a requirements.txt, use:
```bash
pip install psutil watchdog requests streamlit streamlit-autorefresh scikit-learn
```

## 🛠️ 2. Configuration

Edit config.json to customize monitored services, memory limits, and webhook:
```json
{
  "services": ["nginx", "mysql", "ssh"],
  "memory_limit_mb": 500,
  "discord_webhook": "https://discord.com/api/webhooks/your_webhook_url_here",
  "log_keywords": ["error", "failed", "unauthorized"]
}
```
## 🚀 3. Run Healix
Usage (via CLI)
```bash
python healix.py <command>
```
Available Commands:

| Command     | Description                                          |
| ----------- | ---------------------------------------------------- |
| `run`       | Start monitoring logs, services, and healing actions |
| `dashboard` | Launch the live Streamlit dashboard                  |
| `inject`    | Simulate system failures (fake logs) for testing     |
| `reset`     | Reset logs and demo data                             |
| `learn`     | Learn from feedback or new logs                      |

## 🧠 How the AI Works

- Healix uses a `log_samples.json` dataset of labeled logs
- New log entries are compared using **TF-IDF + cosine similarity**
- If the similarity score is high, a healing action is triggered (e.g. `restart_nginx`, `kill_memory_hog`)
- Easily expandable — just add new logs to `ai/log_samples.json`

## 🧪 Simulate System Failures

| Scenario          | Command                                            |
| ----------------- | -------------------------------------------------- |
| Crash nginx       | `sudo systemctl stop nginx`                        |
| Trigger OOM       | `python3 -c "a = ['A'*1024*1024]*1000"`            |
| SSH intrusion log | `logger 'unauthorized ssh login attempt'`          |
| Fill disk space   | `dd if=/dev/zero of=/tmp/junkfile bs=1M count=500` |



## 🐻 Contribution

- Yubo Sun
- Dev Godhani
- Ruslan Parkhomenko