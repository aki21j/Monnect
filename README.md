# Monnect

[![PyPI version](https://img.shields.io/pypi/v/monnect.svg)](https://pypi.org/project/monnect/)
[![Python](https://img.shields.io/pypi/pyversions/monnect.svg)](https://pypi.org/project/monnect/)
[![License](https://img.shields.io/github/license/aki21j/Monnect)](LICENSE)
[![CI](https://github.com/aki21j/Monnect/actions/workflows/ci.yml/badge.svg)](https://github.com/aki21j/Monnect/actions/workflows/ci.yml)

Automatically connect or disconnect a Bluetooth speaker when a specific display is connected on macOS.

Monnect runs in the background and watches for a configured external display.
When the display is detected, it connects your chosen Bluetooth speaker.
When the display is disconnected, it disconnects the speaker.

---

## Why?

If you use:

- An external monitor at your desk
- A Bluetooth speaker
- A MacBook that you dock and undock

You’ve probably manually switched audio devices more times than you’d like.

Monnect automates that.

---

## Installation

### Option 1: pipx (Recommended)

pipx install monnect

### Option 2: Homebrew

brew tap aki21j/monnect  
brew install monnect

---

## Requirements

- macOS
- blueutil

Install blueutil with:

brew install blueutil

---

## Setup

Run:

monnect setup

This will guide you through selecting:

- A display
- A Bluetooth device

Then start the service:

monnect start

---

## Commands

monnect start      - Start background service  
monnect stop       - Stop background service  
monnect status     - Show current status  
monnect doctor     - Validate environment  
monnect --version  - Show version  

---

## How It Works

- Uses system_profiler to detect display state
- Uses blueutil to manage Bluetooth connections
- Runs as a macOS LaunchAgent
- Polling-based with debounce logic

---

## Uninstall

If installed via pipx:

pipx uninstall monnect

If installed via Homebrew:

brew uninstall monnect  
brew untap aki21j/monnect  

---

## License

MIT