import json
import subprocess
import sys
from pathlib import Path
import shutil

CONFIG_DIR = Path.home() / ".config" / "monnect"
CONFIG_PATH = CONFIG_DIR / "config.json"
PLIST_PATH = Path.home() / "Library/LaunchAgents/com.monnect.plist"
LABEL = "com.monnect"

def ensure_blueutil():
    blueutil_path = shutil.which("blueutil")
    if blueutil_path:
        return blueutil_path

    print("blueutil not found.")
    choice = input("Install via Homebrew? (y/n): ").strip().lower()

    if choice == "y":
        subprocess.run(["brew", "install", "blueutil"])
        blueutil_path = shutil.which("blueutil")

        if blueutil_path:
            return blueutil_path

    raise RuntimeError(
        "blueutil is required. Install manually with: brew install blueutil"
    )


def save_config(display, speaker_mac):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    blueutil_path = ensure_blueutil()
    system_profiler_path = shutil.which("system_profiler")

    if not system_profiler_path:
        raise RuntimeError("system_profiler not found (unexpected macOS issue).")

    with open(CONFIG_PATH, "w") as f:
        json.dump({
            "display": display,
            "speaker_mac": speaker_mac,
            "interval": 5,
            "blueutil_path": blueutil_path,
            "system_profiler_path": system_profiler_path
        }, f, indent=2)


def create_launch_agent():
    python_path = sys.executable
    watcher_path = Path(__file__).parent / "watcher.py"

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{watcher_path}</string>
    </array>

    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PLIST_PATH, "w") as f:
        f.write(plist_content)


def start():
    subprocess.run(["launchctl", "load", str(PLIST_PATH)])


def stop():
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)])


def is_running():
    result = subprocess.run(
        ["launchctl", "list"],
        capture_output=True,
        text=True
    )
    return LABEL in result.stdout


def uninstall():
    stop()
    if PLIST_PATH.exists():
        PLIST_PATH.unlink()
    if CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
