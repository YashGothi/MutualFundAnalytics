"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd

df = pd.read_csv("data/raw/09_portfolio_holdings.csv")

print("Columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
# print(df.head())