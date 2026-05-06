#!/bin/bash
# Fix LaunchAgent to use venv Python

LAUNCHAGENT="$HOME/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist"
VENV_PYTHON="$HOME/synthetic-menubar/venv/bin/python"

echo "Fixing LaunchAgent to use venv Python..."

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: venv Python not found at $VENV_PYTHON"
    echo "Make sure you're in the synthetic-menubar directory with venv"
    exit 1
fi

echo "✓ Found venv Python: $VENV_PYTHON"

# Stop current agent
launchctl unload "$LAUNCHAGENT" 2>/dev/null || true

# Fix the plist
sed -i '' "s|/usr/bin/python3|$VENV_PYTHON|g" "$LAUNCHAGENT"

echo "✓ Updated plist to use venv Python"

# Start agent
launchctl load "$LAUNCHAGENT"

echo "✓ LaunchAgent reloaded with venv Python!"
echo ""
echo "Testing..."
sleep 2

if launchctl list | grep -q "com.botbotbot133.synthetic-menubar"; then
    echo "✅ SUCCESS! Check your menu bar in 3-5 seconds 💳"
else
    echo "❌ Still not running. Check: cat /tmp/synthetic-menubar.error.log"
fi
