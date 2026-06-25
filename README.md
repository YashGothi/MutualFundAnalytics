# 📊 Mutual Fund Analytics Platform

## Overview

The **Mutual Fund Analytics Platform** is an end-to-end financial analytics project that demonstrates data engineering, risk analytics, SQL database design, and business intelligence using mutual fund datasets. The platform processes historical and transactional mutual fund data, performs ETL operations, computes financial risk metrics, and presents actionable insights through Power BI dashboards.

This project was developed as part of the **Bluestock Fintech Capstone Project**.

---

# Features

* Automated ETL pipeline using Python and Pandas
* Data cleaning and validation for multiple financial datasets
* SQLite star schema data warehouse
* Historical NAV analysis
* Investor demographic and cohort analysis
* SIP continuity and retention analysis
* Risk analytics (Historical VaR, CVaR, Rolling Sharpe Ratio)
* Portfolio concentration analysis using HHI
* Rule-based mutual fund recommendation engine
* Interactive Power BI dashboard

---

# Technology Stack

| Category        | Technologies                 |
| --------------- | ---------------------------- |
| Programming     | Python 3                     |
| Data Processing | Pandas, NumPy                |
| Visualization   | Matplotlib, Plotly, Power BI |
| Database        | SQLite, SQLAlchemy           |
| Notebook        | Jupyter Notebook             |
| Version Control | Git, GitHub                  |

---

# Project Structure

```text
MutualFundAnalytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dashboard/
│
├── notebooks/
│
├── reports/
│
├── scripts/
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── run_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Datasets

The project uses ten primary datasets.

| Dataset               | Description                                 |
| --------------------- | ------------------------------------------- |
| Fund Master           | Mutual fund metadata and scheme information |
| NAV History           | Historical Net Asset Value (NAV) records    |
| AUM by Fund House     | Assets under Management across AMCs         |
| Monthly SIP Inflows   | Monthly SIP investment trends               |
| Category Inflows      | Net inflows by mutual fund category         |
| Industry Folio Count  | Growth of mutual fund investor folios       |
| Scheme Performance    | Historical returns and risk metrics         |
| Investor Transactions | SIP, Lumpsum, and Redemption transactions   |
| Portfolio Holdings    | Equity holdings and sector allocations      |
| Benchmark Indices     | NIFTY benchmark performance data            |

The project also retrieves live NAV information using the **mfapi.in** API.

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/YashGothi/MutualFundAnalytics.git
cd MutualFundAnalytics
```

## 2. Create a virtual environment

Windows (Git Bash):

```bash
python -m venv venv
source venv/Scripts/activate
```

Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the ETL Pipeline

Execute the complete project pipeline:

```bash
python run_pipeline.py
```

The pipeline performs:

* Data ingestion
* Data cleaning
* Data validation
* SQLite database loading
* Risk metric calculations
* Investor analytics
* Portfolio concentration analysis
* Report generation

---

# Database Design

The project follows a **Star Schema** consisting of:

### Dimension Tables

* dim_fund
* dim_date

### Fact Tables

* fact_nav
* fact_transactions
* fact_performance
* fact_aum

The schema is optimized for analytical queries and Power BI reporting.

---

# Key Analytics

The platform includes:

### Investor Analytics

* Age Group Distribution
* Gender Distribution
* Geographic Distribution
* Investor Cohort Analysis
* SIP Continuity Analysis

### Performance Analytics

* CAGR Comparison
* Alpha/Beta Analysis
* Sharpe Ratio
* Sortino Ratio
* Maximum Drawdown

### Risk Analytics

* Historical VaR (95%)
* Conditional VaR (CVaR)
* Rolling 90-Day Sharpe Ratio
* Correlation Analysis

### Portfolio Analytics

* Sector Allocation
* Herfindahl-Hirschman Index (HHI)
* Fund Recommendation Engine

---

# Dashboard

The Power BI dashboard provides:

* Executive Overview
* Investor Analytics
* Fund Performance Analysis
* Risk Analytics
* Geographic Insights
* Portfolio Diversification

To open the dashboard:

1. Install Microsoft Power BI Desktop.
2. Open either:

   * `BlueStock_PowerBI_Dashboard.pbix`, or
   * `bluestock_mf_dashboard.pbix` (if this is your final version).
3. Refresh the data source if prompted.

---

# Reports

The project includes:

* Final Project Report
* Data Dictionary
* Analytical SQL Queries
* Jupyter Notebook Analysis
* Power BI Dashboard

---

# Key Business Insights

* Identified high-risk mutual fund schemes using Historical VaR and CVaR.
* Evaluated risk-adjusted fund performance using Rolling Sharpe Ratio.
* Segmented investors through cohort and demographic analysis.
* Measured SIP continuity to identify potential investor churn.
* Assessed portfolio diversification using the Herfindahl-Hirschman Index (HHI).
* Developed a rule-based recommendation engine for matching funds to investor risk profiles.

---

# Future Enhancements

* Real-time dashboard refresh
* Machine learning-based fund recommendation system
* Predictive SIP churn modeling
* Portfolio optimization using Modern Portfolio Theory
* Cloud deployment with scheduled ETL jobs

---

# Author

**Yash Gothi**


GitHub: https://github.com/YashGothi

---

# License

This project is intended for educational and portfolio purposes.
