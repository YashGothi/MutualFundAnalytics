"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd
import plotly.express as px

# Load data
folio = pd.read_csv("data/raw/06_industry_folio_count.csv")

# Convert month column
folio["month"] = pd.to_datetime(folio["month"])

# Create line chart
fig = px.line(
    folio,
    x="month",
    y="total_folios_crore",
    markers=True,
    title="Mutual Fund Folio Count Growth (2022–2025)"
)

# Starting point
fig.add_annotation(
    x="2022-01-01",
    y=13.26,
    text="13.26 Cr",
    showarrow=True,
    ax=-40,
    ay=-40
)

# 15 Cr milestone
fig.add_annotation(
    x="2023-01-01",
    y=14.81,
    text="~15 Cr",
    showarrow=True,
    ax=40,
    ay=-40
)

# 20 Cr milestone
fig.add_annotation(
    x="2024-07-01",
    y=20.40,
    text="20 Cr+",
    showarrow=True,
    ax=40,
    ay=-40
)

# Final milestone
fig.add_annotation(
    x="2025-10-01",
    y=26.12,
    text="26.12 Cr",
    showarrow=True,
    ax=-70,
    ay=-60
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Folios (Crores)",
    template="plotly_white"
)

fig.show()