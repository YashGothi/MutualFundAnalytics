import pandas as pd
import plotly.express as px

# Load portfolio holdings data
portfolio = pd.read_csv("data/raw/09_portfolio_holdings.csv")

# Aggregate sector weights across all funds
sector_weights = (
    portfolio.groupby("sector")["weight_pct"]
    .sum()
    .reset_index()
    .sort_values("weight_pct", ascending=False)
)

# Create donut chart
fig = px.pie(
    sector_weights,
    names="sector",
    values="weight_pct",
    hole=0.5,
    title="Sector Allocation Across Equity Funds"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    template="plotly_white"
)

fig.show()