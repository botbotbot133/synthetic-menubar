# Synthetic Credits Monitor

Simple Python script to check Synthetic API credits — no external dependencies.

## Installation

```bash
git clone https://github.com/botbotbot133/synthetic-menubar.git
cd synthetic-menubar
python3 synthetic_menubar.py
```

## Usage

1. Run the script
2. Enter your Synthetic API key
3. See your credits!

## API Endpoint

Uses: `GET https://api.synthetic.new/v2/quotas`

Returns:
- `credits_remaining` — Available credits
- `credits_used_today` — Today's usage
- `monthly_limit` — Monthly limit

## Requirements

- Python 3.7+
- Synthetic API key

## No Dependencies!

Just Python standard library — no `pip install` needed.
