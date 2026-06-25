"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/sector_hhi_analysis.csv"
)

top10 = df.head(10)

plt.figure(figsize=(10,6))
plt.bar(top10["amfi_code"], top10["hhi"])
plt.title("Top 10 Most Concentrated Funds")
plt.ylabel("HHI")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(
    "reports/hhi_concentration_chart.png"
)

plt.show()