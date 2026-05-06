#!/usr/bin/env python3
"""
Synthetic Credits Menu Bar App
Real-time macOS menu bar monitor for Synthetic API usage
"""

import rumps
import urllib.request
import urllib.error
import json
import os
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
API_ENDPOINT = "https://api.synthetic.new/v2/quotas"

class SyntheticMenuBarApp(rumps.App):
    def __init__(self):
        # Load config first
        self.config = self.load_config()
        self.api_key = self.config.get('api_key', '')
        self.refresh_interval = self.config.get('refresh_interval', 120)  # Default 2 minutes
        
        super().__init__("💳", title="Loading...")
        self.timer = None
        self.data = None
        
        # Build menu
        self.build_menu()
        
        # Start if API key exists
        if self.api_key:
            self.start_refresh_timer()
            self.refresh(None)  # Initial fetch
        else:
            self.title = "❌ Setup"
    
    def build_menu(self):
        """Build the menu structure"""
        interval_text = f"⏱️ Refresh Interval: {self.refresh_interval}s"
        self.menu = [
            "⏰ 5-Hour Limit",
            "💰 Weekly Credits",
            None,
            interval_text,
            "🔄 Refresh Now",
            "⚙️ Settings",
            None,
            "ℹ️ About",
            "🚪 Quit"
        ]
    
    def load_config(self):
        """Load config from file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'api_key': '', 'refresh_interval': 120}
    
    def save_config(self):
        """Save current config"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def start_refresh_timer(self):
        """Start or restart refresh timer with current interval"""
        if self.timer:
            self.timer.stop()
        self.timer = rumps.Timer(self.refresh, self.refresh_interval)
        self.timer.start()
    
    def fetch_data(self):
        """Fetch data from Synthetic API"""
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
    
    def refresh(self, _):
        """Refresh data and update menu bar"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Refreshing...")
        data, error = self.fetch_data()
        
        if error:
            self.title = "❌ Error"
            print(f"Error: {error}")
        else:
            old_data = self.data
            self.data = data
            self.update_display()
            
            # Check if data changed significantly
            if old_data and self.data_changed(old_data, data):
                rumps.notification("Synthetic", "⚡ Credits Changed!", "Check your limits")
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Updated ✓")
    
    def data_changed(self, old, new):
        """Check if important data changed"""
        try:
            old_rolling = old.get("rollingFiveHourLimit", {}).get("tickPercent", 0)
            new_rolling = new.get("rollingFiveHourLimit", {}).get("tickPercent", 0)
            old_weekly = old.get("weeklyTokenLimit", {}).get("percentRemaining", 0)
            new_weekly = new.get("weeklyTokenLimit", {}).get("percentRemaining", 0)
            
            return old_rolling != new_rolling or old_weekly != new_weekly
        except:
            return False
    
    def update_display(self):
        """Update menu bar title based on data"""
        if not self.data:
            return
        
        rolling = self.data.get("rollingFiveHourLimit", {})
        weekly = self.data.get("weeklyTokenLimit", {})
        
        rolling_percent = rolling.get("tickPercent", 0) * 100 if rolling.get("tickPercent") else 0
        weekly_percent = weekly.get("percentRemaining", 0) if weekly.get("percentRemaining") else 0
        
        # Update title: "⚡97% | 💵73%" 
        self.title = f"⚡{rolling_percent:.0f}% | 💵{weekly_percent:.0f}%"
        
        # Rebuild menu with fresh data
        self.build_menu()
    
    def format_time_short(self, iso_string):
        """Format time to HH:MM"""
        try:
            dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            return dt.strftime("%H:%M")
        except:
            return iso_string[:5]
    
    # --- Menu Handlers ---
    
    @rumps.clicked("⏰ 5-Hour Limit")
    def show_5hour(self, _):
        if self.data and "rollingFiveHourLimit" in self.data:
            rolling = self.data["rollingFiveHourLimit"]
            percent = rolling.get("tickPercent", 0) * 100
            remaining = rolling.get("remaining", 0)
            max_val = rolling.get("max", 0)
            next_tick = self.format_time_short(rolling.get("nextTickAt", ""))
            
            rumps.alert(
                "⏰ Rolling 5-Hour Limit",
                f"✅ Remaining: {percent:.1f}%\n"
                f"💳 Requests: {remaining:.1f} / {max_val}\n"
                f"🔄 Next Tick: {next_tick}h"
            )
        else:
            rumps.alert("No Data", "Please wait for first refresh.")
    
    @rumps.clicked("💰 Weekly Credits")
    def show_weekly(self, _):
        if self.data and "weeklyTokenLimit" in self.data:
            weekly = self.data["weeklyTokenLimit"]
            percent = weekly.get("percentRemaining", 0)
            remaining = weekly.get("remainingCredits", "N/A")
            max_credits = weekly.get("maxCredits", "N/A")
            next_regen = self.format_time_short(weekly.get("nextRegenAt", ""))
            
            rumps.alert(
                "💰 Weekly Credits",
                f"✅ Remaining: {percent:.1f}%\n"
                f"💵 Credits: {remaining} / {max_credits}\n"
                f"🔄 Next Regen: {next_regen}h"
            )
        else:
            rumps.alert("No Data", "Please wait for first refresh.")
    
    @rumps.clicked("🔄 Refresh Now")
    def manual_refresh(self, _):
        self.refresh(None)
        rumps.notification("Synthetic", "✓ Refreshed", f"Next: {self.refresh_interval}s")
    
    @rumps.clicked("⏱️ Refresh Interval")
    def change_interval(self, _):
        """Change auto-refresh interval"""
        current = self.refresh_interval
        
        window = rumps.Window(
            "Refresh Interval",
            f"Current: {current} seconds ({current//60} min)\n\n"
            "Enter new interval in seconds:\n"
            "• 60 = 1 minute\n"
            "• 120 = 2 minutes (default)\n"
            "• 300 = 5 minutes\n"
            "• 600 = 10 minutes",
            default_text=str(current)
        )
        
        response = window.run()
        if response.clicked:
            try:
                new_interval = int(response.text.strip())
                if new_interval >= 10:  # Minimum 10 seconds
                    self.refresh_interval = new_interval
                    self.config['refresh_interval'] = new_interval
                    self.save_config()
                    self.start_refresh_timer()
                    rumps.notification(
                        "Synthetic", 
                        "✓ Interval Updated", 
                        f"Now refreshing every {new_interval}s"
                    )
                else:
                    rumps.alert("Error", "Minimum interval: 10 seconds")
            except ValueError:
                rumps.alert("Error", "Please enter a valid number")
    
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
        rumps.alert(
            "Synthetic Credits Monitor",
            "Version 1.0\n\n"
            "Real-time Synthetic API usage.\n\n"
            "Shows in menu bar:\n"
            "• 5-hour rate limit %\n"
            "• Weekly credits %\n"
            "• Auto-refresh\n\n"
            f"Refresh interval: {self.refresh_interval}s\n"
            "GitHub: botbotbot133/synthetic-menubar"
        )
    
    @rumps.clicked("🚪 Quit")
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    app = SyntheticMenuBarApp()
    app.run()
