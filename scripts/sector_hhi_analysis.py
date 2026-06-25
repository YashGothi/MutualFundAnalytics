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

INPUT_FILE = "data/raw/09_portfolio_holdings.csv"
OUTPUT_FILE = "data/processed/sector_hhi_analysis.csv"


def calculate_hhi():

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df["weight_pct"] = pd.to_numeric(
        df["weight_pct"],
        errors="coerce"
    )

    # Convert to decimal
    df["weight"] = df["weight_pct"] / 100

    # Aggregate stock weights into sector weights
    sector_weights = (
        df.groupby(
            ["amfi_code", "sector"]
        )["weight"]
        .sum()
        .reset_index()
    )

    # Calculate HHI
    hhi = (
        sector_weights
        .groupby("amfi_code")["weight"]
        .apply(lambda x: (x ** 2).sum())
        .reset_index(name="hhi")
    )

    # Classification
    def classify(x):

        if x < 0.15:
            return "Highly Diversified"

        elif x < 0.25:
            return "Moderately Concentrated"

        else:
            return "Highly Concentrated"

    hhi["concentration_level"] = hhi["hhi"].apply(classify)

    hhi = hhi.sort_values(
        by="hhi",
        ascending=False
    )

    Path("data/processed").mkdir(
        parents=True,
        exist_ok=True
    )

    hhi.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nTop 10 Most Concentrated Funds")
    print(hhi.head(10))

    print("\nTop 10 Most Diversified Funds")
    print(hhi.tail(10))

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    calculate_hhi()