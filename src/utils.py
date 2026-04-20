import os

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "logs")


def ensure_log_dir():
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def load_devices(file_path):
    devices = []
    with open(file_path, "r") as f:
        for line in f:
            ip = line.strip()
            if ip:
                devices.append(ip)
    return devices