from flask import Flask, jsonify
import time
import psutil
from datetime import datetime, timezone

app = Flask(__name__)

START_TIME = time.time()

@app.route("/")
def home():
    return "Pragati Singh Cloud App Running"

@app.route("/analyze")
def analyze():
    timestamp = datetime.now(timezone.utc).isoformat()
    uptime_seconds = int(time.time() - START_TIME)

    cpu_metric = psutil.cpu_percent(interval=1)
    memory_metric = psutil.virtual_memory().percent

    score = 100
    score -= cpu_metric * 0.3
    score -= memory_metric * 0.3
    score -= min(uptime_seconds / 300, 10)
    score = max(0, min(100, int(score)))

    if score > 80:
        message = "System healthy"
    elif score > 50:
        message = "System moderate"
    else:
        message = "System critical"

    return jsonify({
        "timestamp": timestamp,
        "uptime_seconds": uptime_seconds,
        "cpu_metric": cpu_metric,
        "memory_metric": memory_metric,
        "health_score": score,
        "message": message
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
