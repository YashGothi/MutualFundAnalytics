"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

import pandas as pd
import plotly.graph_objects as go

nav = pd.read_csv("data/processed/clean_nav_history.csv")
nav["date"] = pd.to_datetime(nav["date"])

scorecard = pd.read_csv("reports/fund_scorecard.csv")
scheme_lookup = pd.read_csv(
    "data/processed/clean_scheme_performance.csv"
)[["amfi_code", "scheme_name"]]

top5 = scorecard.head(5)["amfi_code"].tolist()

benchmark = pd.read_csv("data/raw/10_benchmark_indices.csv")
benchmark["date"] = pd.to_datetime(benchmark["date"])

latest_date = nav["date"].max()
start_date = latest_date - pd.DateOffset(years=3)

nav = nav[nav["date"] >= start_date]

nifty50 = benchmark[
    (benchmark["index_name"] == "NIFTY50") &
    (benchmark["date"] >= start_date)
].copy()

nifty100 = benchmark[
    (benchmark["index_name"] == "NIFTY100") &
    (benchmark["date"] >= start_date)
].copy()

fig = go.Figure()



for fund in top5:

    fund_data = nav[
        nav["amfi_code"] == fund
    ].sort_values("date")

    base = fund_data["nav"].iloc[0]

    fund_data["normalized"] = (
        fund_data["nav"] / base
    ) * 100

    scheme_name = scheme_lookup.loc[
        scheme_lookup["amfi_code"] == fund,
        "scheme_name"
    ].iloc[0]

    fig.add_trace(
        go.Scatter(
            x=fund_data["date"],
            y=fund_data["normalized"],
            name=scheme_name
        )
    )

nifty50["normalized"] = nifty50["close_value"] / nifty50["close_value"].iloc[0] * 100
nifty100["normalized"] = nifty100["close_value"] / nifty100["close_value"].iloc[0] * 100

fig.add_trace(
    go.Scatter(
        x=nifty50["date"],
        y=nifty50["normalized"],
        mode="lines",
        name="NIFTY50"
    )
)

fig.add_trace(
    go.Scatter(
        x=nifty100["date"],
        y=nifty100["normalized"],
        mode="lines",
        name="NIFTY100"
    )
)

fig.update_layout(
    title="Top 5 Funds vs NIFTY50 and NIFTY100",
    xaxis_title="Date",
    yaxis_title="Normalized Value (Base = 100)",
    template="plotly_white"
)

fig.write_image("reports/benchmark_comparison_chart.png")
fig.show()

print("Saved: reports/benchmark_comparison_chart.png")