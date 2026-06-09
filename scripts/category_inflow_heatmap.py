import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/05_category_inflows.csv")

# Create pivot table
heatmap_data = df.pivot_table(
    index="category",
    columns="month",
    values="net_inflow_cr",
    aggfunc="sum"
)

plt.figure(figsize=(16,8))

sns.heatmap(
    heatmap_data,
    cmap="YlGnBu",
    annot=False,
    linewidths=0.5
)

plt.title(
    "Category-wise Monthly Net Inflows",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Fund Category")

plt.tight_layout()
plt.show()