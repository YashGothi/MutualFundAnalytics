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

nav = pd.read_csv("data/processed/clean_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"].pct_change()
)

annual_rf = 0.065
daily_rf = annual_rf / 252

results = []

for fund in nav["amfi_code"].unique():

    returns = nav[
        nav["amfi_code"] == fund
    ]["daily_return"].dropna()

    if len(returns) < 30:
        continue

    avg_return = returns.mean()

    downside_returns = returns[returns < 0]

    if len(downside_returns) < 2:
        continue

    downside_std = downside_returns.std()

    sortino = (
        (avg_return - daily_rf)
        / downside_std
    ) * np.sqrt(252)

    results.append({
         "amfi_code": fund,
        "avg_daily_return": round(avg_return, 6),
        "downside_std": round(downside_std, 6),
        "sortino_ratio": round(sortino, 3)
    })

    sortino_df = pd.DataFrame(results)

sortino_df = sortino_df.sort_values(
    "sortino_ratio",
    ascending=False
)

print("\nTop 10 Funds by Sortino Ratio\n")
print(sortino_df.head(10))

# Export
sortino_df.to_csv(
    "reports/sortino_ratio_ranking.csv",
    index=False
)

print("\nSaved: reports/sortino_ratio_ranking.csv")