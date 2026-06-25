# Mutual Fund Analytics Platform

### Bluestock Fintech Capstone Project

**Author:** Yash Gothi
**Tools Used:** Python, Pandas, NumPy, SQLite, SQLAlchemy, Jupyter Notebook, Power BI, Git, GitHub
**Project Duration:** Day 1 – Day 4
**Report Version:** Final Submission

---

# Executive Summary

The Mutual Fund Analytics Platform was developed to analyze mutual fund performance, investor behavior, portfolio risk, and industry trends using historical and transactional data. The project integrates data engineering, data analytics, risk analytics, SQL database design, and dashboard visualization into a single end-to-end analytics solution.

The platform processes ten mutual fund datasets containing fund metadata, NAV history, investor transactions, AUM information, portfolio holdings, and benchmark data. Through ETL pipelines, data quality validation, database modeling, and analytical reporting, the project provides actionable insights for investors, fund managers, and financial institutions.

Key outcomes include investor segmentation, risk-adjusted fund performance evaluation, Value-at-Risk analysis, SIP continuity monitoring, portfolio concentration assessment, and a rule-based fund recommendation engine.

---

# 1. Project Objectives

## Business Objectives

The project aims to:

* Analyze mutual fund performance across multiple schemes.
* Evaluate investor behavior and transaction patterns.
* Measure portfolio risk using quantitative risk metrics.
* Monitor SIP continuity and investor retention.
* Compare fund diversification and concentration levels.
* Develop dashboards for executive decision-making.
* Create a recommendation framework based on investor risk profiles.

## Technical Objectives

* Build ETL pipelines using Python.
* Design a star-schema SQLite data warehouse.
* Implement SQL analytics and reporting.
* Create Power BI dashboards.
* Perform risk analytics using historical returns.
* Document the complete analytics workflow.

---

# 2. Data Sources

The project utilizes ten datasets:

| Dataset               | Description                     |
| --------------------- | ------------------------------- |
| Fund Master           | Scheme metadata                 |
| NAV History           | Historical daily NAV values     |
| AUM by Fund House     | Assets under management         |
| SIP Inflows           | Monthly SIP trends              |
| Category Inflows      | Category-level investment flows |
| Industry Folio Count  | Industry growth metrics         |
| Scheme Performance    | Return and risk measures        |
| Investor Transactions | Investor transaction history    |
| Portfolio Holdings    | Security and sector holdings    |
| Benchmark Indices     | Market benchmark data           |

### External API

mfapi.in

Used for live NAV retrieval and validation of scheme performance.

---

# 3. ETL Design & Data Engineering

## Project Architecture

Raw Data → Data Cleaning → Validation → SQLite Warehouse → Analytics → Power BI Dashboard

### Data Cleaning Activities

* Missing value handling
* Duplicate removal
* Data type standardization
* Transaction type normalization
* Date parsing and validation
* NAV validation
* Expense ratio validation
* KYC status verification

### Data Quality Controls

* Referential integrity checks
* Row count validation
* Duplicate detection
* Range validation rules
* Null value analysis

---

# 4. Database Design

## Star Schema Overview

### Dimension Tables

#### dim_fund

Contains fund metadata.

#### dim_date

Calendar dimension supporting time-series analysis.

### Fact Tables

#### fact_nav

Daily NAV records.

#### fact_transactions

Investor transactions.

#### fact_performance

Risk and return metrics.

#### fact_aum

Fund house AUM records.

### Database Benefits

* Faster analytical queries
* Reduced redundancy
* Better dashboard performance
* Improved scalability

(Insert Star Schema Diagram Screenshot)

---

# 5. Exploratory Data Analysis

## Investor Demographics

### Age Group Distribution

Key findings:

* Majority of investors belong to the working-age population.
* Younger investors show increasing participation.

(Insert Pie Chart Screenshot)

---

## Gender Distribution

Key findings:

* Male investors represent the majority share.
* Female participation continues to grow.

(Insert Chart Screenshot)

---

## Geographic Analysis

### SIP Amount by State

Key findings:

* Major metro states contribute most investments.
* Significant opportunity exists in underpenetrated regions.

(Insert Bar Chart Screenshot)

---

## T30 vs B30 Analysis

Key findings:

* T30 cities dominate investment activity.
* B30 growth indicates improving financial inclusion.

(Insert Pie Chart Screenshot)

---

# 6. Mutual Fund Performance Analysis

## Return Analysis

Metrics evaluated:

* 1-Year Returns
* 3-Year Returns
* 5-Year Returns

Key findings:

* Large-cap funds demonstrated consistent performance.
* Some funds significantly outperformed benchmarks.

(Insert Performance Charts)

---

## Risk-Adjusted Performance

Metrics:

* Sharpe Ratio
* Sortino Ratio
* Alpha
* Beta

Key findings:

* High Sharpe Ratio funds delivered superior risk-adjusted returns.
* Several funds generated positive alpha against benchmarks.

(Insert Risk Analysis Dashboard)

---

# 7. Risk Analytics

## Historical Value-at-Risk (VaR)

Methodology:

* Daily return calculation
* 5th percentile estimation

Findings:

* Certain schemes exhibit significantly higher downside risk.
* Risk varies considerably across categories.

---

## Conditional Value-at-Risk (CVaR)

Methodology:

* Average loss below VaR threshold

Findings:

* CVaR identified tail-risk exposure not visible through standard volatility measures.

---

## Rolling 90-Day Sharpe Ratio

Findings:

* Performance stability differs across funds.
* Some funds maintain consistently superior risk-adjusted returns.

(Insert Rolling Sharpe Chart)

---

# 8. Investor Behavior Analytics

## Cohort Analysis

Findings:

* Newer investor cohorts invest larger amounts.
* Average SIP values have increased over time.

(Insert Cohort Analysis Screenshot)

---

## SIP Continuity Analysis

Findings:

* Most investors maintain regular SIP schedules.
* At-risk investors identified through transaction gap analysis.

(Insert SIP Continuity Dashboard)

---

# 9. Portfolio Diversification Analysis

## HHI Concentration Analysis

The Herfindahl-Hirschman Index (HHI) was used to evaluate portfolio concentration.

Findings:

* Some equity funds exhibit concentrated sector exposure.
* Diversified funds generally display lower concentration risk.

(Insert HHI Comparison Chart)

---

# 10. Fund Recommendation Engine

A rule-based recommendation system was developed using:

* Risk Grade
* Sharpe Ratio
* Fund Performance Metrics

### Risk Categories

* Low Risk
* Moderate Risk
* High Risk

The engine recommends the top-performing funds within each risk profile.

(Insert Recommendation Output Screenshot)

---

# 11. Dashboard Overview

### Dashboard Components

* Executive Summary
* Investor Analytics
* Fund Performance
* Risk Analytics
* Portfolio Concentration
* Geographic Analysis

(Insert Dashboard Screenshots)

Screenshot 1: Overview Dashboard

Screenshot 2: Investor Analytics Dashboard

Screenshot 3: Risk Analytics Dashboard

Screenshot 4: Fund Performance Dashboard

---

# 12. Key Insights

### Insight 1

Funds with the highest VaR values exhibited significantly larger downside exposure.

### Insight 2

Recent investor cohorts contribute the largest investment volumes.

### Insight 3

A small group of states account for the majority of SIP investments.

### Insight 4

Higher Sharpe Ratio funds consistently outperform peers on a risk-adjusted basis.

### Insight 5

Portfolio concentration varies significantly across equity schemes.

---

# 13. Limitations

* Historical performance does not guarantee future returns.
* Limited availability of live market data.
* Simplified recommendation engine.
* Assumed transaction consistency for SIP analysis.
* Portfolio holdings snapshots may not represent real-time allocations.

---

# 14. Recommendations

### For Investors

* Focus on risk-adjusted returns rather than absolute returns.
* Maintain SIP discipline for long-term wealth creation.
* Diversify across categories and sectors.

### For Fund Houses

* Improve investor engagement in B30 regions.
* Monitor SIP continuity to reduce churn.
* Promote diversified investment strategies.

### For Future Enhancements

* Machine Learning-based recommendation engine.
* Real-time NAV integration.
* Portfolio optimization models.
* Predictive investor churn analytics.
* Automated dashboard refresh pipelines.

---

# Conclusion

The Mutual Fund Analytics Platform successfully combines data engineering, risk analytics, business intelligence, and investment analysis into a unified solution. The project demonstrates practical application of Python, SQL, Power BI, and financial analytics concepts while delivering meaningful insights into mutual fund performance and investor behavior.
