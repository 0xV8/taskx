#!/usr/bin/env python3
"""
Validate cryptocurrency data quality
Real-world example: Data validation and quality checks
"""

import json
from pathlib import Path


def validate_price_data(data: dict) -> tuple[bool, list]:
    """Validate price data structure and values."""
    errors = []

    # Check required fields
    if "prices" not in data:
        errors.append("Missing 'prices' field")
        return False, errors

    prices = data["prices"]

    # Check each price entry
    for idx, price in enumerate(prices):
        if "symbol" not in price:
            errors.append(f"Entry {idx}: Missing symbol")

        if "price" not in price:
            errors.append(f"Entry {idx}: Missing price")
        elif price["price"] <= 0:
            errors.append(f"Entry {idx}: Invalid price {price['price']}")

        if "timestamp" not in price:
            errors.append(f"Entry {idx}: Missing timestamp")

    return len(errors) == 0, errors


def main():
    print("Validating cryptocurrency data...")

    # Load data
    input_file = Path("data/raw_prices.json")
    if not input_file.exists():
        print(f"✗ Error: {input_file} not found")
        return 1

    with open(input_file) as f:
        data = json.load(f)

    # Validate
    is_valid, errors = validate_price_data(data)

    if is_valid:
        print(f"✓ Validation passed!")
        print(f"  → {data['count']} entries validated")
        print(f"  → All required fields present")
        print(f"  → All prices are positive values")
        return 0
    else:
        print(f"✗ Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  → {error}")
        return 1


if __name__ == "__main__":
    exit(main())
