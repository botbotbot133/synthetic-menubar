#!/bin/bash
# Installation script for Synthetic Menu Bar LaunchAgent
# Automatically detects virtual environment

set -e  # Exit on error

echo "=========================================="
echo "Synthetic Menu Bar - LaunchAgent Setup"
echo "=========================================="
echo ""

# Detect repository path (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="$(basename "$SCRIPT_DIR")"

# Check if running from correct directory
if [ ! -f "synthetic_menubar_app.py" ]; then
    echo "❌ Error: Run this script from the synthetic-menubar directory"
    echo "   cd ~/synthetic-menubar"
    echo "   ./install_launchagent.sh"
    exit 1
fi

echo "✓ Found repository at: $SCRIPT_DIR"

# Detect virtual environment
VENV_PATH=""
if [ -d "$SCRIPT_DIR/venv" ]; then
    VENV_PATH="$SCRIPT_DIR/venv/bin/python"
    echo "✓ Found venv at: $SCRIPT_DIR/venv"
elif [ -d "$SCRIPT_DIR/.venv" ]; then
    VENV_PATH="$SCRIPT_DIR/.venv/bin/python"
    echo "✓ Found .venv at: $SCRIPT_DIR/.venv"
else
    # Try to find any venv in the directory
    VENV_DIR=$(find "$SCRIPT_DIR" -maxdepth 1 -type d \( -name "venv" -o -name ".venv" -o -name "env" \) | head -1)
    if [ -n "$VENV_DIR" ]; then
        VENV_PATH="$VENV_DIR/bin/python"
        echo "✓ Found venv at: $VENV_DIR"
    fi
fi

if [ -z "$VENV_PATH" ] || [ ! -f "$VENV_PATH" ]; then
    echo ""
    echo "⚠️  No virtual environment found!"
    echo ""
    echo "Please create a venv first:"
    echo "   cd $SCRIPT_DIR"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install rumps"
    echo ""
    echo "Or install rumps system-wide:"
    echo "   pip3 install --user rumps"
    echo ""
    read -p "Continue with system Python? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        VENV_PATH="/usr/bin/python3"
        echo "⚠️  Using system Python (may not have rumps)"
    else
        exit 1
    fi
fi

echo "✓ Using Python: $VENV_PATH"

# Check if rumps is available in the venv
if ! "$VENV_PATH" -c "import rumps" 2>/dev/null; then
    echo ""
    echo "⚠️  rumps not found in venv!"
    echo ""
    echo "Installing rumps..."
    "$VENV_PATH" -m pip install rumps
fi

LAUNCHAGENT_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.botbotbot133.synthetic-menubar.plist"
PLIST_SOURCE="$SCRIPT_DIR/$PLIST_NAME"
PLIST_DEST="$LAUNCHAGENT_DIR/$PLIST_NAME"

# Create LaunchAgents directory if needed
if [ ! -d "$LAUNCHAGENT_DIR" ]; then
    echo "✓ Creating LaunchAgents directory..."
    mkdir -p "$LAUNCHAGENT_DIR"
fi

# Copy plist and replace placeholders
echo "✓ Configuring LaunchAgent with venv Python..."
cp "$PLIST_SOURCE" "$PLIST_DEST"

# Replace VENV_PLACEHOLDER with actual venv python path
sed -i '' "s|VENV_PLACEHOLDER|$VENV_PATH|g" "$PLIST_DEST"

# Replace REPO_PLACEHOLDER with actual repo path
sed -i '' "s|REPO_PLACEHOLDER|$SCRIPT_DIR|g" "$PLIST_DEST"

echo "✓ LaunchAgent configured with:"
echo "   Python: $VENV_PATH"
echo "   Repo: $SCRIPT_DIR"

# Check if already running and unload it
if launchctl list | grep -q "com.botbotbot133.synthetic-menubar"; then
    echo "⚠️  Unloading previous instance..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

# Load the new LaunchAgent
echo "✓ Loading LaunchAgent..."
launchctl load "$PLIST_DEST"

echo ""
echo "=========================================="
echo "✅ SUCCESS! LaunchAgent installed!"
echo "=========================================="
echo ""
echo "The app should appear in your menu bar in 3-5 seconds 💳"
echo ""
echo "Commands:"
echo "  Status:  launchctl list | grep synthetic"
echo "  Stop:    launchctl unload ~/Library/LaunchAgents/$PLIST_NAME"
echo "  Start:   launchctl load ~/Library/LaunchAgents/$PLIST_NAME"
echo "  Logs:    tail -f /tmp/synthetic-menubar.log"
echo "  Errors:  cat /tmp/synthetic-menubar.error.log"
echo ""
echo "The app will auto-start on next login! 🚀"
echo ""
echo "Note: You can now deactivate your venv if active"
echo "      The LaunchAgent will use the venv Python automatically"
