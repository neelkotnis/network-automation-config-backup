import os
from netmiko import ConnectHandler
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "logs")

COMMAND = "show running-config"


def get_latest_backup(ip):
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(ip)]
    if not files:
        return None

    files.sort(reverse=True)
    return os.path.join(OUTPUT_DIR, files[0])


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
        conn.disconnect()

        # Check previous backup
        previous_file = get_latest_backup(ip)
        change_detected = False

        if previous_file:
            with open(previous_file, "r") as f:
                old_config = f.read()

            if old_config != output:
                change_detected = True
                print(f"[CHANGE DETECTED] {ip}")
            else:
                print(f"[NO CHANGE] {ip}")
        else:
            print(f"[FIRST BACKUP] {ip}")

        # Save new backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"{ip}_{timestamp}.txt")

        with open(filename, "w") as f:
            f.write(output)

        print(f"[OK] Backup saved for {ip}")

        return True

    except Exception as err:
        print(f"[ERROR] {ip} -> {err}")
        return False