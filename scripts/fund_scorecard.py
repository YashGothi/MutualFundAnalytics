import pandas as pd

df = pd.read_csv(
    "data/processed/clean_scheme_performance.csv"
)

# Rank metrics (0-100 scale)

df["return_score"] = (
    df["return_3yr_pct"]
    .rank(pct=True) * 100
)

df["sharpe_score"] = (
    df["sharpe_ratio"]
    .rank(pct=True) * 100
)

df["alpha_score"] = (
    df["alpha"]
    .rank(pct=True) * 100
)

# Lower expense ratio = better
df["expense_score"] = (
    df["expense_ratio_pct"]
    .rank(ascending=False, pct=True) * 100
)

# Lower drawdown = better
df["drawdown_score"] = (
    df["max_drawdown_pct"]
    .abs()
    .rank(ascending=False, pct=True) * 100
)

# Composite Score
df["fund_score"] = (
      0.30 * df["return_score"]
    + 0.25 * df["sharpe_score"]
    + 0.20 * df["alpha_score"]
    + 0.15 * df["expense_score"]
    + 0.10 * df["drawdown_score"]
)

df["fund_score"] = df["fund_score"].round(2)

# Final Ranking
scorecard = df[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "fund_score"
    ]
].sort_values(
    "fund_score",
    ascending=False
)

print("\nTop 10 Funds\n")
print(scorecard.head(10))

scorecard.to_csv(
    "reports/fund_scorecard.csv",
    index=False
)

print("\nSaved: reports/fund_scorecard.csv")