import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import ensure_log_dir, load_devices
from backup import backup_device

DEVICE_TYPE = "cisco_ios"


def parse_args():
    parser = argparse.ArgumentParser(description="Network Config Backup Tool")

    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument(
        "--file",
        default="config/devices.txt",
        help="Path to device list file",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=5,
        help="Number of parallel connections",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    device_file = os.path.join(base_dir, args.file)

    ensure_log_dir()
    devices = load_devices(device_file)

    success = 0
    failed = []

    print(f"\n[INFO] Running with {args.threads} parallel threads...\n")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_ip = {
            executor.submit(
                backup_device,
                ip,
                args.username,
                args.password,
                DEVICE_TYPE,
            ): ip
            for ip in devices
        }

        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                result = future.result()
                if result:
                    success += 1
                else:
                    failed.append(ip)
            except Exception as e:
                print(f"[CRITICAL] {ip} -> {e}")
                failed.append(ip)

    print("\n========== SUMMARY ==========")
    print(f"Successful: {success}")
    print(f"Failed: {len(failed)}")


if __name__ == "__main__":
    main()