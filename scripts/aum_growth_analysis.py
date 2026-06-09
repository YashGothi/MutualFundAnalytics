import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
aum = pd.read_csv("aum_data.csv")

# Keep required years
aum = aum[aum["year"].isin([2022, 2023, 2024, 2025])]

# Create grouped bar chart
plt.figure(figsize=(16, 8))

ax = sns.barplot(
    data=aum,
    x="fund_house",
    y="aum_cr",
    hue="year"
)

# Rotate labels
plt.xticks(rotation=45, ha="right")

# Highlight SBI dominance
sbi_2025 = aum[
    (aum["fund_house"] == "SBI Mutual Fund") &
    (aum["year"] == 2025)
]

if not sbi_2025.empty:
    value = sbi_2025["aum_cr"].iloc[0]

    plt.annotate(
        "SBI Dominance\n₹12.5L Cr",
        xy=("SBI Mutual Fund", value),
        xytext=(2, value * 1.1),
        arrowprops=dict(arrowstyle="->"),
        fontsize=11,
        fontweight="bold"
    )

plt.title(
    "AUM Growth by Fund House (2022–2025)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Fund House")
plt.ylabel("AUM (₹ Crores)")
plt.legend(title="Year")
plt.tight_layout()

plt.show()