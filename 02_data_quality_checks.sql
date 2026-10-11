USE MutualFundAnalytics;
GO
-- Row count and duplicate scheme-name check (fund houses can have similarly named schemes).
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT scheme_name) AS distinct_scheme_names FROM dbo.MutualFund;
SELECT scheme_name, amc_name, COUNT(*) AS duplicate_count
FROM dbo.MutualFund GROUP BY scheme_name, amc_name HAVING COUNT(*) > 1;
-- Required fields and invalid ranges.
SELECT SUM(CASE WHEN scheme_name IS NULL OR LTRIM(RTRIM(scheme_name))='' THEN 1 ELSE 0 END) AS missing_scheme_name,
       SUM(CASE WHEN risk_category NOT IN ('Low','Medium','High') OR risk_category IS NULL THEN 1 ELSE 0 END) AS invalid_risk_category,
       SUM(CASE WHEN rating < 0 OR rating > 5 THEN 1 ELSE 0 END) AS rating_out_of_range,
       SUM(CASE WHEN expense_ratio < 0 THEN 1 ELSE 0 END) AS negative_expense_ratio,
       SUM(CASE WHEN sd < 0 THEN 1 ELSE 0 END) AS negative_volatility
FROM dbo.MutualFund;
-- Check numeric fields for nulls.
SELECT SUM(CASE WHEN returns_3yr IS NULL THEN 1 ELSE 0 END) AS missing_3yr_returns,
       SUM(CASE WHEN sd IS NULL THEN 1 ELSE 0 END) AS missing_volatility,
       SUM(CASE WHEN sharpe IS NULL THEN 1 ELSE 0 END) AS missing_sharpe
FROM dbo.MutualFund;
GO
