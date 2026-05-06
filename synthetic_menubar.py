#!/usr/bin/env python3
"""
Synthetic Credits Monitor
Shows subscription usage from /v2/quotas endpoint
"""

import urllib.request
import urllib.error
import json
import os
from datetime import datetime

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

def format_date(iso_string):
    """Format ISO date string to readable date"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return iso_string

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
            data = json.loads(response.read().decode('utf-8'))
            return data, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)

def main():
    config = load_config()
    
    print("="*50)
    print("Synthetic Credits Monitor")
    print("="*50)
    
    # Check/ask for API key
    if not config.get("api_key"):
        print("\n📝 Enter your Synthetic API key:")
        api_key = input("> ").strip()
        if api_key:
            config["api_key"] = api_key
            save_config(config)
            print("✓ API key saved!")
        else:
            print("❌ No key entered.")
            return
    
    print("\n🔄 Fetching subscription data...")
    data, error = fetch_credits(config["api_key"])
    
    if error:
        print(f"\n❌ Error: {error}")
        if error == "HTTP 401":
            print("💡 Check: Is your API key correct?")
        return
    
    # Parse the response
    if "subscription" in data:
        sub = data["subscription"]
        limit = sub.get("limit", "N/A")
        requests = sub.get("requests", 0)
        renews_at = sub.get("renewsAt", "N/A")
        
        # Calculate remaining
        try:
            remaining = limit - requests if isinstance(limit, int) and isinstance(requests, int) else "N/A"
        except:
            remaining = "N/A"
        
        print("\n" + "="*50)
        print("📊 SUBSCRIPTION STATUS")
        print("="*50)
        print(f"\n💳 Monthly limit: {limit} requests")
        print(f"📈 Used this period: {requests} requests")
        print(f"✅ Remaining: {remaining} requests")
        print(f"🔄 Renews at: {format_date(renews_at)}")
        print("="*50)
        
        # Warning if low
        if isinstance(remaining, int) and remaining < 20:
            print("\n⚠️  WARNING: Low credits remaining!")
        
        print("\n✓ Data retrieved successfully!")
    else:
        print("\n⚠️  Unexpected response format:")
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
