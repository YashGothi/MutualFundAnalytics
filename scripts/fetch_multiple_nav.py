from pathlib import Path
import requests
import pandas as pd


OUTPUT_DIR = Path("data/raw")

SCHEMES = {
    "119551": "sbi_bluechip",
    "120503": "icici_bluechip",
    "118632": "nippon_large_cap",
    "119092": "axis_bluechip",
    "120841": "kotak_bluechip",
}


def fetch_scheme_nav(scheme_code, scheme_label):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    json_data = response.json()

    meta = json_data.get("meta", {})
    nav_data = json_data.get("data", [])

    df = pd.DataFrame(nav_data)

    df["scheme_code"] = meta.get("scheme_code", scheme_code)
    df["scheme_name"] = meta.get("scheme_name")
    df["fund_house"] = meta.get("fund_house")
    df["scheme_category"] = meta.get("scheme_category")

    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{scheme_code}_{scheme_label}_nav.csv"
    df.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print(f"Fetched: {scheme_label}")
    print(f"Scheme Code: {scheme_code}")
    print(f"API Scheme Name: {meta.get('scheme_name')}")
    print(f"Fund House: {meta.get('fund_house')}")
    print(f"Saved To: {output_file}")
    print(f"Shape: {df.shape}")
    print(df.head())


def fetch_all_schemes():
    """Fetch NAV data for all configured schemes."""
    print("\n" + "=" * 70)
    print("FETCHING MULTIPLE SCHEMES NAV DATA")
    print("=" * 70)
    
    for scheme_code, scheme_label in SCHEMES.items():
        try:
            fetch_scheme_nav(scheme_code, scheme_label)
        except Exception as e:
            print(f"\n✗ Error fetching {scheme_label} (Code: {scheme_code}): {e}")


if __name__ == "__main__":
    fetch_all_schemes()


def main():
    for scheme_code, scheme_label in SCHEMES.items():
        fetch_scheme_nav(scheme_code, scheme_label)

    print("\nAll 5 NAV files fetched successfully.")


if __name__ == "__main__":
    main()

