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
OUTPUT_FILE = "data/processed/investor_cohort_analysis.csv"


def investor_cohort_analysis():

    df = pd.read_csv(INPUT_FILE)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    # ------------------------------------------------
    # First transaction date for each investor
    # ------------------------------------------------

    first_txn = (
        df.groupby("investor_id")["transaction_date"]
        .min()
        .reset_index()
    )

    first_txn["cohort_year"] = (
        first_txn["transaction_date"]
        .dt.year
    )

    # Merge cohort back
    df = df.merge(
        first_txn[
            ["investor_id", "cohort_year"]
        ],
        on="investor_id",
        how="left"
    )

    # ------------------------------------------------
    # SIP only analysis
    # ------------------------------------------------

    sip_df = df[
        df["transaction_type"] == "SIP"
    ]

    # Average SIP amount
    avg_sip = (
        sip_df
        .groupby("cohort_year")["amount_inr"]
        .mean()
        .reset_index(name="avg_sip_amount")
    )

    # Total invested
    total_invested = (
        df
        .groupby("cohort_year")["amount_inr"]
        .sum()
        .reset_index(name="total_invested")
    )

    # Top fund preference
    top_funds = (
        df.groupby(
            ["cohort_year", "amfi_code"]
        )
        .size()
        .reset_index(name="transaction_count")
    )

    top_funds = (
        top_funds
        .sort_values(
            ["cohort_year", "transaction_count"],
            ascending=[True, False]
        )
        .groupby("cohort_year")
        .head(1)
    )

    # Combine results
    cohort_summary = (
        avg_sip
        .merge(
            total_invested,
            on="cohort_year"
        )
        .merge(
            top_funds[
                [
                    "cohort_year",
                    "amfi_code",
                    "transaction_count"
                ]
            ],
            on="cohort_year"
        )
    )

    cohort_summary.rename(
        columns={
            "amfi_code": "top_fund"
        },
        inplace=True
    )

    cohort_summary.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 70)
    print("INVESTOR COHORT ANALYSIS")
    print("=" * 70)

    print(cohort_summary)

    print(
        f"\nResults saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    investor_cohort_analysis()