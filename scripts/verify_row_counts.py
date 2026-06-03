import sqlite3
import pandas as pd

DB_FILE = "data/processed/bluestock_mf.db"

TABLE_TO_CSV = {
    "dim_fund": "data/processed/clean_fund_master.csv",
    "fact_nav": "data/processed/clean_nav_history.csv",
    "fact_transactions": "data/processed/clean_investor_transactions.csv",
    "fact_performance": "data/processed/clean_scheme_performance.csv",
    "fact_aum": "data/raw/03_aum_by_fund_house.csv"
}


def get_table_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("=" * 80)
print("ROW COUNT VALIDATION REPORT")
print("=" * 80)

all_passed = True

for table_name, csv_path in TABLE_TO_CSV.items():

    csv_count = len(pd.read_csv(csv_path))
    db_count = get_table_count(cursor, table_name)

    status = "PASS" if csv_count == db_count else "FAIL"

    if status == "FAIL":
        all_passed = False

    print(
        f"{table_name:<20} "
        f"CSV={csv_count:<8} "
        f"DB={db_count:<8} "
        f"STATUS={status}"
    )

print("\n" + "=" * 80)

if all_passed:
    print("SUCCESS: All table counts match source CSVs.")
else:
    print("WARNING: One or more tables have row count mismatches.")

conn.close()