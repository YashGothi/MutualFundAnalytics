from pathlib import Path
import pandas as pd
import sys

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def ingest_all_data():
    """Main data ingestion pipeline - orchestrates all data cleaning scripts."""
    
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("DATA INGESTION PIPELINE")
    print("=" * 70)
    
    # Import cleaning functions
    try:
        from clean_nav_history import clean_nav_history
        from clean_investor_transactions import clean_investor_transactions
        from clean_scheme_performance import clean_scheme_performance
        
        print("\n[1/3] Cleaning NAV History...")
        try:
            clean_nav_history()
            print("✓ NAV History cleaned successfully\n")
        except Exception as e:
            print(f"✗ Error cleaning NAV History: {e}\n")
        
        print("[2/3] Cleaning Investor Transactions...")
        try:
            clean_investor_transactions()
            print("✓ Investor Transactions cleaned successfully\n")
        except Exception as e:
            print(f"✗ Error cleaning Investor Transactions: {e}\n")
        
        print("[3/3] Cleaning Scheme Performance...")
        try:
            clean_scheme_performance()
            print("✓ Scheme Performance cleaned successfully\n")
        except Exception as e:
            print(f"✗ Error cleaning Scheme Performance: {e}\n")
        
        print("=" * 70)
        print("DATA INGESTION COMPLETE")
        print("=" * 70)
        
    except ImportError as e:
        print(f"Error importing cleaning functions: {e}")
        sys.exit(1)


if __name__ == "__main__":
    ingest_all_data()
