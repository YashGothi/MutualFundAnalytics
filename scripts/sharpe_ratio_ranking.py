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

# Prepare data
nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

# Daily returns
nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
       .pct_change()
)

# Annual repo rate proxy
risk_free_rate = 0.065

# Daily risk-free rate
daily_rf = risk_free_rate / 252

results = []

for fund in nav["amfi_code"].unique():

    fund_returns = nav[
        nav["amfi_code"] == fund
    ]["daily_return"].dropna()

    if len(fund_returns) < 30:
        continue

    mean_return = fund_returns.mean()
    std_return = fund_returns.std()

    sharpe = (
        (mean_return - daily_rf)
        / std_return
    ) * np.sqrt(252)

    results.append({
        "amfi_code": fund,
        "avg_daily_return": round(mean_return, 6),
        "volatility": round(std_return, 6),
        "sharpe_ratio": round(sharpe, 3)
    })

# Ranking
sharpe_df = pd.DataFrame(results)

sharpe_df = sharpe_df.sort_values(
    "sharpe_ratio",
    ascending=False
)

print("\nTop 10 Funds by Sharpe Ratio\n")
print(sharpe_df.head(10))

# Export
sharpe_df.to_csv(
    "reports/sharpe_ratio_ranking.csv",
    index=False
)

print("\nSaved: reports/sharpe_ratio_ranking.csv")