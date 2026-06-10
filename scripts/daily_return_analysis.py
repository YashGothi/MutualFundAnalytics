import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load NAV history
nav = pd.read_csv("data/processed/clean_nav_history.csv")

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Sort data
nav = nav.sort_values(["amfi_code", "date"])

# Compute daily returns
nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
       .pct_change()
)

# Remove first NaN return for each scheme
returns = nav["daily_return"].dropna()

# Summary statistics
print("\nDaily Return Summary")
print(returns.describe())

# Check extreme values
print("\nMinimum Return:", returns.min())
print("Maximum Return:", returns.max())

# Distribution Plot
plt.figure(figsize=(10,6))

sns.histplot(
    returns,
    bins=100,
    kde=True
)

plt.title("Distribution of Daily Returns Across All Schemes")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()