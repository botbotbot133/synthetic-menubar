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
from datetime import datetime, timezone

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
API_ENDPOINT = "https://api.synthetic.new/v2/quotas"


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
        
        # Calculate remaining percentages
        remaining_5h = rolling.get("remaining", 0)
        max_5h = rolling.get("max", 1)
        five_percent = (remaining_5h / max_5h * 100) if max_5h > 0 else 0
        
        weekly_remaining = weekly.get("percentRemaining", 0)
        
        # Get regeneration times
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


def main():
    """Entry point for command line execution"""
    app = SyntheticMenuBarApp()
    app.run()


if __name__ == "__main__":
    main()
