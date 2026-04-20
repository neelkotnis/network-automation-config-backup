# Network Automation Config Backup

Automates backup of running configurations from multiple network devices over SSH using Python and Netmiko.

---

## Problem
Manually backing up configurations across multiple network devices is time-consuming, inconsistent, and prone to human error.

---

## Solution
This tool connects to multiple devices, retrieves their running configuration, and stores them locally with error handling and summary reporting.

---

## Features
- Multi-device SSH automation using Netmiko  
- Parallel execution (faster backups)  
- Timestamped configuration backups  
- Error handling for unreachable devices  
- Summary report of success/failure  

---

## Tech Stack
- Python  
- Netmiko (Paramiko under the hood)  

---

## Project Structure
```
├── src/
│   ├── main.py             # Entry point
│   ├── backup.py           # Backup logic
│   ├── utils.py            # Helper functions
├── config/
│   └── devices.txt         # Device list
├── logs/                   # Output (ignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```
---

## Usage
Run the script with:
```bash
python src/main.py --username <username> --password <password> --file config/devices.txt
```
Optional:
```bash
threads 5   # Number of parallel connections (default = 5)
```

---

## Input
- config/devices.txt:
```bash
10.0.0.1
10.0.0.2
10.0.0.3
```

## Output
- logs/<ip>_<timestamp>.txt → Configuration backups
```bash
Console summary:
========== SUMMARY ==========
Successful: X
Failed: Y
```

## Notes
- Uses SSH (port 22) to connect to devices
- Device type is currently set to cisco_ios
- This is a personal project built for real-world automation scenarios
- No proprietary or confidential data is included

## Future Improvements
- Support for multiple device vendors
- Secure credential handling (.env / vault integration)
- Logging framework instead of print statements
- Config diff & change detection
- Export reports (JSON / CSV)

## Author
**Neel Kotnis**
