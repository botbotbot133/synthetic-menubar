# Synthetic Credits Menu Bar App

A lightweight Python-based macOS menu bar application that displays your Synthetic API credits in real-time.

![Menu Bar Screenshot](screenshot.png)

## Features

- 📊 **Real-time credit display** — See remaining credits directly in your menu bar
- 🔄 **Auto-refresh** — Updates automatically every 5 minutes
- 🔐 **Secure API key storage** — Saves API key to local config file
- 📈 **Usage tracking** — View credits used today and monthly limit
- ⚙️ **Settings** — Easy configuration via menu
- 🚨 **Low credit alerts** — Visual warning when credits are below 100
- 🐍 **Pure Python** — No compilation needed, runs directly

## Requirements

- macOS 10.14 (Mojave) or later
- Python 3.7 or later
- A Synthetic API key (get yours at [synthetic.new](https://synthetic.new))

## Installation

### Option 1: Clone & Run (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/botbotbot133/synthetic-menubar.git
   cd synthetic-menubar
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python3 synthetic_menubar.py
   ```

4. **Set your API key**
   - Click the **💳** menu bar icon
   - Select **Settings**
   - Enter your Synthetic API key
   - Click **Save**

### Option 2: Direct Download

1. Download the latest release from [Releases](https://github.com/botbotbot133/synthetic-menubar/releases)
2. Extract the zip file
3. Install dependencies: `pip3 install rumps requests`
4. Run: `python3 synthetic_menubar.py`

## How It Works

The app connects to the Synthetic API to fetch your current usage statistics:

**Endpoint:** `GET https://api.synthetic.new/openai/v1/quotas`

**Authentication:** Bearer token with your API key

**Response includes:**
- `credits_remaining` — Available credits
- `credits_used_today` — Credits consumed today
- `monthly_limit` — Your monthly credit limit

### Auto-Refresh

The app automatically refreshes every **5 minutes** (300 seconds). You can manually refresh anytime by clicking **Refresh Now** in the menu.

### Visual Indicators

- 💳 **100+ credits** — Normal (credit card icon)
- 🔴 **< 100 credits** — Low credits warning (red icon)
- ❌ **No API key** — Configuration needed
- ⏳ **Rate limited** — Too many requests
- 🌐 **Offline** — Network connection issue

## Configuration

### Setting Your API Key

1. Click the **menu bar icon** (💳 or 🔴)
2. Select **Settings**
3. Enter your API key
4. Click **Save**

Your API key is stored in `~/.synthetic_menubar_config.json`

### Finding Your API Key

1. Log in to [synthetic.new](https://synthetic.new)
2. Go to **Settings** → **API**
3. Copy your API key
4. Paste it into the app

## Architecture

### File Structure

```
synthetic-menubar/
├── synthetic_menubar.py    # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

### Dependencies

- **[rumps](https://pypi.org/project/rumps/)** — Ridiculously Uncomplicated macOS Python Statusbar apps
- **[requests](https://pypi.org/project/requests/)** — HTTP library for API calls

### Why Python?

- ✅ Easy to modify and extend
- ✅ No compilation needed
- ✅ Cross-platform potential (Windows/Linux support could be added)
- ✅ Quick development cycle
- ✅ No Xcode or Apple Developer account needed

## Development

### Running from source

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
pip3 install -r requirements.txt
python3 synthetic_menubar.py
```

### Making changes

Edit `synthetic_menubar.py` and re-run:
```bash
python3 synthetic_menubar.py
```

No build process needed!

## Troubleshooting

### "No API key configured"

- Open Settings and enter your Synthetic API key
- Ensure the key is correct and active
- Check `~/.synthetic_menubar_config.json` exists

### "Unauthorized" error

- Verify your API key is valid at [synthetic.new](https://synthetic.new)
- Try regenerating the key if needed

### "Rate Limited"

- Wait a few minutes before refreshing again
- The free tier has rate limits

### App not showing in menu bar

- Check if Python is running: `ps aux | grep synthetic_menubar`
- Try running from Terminal to see errors
- Ensure `rumps` is installed: `pip3 list | grep rumps`

### Module not found errors

```bash
pip3 install rumps requests
# Or
pip3 install -r requirements.txt
```

## Privacy & Security

- **Local storage only** — API key stored in `~/.synthetic_menubar_config.json` (local file)
- **No data collection** — The app only communicates with Synthetic's API
- **No analytics** — No tracking or telemetry
- **Open source** — You can inspect all code

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Improvements

Potential features for future versions:
- [ ] macOS notification support for low credits
- [ ] Configurable refresh intervals
- [ ] Dark mode support
- [ ] Historical usage graph
- [ ] Multiple API key support
- [ ] Windows/Linux support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [rumps](https://github.com/jaredks/rumps) — Ridiculously Uncomplicated macOS Statusbar apps
- Powered by [Synthetic API](https://synthetic.new)
- Inspired by the need for real-time API usage monitoring

## Support

- 🐛 **Bug reports** — Use [GitHub Issues](https://github.com/botbotbot133/synthetic-menubar/issues)
- 💡 **Feature requests** — Open a discussion
- 📧 **Contact** — [synthetic.new/discord](https://synthetic.new/discord)

---

**Note:** This is an unofficial community project. Not affiliated with Synthetic Inc.
