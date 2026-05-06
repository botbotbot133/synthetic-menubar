# Synthetic Credits Menu Bar App

Real-time macOS menu bar monitor for Synthetic API credits.

## Installation via pipx (Recommended)

The easiest way to install:

```bash
# Install pipx (macOS package manager)
brew install pipx

# Install the app
pipx install synthetic-menubar

# Run with auto-setup
synthetic-menubar --auto
```

That's it! pipx handles all dependencies including PyObjC automatically.

## Manual Installation

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
pip3 install rumps pyobjc-core pyobjc-framework-Cocoa
python3 synthetic_menubar_app.py --auto
```

## Features

- 🚀 **Menu bar icon** — Shows `⚡97% | 💵73%` live in your menu bar
- 📊 **Toggle detailed/simple view** — Switch between `⚡97%(5m)` and `⚡97%`
- 🔄 **Auto-refresh** — Configurable interval (default: 2 minutes)
- 🚀 **Auto-start** — LaunchAgent runs app on login
- 🗝️ **Secure** — API key stored locally in `~/.synthetic_menubar_config.json`

## Usage

### With `--auto` (Recommended)

```bash
# Does everything: setup + LaunchAgent + start app
synthetic-menubar --auto
```

### Manual Setup

```bash
# 1. Configure API key
synthetic-menubar --setup

# 2. Run manually
synthetic-menubar

# 3. Enable auto-start (optional)
mkdir -p ~/Library/LaunchAgents
cp /path/to/com.botbotbot133.synthetic-menubar.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
```

## Requirements

- macOS 10.14+
- Python 3.8+

## Quick Start

1. Run `synthetic-menubar --auto` or `synthetic-menubar --setup`
2. Click menu bar icon for settings
3. Configure refresh interval
4. Enable auto-start

## API

Get your Synthetic API key at: https://synthetic.new/settings/api

## License

MIT
