# Synthetic Credits Monitor

Monitor Synthetic API credits in real-time — CLI or macOS Menu Bar.

## Two Versions

### 1. CLI Version (No Dependencies)

```bash
python3 synthetic_menubar.py
```

Shows complete data once, then exits.

### 2. Menu Bar Version (Recommended) 🍎

**Requires:** `pip3 install rumps`

```bash
pip3 install rumps
python3 synthetic_menubar_app.py
```

**Features:**
- 🚀 Runs in menu bar (next to WiFi, clock)
- 🔄 Auto-refresh every 2 minutes
- 💬 Click icon for detailed info
- ⚡ Shows both metrics in title:
  - `⚡97% | 💵73%` (5-hour | weekly)

## What It Shows

Both versions display:
- **5-Hour Limit** — Rolling rate limit (% remaining, next tick time)
- **Weekly Credits** — Dollar amount ($34.89 / $48.00)
- **Monthly Requests** — Request count vs limit
- **Search (Hourly)** — Hourly search limits
- **Free Tool Calls** — Free tier usage

## Sample Output (CLI)

```
💳 Synthetic Credits Monitor

💰 WEEKLY TOKEN LIMIT
   💵 Max: $48.00
   💵 Remaining: $34.89 (72.7%)
   🔄 Next: 06.05.2026 07:36

⏰ ROLLING 5-HOUR LIMIT
   ✅ Remaining: 973.33 / 1000 (97.3%)
   🔄 Next tick: 06.05.2026 06:30
```

## Installation

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar

# For Menu Bar
pip3 install -r requirements.txt

# Then run
python3 synthetic_menubar_app.py  # Menu bar
# OR
python3 synthetic_menubar.py      # CLI
```

## Files

- `synthetic_menubar_app.py` → **Menu bar app** (rumps, auto-refresh)
- `synthetic_menubar.py` → **CLI version** (no deps, run once)
- `requirements.txt` → rumps dependency

## API

Uses: `GET https://api.synthetic.new/v2/quotas`

## Menu Bar App Screenshot

```
┌─────────────────────────┐
│ 💳 ⚡97% | 💵73%        │  ← Menu bar icon
└─────────────────────────┘
│ ⏰ 5-Hour Limit         │
│ 💰 Weekly Credits      │
│ ─────────────────────   │
│ 🔄 Refresh Now          │
│ ⚙️ Settings             │
└─────────────────────────┘
```

## Why Two Versions?

| Feature | CLI | Menu Bar |
|---------|-----|----------|
| Dependencies | ❌ None | ✅ rumps |
| Auto-refresh | ❌ Manual | ✅ Every 2 min |
| Menu bar icon | ❌ No | ✅ Yes |
| Click for details | ❌ No | ✅ Yes |
| Use case | Quick check | Monitoring |

## Troubleshooting

### "rumps not found"
```bash
pip3 install rumps
```

### "No API key"
Click **Settings** menu and enter key from [synthetic.new](https://synthetic.new)

## License

MIT — see LICENSE file
