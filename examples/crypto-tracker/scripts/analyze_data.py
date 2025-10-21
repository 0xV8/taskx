#!/usr/bin/env python3
"""
Analyze cryptocurrency price data
Real-world example: Process and compute statistics
"""

import json
from pathlib import Path
from datetime import datetime


def calculate_statistics(prices: list) -> dict:
    """Calculate statistical insights from price data."""
    price_values = [p["price"] for p in prices]

    total_value = sum(price_values)
    avg_price = total_value / len(price_values)
    max_price = max(price_values)
    min_price = min(price_values)

    max_crypto = next(p for p in prices if p["price"] == max_price)
    min_crypto = next(p for p in prices if p["price"] == min_price)

    return {
        "total_cryptocurrencies": len(prices),
        "total_market_value": total_value,
        "average_price": avg_price,
        "highest": {
            "symbol": max_crypto["symbol"],
            "price": max_price
        },
        "lowest": {
            "symbol": min_crypto["symbol"],
            "price": min_price
        }
    }


def main():
    print("Analyzing cryptocurrency data...")

    # Load raw data
    input_file = Path("data/raw_prices.json")
    if not input_file.exists():
        print(f"Error: {input_file} not found. Run fetch_prices.py first.")
        return 1

    with open(input_file) as f:
        raw_data = json.load(f)

    prices = raw_data["prices"]
    print(f"  → Loaded {len(prices)} cryptocurrency prices")

    # Calculate statistics
    stats = calculate_statistics(prices)

    print(f"\n  Analysis Results:")
    print(f"  ─────────────────────────────────────────")
    print(f"  Total cryptocurrencies: {stats['total_cryptocurrencies']}")
    print(f"  Total market value: ${stats['total_market_value']:,.2f}")
    print(f"  Average price: ${stats['average_price']:,.2f}")
    print(f"  Highest: {stats['highest']['symbol']} (${stats['highest']['price']:,.2f})")
    print(f"  Lowest: {stats['lowest']['symbol']} (${stats['lowest']['price']:,.2f})")

    # Save analysis
    output_file = Path("data/analysis.json")
    with open(output_file, "w") as f:
        json.dump({
            "analyzed_at": datetime.now().isoformat(),
            "statistics": stats,
            "prices": prices
        }, f, indent=2)

    print(f"\n✓ Analysis saved to {output_file}")


if __name__ == "__main__":
    main()
