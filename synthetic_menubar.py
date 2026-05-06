#!/usr/bin/env python3
"""
Synthetic Credits Monitor
Simple, no external dependencies
"""

import urllib.request
import urllib.error
import json
import os

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")
API_ENDPOINT = "https://api.synthetic.new/v2/quotas"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"api_key": ""}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def fetch_credits(api_key):
    if not api_key:
        return None, "No API key configured"
    
    req = urllib.request.Request(
        API_ENDPOINT,
        headers={
            "Authorization": f"Bearer {api_key}",
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

def main():
    config = load_config()
    
    print("="*50)
    print("Synthetic Credits Monitor")
    print("="*50)
    
    if not config.get("api_key"):
        print("\nEnter your API key:")
        api_key = input("> ").strip()
        if api_key:
            config["api_key"] = api_key
            save_config(config)
            print("✓ Saved!")
        else:
            return
    
    print("\nFetching credits...")
    data, error = fetch_credits(config["api_key"])
    
    if error:
        print(f"❌ Error: {error}")
    else:
        print(f"\n💳 Credits remaining: {data.get('credits_remaining', 'N/A')}")
        print(f"📊 Used today: {data.get('credits_used_today', 'N/A')}")
        print(f"📈 Monthly limit: {data.get('monthly_limit', 'N/A')}")
        print(f"\n✓ Success!")

if __name__ == "__main__":
    main()
