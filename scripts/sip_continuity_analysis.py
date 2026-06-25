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

INPUT_FILE = "data/processed/clean_investor_transactions.csv"
OUTPUT_FILE = "data/processed/sip_continuity_analysis.csv"

def analyze_sip_continuity():

    df = pd.read_csv(INPUT_FILE)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    # Only SIP transactions
    sip_df = df[
        df["transaction_type"] == "SIP"
    ].copy()

    results = []

    for investor_id, group in sip_df.groupby("investor_id"):

        # Minimum 6 SIPs required
        if len(group) < 6:
            continue

        group = group.sort_values(
            "transaction_date"
        )

        group["gap_days"] = (
            group["transaction_date"]
            .diff()
            .dt.days
        )

        avg_gap = (
            group["gap_days"]
            .dropna()
            .mean()
        )

        max_gap = (
            group["gap_days"]
            .dropna()
            .max()
        )

        risk_status = (
            "At-Risk"
            if avg_gap > 35
            else "Healthy"
        )

        results.append({
            "investor_id": investor_id,
            "sip_count": len(group),
            "avg_gap_days": round(avg_gap, 2),
            "max_gap_days": max_gap,
            "risk_status": risk_status
        })

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        by="avg_gap_days",
        ascending=False
    )

    OUTPUT_FILE = Path(OUTPUT_FILE)
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 70)
    print("SIP CONTINUITY ANALYSIS")
    print("=" * 70)

    print("\nTotal Investors Analyzed:")
    print(len(result_df))

    print("\nRisk Status Summary:")
    print(
        result_df["risk_status"]
        .value_counts()
    )

    print("\nTop 10 Highest Gap Investors:")
    print(
        result_df.head(10)
    )

    print(
        f"\nResults saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    analyze_sip_continuity()