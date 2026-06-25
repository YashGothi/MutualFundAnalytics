"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd
from scipy.stats import linregress

nav = pd.read_csv("data/processed/clean_nav_history.csv")
nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

nav["fund_return"] = nav.groupby("amfi_code")["nav"].pct_change()

benchmark = pd.read_csv("data/raw/10_benchmark_indices.csv")
benchmark["date"] = pd.to_datetime(benchmark["date"])

benchmark = benchmark[benchmark["index_name"] == "NIFTY100"].copy()
benchmark = benchmark.sort_values("date")
benchmark["benchmark_return"] = benchmark["close_value"].pct_change()

benchmark = benchmark[["date", "benchmark_return"]]

results = []

for fund in nav["amfi_code"].unique():
    fund_data = nav[nav["amfi_code"] == fund][["date", "amfi_code", "fund_return"]]

    merged = pd.merge(fund_data, benchmark, on="date", how="inner").dropna()

    if len(merged) < 30:
        continue

    reg = linregress(
        merged["benchmark_return"],
        merged["fund_return"]
    )

    results.append({
        "amfi_code": fund,
        "alpha_annual": round(reg.intercept * 252, 4),
        "beta": round(reg.slope, 4),
        "r_squared": round(reg.rvalue ** 2, 4)
    })

alpha_beta_df = pd.DataFrame(results)
alpha_beta_df = alpha_beta_df.sort_values("alpha_annual", ascending=False)

alpha_beta_df.to_csv("reports/alpha_beta.csv", index=False)

print(alpha_beta_df.head(10))
print("Saved: reports/alpha_beta.csv")