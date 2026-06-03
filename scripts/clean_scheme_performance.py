from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/07_scheme_performance.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "clean_scheme_performance.csv"
ANOMALY_FILE = OUTPUT_DIR / "scheme_performance_anomalies.csv"


def clean_scheme_performance():
    df = pd.read_csv(RAW_FILE)

    print("Original Shape:", df.shape)

    df.columns = df.columns.str.strip().str.lower()

    numeric_columns = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "expense_ratio_pct",
    ]

    existing_numeric_columns = [col for col in numeric_columns if col in df.columns]

    for col in existing_numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    anomalies = pd.DataFrame()

    for col in existing_numeric_columns:
        invalid_numeric = df[df[col].isna()].copy()
        if not invalid_numeric.empty:
            invalid_numeric["anomaly_reason"] = f"{col} is not numeric or missing"
            anomalies = pd.concat([anomalies, invalid_numeric], ignore_index=True)

    if "expense_ratio_pct" in df.columns:
        invalid_expense = df[
            (df["expense_ratio_pct"] < 0.1) |
            (df["expense_ratio_pct"] > 2.5)
        ].copy()

        if not invalid_expense.empty:
            invalid_expense["anomaly_reason"] = "expense_ratio_pct outside 0.1% - 2.5%"
            anomalies = pd.concat([anomalies, invalid_expense], ignore_index=True)

    if "sharpe_ratio" in df.columns:
        negative_sharpe = df[df["sharpe_ratio"] < 0].copy()

        if not negative_sharpe.empty:
            negative_sharpe["anomaly_reason"] = "negative sharpe_ratio"
            anomalies = pd.concat([anomalies, negative_sharpe], ignore_index=True)

    if "max_drawdown_pct" in df.columns:
        positive_drawdown = df[df["max_drawdown_pct"] > 0].copy()

        if not positive_drawdown.empty:
            positive_drawdown["anomaly_reason"] = "max_drawdown_pct should usually be negative"
            anomalies = pd.concat([anomalies, positive_drawdown], ignore_index=True)

    duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    if anomalies.empty:
        print("\nNo anomalies found.")
    else:
        anomalies.to_csv(ANOMALY_FILE, index=False)
        print(f"\nAnomalies saved to: {ANOMALY_FILE}")

    print("\nCleaning Summary")
    print("-" * 50)
    print(f"Numeric columns checked: {existing_numeric_columns}")
    print(f"Duplicate rows removed: {duplicate_rows}")
    print(f"Final Shape: {df.shape}")
    print(f"Saved cleaned file to: {OUTPUT_FILE}")

    if "expense_ratio_pct" in df.columns:
        print("\nExpense Ratio Summary:")
        print(df["expense_ratio_pct"].describe())

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    clean_scheme_performance()
