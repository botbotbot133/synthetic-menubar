# Synthetic Credits Menu Bar App

Real-time macOS menu bar monitor for Synthetic API credits.

[![Homebrew](https://img.shields.io/badge/brew-install-blue.svg)](https://github.com/botbotbot133/homebrew-synthetic)

## Quick Install (Homebrew) 🍺

**One command installs everything:**

```bash
brew tap botbotbot133/synthetic && brew install synthetic-menubar
```

**Then run:**
```bash
synthetic-menubar --auto
```

That's it! The `--auto` flag will:
- Configure your API key (asks if needed)
- Install the LaunchAgent for auto-start
- Start the app immediately

## Features

- 🚀 **Menu bar icon** — Shows `⚡97% | 💵73%` live in your menu bar
- 📊 **Toggle detailed/simple view** — Click to switch between `⚡97%(5m)` and `⚡97%`
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
cp $(brew --prefix)/share/synthetic-menubar/com.botbotbot133.synthetic-menubar.plist \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
```

## Requirements

- macOS 10.14+
- Python 3.7+ (installed automatically by Homebrew)

## Menu Bar Display

```
┌──────────────────────────────┐
│ 💳 ⚡97%(5m)|💵73%(2h)       │  ← Menu bar title
└──────────────────────────────┘
│ ⏰ 5-Hour: 97% (regen 5m)   │  ← Click for details
│ 💰 Weekly: 73% (regen 2h)   │
│ ──────────────────────────── │
│ 📊 Detailed View: ✓ ON      │  ← Toggle mode
│ ⏱️ Refresh Interval         │
│ 🔄 Refresh Now              │
│ ⚙️ Settings                 │
└──────────────────────────────┘
```

## Configuration

Config file: `~/.synthetic_menubar_config.json`

```json
{
  "api_key": "your-api-key",
  "refresh_interval": 120,
  "detailed_view": true
}
```

Create manually or use `synthetic-menubar --setup`.

## Installation Methods

### 1. Homebrew (Recommended)

```bash
brew tap botbotbot133/synthetic
brew install synthetic-menubar
synthetic-menubar --auto
```

### 2. Manual (without Homebrew)

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
python3 -m venv venv
source venv/bin/activate
pip install rumps
python3 synthetic_menubar_app.py --setup
```

## Uninstall

**Homebrew:**
```bash
brew uninstall synthetic-menubar
brew untap botbotbot133/synthetic
```

**Manual:**
```bash
launchctl unload ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist 2>/dev/null || true
rm ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist 2>/dev/null || true
brew uninstall synthetic-menubar 2>/dev/null || true
```

## API

Uses: `GET https://api.synthetic.new/v2/quotas`

Get your API key at: https://synthetic.new/settings/api

## License

MIT
