#!/usr/bin/env python3
"""
Generate HTML report from analysis
Real-world example: Create visual reports
"""

import json
from pathlib import Path
from datetime import datetime


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cryptocurrency Price Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }}
        .crypto-table {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f9f9f9;
        }}
        .price {{
            font-weight: bold;
            color: #10b981;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
            margin-top: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Cryptocurrency Price Report</h1>
        <p>Live market data analysis</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-label">Total Cryptocurrencies</div>
            <div class="stat-value">{total_crypto}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Market Value</div>
            <div class="stat-value">${total_value:,.2f}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Average Price</div>
            <div class="stat-value">${avg_price:,.2f}</div>
        </div>
    </div>

    <div class="crypto-table">
        <table>
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Price (USD)</th>
                    <th>Last Updated</th>
                </tr>
            </thead>
            <tbody>
                {price_rows}
            </tbody>
        </table>
    </div>

    <div class="timestamp">
        Generated at {generated_at}
    </div>
</body>
</html>
"""


def main():
    print("Generating cryptocurrency report...")

    # Load analysis data
    input_file = Path("data/analysis.json")
    if not input_file.exists():
        print(f"Error: {input_file} not found. Run analyze_data.py first.")
        return 1

    with open(input_file) as f:
        data = json.load(f)

    stats = data["statistics"]
    prices = data["prices"]

    # Generate price rows
    price_rows = ""
    for p in sorted(prices, key=lambda x: x["price"], reverse=True):
        price_rows += f"""
                <tr>
                    <td><strong>{p['symbol']}</strong></td>
                    <td class="price">${p['price']:,.2f}</td>
                    <td>{p['timestamp']}</td>
                </tr>"""

    # Generate HTML
    html = HTML_TEMPLATE.format(
        total_crypto=stats["total_cryptocurrencies"],
        total_value=stats["total_market_value"],
        avg_price=stats["average_price"],
        price_rows=price_rows,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Save report
    output_file = Path("reports/crypto_report.html")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        f.write(html)

    print(f"✓ Report generated: {output_file.absolute()}")
    print(f"\nOpen the report in your browser:")
    print(f"  open {output_file.absolute()}")


if __name__ == "__main__":
    main()
