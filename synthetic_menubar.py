#!/usr/bin/env python3
"""
Synthetic Credits Menu Bar App
Lite Version - Only Python Standard Library, no external dependencies
"""

import urllib.request
import urllib.error
import json
import os
import sys
from datetime import datetime

# Configuration
CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
API_BASE = "https://api.synthetic.new/openai/v1"

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"api_key": "", "last_credits": None}

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def fetch_credits(api_key):
    """Fetch credits from Synthetic API using only standard library"""
    if not api_key:
        return None, "No API key configured"
    
    url = f"{API_BASE}/quotas"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data, None
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return None, "Unauthorized - check your API key"
        elif e.code == 429:
            return None, "Rate limited"
        else:
            return None, f"HTTP Error {e.code}"
    except urllib.error.URLError as e:
        return None, f"Network error: {str(e.reason)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def print_status_line(credits_data, error_msg=None):
    """Print a simple status line (for menu bar simulation)"""
    if error_msg:
        print(f"[ERROR] {error_msg[:40]}")
    elif credits_data:
        remaining = credits_data.get('credits_remaining', 0)
        used_today = credits_data.get('credits_used_today', 0)
        monthly_limit = credits_data.get('monthly_limit', 0)
        
        # Simple visual indicator
        if remaining < 100:
            icon = "🔴"
        else:
            icon = "💳"
        
        print(f"{icon} Credits: {remaining} | Used today: {used_today} | Limit: {monthly_limit}")
    else:
        print("[UNKNOWN] Check API key")

def show_menu():
    """Simple CLI menu"""
    config = load_config()
    
    while True:
        print("\n" + "="*50)
        print("Synthetic Credits Monitor")
        print("="*50)
        
        api_key_status = "✓ Set" if config.get("api_key") else "✗ Not set"
        print(f"\n1. Refresh credits now")
        print(f"2. Settings (API Key: {api_key_status})")
        print(f"3. Show last known credits")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            print("\nFetching credits...")
            data, error = fetch_credits(config.get("api_key", ""))
            if error:
                print(f"❌ {error}")
            else:
                print_status_line(data)
                config["last_credits"] = data
                save_config(config)
        
        elif choice == "2":
            print("\n" + "-"*50)
            current_key = config.get("api_key", "")
            if current_key:
                masked = "*" * (len(current_key) - 4) + current_key[-4:] if len(current_key) > 4 else "*" * len(current_key)
                print(f"Current API key: {masked}")
            else:
                print("No API key configured")
            
            new_key = input("Enter new API key (or press Enter to keep current): ").strip()
            if new_key:
                config["api_key"] = new_key
                save_config(config)
                print("✓ API key saved")
            elif new_key == "" and current_key:
                # Clear key
                config["api_key"] = ""
                save_config(config)
                print("✓ API key cleared")
        
        elif choice == "3":
            if config.get("last_credits"):
                print("\nLast known credits:")
                print_status_line(config["last_credits"])
            else:
                print("No cached data. Please refresh first.")
        
        elif choice == "4":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid option")

def auto_refresh_mode():
    """Auto-refresh mode (prints status every 5 minutes)"""
    config = load_config()
    
    import time
    
    if not config.get("api_key"):
        print("No API key configured. Please run with --setup first.")
        sys.exit(1)
    
    print("Auto-refresh mode started. Press Ctrl+C to stop.")
    print("Checking credits every 5 minutes...\n")
    
    while True:
        data, error = fetch_credits(config["api_key"])
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if error:
            print(f"[{timestamp}] ❌ {error}")
        else:
            remaining = data.get('credits_remaining', 0)
            if remaining < 100:
                print(f"[{timestamp}] 🔴 LOW CREDITS: {remaining}")
            else:
                print(f"[{timestamp}] 💳 Credits: {remaining}")
            
            # Save to config
            config["last_credits"] = data
            save_config(config)
        
        try:
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            print("\n\nStopping...")
            break

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description='Synthetic Credits Monitor')
    parser.add_argument('--setup', action='store_true', help='Initial setup')
    parser.add_argument('--auto', action='store_true', help='Auto-refresh mode')
    parser.add_argument('--once', action='store_true', help='Fetch once and exit')
    
    args = parser.parse_args()
    
    if args.once:
        config = load_config()
        data, error = fetch_credits(config.get("api_key", ""))
        if error:
            print(f"Error: {error}")
            sys.exit(1)
        else:
            print_status_line(data)
    
    elif args.auto:
        auto_refresh_mode()
    
    elif args.setup:
        config = load_config()
        print("Synthetic Credits Monitor - Setup")
        print("="*50)
        
        current_key = config.get("api_key", "")
        if current_key:
            masked = "*" * (len(current_key) - 4) + current_key[-4:]
            print(f"Current API key: {masked}")
        
        new_key = input("\nEnter your Synthetic API key: ").strip()
        if new_key:
            config["api_key"] = new_key
            save_config(config)
            print("\n✓ API key saved!")
            
            # Test it
            print("\nTesting API connection...")
            data, error = fetch_credits(new_key)
            if error:
                print(f"❌ Test failed: {error}")
            else:
                print("✓ Connection successful!")
                print_status_line(data)
        else:
            print("No key entered. Setup cancelled.")
    
    else:
        # Interactive menu mode
        show_menu()

if __name__ == "__main__":
    main()
