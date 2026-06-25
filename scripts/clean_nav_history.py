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

RAW_FILE = Path("data/raw/02_nav_history.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "clean_nav_history.csv"

def clean_nav_history():
    df = pd.read_csv(RAW_FILE)

    print("Original Shape:", df.shape)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Parse date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert NAV to numeric
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    # Convert AMFI code to string
    df["amfi_code"] = df["amfi_code"].astype(str)

    # Remove rows with invalid dates or missing AMFI codes
    df = df.dropna(subset=["date", "amfi_code"])

    # Remove duplicate records
    before_duplicates = df.shape[0]
    df = df.drop_duplicates(subset=["amfi_code", "date"])
    duplicates_removed = before_duplicates - df.shape[0]

    # Sort by AMFI code and date
    df = df.sort_values(by=["amfi_code", "date"])

    # Validate NAV > 0
    invalid_nav_count = (df["nav"] <= 0).sum()
    df = df[df["nav"] > 0]

    # Forward-fill missing NAV values within each fund
    df["nav"] = df.groupby("amfi_code")["nav"].ffill()

    # Final checks
    missing_nav_count = df["nav"].isna().sum()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCleaning Summary")
    print("-" * 50)
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Invalid NAV rows removed: {invalid_nav_count}")
    print(f"Missing NAV values after forward-fill: {missing_nav_count}")
    print(f"Final Shape: {df.shape}")
    print(f"Saved cleaned file to: {OUTPUT_FILE}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)


if __name__ == "__main__":
    clean_nav_history()