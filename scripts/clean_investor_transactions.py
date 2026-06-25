"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/08_investor_transactions.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "clean_investor_transactions.csv"

VALID_TRANSACTION_TYPES = ["SIP", "Lumpsum", "Redemption"]
VALID_KYC_STATUSES = ["Verified", "Pending"]

def clean_investor_transactions():
    df = pd.read_csv(RAW_FILE)

    print("Original Shape:", df.shape)

    df.columns = df.columns.str.strip().str.lower()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "sip": "SIP",
            "s.i.p": "SIP",
            "lumpsum": "Lumpsum",
            "lump sum": "Lumpsum",
            "lump_sum": "Lumpsum",
            "redemption": "Redemption",
            "redeem": "Redemption",
            "withdrawal": "Redemption"
        })
    )

    df["kyc_status"] = (
        df["kyc_status"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")

    invalid_dates = df["transaction_date"].isna().sum()
    invalid_amounts = (df["amount_inr"].isna() | (df["amount_inr"] <= 0)).sum()
    invalid_transaction_types = ~df["transaction_type"].isin(VALID_TRANSACTION_TYPES)
    invalid_kyc_statuses = ~df["kyc_status"].isin(VALID_KYC_STATUSES)

    duplicate_rows = df.duplicated().sum()

    print("\nValidation Summary")
    print("-" * 50)
    print(f"Invalid dates: {invalid_dates}")
    print(f"Invalid amount rows: {invalid_amounts}")
    print(f"Invalid transaction_type rows: {invalid_transaction_types.sum()}")
    print(f"Invalid KYC status rows: {invalid_kyc_statuses.sum()}")
    print(f"Duplicate rows: {duplicate_rows}")

    df = df.dropna(subset=["transaction_date"])
    df = df[df["amount_inr"] > 0]
    df = df[df["transaction_type"].isin(VALID_TRANSACTION_TYPES)]
    df = df[df["kyc_status"].isin(VALID_KYC_STATUSES)]
    df = df.drop_duplicates()

    df = df.sort_values(by=["investor_id", "transaction_date"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCleaning Complete")
    print("-" * 50)
    print(f"Final Shape: {df.shape}")
    print(f"Saved cleaned file to: {OUTPUT_FILE}")

    print("\nTransaction Type Counts:")
    print(df["transaction_type"].value_counts())

    print("\nKYC Status Counts:")
    print(df["kyc_status"].value_counts())

    print("\nFirst 5 rows:")
    print(df.head())

if __name__ == "__main__":
    clean_investor_transactions()