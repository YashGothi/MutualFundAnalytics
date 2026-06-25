"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd

FUND_FILE = "data/raw/01_fund_master.csv"
PERFORMANCE_FILE = "data/processed/clean_scheme_performance.csv"

def recommend_funds(risk_appetite):

    funds = pd.read_csv(FUND_FILE)
    performance = pd.read_csv(PERFORMANCE_FILE)

    funds.columns = funds.columns.str.lower()
    performance.columns = performance.columns.str.lower()

    df = funds.merge(
        performance,
        on="amfi_code",
        how="inner"
    )

    print("\nColumns after merge:")
    print(df.columns.tolist())

    risk_mapping = {
        "low": ["low"],
        "moderate": ["moderate"],
        "high": ["high", "very high"]
    }

    risk_values = risk_mapping.get(
        risk_appetite.lower(),
        []
    )

    recommendations = df[
        df["risk_category"]
        .str.lower()
        .isin(risk_values)
    ].copy()

    recommendations = recommendations.sort_values(
        by="sharpe_ratio",
        ascending=False
    )

    recommendations = recommendations[
    [
        "amfi_code",
        "scheme_name_x",
        "fund_house_x",
        "risk_category",
        "sharpe_ratio",
        "return_3yr_pct",
        "expense_ratio_pct_x"
    ]
].head(3)
    
    recommendations = recommendations.rename(
    columns={
        "scheme_name_x": "scheme_name",
        "fund_house_x": "fund_house",
        "expense_ratio_pct_x": "expense_ratio_pct"
    }
)

    print("\n" + "=" * 80)
    print(f"TOP 3 RECOMMENDED FUNDS ({risk_appetite.upper()} RISK)")
    print("=" * 80)

    if recommendations.empty:
        print("No matching funds found.")
        return

    print(recommendations.to_string(index=False))


if __name__ == "__main__":

    print("\nRisk Options:")
    print("1. Low")
    print("2. Moderate")
    print("3. High")

    risk = input("\nEnter Risk Appetite: ")

    recommend_funds(risk)