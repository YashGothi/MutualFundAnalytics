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

df = pd.read_csv("data/processed/clean_investor_transactions.csv")

# Age Group Distribution
age_dist = (
    df["age_group"]
    .value_counts()
    .reset_index()
)

age_dist.columns = ["age_group", "count"]

fig = px.pie(
    age_dist,
    names="age_group",
    values="count",
    title="Investor Age Group Distribution"
)

fig.show()

# Gender Split
gender_dist = (
    df["gender"]
    .value_counts()
    .reset_index()
)

gender_dist.columns = ["gender", "count"]

fig = px.pie(
    gender_dist,
    names="gender",
    values="count",
    title="Investor Gender Distribution"
)

fig.show()

# SIP Box Plot by Age Group
sip = df[
    df["transaction_type"].str.upper() == "SIP"
]

fig = px.box(
    sip,
    x="age_group",
    y="amount_inr",
    title="SIP Amount Distribution by Age Group"
)

fig.show()