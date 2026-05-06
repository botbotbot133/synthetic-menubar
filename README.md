# Synthetic Credits Monitor

Simple Python script to check all Synthetic API usage metrics — no external dependencies.

## Installation

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
python3 synthetic_menubar.py
```

## Usage

1. Run: `python3 synthetic_menubar.py`
2. Enter your API key
3. See complete usage data

## Displays

- **Monthly Requests** — Total limit and usage
- **Search (Hourly)** — Search request limits
- **Weekly Token Limit** — 💰 Dollar credits (`$34.89` remaining of `$48.00`)
- **Rolling 5-Hour Limit** — Current rate limit status
- **Free Tool Calls** — Free tier usage

## API

**Endpoint:** `GET https://api.synthetic.new/v2/quotas`

**No dependencies** — Uses only Python standard library.

## Sample Output

```
📄 COMPLETE API RESPONSE (RAW JSON):
{ "subscription": {...}, "search": {...}, ... }

📊 PARSED SUBSCRIPTION DATA

💰 WEEKLY TOKEN LIMIT (Credits in $)
   💵 Max Credits: $48.00
   💵 Remaining: $34.89
   📊 Percent: 72.7%
```
