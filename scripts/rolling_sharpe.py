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
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE = "data/processed/clean_nav_history.csv"

KEY_FUNDS = [
    "119551",  # SBI Bluechip
    "120503",  # ICICI Bluechip
    "118632",  # Nippon Large Cap
    "119092",  # Axis Bluechip
    "120841"   # Kotak Bluechip
]


def calculate_rolling_sharpe():

    df = pd.read_csv(INPUT_FILE)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["amfi_code", "date"])

    plt.figure(figsize=(14, 7))

    for fund in KEY_FUNDS:

        fund_df = df[df["amfi_code"].astype(str) == fund].copy()

        if fund_df.empty:
            print(f"Fund not found: {fund}")
            continue

        fund_df["daily_return"] = (
            fund_df["nav"]
            .pct_change()
        )

        rolling_mean = (
            fund_df["daily_return"]
            .rolling(90)
            .mean()
        )

        rolling_std = (
            fund_df["daily_return"]
            .rolling(90)
            .std()
        )

        fund_df["rolling_sharpe"] = (
            rolling_mean /
            rolling_std
        ) * np.sqrt(252)

        plt.plot(
            fund_df["date"],
            fund_df["rolling_sharpe"],
            label=fund
        )

    plt.title("90-Day Rolling Sharpe Ratio")
    plt.xlabel("Date")
    plt.ylabel("Sharpe Ratio")
    plt.legend()
    plt.grid(True)

    output_dir = Path("reports")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / "rolling_sharpe.png"

    plt.savefig(
        output_file,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved to: {output_file}")


if __name__ == "__main__":
    calculate_rolling_sharpe()