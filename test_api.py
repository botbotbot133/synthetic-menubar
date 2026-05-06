#!/usr/bin/env python3
"""Test different API endpoints to find the correct one"""

import urllib.request
import urllib.error
import json
import sys

API_KEY = input("Enter your API key: ").strip()
BASE_URL = "https://api.synthetic.new"

# Test different endpoints
endpoints = [
    "/openai/v1/quotas",
    "/v1/quotas", 
    "/v1/usage",
    "/v1/billing/usage",
    "/v1/user",
    "/v1/account"
]

print("\n" + "="*60)
print("Testing Synthetic API Endpoints")
print("="*60 + "\n")

for endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing: {endpoint}")
    
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        },
        method='GET'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"  ✅ SUCCESS!")
            print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
            print(f"\n  ✨ CORRECT ENDPOINT: {endpoint}")
            break
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP {e.code}")
    except urllib.error.URLError as e:
        print(f"  ❌ {e.reason}")
    except Exception as e:
        print(f"  ❌ {str(e)}")
    print()

print("="*60)
print("Test complete!")
