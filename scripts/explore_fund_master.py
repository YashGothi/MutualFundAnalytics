import pandas as pd
df = pd.read_csv("data/raw/01_fund_master.csv")

print("=" * 70)
print("FUND MASTER EXPLORATION REPORT")
print("=" * 70)

print("\n1. Dataset Shape")
print(df.shape)

print("\n2. Columns")
print(df.columns.tolist())

print("\n3. First 5 Rows")
print(df.head())

print("\n4. Unique Fund Houses")
print(df["fund_house"].dropna().unique())

print("\n5. Unique Categories")
print(df["category"].dropna().unique())

print("\n6. Unique Sub-Categories")
print(df["sub_category"].dropna().unique())

print("\n7. Unique Risk Grades / Risk Categories")
risk_col = "risk_category" if "risk_category" in df.columns else "risk_grade"
print(df[risk_col].dropna().unique())

print("\n8. Count by Fund House")
print(df["fund_house"].value_counts())

print("\n9. Count by Category")
print(df["category"].value_counts())

print("\n10. Count by Sub-Category")
print(df["sub_category"].value_counts())

print("\n11. Count by Risk Category")
print(df[risk_col].value_counts())

print("\n12. AMFI Scheme Code Check")
print("AMFI code dtype:", df["amfi_code"].dtype)
print("Total AMFI codes:", df["amfi_code"].count())
print("Unique AMFI codes:", df["amfi_code"].nunique())
print("Duplicate AMFI codes:", df["amfi_code"].duplicated().sum())

print("\nSample AMFI Codes:")
print(df[["amfi_code", "scheme_name", "fund_house", "category", "sub_category"]].head(10))

print("\n13. AMFI Code Structure Notes")
print("""
AMFI scheme codes are unique identifiers assigned to mutual fund schemes.
In this project:
- Each AMFI code identifies one mutual fund scheme.
- The code is used as the key to connect fund_master with nav_history.
- It works like a primary key in fund_master.
- It works like a foreign key in nav_history.
- The code itself is not meant to be decoded like category/year/fund house.
- Example: 125497 refers to one specific scheme in the mfapi/AMFI ecosystem.
""")