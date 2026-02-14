#!/usr/bin/env python3

import subprocess
import time

# ===== CONFIG =====
TARGET_DISPLAY = "DELL U2717D"
SPEAKER_MAC = "48-d6-d5-f3-8f-7c"
CHECK_INTERVAL = 10  # seconds
# ==================

def display_connected():
    try:
        output = subprocess.check_output(
            ["system_profiler", "SPDisplaysDataType"],
            stderr=subprocess.DEVNULL
        ).decode()

        return TARGET_DISPLAY in output

    except Exception:
        return False


def connect_speaker():
    subprocess.run(
        ["blueutil", "--connect", SPEAKER_MAC],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def disconnect_speaker():
    subprocess.run(
        ["blueutil", "--disconnect", SPEAKER_MAC],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def main():
    connected = False

    print("monnect running...")
    print(f"Watching for display: {TARGET_DISPLAY}")
    print(f"Speaker MAC: {SPEAKER_MAC}")
    print("Press CTRL+C to stop.\n")

    while True:
        monitor_present = display_connected()

        if monitor_present and not connected:
            print("Display detected → Connecting speaker")
            connect_speaker()
            connected = True

        elif not monitor_present and connected:
            print("Display removed → Disconnecting speaker")
            disconnect_speaker()
            connected = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
