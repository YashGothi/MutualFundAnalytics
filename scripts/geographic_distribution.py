import pandas as pd
import plotly.express as px

df = pd.read_csv("data/processed/clean_investor_transactions.csv")

sip = df[
    df["transaction_type"].str.upper() == "SIP"
]

# State-wise SIP Amount
state_sip = (
    sip.groupby("state")["amount_inr"]
       .sum()
       .reset_index()
       .sort_values("amount_inr")
)

fig = px.bar(
    state_sip,
    x="amount_inr",
    y="state",
    orientation="h",
    title="SIP Amount by State"
)

fig.show()

# T30 vs B30 Pie Chart
tier_dist = (
    sip.groupby("city_tier")["amount_inr"]
       .sum()
       .reset_index()
)

fig = px.pie(
    tier_dist,
    names="city_tier",
    values="amount_inr",
    title="T30 vs B30 SIP Contribution"
)

fig.show()