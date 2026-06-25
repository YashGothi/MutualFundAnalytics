"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd
from pathlib import Path

INPUT_FILE = "data/processed/clean_nav_history.csv"
OUTPUT_FILE = "data/processed/var_cvar_results.csv"


def calculate_var_cvar():
    """
    Calculate Historical Value-at-Risk (95%) and Conditional VaR
    for all mutual fund schemes using daily returns.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing VaR and CVaR metrics.
    """
 
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["amfi_code", "date"])

    df["daily_return"] = (
        df.groupby("amfi_code")["nav"]
        .pct_change()
    )

    results = []

    for amfi_code, group in df.groupby("amfi_code"):

        returns = group["daily_return"].dropna()

        if len(returns) < 30:
            continue

        # Historical VaR (95%)
        var_95 = returns.quantile(0.05)

        # CVaR (Expected Shortfall)
        cvar_95 = returns[returns <= var_95].mean()

        results.append({
            "amfi_code": amfi_code,
            "observations": len(returns),
            "mean_daily_return_pct": round(returns.mean() * 100, 4),
            "volatility_pct": round(returns.std() * 100, 4),
            "var_95_pct": round(var_95 * 100, 4),
            "cvar_95_pct": round(cvar_95 * 100, 4)
        })

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        by="var_95_pct"
    )

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 70)
    print("VaR / CVaR ANALYSIS")
    print("=" * 70)

    print("\nTotal Schemes Analyzed:")
    print(len(result_df))

    print("\nTop 10 Riskiest Schemes")
    print(
        result_df[
            [
                "amfi_code",
                "var_95_pct",
                "cvar_95_pct",
                "volatility_pct"
            ]
        ].head(10)
    )

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    calculate_var_cvar()