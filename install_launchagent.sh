#!/bin/bash
# Installation script for Synthetic Menu Bar LaunchAgent

echo "=========================================="
echo "Synthetic Menu Bar - LaunchAgent Setup"
echo "=========================================="
echo ""

# Check if running from correct directory
if [ ! -f "synthetic_menubar_app.py" ]; then
    echo "❌ Error: Run this script from the synthetic-menubar directory"
    echo "   cd ~/synthetic-menubar"
    echo "   ./install_launchagent.sh"
    exit 1
fi

# Get the actual home directory (handles ~ expansion)
REPO_PATH="$HOME/synthetic-menubar"
LAUNCHAGENT_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.botbotbot133.synthetic-menubar.plist"

# Update plist with correct path
if [ -f "$PLIST_NAME" ]; then
    echo "✓ Updating plist with correct paths..."
    sed -i '' "s|/Users/lesu|$HOME|g" "$PLIST_NAME"
else
    echo "❌ Error: $PLIST_NAME not found"
    exit 1
fi

# Create LaunchAgents directory if needed
if [ ! -d "$LAUNCHAGENT_DIR" ]; then
    echo "✓ Creating LaunchAgents directory..."
    mkdir -p "$LAUNCHAGENT_DIR"
fi

# Copy plist to LaunchAgents
echo "✓ Copying LaunchAgent to $LAUNCHAGENT_DIR"
cp "$REPO_PATH/$PLIST_NAME" "$LAUNCHAGENT_DIR/"

# Check if already running and unload it
if launchctl list | grep -q "com.botbotbot133.synthetic-menubar"; then
    echo "⚠️  Unloading previous instance..."
    launchctl unload "$LAUNCHAGENT_DIR/$PLIST_NAME" 2>/dev/null || true
fi

# Load the new LaunchAgent
echo "✓ Loading LaunchAgent..."
launchctl load "$LAUNCHAGENT_DIR/$PLIST_NAME"

# Verify
if launchctl list | grep -q "com.botbotbot133.synthetic-menubar"; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! LaunchAgent installed!"
    echo "=========================================="
    echo ""
    echo "The app should now appear in your menu bar 💳"
    echo ""
    echo "Commands:"
    echo "  Status:  launchctl list | grep synthetic"
    echo "  Stop:    launchctl unload ~/Library/LaunchAgents/$PLIST_NAME"
    echo "  Start:   launchctl load ~/Library/LaunchAgents/$PLIST_NAME"
    echo "  Logs:    tail -f /tmp/synthetic-menubar.log"
    echo ""
    echo "The app will auto-start on next login! 🚀"
else
    echo "❌ Error: Failed to load LaunchAgent"
    echo "Check logs: cat /tmp/synthetic-menubar.error.log"
    exit 1
fi
