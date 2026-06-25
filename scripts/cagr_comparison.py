"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd
import numpy as np

# Load NAV data
nav = pd.read_csv("data/processed/clean_nav_history.csv")

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Sort
nav = nav.sort_values(["amfi_code", "date"])

# Latest date in dataset
latest_date = nav["date"].max()

print("Latest NAV Date:", latest_date)

results = []

for fund in nav["amfi_code"].unique():

    fund_data = nav[nav["amfi_code"] == fund].sort_values("date")

    latest_nav = fund_data.iloc[-1]["nav"]

    fund_result = {
        "amfi_code": fund
    }

    for years in [1, 3, 5]:

        target_date = latest_date - pd.DateOffset(years=years)

        historical = fund_data[
            fund_data["date"] <= target_date
        ]

        if len(historical) > 0:

            start_nav = historical.iloc[-1]["nav"]

            cagr = (
                (latest_nav / start_nav) ** (1 / years)
                - 1
            ) * 100

            fund_result[f"{years}Y_CAGR_%"] = round(cagr, 2)

        else:
            fund_result[f"{years}Y_CAGR_%"] = np.nan

    results.append(fund_result)

# Create comparison table
cagr_df = pd.DataFrame(results)

# Sort by 3Y CAGR
cagr_df = cagr_df.sort_values(
    "3Y_CAGR_%",
    ascending=False
)

print(cagr_df.head(10))

# Save report
cagr_df.to_csv(
    "reports/cagr_comparison_table.csv",
    index=False
)

print("\nSaved: reports/cagr_comparison_table.csv")