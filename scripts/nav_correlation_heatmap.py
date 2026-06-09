import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned NAV data
nav = pd.read_csv("data/processed/clean_nav_history.csv")

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Select 10 funds
selected_funds = nav["amfi_code"].unique()[:10]

nav = nav[
    nav["amfi_code"].isin(selected_funds)
]

# Create matrix
nav_matrix = nav.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

# Calculate daily returns
daily_returns = nav_matrix.pct_change()

# Correlation matrix
corr_matrix = daily_returns.corr()

# Plot
plt.figure(figsize=(12, 10))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f",
    linewidths=0.5
)

plt.title(
    "Correlation Matrix of Daily NAV Returns (10 Selected Funds)",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()
plt.show()