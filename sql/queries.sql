-- =========================================================
-- Bluestock Mutual Fund Analytics
-- 10 Analytical SQL Queries
-- =========================================================


-- 1. Top 5 fund houses by latest AUM
SELECT
    fa.fund_house,
    dd.full_date,
    fa.aum_crore,
    fa.num_schemes
FROM fact_aum fa
JOIN dim_date dd
    ON fa.date_id = dd.date_id
WHERE dd.full_date = (
    SELECT MAX(dd2.full_date)
    FROM fact_aum fa2
    JOIN dim_date dd2
        ON fa2.date_id = dd2.date_id
)
ORDER BY fa.aum_crore DESC
LIMIT 5;


-- 2. Average NAV per month by fund
SELECT
    f.amfi_code,
    f.scheme_name,
    dd.year,
    dd.month,
    ROUND(AVG(n.nav), 2) AS avg_monthly_nav
FROM fact_nav n
JOIN dim_fund f
    ON n.amfi_code = f.amfi_code
JOIN dim_date dd
    ON n.date_id = dd.date_id
GROUP BY
    f.amfi_code,
    f.scheme_name,
    dd.year,
    dd.month
ORDER BY
    f.scheme_name,
    dd.year,
    dd.month;


-- 3. SIP YoY growth by year
SELECT
    curr.year,
    curr.total_sip_amount AS current_year_sip,
    prev.total_sip_amount AS previous_year_sip,
    ROUND(
        ((curr.total_sip_amount - prev.total_sip_amount) * 100.0)
        / prev.total_sip_amount,
        2
    ) AS yoy_growth_pct
FROM (
    SELECT
        dd.year,
        SUM(ft.amount_inr) AS total_sip_amount
    FROM fact_transactions ft
    JOIN dim_date dd
        ON ft.date_id = dd.date_id
    WHERE ft.transaction_type = 'SIP'
    GROUP BY dd.year
) curr
JOIN (
    SELECT
        dd.year,
        SUM(ft.amount_inr) AS total_sip_amount
    FROM fact_transactions ft
    JOIN dim_date dd
        ON ft.date_id = dd.date_id
    WHERE ft.transaction_type = 'SIP'
    GROUP BY dd.year
) prev
    ON curr.year = prev.year + 1
ORDER BY curr.year;


-- 4. Total transactions and amount by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;


-- 5. Funds with expense ratio less than 1%
SELECT
    amfi_code,
    fund_house,
    scheme_name,
    category,
    sub_category,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;


-- 6. Top 10 funds by 3-year return
SELECT
    f.amfi_code,
    f.fund_house,
    f.scheme_name,
    f.category,
    f.sub_category,
    fp.return_3yr_pct,
    fp.sharpe_ratio,
    fp.alpha
FROM fact_performance fp
JOIN dim_fund f
    ON fp.amfi_code = f.amfi_code
ORDER BY fp.return_3yr_pct DESC
LIMIT 10;


-- 7. Best risk-adjusted funds by Sharpe ratio
SELECT
    f.amfi_code,
    f.fund_house,
    f.scheme_name,
    f.category,
    f.risk_category,
    fp.sharpe_ratio,
    fp.return_3yr_pct,
    fp.std_dev_ann_pct
FROM fact_performance fp
JOIN dim_fund f
    ON fp.amfi_code = f.amfi_code
WHERE fp.sharpe_ratio IS NOT NULL
ORDER BY fp.sharpe_ratio DESC
LIMIT 10;


-- 8. Transaction split by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(
        COUNT(*) * 100.0 / (
            SELECT COUNT(*) FROM fact_transactions
        ),
        2
    ) AS transaction_count_pct
FROM fact_transactions
GROUP BY transaction_type
ORDER BY transaction_count DESC;


-- 9. Monthly transaction trend
SELECT
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(*) AS transaction_count,
    ROUND(SUM(ft.amount_inr), 2) AS total_amount_inr
FROM fact_transactions ft
JOIN dim_date dd
    ON ft.date_id = dd.date_id
GROUP BY
    dd.year,
    dd.month,
    dd.month_name
ORDER BY
    dd.year,
    dd.month;


-- 10. Category-wise average performance
SELECT
    f.category,
    f.sub_category,
    COUNT(*) AS fund_count,
    ROUND(AVG(fp.return_1yr_pct), 2) AS avg_1yr_return_pct,
    ROUND(AVG(fp.return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(fp.return_5yr_pct), 2) AS avg_5yr_return_pct,
    ROUND(AVG(fp.sharpe_ratio), 2) AS avg_sharpe_ratio,
    ROUND(AVG(fp.max_drawdown_pct), 2) AS avg_max_drawdown_pct
FROM fact_performance fp
JOIN dim_fund f
    ON fp.amfi_code = f.amfi_code
GROUP BY
    f.category,
    f.sub_category
ORDER BY avg_3yr_return_pct DESC;