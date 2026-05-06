# Synthetic Credits Monitor

A lightweight Python-based macOS menu bar application that displays your Synthetic API credits in real-time.

## Features

- 📊 **Auto-discovery** — Automatically finds the correct API endpoint
- 🔄 **Auto-refresh** — Updates every 5 minutes
- 🔐 **Secure** — Saves API key locally
- 📈 **Usage tracking** — View credits remaining, used today, and monthly limit
- 🎯 **No external dependencies** — Uses only Python standard library
- 🔍 **Debug mode** — Test all endpoints to find the correct one

## Requirements

- macOS 10.14 or later
- Python 3.7+ (tested with 3.14, 3.12, 3.11)
- Synthetic API key from [synthetic.new](https://synthetic.new)

## Installation

Just clone and run — **no external dependencies!**

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
python3 synthetic_menubar.py
```

## Quick Start

1. **Run the app:**
   ```bash
   python3 synthetic_menubar.py
   ```

2. **Enter your API key:**
   - Select option `2` (Settings)
   - Paste your Synthetic API key
   - The app will auto-discover the correct endpoint

3. **Refresh credits:**
   - Select option `1` (Refresh credits now)
   - The app tries multiple endpoints and uses the one that works

## How It Works

### Auto-Discovery

The app automatically tries multiple API endpoints to find the one that works with your account:

- `/v1/quotas`
- `/v1/usage`
- `/v1/billing/usage`
- `/v1/credits`
- `/v1/account`
- `/v1/user`
- `/openai/v1/quotas`

Once it finds a working endpoint, it caches it for future use.

### Manual Endpoint Testing

If auto-discovery fails, you can manually test all endpoints:

1. Select option `4` (Test all endpoints)
2. The app will try each one and show which works
3. The working endpoint is automatically saved

## Configuration

API key and discovered endpoint are stored in:
`~/.synthetic_menubar_config.json`

## Troubleshooting

### "No working endpoint found"

1. Make sure your API key is correct
2. Run option `4` (Test all endpoints) to see which work
3. Check your Synthetic dashboard to verify API access

### Getting 401/403 errors

Your API key might not have access to usage data. Check your Synthetic account settings.

## Why Python Standard Library Only?

- ✅ Works with any Python version (3.7 - 3.14+)
- ✅ No `pip install` needed
- ✅ No compilation required
- ✅ Easy to modify and debug

## Files

- `synthetic_menubar.py` — Main application
- `test_api.py` — Debug: Test all endpoints
- `synthetic_menubar_debug.py` — Debug: Detailed error logging

## License

MIT License — see [LICENSE](LICENSE) file

## Support

- 🐛 Issues: [GitHub Issues](https://github.com/botbotbot133/synthetic-menubar/issues)
- 💬 Discord: [synthetic.new/discord](https://synthetic.new/discord)

---

**Note:** Unofficial community project. Not affiliated with Synthetic Inc.
