"""
Master Pipeline

Executes the complete Mutual Fund Analytics workflow.

Author: Yash Gothi
"""

import subprocess

scripts = [
    "scripts/data_ingestion.py",
    "scripts/explore_fund_master.py",
    "scripts/live_nav_fetch.py",
    "scripts/fetch_multiple_nav.py",
    "scripts/clean_nav_history.py",
    "scripts/clean_transactions.py",
    "scripts/clean_performance.py",
    "scripts/load_sqlite.py",
    "scripts/calculate_var_cvar.py",
    "scripts/rolling_sharpe.py",
    "scripts/investor_cohort_analysis.py",
    "scripts/sip_continuity_analysis.py",
    "scripts/fund_recommender.py",
    "scripts/sector_hhi_analysis.py"
]

print("=" * 60)
print("MUTUAL FUND ANALYTICS PIPELINE")
print("=" * 60)

for script in scripts:

    print(f"\nRunning: {script}")

    result = subprocess.run(
        ["python", script]
    )

    if result.returncode == 0:
        print("✓ Success")

    else:
        print("✗ Failed")
        break

print("\nPipeline Completed.")