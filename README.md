# Synthetic Credits Menu Bar App

A lightweight macOS menu bar application that displays your Synthetic API credits and usage in real-time.

## Features

- 📊 **Real-time credit display** — See remaining credits directly in your menu bar
- 🔄 **Auto-refresh** — Updates automatically every 5 minutes (configurable)
- 🔐 **Secure API key storage** — Uses macOS Keychain for safe credential storage
- 📈 **Usage tracking** — View credits used today and monthly limit
- ⚙️ **Settings panel** — Configure API key and refresh interval
- 🎯 **Low credit alerts** — Visual indicator when credits are running low

## Requirements

- macOS 13.0 (Ventura) or later
- Swift 5.9 or later
- Xcode 15.0 or later (for building)
- A Synthetic API key (get yours at [synthetic.new](https://synthetic.new))

## Installation

### Option 1: Build from Source (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/botbotbot133/synthetic-menubar.git
   cd synthetic-menubar
   ```

2. **Open in Xcode**
   ```bash
   open SyntheticMenuBarApp.xcodeproj
   ```
   Or open `SyntheticMenuBarApp.swift` in Xcode directly

3. **Build & Run**
   - Press `Cmd+R` to build and run
   - Or select **Product** → **Run** from the menu

4. **First Launch Setup**
   - Click the **Synthetic** menu bar icon (credit card icon)
   - Select **Open Settings**
   - Enter your Synthetic API key
   - Click **Save**
   - The app will immediately fetch and display your credits

### Option 2: Download Pre-built App (Coming Soon)

Pre-built releases will be available in the [Releases](https://github.com/botbotbot133/synthetic-menubar/releases) section.

## How It Works

### API Integration

The app connects to the Synthetic API to fetch your current usage statistics:

**Endpoint:** `GET https://api.synthetic.new/openai/v1/quotas`

**Authentication:** Bearer token with your API key

**Response includes:**
- `credits_remaining` — Available credits
- `credits_used_today` — Credits consumed today
- `monthly_limit` — Your monthly credit limit

### Auto-Refresh

By default, the app refreshes every **5 minutes**. You can configure this in settings:
- 1 minute
- 5 minutes (default)
- 15 minutes
- 30 minutes

### Display

The menu bar shows:
- **Credits remaining** — Large number in the menubar
- **Detailed view** — Click the icon for full usage breakdown

### Visual Indicators

- 🟢 **Green** — Healthy credit balance (>100 credits)
- 🔴 **Red** — Low credits (<100 remaining)

## Configuration

### Setting Your API Key

1. Click the **Synthetic** menu bar icon
2. Select **Open Settings**
3. Enter your API key in the secure field
4. Select your preferred refresh interval
5. Click **Save**

Your API key is stored securely in the macOS Keychain.

### Finding Your API Key

1. Log in to [synthetic.new](https://synthetic.new)
2. Go to **Settings** → **API**
3. Copy your API key
4. Paste it into the app's settings

## Architecture

### File Structure

```
synthetic-menubar/
├── SyntheticMenuBarApp.swift    # Main app & UI
├── SyntheticAPIClient.swift    # API communication
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

### Key Components

1. **SyntheticMenuBarApp.swift**
   - `AppDelegate`: Manages menu bar item and popover
   - `ContentView`: Main UI showing credits
   - `SettingsView`: Configuration panel

2. **SyntheticAPIClient.swift**
   - `SyntheticAPIClient`: Handles API requests
   - `QuotaResponse`: Data model for API response
   - Error handling for network/API issues

### Dependencies

- **SwiftUI** — Modern declarative UI framework
- **Combine** — Reactive programming for async operations
- **Foundation** — Core networking and data handling

## Development

### Building

```bash
# From the project directory
swift build

# Or open in Xcode and build
xcodebuild -project SyntheticMenuBarApp.xcodeproj -scheme SyntheticMenuBarApp
```

### Running Tests

```bash
swift test
```

## Troubleshooting

### "No API key configured" error

- Open Settings and enter your Synthetic API key
- Ensure the key is correct and active

### "Unauthorized" error

- Check that your API key is valid
- Verify the key hasn't expired
- Try regenerating the key at [synthetic.new](https://synthetic.new)

### Menu bar icon not showing

- Check that the app is running
- Look for the **credit card icon** (💳) in the menu bar
- Try quitting and reopening the app

### Not updating

- Check your internet connection
- Verify the refresh interval in settings
- Click **Refresh Now** in the menu to force an update

## Privacy & Security

- **No data collection** — The app only communicates with Synthetic's API
- **Local storage** — Your API key is stored in the macOS Keychain
- **No analytics** — No tracking or telemetry is implemented

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [SwiftUI](https://developer.apple.com/xcode/swiftui/)
- Powered by [Synthetic API](https://synthetic.new)
- Inspired by the need for real-time API usage monitoring

## Support

- 🐛 **Bug reports** — Use [GitHub Issues](https://github.com/botbotbot133/synthetic-menubar/issues)
- 💡 **Feature requests** — Open a discussion
- 📧 **Contact** — [synthetic.new/discord](https://synthetic.new/discord)

---

**Note:** This is an unofficial community project. Not affiliated with Synthetic Inc.
