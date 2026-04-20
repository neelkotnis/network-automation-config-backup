from netmiko import ConnectHandler
from datetime import datetime
import os

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "logs")

COMMAND = "show running-config"


def backup_device(ip, username, password, device_type):
    device_params = {
        "device_type": device_type,
        "host": ip,
        "username": username,
        "password": password,
    }

    try:
        print(f"[+] Connecting -> {ip}")
        conn = ConnectHandler(**device_params)

        output = conn.send_command(COMMAND)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"{ip}_{timestamp}.txt")

        with open(filename, "w") as f:
            f.write(output)

        conn.disconnect()
        print(f"[OK] Backup completed for {ip}")
        return True

    except Exception as err:
        print(f"[ERROR] {ip} -> {err}")
        return False