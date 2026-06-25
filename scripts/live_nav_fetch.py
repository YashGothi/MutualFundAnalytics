"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

from pathlib import Path
import requests
import pandas as pd


URL = "https://api.mfapi.in/mf/125497"
OUTPUT_DIR = Path("data/raw")
OUTPUT_FILE = OUTPUT_DIR / "hdfc_top_100_live_nav.csv"

def fetch_live_nav():
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return

    json_data = response.json()

    print("\n===== API META DATA =====")
    print(json_data["meta"])

    meta = json_data.get("meta", {})
    nav_data = json_data.get("data", [])

    df = pd.DataFrame(nav_data)

    df["scheme_code"] = meta.get("scheme_code")
    df["scheme_name"] = meta.get("scheme_name")
    df["fund_house"] = meta.get("fund_house")
    df["scheme_category"] = meta.get("scheme_category")

    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("Live NAV data fetched successfully.")
    print(f"Saved to: {OUTPUT_FILE}")
    print("\nShape:")
    print(df.shape)
    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    fetch_live_nav()

