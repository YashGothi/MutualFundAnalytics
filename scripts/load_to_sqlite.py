"""
Script: data_ingestion.py

Description:
Loads all raw mutual fund datasets, performs data quality validation,
and generates a comprehensive data quality report.

Author: Yash Gothi
Project: Mutual Fund Analytics Platform
"""

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, inspect
import os

# Define paths
PROCESSED_DATA_DIR = Path("data/processed")
DB_PATH = PROCESSED_DATA_DIR / "bluestock_mf.db"
DATABASE_URL = f"sqlite:///{DB_PATH.absolute()}"

# Mapping of CSV files to table names and source verification files
DATASETS = {
    "clean_nav_history.csv": {
        "table_name": "nav_history",
        "source_csv": "data/raw/02_nav_history.csv"
    },
    "clean_investor_transactions.csv": {
        "table_name": "investor_transactions",
        "source_csv": "data/raw/08_investor_transactions.csv"
    },
    "clean_scheme_performance.csv": {
        "table_name": "scheme_performance",
        "source_csv": "data/raw/07_scheme_performance.csv"
    }
}


def get_row_count(file_path):
    """Get row count from CSV file."""
    if not Path(file_path).exists():
        return None
    try:
        # Use wc -l equivalent via pandas
        df = pd.read_csv(file_path)
        return len(df)
    except Exception as e:
        print(f"  Error reading {file_path}: {e}")
        return None


def load_datasets_to_sqlite():
    """Load all cleaned datasets into SQLite database."""
    
    print("\n" + "=" * 80)
    print("LOADING CLEANED DATASETS TO SQLITE")
    print("=" * 80)
    
    # Create SQLite engine
    try:
        engine = create_engine("sqlite:///data/processed/bluestock_mf.db")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return
    
    # Create processed data directory if it doesn't exist
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    total_loaded = 0
    total_verified = 0
    
    # Load each dataset
    for csv_file, config in DATASETS.items():
        csv_path = PROCESSED_DATA_DIR / csv_file
        table_name = config["table_name"]
        source_csv = config["source_csv"]
        
        print(f"\n{'-' * 80}")
        print(f"Loading: {csv_file} → {table_name}")
        print(f"{'-' * 80}")
        
        # Check if cleaned CSV exists
        if not csv_path.exists():
            print(f"  ⚠ Cleaned file not found: {csv_path}")
            print(f"    Please run the cleaning scripts first.")
            continue
        
        try:
            # Load cleaned CSV
            df = pd.read_csv(csv_path)
            cleaned_row_count = len(df)
            print(f"  ✓ Loaded cleaned CSV: {csv_file}")
            print(f"    Rows in cleaned file: {cleaned_row_count:,}")
            
            # Get source row count for verification
            source_row_count = get_row_count(source_csv)
            if source_row_count:
                removed_rows = source_row_count - cleaned_row_count
                print(f"    Rows in source file: {source_row_count:,}")
                print(f"    Rows removed during cleaning: {removed_rows:,}")
            
            # Load to SQLite
            df.to_sql(table_name, con=engine, if_exists="replace", index=False)
            print(f"  ✓ Loaded to SQLite table: {table_name}")
            
            # Verify data in database
            inspector = inspect(engine)
            
            if table_name in inspector.get_table_names():
                db_row_count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", con=engine)
                db_row_count = db_row_count['count'].values[0]
                
                print(f"    Rows in database table: {db_row_count:,}")
                
                if db_row_count == cleaned_row_count:
                    print(f"  ✓ VERIFIED: Row count matches!")
                    total_verified += 1
                else:
                    print(f"  ✗ MISMATCH: Expected {cleaned_row_count:,}, got {db_row_count:,}")
            
            total_loaded += 1
            
        except Exception as e:
            print(f"  ✗ Error loading {csv_file}: {e}")
    
    # Display summary statistics
    print(f"\n{'=' * 80}")
    print("LOADING SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total datasets loaded: {total_loaded}/{len(DATASETS)}")
    print(f"Total datasets verified: {total_verified}/{len(DATASETS)}")
    
    # Display database schema
    print(f"\n{'=' * 80}")
    print("DATABASE SCHEMA")
    print(f"{'=' * 80}")
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\nTables in database ({len(tables)}):")
        for table in tables:
            columns = inspector.get_columns(table)
            row_count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", con=engine)
            row_count = row_count['count'].values[0]
            
            print(f"\n  Table: {table} ({row_count:,} rows)")
            print(f"  Columns ({len(columns)}):")
            for col in columns:
                print(f"    - {col['name']}: {col['type']}")
    
    except Exception as e:
        print(f"  Error inspecting database: {e}")
    
    print(f"\n{'=' * 80}\n")
    return total_loaded == len(DATASETS)


if __name__ == "__main__":
    success = load_datasets_to_sqlite()
    exit(0 if success else 1)
