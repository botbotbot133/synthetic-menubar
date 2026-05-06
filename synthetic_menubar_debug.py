#!/usr/bin/env python3
"""
Synthetic Credits Monitor - DEBUG VERSION
Shows full error details
"""

import urllib.request
import urllib.error
import json
import os

CONFIG_FILE = os.path.expanduser("~/.synthetic_menubar_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"api_key": ""}

def test_endpoint(url, api_key):
    """Test an endpoint with full debugging"""
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        },
        method='GET'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return {
                "status": response.status,
                "headers": dict(response.headers),
                "data": json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        return {
            "error": True,
            "status": e.code,
            "body": e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        }
    except Exception as e:
        return {
            "error": True,
            "exception": str(e)
        }

if __name__ == "__main__":
    # Load API key
    api_key = input("API Key (or press Enter to load from config): ").strip()
    if not api_key:
        config = load_config()
        api_key = config.get("api_key", "")
        if api_key:
            print(f"Loaded from config: {api_key[:10]}...")
    
    if not api_key:
        print("No API key!")
        exit(1)
    
    # Test various endpoints
    endpoints = [
        "https://api.synthetic.new/openai/v1/quotas",
        "https://api.synthetic.new/v1/quotas",
        "https://api.synthetic.new/v1/usage",
    ]
    
    print("\n" + "="*70)
    print("DEBUG: Testing API Endpoints")
    print("="*70 + "\n")
    
    for url in endpoints:
        print(f"\nTesting: {url}")
        result = test_endpoint(url, api_key)
        
        if "error" in result:
            print(f"  ❌ FAILED")
            print(f"     Status: {result.get('status', 'N/A')}")
            print(f"     Body: {result.get('body', result.get('exception', 'Unknown'))[:200]}")
        else:
            print(f"  ✅ SUCCESS!")
            print(f"     Status: {result['status']}")
            print(f"     Data: {json.dumps(result['data'], indent=2)[:500]}...")
    
    print("\n" + "="*70)
    
    # Also test if the key works with chat completions
    print("\n\nTesting /models endpoint:")
    models_result = test_endpoint("https://api.synthetic.new/openai/v1/models", api_key)
    if "error" not in models_result:
        print("✅ API Key is valid!")
        print(f"Found {len(models_result['data'].get('data', []))} models")
    else:
        print(f"❌ API Key test failed: {models_result}")
