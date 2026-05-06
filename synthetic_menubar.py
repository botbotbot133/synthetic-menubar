#!/usr/bin/env python3
"""
Synthetic Credits Menu Bar App
Auto-discovers correct API endpoint
"""

import urllib.request
import urllib.error
import json
import os
import sys
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
BASE_URL = "https://api.synthetic.new"

# Multiple possible endpoints - will try each one
POSSIBLE_ENDPOINTS = [
    "/v1/quotas",
    "/v1/usage",
    "/v1/billing/usage",
    "/v1/credits",
    "/v1/account",
    "/v1/user",
    "/openai/v1/quotas",
]

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"api_key": "", "working_endpoint": None}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def fetch_with_endpoint(endpoint, api_key):
    """Try a specific endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)

def fetch_credits(api_key, working_endpoint=None):
    """Auto-discover working endpoint or use cached one"""
    if not api_key:
        return None, "No API key configured"
    
    # If we have a working endpoint from before, try it first
    if working_endpoint:
        data, error = fetch_with_endpoint(working_endpoint, api_key)
        if data:
            return data, None, working_endpoint
    
    # Try all possible endpoints
    print("  Discovering API endpoint...")
    for endpoint in POSSIBLE_ENDPOINTS:
        data, error = fetch_with_endpoint(endpoint, api_key)
        if data:
            return data, None, endpoint
    
    return None, "No working endpoint found", None

def print_status(credits_data, error_msg=None, endpoint=None):
    if error_msg:
        print(f"❌ {error_msg}")
        return
    
    if credits_data:
        remaining = credits_data.get('credits_remaining', credits_data.get('credits', 0))
        used_today = credits_data.get('credits_used_today', credits_data.get('used_today', 0))
        monthly_limit = credits_data.get('monthly_limit', credits_data.get('limit', 0))
        
        icon = "🔴" if remaining < 100 else "💳"
        
        print(f"\n{icon} Credits: {remaining}")
        print(f"📊 Used today: {used_today}")
        print(f"📈 Monthly limit: {monthly_limit}")
        if endpoint:
            print(f"🔗 Endpoint: {endpoint}")

def show_menu():
    config = load_config()
    working_endpoint = config.get("working_endpoint")
    
    while True:
        print("\n" + "="*50)
        print("Synthetic Credits Monitor")
        print("="*50)
        
        api_status = "✓ Set" if config.get("api_key") else "✗ Not set"
        endpoint_status = working_endpoint or "Not discovered"
        
        print(f"\n1. Refresh credits now")
        print(f"2. Settings (API Key: {api_status})")
        print(f"3. Show last known credits")
        print(f"4. Test all endpoints")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            print("\nFetching credits...")
            data, error, endpoint = fetch_credits(config.get("api_key", ""), working_endpoint)
            if error:
                print(f"❌ {error}")
            else:
                print_status(data, endpoint=endpoint)
                config["last_credits"] = data
                if endpoint:
                    config["working_endpoint"] = endpoint
                    working_endpoint = endpoint
                save_config(config)
        
        elif choice == "2":
            print("\n" + "-"*50)
            current_key = config.get("api_key", "")
            if current_key:
                masked = "*" * (len(current_key) - 4) + current_key[-4:] if len(current_key) > 4 else ""
                print(f"Current API key: {masked or '*'}")
            
            new_key = input("\nEnter new API key: ").strip()
            if new_key:
                config["api_key"] = new_key
                config["working_endpoint"] = None  # Reset endpoint discovery
                save_config(config)
                print("✓ API key saved!")
        
        elif choice == "3":
            if config.get("last_credits"):
                print("\nLast known credits:")
                print_status(config["last_credits"])
            else:
                print("No cached data. Please refresh first.")
        
        elif choice == "4":
            if not config.get("api_key"):
                print("No API key configured!")
                continue
            
            print("\n" + "="*50)
            print("Testing all possible endpoints...")
            print("="*50 + "\n")
            
            for endpoint in POSSIBLE_ENDPOINTS:
                print(f"Testing {endpoint}...", end=" ")
                data, error = fetch_with_endpoint(endpoint, config["api_key"])
                if data:
                    print("✅ WORKS!")
                    print(f"   Data: {json.dumps(data, indent=2)[:100]}...")
                    config["working_endpoint"] = endpoint
                    save_config(config)
                    break
                else:
                    print(f"❌ {error}")
            
            print("\n" + "="*50)
        
        elif choice == "5":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid option")

if __name__ == "__main__":
    show_menu()
