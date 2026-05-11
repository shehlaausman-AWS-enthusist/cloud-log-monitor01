
---

# 🐍 3. `log_monitor.py`

```python
import argparse
from datetime import datetime, timedelta
from collections import Counter
import json
import time

LOG_FORMAT = "%Y-%m-%d %H:%M:%S"

def parse_log_line(line):
    try:
        timestamp_str, level, message = line.strip().split(" ", 2)
        timestamp = datetime.strptime(timestamp_str, LOG_FORMAT)
        return timestamp, level, message
    except ValueError:
        return None

def read_log_file(file_path, retries=3, delay=2):
    for attempt in range(retries):
        try:
            with open(file_path, "r") as f:
                return f.readlines()
        except Exception:
            print(f"[Retry {attempt+1}] Unable to read file. Retrying...")
            time.sleep(delay)
    raise FileNotFoundError("Failed to access log file.")

def analyze_logs(lines, window_minutes, threshold):
    counts = Counter()
    error_timestamps = []
    messages = []

    for line in lines:
        parsed = parse_log_line(line)
        if not parsed:
            continue

        timestamp, level, message = parsed
        counts[level] += 1
        messages.append(message)

        if level in ["ERROR", "CRITICAL"]:
            error_timestamps.append(timestamp)

    error_timestamps.sort()
    flagged_windows = []

    for i in range(len(error_timestamps)):
        start = error_timestamps[i]
        end = start + timedelta(minutes=window_minutes)

        count = sum(1 for t in error_timestamps if start <= t <= end)

        if count >= threshold:
            flagged_windows.append({
                "start": start.strftime(LOG_FORMAT),
                "end": end.strftime(LOG_FORMAT),
                "count": count
            })

    top_messages = Counter(messages).most_common(3)

    return counts, flagged_windows, top_messages

def get_health_status(flagged_windows):
    if not flagged_windows:
        return "OK"
    elif len(flagged_windows) < 3:
        return "DEGRADED"
    return "CRITICAL"

def save_report(report):
    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Cloud Log Monitor")
    parser.add_argument("--file", default="sample.log")
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--threshold", type=int, default=3)

    args = parser.parse_args()

    lines = read_log_file(args.file)

    counts, flagged_windows, top_messages = analyze_logs(
        lines, args.window, args.threshold
    )

    status = get_health_status(flagged_windows)

    report = {
        "counts": dict(counts),
        "flagged_windows": flagged_windows,
        "top_messages": top_messages,
        "health_status": status
    }

    print("\n===== ALERT REPORT =====")
    print("Counts:", counts)
    print("Flagged Windows:", flagged_windows)
    print("Top Messages:", top_messages)
    print("Health Status:", status)

    save_report(report)

if __name__ == "__main__":
    main()
