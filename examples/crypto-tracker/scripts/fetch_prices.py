#!/usr/bin/env python3
"""
Fetch cryptocurrency prices from public API
Real-world example: Download live crypto data
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError


def fetch_crypto_price(symbol: str) -> dict:
    """Fetch current price for a cryptocurrency."""
    url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "symbol": symbol,
                "price": float(data["data"]["amount"]),
                "currency": data["data"]["currency"],
                "timestamp": datetime.now().isoformat()
            }
    except URLError as e:
        print(f"Error fetching {symbol}: {e}", file=sys.stderr)
        return None


def main():
    # Fetch prices for multiple cryptocurrencies
    symbols = ["BTC", "ETH", "SOL", "ADA", "DOT"]

    print(f"Fetching prices for {len(symbols)} cryptocurrencies...")

    prices = []
    for symbol in symbols:
        print(f"  → Fetching {symbol}...")
        price_data = fetch_crypto_price(symbol)
        if price_data:
            prices.append(price_data)
            print(f"    ✓ {symbol}: ${price_data['price']:,.2f}")

    # Save to file
    output_file = Path("data/raw_prices.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump({
            "fetched_at": datetime.now().isoformat(),
            "count": len(prices),
            "prices": prices
        }, f, indent=2)

    print(f"\n✓ Saved {len(prices)} prices to {output_file}")


if __name__ == "__main__":
    main()
