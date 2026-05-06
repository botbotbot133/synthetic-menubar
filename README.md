# Synthetic Credits Menu Bar App

Real-time macOS menu bar monitor for Synthetic API usage. Auto-starts on login with virtual environment support.

## Features

- 🚀 **Menu bar icon** — Shows at top of screen (next to WiFi/clock)
- ⏱️ **Configurable refresh** — Set your own interval (10s to unlimited)
- 🔄 **Auto-start** — Automatically starts when you login (LaunchAgent)
- 💡 **Live display** — Shows `⚡97% | 💵73%` (5-hour % | weekly %)
- 🔘 **Click for details** — Full info on both metrics
- 📊 **Smart notifications** — Alerts when data changes significantly
- 💾 **Persistent settings** — Saves API key and refresh interval
- 🐍 **Virtual environment** — Uses venv for isolated dependencies

## Installation

### Option 1: Homebrew (Recommended) 🍺

The easiest way to install:

```bash
# Add the tap
brew tap botbotbot133/synthetic

# Install
brew install synthetic-menubar

# First time setup
synthetic-menubar --setup
```

**Enable auto-start:**
```bash
mkdir -p ~/Library/LaunchAgents
cp $(brew --prefix)/share/synthetic-menubar/com.botbotbot133.synthetic-menubar.plist \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
```

### Option 2: Manual (with venv)

See below for manual installation instructions.

## Requirements

- macOS 10.14+
- Python 3.7+

## Manual Installation (with venv)

### 1. Clone & Setup venv

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar

# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install rumps
```

### 2. Run

```bash
python3 synthetic_menubar_app.py
```

Click **Settings** → Enter API key, then **Refresh Interval** → Set to `120`.

### 3. Auto-Start

```bash
chmod +x install_launchagent.sh
./install_launchagent.sh
```

## Quick Start

Once installed (via Homebrew or manual):

1. The app shows in menu bar: `⚡97% | 💵73%`
2. Click icon for settings and details
3. Configure refresh interval (default: 120s)
4. Enable auto-start for login

## Configuration

Create config at `~/.synthetic_menubar_config.json`:

```json
{
  "api_key": "your-api-key",
  "refresh_interval": 120,
  "detailed_view": true
}
```

## Menu Bar Display

```
┌────────────────────────────────┐
│ 💳 ⚡97% | 💵73%               │
└────────────────────────────────┘
│ ⏰ 5-Hour: --% (-- min)      │
│ 💰 Weekly: --% (in --)      │
│ ─────────────────────────────│
│ 📊 Detailed View: ✓ ON       │
│ ⏱️ Refresh Interval          │
│ 🔄 Refresh Now               │
│ ⚙️ Settings                  │
└────────────────────────────────┘
```

## What It Shows

- **5-Hour Limit**: Remaining % and time until regeneration
- **Weekly Credits**: Remaining % and dollar amount
- **Detailed/Simple toggle**: Switch between `⚡97%(5m)` and `⚡97%`

## Files

```
synthetic-menubar/
├── synthetic_menubar_app.py              # Main app
├── setup.py                                # Package setup
├── install_launchagent.sh                  # Auto-start setup
├── com.botbotbot133.synthetic-menubar.plist  # LaunchAgent
└── README.md
```

## Uninstall

**Homebrew:**
```bash
brew uninstall synthetic-menubar
brew untap botbotbot133/synthetic
```

**Manual:**
```bash
launchctl unload ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
rm ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
cd ~ && rm -rf synthetic-menubar
```

## API

Uses: `GET https://api.synthetic.new/v2/quotas`

## License

MIT
