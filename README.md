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

## Requirements

- macOS 10.14+
- Python 3.7+
- **Virtual environment** (venv) — Required for LaunchAgent

## Quick Start (with venv)

### 1. Clone & Setup venv

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar

# Create virtual environment (REQUIRED for LaunchAgent)
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies in venv
pip install rumps
```

### 2. Test Run (in venv)

```bash
# Make sure venv is active (you'll see (venv) in prompt)
python3 synthetic_menubar_app.py
```

- Click **Settings** → Enter your Synthetic API key
- Click **Refresh Interval** → Set to `120` (2 minutes)
- The app appears in your menu bar! 💳

### 3. Enable Auto-Start (Recommended)

The LaunchAgent **requires** the venv. Our install script auto-detects it:

```bash
# Make sure you're in the repo directory with venv
./install_launchagent.sh
```

The script will:
- ✅ Auto-detect your venv (`venv/`, `.venv/`, or `env/`)
- ✅ Configure LaunchAgent to use venv Python
- ✅ Start immediately
- ✅ Auto-start on login

**Done!** The app will now auto-start every time you login.

## Important: Virtual Environment

⚠️ **Why venv is required:**

The LaunchAgent runs **independently** of your terminal. It cannot access packages installed via `pip3 install --user` or system packages. **It MUST use a venv.**

### If you didn't use venv:

You may see errors like:
```
ModuleNotFoundError: No module named 'rumps'
```

**Fix:** Create venv and reinstall:
```bash
cd ~/synthetic-menubar
python3 -m venv venv
source venv/bin/activate
pip install rumps
./install_launchagent.sh
```

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

## Configure Refresh Interval

1. Click **⏱️ Refresh Interval** in menu
2. Enter seconds:
   - `60` = 1 minute
   - `120` = 2 minutes (default)
   - `300` = 5 minutes
   - Minimum: `10` seconds
3. Timer restarts automatically

## Auto-Start on Login (LaunchAgent)

The included `install_launchagent.sh` script sets up auto-start:

```bash
# Auto-detects venv and configures LaunchAgent
./install_launchagent.sh
```

**Features:**
- ✅ Auto-detects venv directory
- ✅ Configures LaunchAgent with venv Python
- ✅ Starts immediately
- ✅ Auto-starts on login
- ✅ Restarts if it crashes

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

```
synthetic-menubar/
├── synthetic_menubar_app.py              # Main application
├── venv/                                 # Virtual environment (auto-created)
├── install_launchagent.sh                # Setup auto-start
├── com.botbotbot133.synthetic-menubar.plist  # LaunchAgent template
├── requirements.txt                      # Dependencies
└── README.md                             # This file
```

## Troubleshooting

### "No virtual environment found"
```bash
# Create venv
cd ~/synthetic-menubar
python3 -m venv venv

# Activate and install
source venv/bin/activate
pip install rumps

# Re-run install
./install_launchagent.sh
```

### LaunchAgent not working
```bash
# Check logs
cat /tmp/synthetic-menubar.error.log

# Common issue: venv not detected
# Re-run install script:
./install_launchagent.sh
```

### "ModuleNotFoundError: No module named 'rumps'"
You installed rumps outside venv. Inside the repo:
```bash
source venv/bin/activate
pip install rumps
launchctl unload ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
launchctl load ~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist
```

## API

Uses: `GET https://api.synthetic.new/v2/quotas`

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
