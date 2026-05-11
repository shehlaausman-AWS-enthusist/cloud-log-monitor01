# 🚀 Cloud Log Monitor & Alert System

## 📌 Overview
This project simulates a cloud-based log monitoring system similar to AWS CloudWatch. It parses log files, detects anomalies, and generates structured alert reports.

---

## 🎯 Features
- ✅ Log ingestion from `.log` files
- ✅ Parsing timestamped log entries
- ✅ Anomaly detection using sliding time windows
- ✅ Threshold-based alerting system
- ✅ Summary report generation
- ✅ CLI interface using argparse
- ✅ JSON export (simulating AWS S3)
- ✅ Retry/backoff mechanism for fault tolerance

---

## 🛠️ Tech Stack
- Python 3.x
- argparse
- datetime
- collections
- pathlib
- json

---

## ▶️ How to Run

```bash
python log_monitor.py --file sample.log --window 5 --threshold 3# cloud-log-monitor01
