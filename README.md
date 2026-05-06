# Synthetic Credits Menu Bar App

Real-time macOS menu bar monitor for Synthetic API usage.

## Features

- 🚀 **Menu bar icon** — Shows at top of screen (next to WiFi/clock)
- ⏱️ **Configurable refresh** — Set your own interval (10s to unlimited)
- 💡 **Live display** — Shows `⚡97% | 💵73%` (5-hour % | weekly %)
- 🔘 **Click for details** — Full info on both metrics
- 📊 **Smart notifications** — Alerts when data changes significantly
- 💾 **Persistent settings** — Saves API key and refresh interval

## Installation

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
pip3 install -r requirements.txt
python3 synthetic_menubar_app.py
```

## First Run

1. App starts in menu bar with "❌ Setup"
2. Click **Settings** → Enter API key
3. Click **Refresh Interval** → Set update frequency:
   - `60` = 1 minute
   - `120` = 2 minutes (default)
   - `300` = 5 minutes

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

## Details Shown

### 5-Hour Limit
- Percentage remaining (e.g., 97%)
- Requests remaining / max
- Next tick time

### Weekly Credits  
- Dollar percentage (e.g., 73%)
- Remaining / max dollars ($34.89 / $48.00)
- Next regeneration time

## Configure Refresh Interval

1. Click **⏱️ Refresh Interval** in menu
2. Enter seconds (e.g., `120` for 2 minutes)
3. Timer restarts automatically

**Examples:**
- `60` = every 1 minute
- `120` = every 2 minutes (default)
- `300` = every 5 minutes
- `30` = every 30 seconds (minimum: 10s)

## Files

- `synthetic_menubar_app.py` — Main application
- `requirements.txt` — Dependencies (rumps)
- `~/.synthetic_menubar_config.json` — Settings stored here

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

### App not showing
- Check if running: Activity Monitor → search "Python"
- Restart: `python3 synthetic_menubar_app.py`

## License

MIT — see LICENSE file
