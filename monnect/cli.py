import sys
from .utils import get_displays, get_paired_devices
from .installer import (
    save_config,
    create_launch_agent,
    start,
    stop,
    is_running,
    uninstall,
)
from .watcher import run
from pathlib import Path
import shutil
import json

CONFIG_PATH = Path.home() / ".config" / "monnect" / "config.json"

def doctor():
    print("Running monnect doctor...\n")

    blueutil = shutil.which("blueutil")
    system_profiler = shutil.which("system_profiler")

    print("blueutil:", "OK" if blueutil else "MISSING")
    print("system_profiler:", "OK" if system_profiler else "MISSING")
    print("config file:", "OK" if CONFIG_PATH.exists() else "MISSING")
    print("service running:", "YES" if is_running() else "NO")

    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text())
        print("\nCurrent configuration:")
        print("Display:", config.get("display"))
        print("Speaker MAC:", config.get("speaker_mac"))



def choose(prompt, options):
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}) {option}")

    choice = int(input("\nSelect number: "))
    return options[choice - 1]


def setup():
    displays = get_displays()
    devices = get_paired_devices()

    display = choose("Select display:", displays)
    names = [name for name, _ in devices]
    device_name = choose("Select Bluetooth speaker:", names)

    mac = dict(devices)[device_name]

    save_config(display, mac)
    create_launch_agent()
    start()

    print("\nmonnect installed and running.")


from .watcher import display_connected, speaker_connected
import json


def status():
    running = is_running()

    print("Service running:", "YES" if running else "NO")

    if not CONFIG_PATH.exists():
        print("No configuration found.")
        return

    config = json.loads(CONFIG_PATH.read_text())

    display = config["display"]
    mac = config["speaker_mac"]
    blueutil_path = config["blueutil_path"]
    system_profiler_path = config["system_profiler_path"]

    monitor = display_connected(display, system_profiler_path)
    speaker = speaker_connected(mac, blueutil_path)

    print("Monitor detected:", monitor)
    print("Speaker connected:", speaker)

def main():
    if len(sys.argv) < 2:
        print("Usage: monnect [setup|start|stop|status|doctor|uninstall]")
        return

    command = sys.argv[1]

    if command == "setup":
        setup()
    elif command == "start":
        start()
        print("monnect started.")
    elif command == "stop":
        stop()
        print("monnect stopped.")
    elif command == "status":
        status()
    elif command == "uninstall":
        uninstall()
        print("monnect uninstalled.")
    elif command == "doctor":
        doctor()
    else:
        print("Unknown command.")
