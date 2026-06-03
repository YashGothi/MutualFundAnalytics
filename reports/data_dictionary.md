# Mutual Fund Analytics Platform – Data Dictionary

## Overview

This document describes all datasets, tables, columns, data types, business definitions, and source references used in the Mutual Fund Analytics Platform project.

---

# 1. dim_fund

Source: `01_fund_master.csv`

Purpose: Master dimension table containing mutual fund scheme details.

| Column             | Data Type | Description                     |
| ------------------ | --------- | ------------------------------- |
| amfi_code          | TEXT      | Unique AMFI scheme identifier   |
| fund_house         | TEXT      | Asset Management Company (AMC)  |
| scheme_name        | TEXT      | Mutual fund scheme name         |
| category           | TEXT      | Broad scheme category           |
| sub_category       | TEXT      | Detailed scheme category        |
| plan               | TEXT      | Direct or Regular plan          |
| launch_date        | DATE      | Scheme launch date              |
| benchmark          | TEXT      | Benchmark index                 |
| expense_ratio_pct  | REAL      | Annual expense ratio (%)        |
| exit_load_pct      | REAL      | Exit load charged on redemption |
| fund_manager       | TEXT      | Scheme fund manager             |
| risk_category      | TEXT      | Risk classification             |
| sebi_category_code | TEXT      | SEBI category identifier        |

Primary Key: `amfi_code`

---

# 2. dim_date

Source: Derived from all date fields

Purpose: Central calendar dimension.

| Column     | Data Type | Description              |
| ---------- | --------- | ------------------------ |
| date_id    | INTEGER   | Surrogate date key       |
| full_date  | DATE      | Calendar date            |
| year       | INTEGER   | Calendar year            |
| month      | INTEGER   | Month number             |
| month_name | TEXT      | Month name               |
| quarter    | INTEGER   | Quarter number           |
| day        | INTEGER   | Day of month             |
| day_name   | TEXT      | Day name                 |
| is_weekday | INTEGER   | 1 = Weekday, 0 = Weekend |

Primary Key: `date_id`

---

# 3. fact_nav

Source: `02_nav_history.csv`

Purpose: Daily Net Asset Value records.

| Column           | Data Type | Description             |
| ---------------- | --------- | ----------------------- |
| nav_id           | INTEGER   | NAV record identifier   |
| amfi_code        | TEXT      | Fund scheme identifier  |
| date_id          | INTEGER   | Date dimension key      |
| nav              | REAL      | Net Asset Value         |
| daily_return_pct | REAL      | Daily percentage return |

Primary Key: `nav_id`

Foreign Keys:

* amfi_code → dim_fund
* date_id → dim_date

---

# 4. fact_transactions

Source: `08_investor_transactions.csv`

Purpose: Investor transaction fact table.

| Column             | Data Type | Description                   |
| ------------------ | --------- | ----------------------------- |
| transaction_id     | TEXT      | Unique transaction identifier |
| investor_id        | TEXT      | Investor identifier           |
| amfi_code          | TEXT      | Fund scheme identifier        |
| date_id            | INTEGER   | Transaction date key          |
| transaction_type   | TEXT      | SIP, Lumpsum, Redemption      |
| amount_inr         | REAL      | Transaction amount            |
| state              | TEXT      | Investor state                |
| city               | TEXT      | Investor city                 |
| city_tier          | TEXT      | Tier 1, 2, or 3 city          |
| age_group          | TEXT      | Investor age segment          |
| gender             | TEXT      | Investor gender               |
| annual_income_lakh | REAL      | Annual income (Lakhs INR)     |
| payment_mode       | TEXT      | UPI, Net Banking, etc.        |
| kyc_status         | TEXT      | KYC verification status       |

Primary Key: `transaction_id`

Foreign Keys:

* amfi_code → dim_fund
* date_id → dim_date

---

# 5. fact_performance

Source: `07_scheme_performance.csv`

Purpose: Fund performance and risk metrics.

| Column             | Data Type | Description                   |
| ------------------ | --------- | ----------------------------- |
| performance_id     | INTEGER   | Performance record identifier |
| amfi_code          | TEXT      | Fund scheme identifier        |
| as_of_date_id      | INTEGER   | Performance measurement date  |
| return_1yr_pct     | REAL      | 1-Year return (%)             |
| return_3yr_pct     | REAL      | 3-Year return (%)             |
| return_5yr_pct     | REAL      | 5-Year return (%)             |
| benchmark_3yr_pct  | REAL      | Benchmark return (%)          |
| alpha              | REAL      | Alpha metric                  |
| beta               | REAL      | Beta metric                   |
| sharpe_ratio       | REAL      | Sharpe Ratio                  |
| sortino_ratio      | REAL      | Sortino Ratio                 |
| std_dev_ann_pct    | REAL      | Annualized volatility         |
| max_drawdown_pct   | REAL      | Maximum drawdown              |
| morningstar_rating | INTEGER   | Rating (1–5)                  |

Primary Key: `performance_id`

Foreign Keys:

* amfi_code → dim_fund
* as_of_date_id → dim_date

---

# 6. fact_aum

Source: `03_aum_by_fund_house.csv`

Purpose: Assets Under Management metrics.

| Column      | Data Type | Description              |
| ----------- | --------- | ------------------------ |
| aum_id      | INTEGER   | AUM record identifier    |
| fund_house  | TEXT      | Asset Management Company |
| date_id     | INTEGER   | Reporting date           |
| aum_crore   | REAL      | AUM value (Crores INR)   |
| num_schemes | INTEGER   | Number of schemes        |

Primary Key: `aum_id`

Foreign Key:

* date_id → dim_date

---

# Source Files

| Dataset               | Source File                  |
| --------------------- | ---------------------------- |
| Fund Master           | 01_fund_master.csv           |
| NAV History           | 02_nav_history.csv           |
| AUM Data              | 03_aum_by_fund_house.csv     |
| SIP Inflows           | 04_monthly_sip_inflows.csv   |
| Category Inflows      | 05_category_inflows.csv      |
| Folio Count           | 06_industry_folio_count.csv  |
| Scheme Performance    | 07_scheme_performance.csv    |
| Investor Transactions | 08_investor_transactions.csv |
| Portfolio Holdings    | 09_portfolio_holdings.csv    |
| Benchmark Index Data  | 10_benchmark_indices.csv     |
| Live NAV API          | mfapi.in                     |

---

# Business Rules

1. Every scheme is uniquely identified by AMFI Code.
2. NAV values must be greater than zero.
3. Transaction amounts must be greater than zero.
4. Transaction types are restricted to SIP, Lumpsum, and Redemption.
5. KYC status must be Verified or Pending.
6. Expense ratios are expected between 0.1% and 2.5%.
7. Date dimension serves as the central calendar reference for all fact tables.
