# Synthetic Credits Monitor

Simple Python script to check Synthetic API subscription usage — no external dependencies.

## Installation

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
python3 synthetic_menubar.py
```

## Usage

1. Run the script
2. Enter your Synthetic API key
3. See your subscription usage

## API

**Endpoint:** `GET https://api.synthetic.new/v2/quotas`

**Authentication:** Bearer token

**Response format:**
```json
{
  "subscription": {
    "limit": 135,
    "requests": 0,
    "renewsAt": "2025-09-21T14:36:14.288Z"
  }
}
```

**Fields:**
- `subscription.limit` — Monthly request limit
- `subscription.requests` — Requests used this period
- `subscription.renewsAt` — Renewal timestamp

## Requirements

- Python 3.7+
- Synthetic API key

## No External Dependencies

Uses only Python standard library — no `pip install` needed.
