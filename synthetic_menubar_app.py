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
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
API_ENDPOINT = "https://api.synthetic.new/v2/quotas"

class SyntheticMenuBarApp(rumps.App):
    def __init__(self):
        # Load config first
        self.config = self.load_config()
        self.api_key = self.config.get('api_key', '')
        self.refresh_interval = self.config.get('refresh_interval', 120)
        
        super().__init__("💳", title="Loading...")
        self.timer = None
        self.data = None
        
        # Build menu ONCE at start
        self.build_menu()
        
        # Start if API key exists
        if self.api_key:
            self.start_refresh_timer()
            self.refresh(None)
        else:
            self.title = "❌ Setup"
    
    def build_menu(self):
        """Build menu structure - called only ONCE at start"""
        self.menu = [
            "⏰ 5-Hour Limit",
            "💰 Weekly Credits",
            None,
            "⏱️ Refresh Interval",
            "🔄 Refresh Now",
            "⚙️ Settings",
            None,
            "ℹ️ About",
            "🚪 Quit"
        ]
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'api_key': '', 'refresh_interval': 120}
    
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
    
    def refresh(self, _):
        """Refresh and update ONLY the title, not the menu"""
        data, error = self.fetch_data()
        
        if error:
            self.title = "❌"
        else:
            self.data = data
            self.update_title()
            # Do NOT rebuild menu here!
    
    def update_title(self):
        """Update ONLY the menu bar title (not menu items)"""
        if not self.data:
            return
        
        rolling = self.data.get("rollingFiveHourLimit", {})
        weekly = self.data.get("weeklyTokenLimit", {})
        
        rolling_percent = rolling.get("tickPercent", 0) * 100 if rolling.get("tickPercent") else 0
        weekly_percent = weekly.get("percentRemaining", 0) if weekly.get("percentRemaining") else 0
        
        # Just update title - that's all!
        self.title = f"⚡{rolling_percent:.0f}%|💵{weekly_percent:.0f}%"
    
    @rumps.clicked("⏰ 5-Hour Limit")
    def show_5hour(self, _):
        if self.data and "rollingFiveHourLimit" in self.data:
            rolling = self.data["rollingFiveHourLimit"]
            percent = rolling.get("tickPercent", 0) * 100
            remaining = rolling.get("remaining", 0)
            max_val = rolling.get("max", 0)
            
            rumps.alert(
                "⏰ 5-Hour Limit",
                f"✅ Remaining: {percent:.1f}%\n"
                f"💳 {remaining:.0f} / {max_val} requests"
            )
        else:
            rumps.alert("No Data", "Waiting for first refresh...")
    
    @rumps.clicked("💰 Weekly Credits")
    def show_weekly(self, _):
        if self.data and "weeklyTokenLimit" in self.data:
            weekly = self.data["weeklyTokenLimit"]
            percent = weekly.get("percentRemaining", 0)
            remaining = weekly.get("remainingCredits", "N/A")
            max_credits = weekly.get("maxCredits", "N/A")
            
            rumps.alert(
                "💰 Weekly Credits",
                f"✅ Remaining: {percent:.1f}%\n"
                f"💵 {remaining} / {max_credits}"
            )
        else:
            rumps.alert("No Data", "Waiting for first refresh...")
    
    @rumps.clicked("🔄 Refresh Now")
    def manual_refresh(self, _):
        self.refresh(None)
        rumps.notification("Synthetic", "Refreshed!", f"Next in {self.refresh_interval}s")
    
    @rumps.clicked("⏱️ Refresh Interval")
    def change_interval(self, _):
        window = rumps.Window(
            "Refresh Interval",
            f"Current: {self.refresh_interval}s\n\nEnter new interval (seconds):",
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
                    rumps.notification("Synthetic", "✓ Interval Updated", f"{new_interval}s")
                else:
                    rumps.alert("Error", "Minimum: 10 seconds")
            except ValueError:
                rumps.alert("Error", "Please enter a number")
    
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
            "About",
            "Synthetic Credits Monitor v1.0\n\n"
            "Shows 5-hour and weekly credit usage\n"
            f"Refresh: {self.refresh_interval}s"
        )
    
    @rumps.clicked("🚪 Quit")
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    app = SyntheticMenuBarApp()
    app.run()
