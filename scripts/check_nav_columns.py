import pandas as pd

nav = pd.read_csv("data/processed/clean_nav_history.csv")

print(nav.columns.tolist())
print(nav.head())