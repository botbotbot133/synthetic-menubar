# Synthetic Credits Menu Bar App

Real-time macOS menu bar monitor for Synthetic API usage. Auto-starts on login.

## Features

- 🚀 **Menu bar icon** — Shows at top of screen (next to WiFi/clock)
- ⏱️ **Configurable refresh** — Set your own interval (10s to unlimited)
- 🔄 **Auto-start** — Automatically starts when you login (LaunchAgent)
- 💡 **Live display** — Shows `⚡97% | 💵73%` (5-hour % | weekly %)
- 🔘 **Click for details** — Full info on both metrics
- 📊 **Smart notifications** — Alerts when data changes significantly
- 💾 **Persistent settings** — Saves API key and refresh interval

## Quick Start

### 1. Install

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
pip3 install -r requirements.txt
```

### 2. Run Once (to test)

```bash
python3 synthetic_menubar_app.py
```
- Click **Settings** → Enter your Synthetic API key
- Click **Refresh Interval** → Set to `120` (2 minutes)
- The app appears in your menu bar! 💳

### 3. Enable Auto-Start (Optional but recommended)

To automatically start on login:

```bash
chmod +x install_launchagent.sh
./install_launchagent.sh
```

**Done!** The app will now auto-start every time you login.

## Menu Bar Display

```
┌────────────────────────────────┐
│ 💳 ⚡97% | 💵73%               │  ← Menu bar
└────────────────────────────────┘
│ ⏰ 5-Hour Limit              │  ← Click for details
│ 💰 Weekly Credits            │
│ ─────────────────────────────│
│ ⏱️ Refresh Interval: 120s   │  ← Click to change
│ 🔄 Refresh Now               │  ← Manual refresh
│ ⚙️ Settings                  │
│ ℹ️ About                     │
└────────────────────────────────┘
```

## Auto-Start on Login (LaunchAgent)

The included `install_launchagent.sh` script sets up auto-start:

```bash
./install_launchagent.sh
```

**What it does:**
- Creates a macOS LaunchAgent
- Auto-starts on login
- Keeps running in background
- Restarts if it crashes

**Manage the LaunchAgent:**

```bash
# Check status
launchctl list | grep synthetic

# Stop
launchctl unload ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist

# Start manually
launchctl load ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist

# View logs
tail -f /tmp/synthetic-menubar.log
cat /tmp/synthetic-menubar.error.log
```

## Configure Refresh Interval

1. Click **⏱️ Refresh Interval** in menu
2. Enter seconds:
   - `60` = 1 minute
   - `120` = 2 minutes (default)
   - `300` = 5 minutes
   - Minimum: `10` seconds
3. Timer restarts automatically

## Details Shown

### 5-Hour Limit
- Percentage remaining (e.g., 97%)
- Requests remaining / max
- Next tick time

### Weekly Credits  
- Dollar percentage (e.g., 73%)
- Remaining / max dollars ($34.89 / $48.00)
- Next regeneration time

## Files

- `synthetic_menubar_app.py` — Main application
- `install_launchagent.sh` — Setup auto-start on login
- `com.botbotbot133.synthetic-menubar.plist` — LaunchAgent config
- `requirements.txt` — Dependencies (rumps)
- `~/.synthetic_menubar_config.json` — Settings (API key, interval)

## Requirements

- macOS 10.14+
- Python 3.7+
- `rumps` library (`pip3 install rumps`)

## API

Uses: `GET https://api.synthetic.new/v2/quotas`

## Troubleshooting

### "rumps not found"
```bash
pip3 install rumps
```

### LaunchAgent not working
```bash
# Check logs
cat /tmp/synthetic-menubar.error.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
launchctl load ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
```

### App not showing
- Check Activity Monitor → search "Python"
- Check logs: `tail -f /tmp/synthetic-menubar.log`
- Restart: `python3 synthetic_menubar_app.py`

## Uninstall

```bash
# Stop and remove LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
rm ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist

# Remove app
cd ~
rm -rf synthetic-menubar
```

## License

MIT — see LICENSE file
