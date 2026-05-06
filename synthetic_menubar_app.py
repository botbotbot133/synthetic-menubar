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
        super().__init__("💳", title="Loading...")
        self.api_key = self.load_api_key()
        self.timer = None
        self.data = None
        
        # Build menu
        self.build_menu()
        
        # Start auto-refresh (every 2 minutes)
        if self.api_key:
            self.timer = rumps.Timer(self.refresh, 120)
            self.timer.start()
            self.refresh(None)  # Initial fetch
        else:
            self.title = "❌ No Key"
    
    def build_menu(self):
        """Build the menu structure"""
        self.menu = [
            "⏰ 5-Hour Limit",
            "💰 Weekly Credits",
            None,  # Separator
            "🔄 Refresh Now",
            "⚙️ Settings",
            None,  # Separator
            "ℹ️ About",
            "🚪 Quit"
        ]
    
    def load_api_key(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('api_key', '')
            except:
                pass
        return ''
    
    def save_config(self, api_key):
        config = {'api_key': api_key}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
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
        """Refresh data and update menu bar"""
        print("Fetching data...")
        data, error = self.fetch_data()
        
        if error:
            self.title = "❌ Error"
            print(f"Error: {error}")
        else:
            self.data = data
            self.update_display()
            print("Data updated!")
    
    def update_display(self):
        """Update menu bar title and menu based on data"""
        if not self.data:
            return
        
        # Get key metrics
        rolling = self.data.get("rollingFiveHourLimit", {})
        weekly = self.data.get("weeklyTokenLimit", {})
        
        rolling_percent = rolling.get("tickPercent", 0) * 100 if rolling.get("tickPercent") else 0
        weekly_percent = weekly.get("percentRemaining", 0) if weekly.get("percentRemaining") else 0
        
        # Update main title (show both percentages)
        # Format: "5h: 97% | $: 73%"
        self.title = f"⚡{rolling_percent:.0f}% | 💵{weekly_percent:.0f}%"
        
        # Force menu update
        self.build_menu()
    
    def format_time(self, iso_string):
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
            next_tick = self.format_time(rolling.get("nextTickAt", ""))
            
            rumps.alert(
                "⏰ Rolling 5-Hour Limit",
                f"Remaining: {percent:.1f}%\n"
                f"Requests: {remaining:.1f} / {max_val}\n"
                f"Next tick: {next_tick}"
            )
        else:
            rumps.alert("No Data", "Please refresh first.")
    
    @rumps.clicked("💰 Weekly Credits")
    def show_weekly(self, _):
        if self.data and "weeklyTokenLimit" in self.data:
            weekly = self.data["weeklyTokenLimit"]
            percent = weekly.get("percentRemaining", 0)
            remaining = weekly.get("remainingCredits", "N/A")
            max_credits = weekly.get("maxCredits", "N/A")
            next_regen = self.format_time(weekly.get("nextRegenAt", ""))
            
            rumps.alert(
                "💰 Weekly Credits",
                f"Remaining: {percent:.1f}%\n"
                f"Credits: {remaining} / {max_credits}\n"
                f"Next regen: {next_regen}"
            )
        else:
            rumps.alert("No Data", "Please refresh first.")
    
    @rumps.clicked("🔄 Refresh Now")
    def manual_refresh(self, _):
        self.refresh(None)
        rumps.notification("Synthetic", "Refreshed!", "Data updated")
    
    @rumps.clicked("⚙️ Settings")
    def settings(self, _):
        if self.api_key:
            masked = "*" * (len(self.api_key) - 4) + self.api_key[-4:] if len(self.api_key) > 4 else ""
            message = f"Current key: {masked}\n\nEnter new API key (or Cancel to keep):"
        else:
            message = "Enter your Synthetic API key:"
        
        window = rumps.Window("Settings", message, default_text="")
        response = window.run()
        
        if response.clicked:
            new_key = response.text.strip()
            if new_key:
                self.api_key = new_key
                self.save_config(new_key)
                rumps.notification("Synthetic", "✓ API Key Saved", "Refreshing...")
                self.refresh(None)
    
    @rumps.clicked("ℹ️ About")
    def about(self, _):
        rumps.alert(
            "Synthetic Credits Monitor",
            "Version 1.0\n\n"
            "Menu bar app for Synthetic API usage.\n\n"
            "Shows:\n"
            "• 5-hour limit %\n"
            "• Weekly credits %\n"
            "• Regeneration times\n\n"
            "GitHub: botbotbot133/synthetic-menubar"
        )
    
    @rumps.clicked("🚪 Quit")
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    app = SyntheticMenuBarApp()
    app.run()
