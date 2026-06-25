"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd

# Load NAV data
nav = pd.read_csv("data/processed/clean_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

results = []

for fund in nav["amfi_code"].unique():
    fund_data = nav[nav["amfi_code"] == fund].copy()
    fund_data = fund_data.sort_values("date")

    # Running max NAV
    fund_data["running_max"] = fund_data["nav"].cummax()

    # Drawdown
    fund_data["drawdown"] = (
        fund_data["nav"] / fund_data["running_max"]
    ) - 1

    # Worst drawdown row
    trough_row = fund_data.loc[fund_data["drawdown"].idxmin()]

    trough_date = trough_row["date"]
    max_drawdown = trough_row["drawdown"]

    # Peak date before trough
    peak_data = fund_data[
        fund_data["date"] <= trough_date
    ]

    peak_row = peak_data.loc[
        peak_data["nav"].idxmax()
    ]

    peak_date = peak_row["date"]

    results.append({
        "amfi_code": fund,
        "max_drawdown_%": round(max_drawdown * 100, 2),
        "peak_date": peak_date.date(),
        "trough_date": trough_date.date(),
        "peak_nav": round(peak_row["nav"], 2),
        "trough_nav": round(trough_row["nav"], 2)
    })

drawdown_df = pd.DataFrame(results)

# Worst drawdowns first
drawdown_df = drawdown_df.sort_values(
    "max_drawdown_%"
)

print("\nWorst 10 Funds by Maximum Drawdown\n")
print(drawdown_df.head(10))

drawdown_df.to_csv(
    "reports/max_drawdown_analysis.csv",
    index=False
)

print("\nSaved: reports/max_drawdown_analysis.csv")