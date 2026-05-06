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
            return json.loads(response.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)

def main():
    config = load_config()
    
    print("="*60)
    print("Synthetic Credits Monitor")
    print("="*60)
    
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
    
    # Show COMPLETE raw response
    print("\n" + "="*60)
    print("📄 COMPLETE API RESPONSE (RAW JSON):")
    print("="*60)
    print(json.dumps(data, indent=2))
    print("="*60)
    
    # Parse different sections
    print("\n" + "="*60)
    print("📊 PARSED SUBSCRIPTION DATA")
    print("="*60)
    
    # 1. Monthly Requests (subscription)
    if "subscription" in data:
        sub = data["subscription"]
        print(f"\n📅 MONTHLY REQUESTS")
        print(f"   💳 Limit: {sub.get('limit', 'N/A')} requests/month")
        print(f"   📈 Used: {sub.get('requests', 0)} requests")
        remaining = sub.get('limit', 0) - sub.get('requests', 0)
        print(f"   ✅ Remaining: {remaining} requests")
        print(f"   🔄 Renews: {format_date(sub.get('renewsAt', 'N/A'))}")
    
    # 2. Search (hourly)
    if "search" in data and "hourly" in data["search"]:
        search = data["search"]["hourly"]
        print(f"\n🔍 SEARCH (Hourly)")
        print(f"   💳 Limit: {search.get('limit', 'N/A')}/hour")
        print(f"   📈 Used: {search.get('requests', 0)}")
        print(f"   🔄 Renews: {format_date(search.get('renewsAt', 'N/A'))}")
    
    # 3. Weekly Token Limit (DOLLAR AMOUNTS!)
    if "weeklyTokenLimit" in data:
        token = data["weeklyTokenLimit"]
        print(f"\n💰 WEEKLY TOKEN LIMIT (Credits in $)")
        print(f"   💵 Max Credits: {token.get('maxCredits', 'N/A')}")
        print(f"   💵 Remaining: {token.get('remainingCredits', 'N/A')}")
        print(f"   📊 Percent: {token.get('percentRemaining', 0):.1f}%")
        print(f"   🔄 Next Regen: {format_date(token.get('nextRegenAt', 'N/A'))}")
        print(f"   ➕ Next Regen Amount: {token.get('nextRegenCredits', 'N/A')}")
    
    # 4. Rolling 5 Hour Limit
    if "rollingFiveHourLimit" in data:
        rolling = data["rollingFiveHourLimit"]
        print(f"\n⏰ ROLLING 5-HOUR LIMIT")
        print(f"   💳 Max: {rolling.get('max', 'N/A')}")
        print(f"   ✅ Remaining: {rolling.get('remaining', 'N/A'):.2f}")
        print(f"   📊 Tick Percent: {rolling.get('tickPercent', 0)}")
        print(f"   🔄 Next Tick: {format_date(rolling.get('nextTickAt', 'N/A'))}")
        print(f"   🚫 Limited: {'YES' if rolling.get('limited') else 'NO'}")
    
    # 5. Free Tool Calls
    if "freeToolCalls" in data:
        free = data["freeToolCalls"]
        print(f"\n🛠️  FREE TOOL CALLS")
        print(f"   💳 Limit: {free.get('limit', 'N/A')}")
        print(f"   📈 Used: {free.get('requests', 0)}")
        print(f"   🔄 Renews: {format_date(free.get('renewsAt', 'N/A'))}")
    
    print("\n" + "="*60)
    print("✓ All data retrieved successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
