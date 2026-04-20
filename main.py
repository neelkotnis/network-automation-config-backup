import os
from netmiko import ConnectHandler
from datetime import datetime

DEVICE_TYPE = "cisco_ios"
OUTPUT_DIR = "logs"
COMMAND = "show running-config"


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


def backup_device(ip, username, password):
    device_params = {
        "device_type": DEVICE_TYPE,
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

        with open(filename, "w") as file:
            file.write(output)

        conn.disconnect()
        print(f"[OK] Backup completed for {ip}")
        return True

    except Exception as err:
        print(f"[ERROR] {ip} -> {err}")
        return False


def main():
    ensure_log_dir()

    username = input("Username: ")
    password = input("Password: ")

    devices = load_devices("devices.txt")

    success_count = 0
    failed_devices = []

    for ip in devices:
        result = backup_device(ip, username, password)
        if result:
            success_count += 1
        else:
            failed_devices.append(ip)

    # Summary
    print("\n========== SUMMARY ==========")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_devices)}")

    summary_path = os.path.join(OUTPUT_DIR, "summary.txt")
    with open(summary_path, "w") as f:
        f.write(f"Successful: {success_count}\n")
        f.write(f"Failed: {len(failed_devices)}\n")

        if failed_devices:
            f.write("\nFailed Devices:\n")
            for ip in failed_devices:
                f.write(f"{ip}\n")


if __name__ == "__main__":
    main()