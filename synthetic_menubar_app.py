#!/usr/bin/env python3
"""
Synthetic Credits Menu Bar App
Uses rumps to display in macOS menu bar
"""

import rumps
import urllib.request
import urllib.error
import json
import os
import sys
import argparse
import subprocess
from datetime import datetime, timezone

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
API_ENDPOINT = "https://api.synthetic.new/v2/quotas"
LAUNCHAGENT_SOURCE = "/opt/homebrew/share/synthetic-menubar/com.botbotbot133.synthetic-menubar.plist"
LAUNCHAGENT_DEST = os.path.expanduser("~/Library/LaunchAgents/com.botbotbot133.synthetic-menubar.plist")


class SyntheticMenuBarApp(rumps.App):
    def __init__(self):
        # Load config
        self.config = self.load_config()
        self.api_key = self.config.get('api_key', '')
        self.refresh_interval = self.config.get('refresh_interval', 120)
        self.detailed_view = self.config.get('detailed_view', True)
        
        super().__init__("💳", title="Loading...")
        self.timer = None
        self.data = None
        
        # Build menu ONCE at start
        self._build_menu()
        
        # Start if API key exists
        if self.api_key:
            self.start_refresh_timer()
            self.refresh(None)
        else:
            self.title = "❌ Setup"
    
    def _build_menu(self):
        """Build menu with current state"""
        self.clear_menu()
        
        # Add regular menu items
        self.menu = [
            rumps.MenuItem("⏰ 5-Hour", callback=self.show_5hour),
            rumps.MenuItem("💰 Weekly", callback=self.show_weekly),
            None,  # Separator
        ]
        
        # Add toggle button with current status
        status = "✓ ON" if self.detailed_view else "✗ OFF"
        self.menu.add(rumps.MenuItem(f"📊 Detailed View: {status}", callback=self.toggle_detailed_view))
        
        # Add remaining items
        self.menu.add(rumps.MenuItem("⏱️ Refresh Interval", callback=self.change_interval))
        self.menu.add(rumps.MenuItem("🔄 Refresh Now", callback=self.manual_refresh))
        self.menu.add(rumps.MenuItem("⚙️ Settings", callback=self.settings))
        self.menu.add(rumps.MenuItem("ℹ️ About", callback=self.about))
        self.menu.add(rumps.MenuItem("🚪 Quit", callback=self.quit_app))
        
        # Add 5-hour and weekly click handlers
        self.menu['⏰ 5-Hour'].set_callback(self.show_5hour)
        self.menu['💰 Weekly'].set_callback(self.show_weekly)
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'api_key': '', 'refresh_interval': 120, 'detailed_view': True}
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def start_refresh_timer(self):
        if self.timer:
            self.timer.stop()
        self.timer = rumps.Timer(self.refresh, self.refresh_interval)
        self.timer.start()
    
    def fetch_data(self):
        if not self.api_key:
            return None, "No API key"
        
        req = urllib.request.Request(
            API_ENDPOINT,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8')), None
        except urllib.error.HTTPError as e:
            return None, f"HTTP {e.code}"
        except Exception as e:
            return None, str(e)
    
    def format_time_until(self, iso_timestamp):
        try:
            target = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            diff = target - now
            
            minutes = int(diff.total_seconds() / 60)
            
            if minutes < 60:
                return f"{minutes}m"
            else:
                hours = minutes // 60
                mins = minutes % 60
                return f"{hours}h{mins}m" if mins else f"{hours}h"
        except:
            return "?"
    
    def refresh(self, _):
        data, error = self.fetch_data()
        
        if error:
            self.title = "❌"
        else:
            self.data = data
            self.update_display()
    
    def update_display(self):
        if not self.data:
            return
        
        rolling = self.data.get("rollingFiveHourLimit", {})
        weekly = self.data.get("weeklyTokenLimit", {})
        
        # Calculate REMAINING %
        remaining_5h = rolling.get("remaining", 0)
        max_5h = rolling.get("max", 1)
        five_percent = (remaining_5h / max_5h * 100) if max_5h > 0 else 0
        
        weekly_remaining = weekly.get("percentRemaining", 0)
        
        five_regen = self.format_time_until(rolling.get("nextTickAt", ""))
        weekly_regen = self.format_time_until(weekly.get("nextRegenAt", ""))
        
        # Toggle between detailed and simplified view
        if self.detailed_view:
            self.title = f"⚡{five_percent:.0f}%({five_regen})|💵{weekly_remaining:.0f}%({weekly_regen})"
        else:
            self.title = f"⚡{five_percent:.0f}%|💵{weekly_remaining:.0f}%"
        
        # Update menu item titles
        for item in self.menu:
            if isinstance(item, rumps.MenuItem):
                if "⏰ 5-Hour" in item.title:
                    item.title = f"⏰ 5-Hour: {five_percent:.1f}% (regen {five_regen})"
                elif "💰 Weekly" in item.title:
                    item.title = f"💰 Weekly: {weekly_remaining:.1f}% (regen {weekly_regen})"
    
    def toggle_detailed_view(self, _):
        """Toggle detailed view mode"""
        self.detailed_view = not self.detailed_view
        self.config['detailed_view'] = self.detailed_view
        self.save_config()
        
        # Update menu text
        status = "✓ ON" if self.detailed_view else "✗ OFF"
        for item in self.menu:
            if isinstance(item, rumps.MenuItem) and "📊 Detailed View" in item.title:
                item.title = f"📊 Detailed View: {status}"
                break
        
        # Update display immediately
        self.update_display()
        
        # Show notification
        mode = "Detailed" if self.detailed_view else "Simple"
        detail_text = "with regen times" if self.detailed_view else "percent only"
        rumps.notification("Synthetic", f"📊 {mode} mode", detail_text)
        
    @rumps.clicked("⏰ 5-Hour")
    def show_5hour(self, _):
        if self.data and "rollingFiveHourLimit" in self.data:
            rolling = self.data["rollingFiveHourLimit"]
            remaining = rolling.get("remaining", 0)
            max_val = rolling.get("max", 0)
            percent = (remaining / max_val * 100) if max_val > 0 else 0
            tick_amount = rolling.get("tickPercent", 0) * 100
            regen = self.format_time_until(rolling.get("nextTickAt", ""))
            
            rumps.alert(
                "⏰ 5-Hour Limit",
                f"✅ {percent:.1f}% remaining\n"
                f"🔄 Regen in: {regen}\n"
                f"➕ +{tick_amount:.1f}% per tick"
            )
        else:
            rumps.alert("No Data", "Waiting...")
    
    @rumps.clicked("💰 Weekly")
    def show_weekly(self, _):
        if self.data and "weeklyTokenLimit" in self.data:
            weekly = self.data["weeklyTokenLimit"]
            percent = weekly.get("percentRemaining", 0)
            remaining = weekly.get("remainingCredits", "N/A")
            max_credits = weekly.get("maxCredits", "N/A")
            regen = self.format_time_until(weekly.get("nextRegenAt", ""))
            
            rumps.alert(
                "💰 Weekly Credits",
                f"✅ {percent:.1f}% remaining\n"
                f"💵 {remaining} / {max_credits}\n"
                f"🔄 Regen in: {regen}"
            )
        else:
            rumps.alert("No Data", "Waiting...")
    
    @rumps.clicked("🔄 Refresh Now")
    def manual_refresh(self, _):
        self.refresh(None)
        rumps.notification("Synthetic", "Refreshed!", f"Next in {self.refresh_interval}s")
    
    @rumps.clicked("⏱️ Refresh Interval")
    def change_interval(self, _):
        window = rumps.Window(
            "Refresh Interval",
            f"Current: {self.refresh_interval}s\n\nEnter new interval:",
            default_text=str(self.refresh_interval)
        )
        
        response = window.run()
        if response.clicked:
            try:
                new_interval = int(response.text.strip())
                if new_interval >= 10:
                    self.refresh_interval = new_interval
                    self.config['refresh_interval'] = new_interval
                    self.save_config()
                    self.start_refresh_timer()
                    rumps.notification("Synthetic", "✓ Updated", f"{new_interval}s")
                else:
                    rumps.alert("Error", "Minimum: 10 seconds")
            except ValueError:
                rumps.alert("Error", "Enter a number")
    
    @rumps.clicked("⚙️ Settings")
    def settings(self, _):
        if self.api_key:
            masked = "*" * (len(self.api_key) - 4) + self.api_key[-4:] if len(self.api_key) > 4 else "*"
            message = f"Current: {masked}\n\nEnter new API key:"
        else:
            message = "Enter your API key:"
        
        window = rumps.Window("Settings", message, default_text="")
        response = window.run()
        
        if response.clicked:
            new_key = response.text.strip()
            if new_key:
                self.api_key = new_key
                self.config['api_key'] = new_key
                self.save_config()
                rumps.notification("Synthetic", "✓ Key Saved", "Refreshing...")
                self.refresh(None)
    
    @rumps.clicked("ℹ️ About")
    def about(self, _):
        mode = "Detailed" if self.detailed_view else "Simple"
        rumps.alert(
            "About",
            f"Synthetic Credits Monitor\n"
            f"Mode: {mode}\n"
            f"Refresh: {self.refresh_interval}s"
        )
    
    @rumps.clicked("🚪 Quit")
    def quit_app(self, _):
        rumps.quit_application()


def run_setup():
    """Interactive setup to configure API key"""
    print("="*50)
    print("Synthetic Menu Bar - Setup")
    print("="*50)
    print()
    print("Enter your Synthetic API key:")
    
    api_key = input("> ").strip()
    
    if api_key:
        config = {
            'api_key': api_key,
            'refresh_interval': 120,
            'detailed_view': True
        }
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Config saved to {CONFIG_FILE}")
        print("\nYou can now run: synthetic-menubar")
        return True
    else:
        print("❌ No API key entered. Setup cancelled.")
        return False


def install_launchagent():
    """Install and load the LaunchAgent for auto-start"""
    print("="*50)
    print("Installing LaunchAgent for auto-start")
    print("="*50)
    
    # Check if source plist exists
    if not os.path.exists(LAUNCHAGENT_SOURCE):
        print(f"❌ Source plist not found: {LAUNCHAGENT_SOURCE}")
        print("   Install via: brew install synthetic-menubar")
        return False
    
    # Create LaunchAgents directory if needed
    launchagents_dir = os.path.expanduser("~/Library/LaunchAgents")
    if not os.path.exists(launchagents_dir):
        print(f"✓ Creating {launchagents_dir}")
        os.makedirs(launchagents_dir)
    
    # Check if already exists
    if os.path.exists(LAUNCHAGENT_DEST):
        print(f"⚠️  LaunchAgent already exists at {LAUNCHAGENT_DEST}")
        print("   Reloading...")
        subprocess.run(["launchctl", "unload", LAUNCHAGENT_DEST], capture_output=True)
    else:
        print(f"✓ Copying LaunchAgent...")
        subprocess.run(["cp", LAUNCHAGENT_SOURCE, LAUNCHAGENT_DEST], check=True)
    
    # Load the LaunchAgent
    print(f"✓ Loading LaunchAgent...")
    result = subprocess.run(["launchctl", "load", LAUNCHAGENT_DEST], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ LaunchAgent installed and loaded!")
        print("\nThe app will now auto-start on login.")
        return True
    else:
        print(f"❌ Failed to load LaunchAgent: {result.stderr}")
        return False


def run_auto():
    """Auto setup: configure if needed, install LaunchAgent, start app"""
    print("="*50)
    print("Synthetic Menu Bar - Auto Setup")
    print("="*50)
    print()
    
    # Check if config exists
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        except:
            pass
    
    # Step 1: Setup API key if needed
    if not config.get('api_key'):
        print("🔑 Step 1: API Key Setup")
        print("-" * 50)
        if not run_setup():
            return False
        # Reload config after setup
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        print("✓ API key already configured")
    
    # Step 2: Install LaunchAgent if needed
    print("\n🚀 Step 2: LaunchAgent Setup")
    print("-" * 50)
    
    if os.path.exists(LAUNCHAGENT_DEST):
        print("✓ LaunchAgent already installed")
        # Make sure it's loaded
        result = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
        if "com.botbotbot133.synthetic-menubar" in result.stdout:
            print("✓ LaunchAgent already running")
        else:
            print("⚠️  LaunchAgent not running, reloading...")
            subprocess.run(["launchctl", "load", LAUNCHAGENT_DEST], capture_output=True)
    else:
        if install_launchagent():
            print("✓ LaunchAgent installed and started")
        else:
            print("⚠️  LaunchAgent setup failed, but app will still run")
    
    # Step 3: Start the app
    print("\n💳 Step 3: Starting Synthetic Menu Bar")
    print("-" * 50)
    print("Starting app...")
    print()
    
    # Actually start the app
    main(run_app=True)
    
    return True


def main(run_app=False):
    """Entry point for command line execution"""
    
    # Check if running in standalone mode (not from --auto which already printed)
    if len(sys.argv) <= 1 or sys.argv[1] not in ['--setup', '--auto']:
        # Check for config, if not exist, show setup message
        if not os.path.exists(CONFIG_FILE):
            print("⚠️  No config found. Run: synthetic-menubar --setup")
            print("    Or: synthetic-menubar --auto")
            sys.exit(1)
    
    if run_app or len(sys.argv) == 1:
        # Normal mode - just run the app
        app = SyntheticMenuBarApp()
        app.run()


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--setup':
            run_setup()
        elif sys.argv[1] == '--auto':
            run_auto()
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Synthetic Menu Bar - Usage:")
            print()
            print("  synthetic-menubar           Run the app (requires setup first)")
            print("  synthetic-menubar --setup   Configure API key")
            print("  synthetic-menubar --auto    Auto setup and start (recommended)")
            print("  synthetic-menubar --help   Show this help")
            print()
            print("Examples:")
            print("  # First time setup")")
            print("  synthetic-menubar --setup")
            print()
            print("  # Or use auto for everything")")
            print("  synthetic-menubar --auto")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Run 'synthetic-menubar --help' for usage")
            sys.exit(1)
    else:
        main()
