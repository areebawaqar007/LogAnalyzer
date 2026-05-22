# 📊 Log Analyzer

A Python-based log analysis tool that parses real-world messy server logs and generates useful insights like error rates, top IPs, endpoint usage, and response time statistics.

---

## ⚙️ Prerequisites

### 1. Make sure Python is installed

Check Python version:

```bash
python --version

You should see something like:

Python 3.8+

If Python is not installed, download it from:
https://www.python.org/downloads/

Clone the Repository
git clone https://github.com/areebawaqar007/LogAnalyzer.git
cd log-analyzer

▶️ How to Run
Step 1: Generate sample logs (optional but recommended)

python scripts/generate_logs.py

This will create:

sample_logs.txt
Step 2: Run the log analyzer
python analyzer.py sample_logs.txt

📁 Project Structure
log-analyzer/
│
├── analyzer.py              # Main entry point
├── parser.py               # Log parsing logic
├── stats.py                # Analytics and reporting
├── scripts/
│   └── generate_logs.py    # Log generator with edge cases
├── sample_logs.txt         # Generated test file
└── README.md

📊 What This Tool Does
Parses server logs safely
Handles multiple formats:
Standard logs
JSON logs
Malformed or incomplete logs
Extracts insights:
Total / valid / malformed logs
Error rates (4xx / 5xx)
Top IP addresses
Most used endpoints
Slowest endpoints (average response time)
🧠 Key Features
Handles real-world messy log data
Supports multiple timestamp formats
Normalizes response times (ms, s, raw values)
Does not crash on malformed input
Gracefully skips invalid logs