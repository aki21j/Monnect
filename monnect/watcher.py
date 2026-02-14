import subprocess
import time
import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "monnect" / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def display_connected(display_name, system_profiler_path):
    try:
        output = subprocess.check_output(
            [system_profiler_path, "SPDisplaysDataType"]
        ).decode()
        return display_name in output
    except:
        return False


def speaker_connected(mac, blueutil_path):
    try:
        output = subprocess.check_output(
            [blueutil_path, "--info", mac, "--format", "json"]
        ).decode()

        info = json.loads(output)
        return info.get("connected", False)
    except:
        return False


def connect(mac, blueutil_path):
    subprocess.run([blueutil_path, "--connect", mac])


def disconnect(mac, blueutil_path):
    subprocess.run([blueutil_path, "--disconnect", mac])


def run():
    config = load_config()

    display = config["display"]
    mac = config["speaker_mac"]
    interval = config.get("interval", 5)
    blueutil_path = config["blueutil_path"]
    system_profiler_path = config["system_profiler_path"]

    stable_false_count = 0
    stable_true_count = 0

    while True:
        monitor_present = display_connected(display, system_profiler_path)
        speaker_is_connected = speaker_connected(mac, blueutil_path)

        if monitor_present:
            stable_true_count += 1
            stable_false_count = 0
        else:
            stable_false_count += 1
            stable_true_count = 0

        if stable_true_count >= 2 and not speaker_is_connected:
            connect(mac, blueutil_path)

        if stable_false_count >= 2 and speaker_is_connected:
            disconnect(mac, blueutil_path)

        time.sleep(interval)


if __name__ == "__main__":
    run()
