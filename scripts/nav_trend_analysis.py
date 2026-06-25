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

# Load NAV data
nav = pd.read_csv("nav_history.csv")

# Check columns
print(nav.columns)

# Convert date column
nav["date"] = pd.to_datetime(nav["date"])

# Keep data from 2022 to 2026
nav = nav[
    (nav["date"] >= "2022-01-01") &
    (nav["date"] <= "2026-12-31")
]

# Sort data
nav = nav.sort_values(["scheme_name", "date"])

# Plot daily NAV for all schemes
fig = px.line(
    nav,
    x="date",
    y="nav",
    color="scheme_name",
    title="Daily NAV Trend Analysis for 40 Schemes (2022–2026)",
    labels={
        "date": "Date",
        "nav": "NAV",
        "scheme_name": "Scheme Name"
    }
)

# Highlight 2023 bull run
fig.add_vrect(
    x0="2023-04-01",
    x1="2023-12-31",
    fillcolor="green",
    opacity=0.15,
    line_width=0,
    annotation_text="2023 Bull Run",
    annotation_position="top left"
)

# Highlight 2024 market correction
fig.add_vrect(
    x0="2024-06-01",
    x1="2024-06-30",
    fillcolor="red",
    opacity=0.15,
    line_width=0,
    annotation_text="2024 Market Correction",
    annotation_position="top left"
)

# Improve layout
fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    height=750,
    legend_title_text="Scheme Name"
)

# Show chart in browser
fig.show()

# Save chart as HTML
fig.write_html("nav_trend_analysis.html")

print("Chart created successfully: nav_trend_analysis.html")
