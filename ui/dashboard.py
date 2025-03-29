import streamlit as st
import os

from streamlit_autorefresh import st_autorefresh

LOG_FILE = "logs/healix.log"

# Configure Streamlit layout
st.set_page_config(page_title="Healix Dashboard", layout="wide")
st.title("🛠️ Healix: Self-Healing Linux Monitor")

# Auto-refresh every 2 seconds
st_autorefresh(interval=2000, limit=None, key="logrefresh")

# Show status
st.markdown("Monitoring system logs and healing events...")

# Check if log file exists
if not os.path.exists(LOG_FILE):
    st.error("🚫 Log file not found. Make sure Healix is running and logging to logs/healix.log.")
else:
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()[-100:]

    formatted_logs = "".join(logs).strip()
    st.text_area("📝 Healix Logs", formatted_logs, height=500, key="healix_logs_display")
