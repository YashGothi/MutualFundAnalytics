PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    "plan" TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL CHECK (
        expense_ratio_pct IS NULL OR 
        expense_ratio_pct BETWEEN 0.1 AND 2.5
    ),
    exit_load_pct REAL CHECK (
        exit_load_pct IS NULL OR 
        exit_load_pct BETWEEN 0 AND 5
    ),
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    month_name TEXT NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_name TEXT NOT NULL,
    is_weekday INTEGER NOT NULL CHECK (is_weekday IN (0, 1))
);

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT NOT NULL,
    date_id INTEGER NOT NULL,
    nav REAL NOT NULL CHECK (nav > 0),
    daily_return_pct REAL CHECK (
        daily_return_pct IS NULL OR 
        daily_return_pct BETWEEN -100 AND 100
    ),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    UNIQUE (amfi_code, date_id)
);

CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id TEXT NOT NULL,
    amfi_code TEXT NOT NULL,
    date_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL CHECK (
        transaction_type IN ('SIP', 'Lumpsum', 'Redemption')
    ),
    amount_inr REAL NOT NULL CHECK (amount_inr > 0),
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL CHECK (
        annual_income_lakh IS NULL OR 
        annual_income_lakh >= 0
    ),
    payment_mode TEXT,
    kyc_status TEXT CHECK (
        kyc_status IS NULL OR 
        kyc_status IN ('Verified', 'Pending')
    ),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT NOT NULL,
    as_of_date_id INTEGER,
    return_1yr_pct REAL CHECK (
        return_1yr_pct IS NULL OR 
        return_1yr_pct BETWEEN -100 AND 500
    ),
    return_3yr_pct REAL CHECK (
        return_3yr_pct IS NULL OR 
        return_3yr_pct BETWEEN -100 AND 500
    ),
    return_5yr_pct REAL CHECK (
        return_5yr_pct IS NULL OR 
        return_5yr_pct BETWEEN -100 AND 500
    ),
    benchmark_3yr_pct REAL CHECK (
        benchmark_3yr_pct IS NULL OR 
        benchmark_3yr_pct BETWEEN -100 AND 500
    ),
    alpha REAL,
    beta REAL CHECK (
        beta IS NULL OR 
        beta >= 0
    ),
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL CHECK (
        std_dev_ann_pct IS NULL OR 
        std_dev_ann_pct >= 0
    ),
    max_drawdown_pct REAL CHECK (
        max_drawdown_pct IS NULL OR 
        max_drawdown_pct BETWEEN -100 AND 0
    ),
    morningstar_rating INTEGER CHECK (
        morningstar_rating IS NULL OR 
        morningstar_rating BETWEEN 1 AND 5
    ),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (as_of_date_id) REFERENCES dim_date(date_id),
    UNIQUE (amfi_code, as_of_date_id)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT NOT NULL,
    date_id INTEGER NOT NULL,
    aum_crore REAL NOT NULL CHECK (aum_crore > 0),
    num_schemes INTEGER CHECK (
        num_schemes IS NULL OR 
        num_schemes > 0
    ),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    UNIQUE (fund_house, date_id)
);

CREATE INDEX idx_fact_nav_amfi_code 
ON fact_nav(amfi_code);

CREATE INDEX idx_fact_nav_date_id 
ON fact_nav(date_id);

CREATE INDEX idx_fact_transactions_amfi_code 
ON fact_transactions(amfi_code);

CREATE INDEX idx_fact_transactions_date_id 
ON fact_transactions(date_id);

CREATE INDEX idx_fact_transactions_state 
ON fact_transactions(state);

CREATE INDEX idx_fact_performance_amfi_code 
ON fact_performance(amfi_code);

CREATE INDEX idx_fact_performance_date_id 
ON fact_performance(as_of_date_id);

CREATE INDEX idx_fact_aum_fund_house 
ON fact_aum(fund_house);

CREATE INDEX idx_fact_aum_date_id 
ON fact_aum(date_id);

CREATE INDEX idx_dim_fund_fund_house 
ON dim_fund(fund_house);

CREATE INDEX idx_fact_transactions_investor_id 
ON fact_transactions(investor_id);

CREATE INDEX idx_fact_transactions_investor_date 
ON fact_transactions(investor_id, date_id);

CREATE INDEX idx_dim_date_full_date 
ON dim_date(full_date);