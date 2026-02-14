# Monnect

Automatically connect or disconnect a Bluetooth speaker when a specific monitor is connected on macOS.

Monnect runs as a background LaunchAgent and manages Bluetooth audio based on display state.

---

## Features

- Auto-connect speaker when monitor is detected
- Auto-disconnect when monitor is removed
- Debounced monitor detection (no flicker)
- `monnect doctor` for environment validation
- `monnect status` for live system state
- CLI lifecycle management
- Installable via pipx

---

## Requirements

- macOS
- Python 3.9+
- Homebrew
- blueutil (auto-installed during setup if missing)

---

## Installation

Recommended:

    brew install pipx
    pipx ensurepath
    pipx install monnect

For development:

    git clone https://github.com/aki21j/Monnect.git
    cd Monnect
    pipx install -e .

---

## Setup

Run interactive setup:

    monnect setup

This will:
- Detect available displays
- Detect paired Bluetooth devices
- Install background service

---

## Commands

Start service:

    monnect start

Stop service:

    monnect stop

Check status:

    monnect status

Run diagnostics:

    monnect doctor

Uninstall service:

    monnect uninstall

---

## How It Works

Monnect:
1. Monitors display state using system_profiler
2. Checks Bluetooth state via blueutil
3. Applies debounced logic
4. Connects or disconnects speaker accordingly
5. Runs continuously via macOS LaunchAgent

---

## Development

    pipx uninstall monnect
    pipx install -e .

---

## License

MIT License
