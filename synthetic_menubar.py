#!/usr/bin/env python3
"""
Synthetic Credits Menu Bar App
A simple macOS menu bar app to display Synthetic API credits in real-time.
"""

import rumps
import requests
import json
import os
from datetime import datetime

# Configuration file path
CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")

class SyntheticCreditsApp(rumps.App):
    def __init__(self):
        super().__init__("💳", title="Loading...")
        self.api_key = self.load_api_key()
        self.refresh_interval = 300  # 5 minutes default
        self.menu = [
            "Credits: Loading...",
            "Used Today: Loading...",
            "Monthly Limit: Loading...",
            None,  # Separator
            "Refresh Now",
            "Settings",
            "About",
            None,  # Separator
            "Quit"
        ]
        
        # Start auto-refresh timer
        self.timer = rumps.Timer(self.auto_refresh, self.refresh_interval)
        self.timer.start()
        
        # Initial fetch
        self.fetch_credits()
    
    def load_api_key(self):
        """Load API key from config file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('api_key', '')
            except:
                pass
        return ''
    
    def save_api_key(self, api_key):
        """Save API key to config file"""
        config = {'api_key': api_key}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    
    @rumps.clicked("Refresh Now")
    def refresh(self, _):
        """Manual refresh triggered by user"""
        self.fetch_credits()
    
    def auto_refresh(self, _):
        """Auto-refresh timer callback"""
        self.fetch_credits()
    
    def fetch_credits(self):
        """Fetch credits from Synthetic API"""
        if not self.api_key:
            self.title = "❌ No API Key"
            self.menu[0] = "Credits: Configure API Key in Settings"
            return
        
        try:
            response = requests.get(
                "https://api.synthetic.new/openai/v1/quotas",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Accept": "application/json"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                credits_remaining = data.get('credits_remaining', 0)
                credits_used_today = data.get('credits_used_today', 0)
                monthly_limit = data.get('monthly_limit', 0)
                
                # Update menu bar title
                self.title = f"💳 {credits_remaining}"
                
                # Update menu items
                self.menu[0] = f"Credits: {credits_remaining}"
                self.menu[1] = f"Used Today: {credits_used_today}"
                self.menu[2] = f"Monthly Limit: {monthly_limit}"
                
                # Change icon color based on remaining credits
                if credits_remaining < 100:
                    self.title = f"🔴 {credits_remaining}"  # Low credits warning
                else:
                    self.title = f"💳 {credits_remaining}"
                    
            elif response.status_code == 401:
                self.title = "❌ Unauthorized"
                self.menu[0] = "Error: Invalid API Key"
            elif response.status_code == 429:
                self.title = "⏳ Rate Limited"
                self.menu[0] = "Error: Rate limit exceeded"
            else:
                self.title = "❌ Error"
                self.menu[0] = f"Error: HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            self.title = "❌ Offline"
            self.menu[0] = f"Error: {str(e)[:30]}"
    
    @rumps.clicked("Settings")
    def settings(self, _):
        """Open settings window"""
        if not self.api_key:
            current_key = ""
        else:
            # Show only last 4 characters
            current_key = "*" * (len(self.api_key) - 4) + self.api_key[-4:] if len(self.api_key) > 4 else ""
        
        window = rumps.Window(
            title="Settings",
            message=f"Enter your Synthetic API Key:\n\nCurrent: {current_key or 'Not set'}",
            default_text="",
            ok="Save",
            cancel="Cancel"
        )
        
        response = window.run()
        if response.clicked:
            new_key = response.text.strip()
            if new_key:
                self.api_key = new_key
                self.save_api_key(new_key)
                rumps.alert("Success", "API Key saved! Refreshing...")
                self.fetch_credits()
    
    @rumps.clicked("About")
    def about(self, _):
        """Show about dialog"""
        rumps.alert(
            "About Synthetic Credits App",
            "Version 1.0\n\n"
            "A simple menu bar app to monitor your Synthetic API credits.\n\n"
            "Features:\n"
            "• Real-time credit display\n"
            "• Auto-refresh every 5 minutes\n"
            "• Low credits warning\n\n"
            "GitHub: botbotbot133/synthetic-menubar"
        )
    
    @rumps.clicked("Quit")
    def quit_app(self, _):
        """Quit the application"""
        rumps.quit_application()

if __name__ == "__main__":
    app = SyntheticCreditsApp()
    app.run()
