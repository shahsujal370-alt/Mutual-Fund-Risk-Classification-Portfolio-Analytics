USE MutualFundAnalytics;
GO
CREATE OR ALTER VIEW dbo.vw_RiskCategorySummary AS
SELECT risk_category, COUNT(*) AS fund_count, AVG(returns_1yr) AS avg_1yr_return,
       AVG(returns_3yr) AS avg_3yr_return, AVG(returns_5yr) AS avg_5yr_return,
       AVG(sd) AS avg_volatility, AVG(CAST(rating AS FLOAT)) AS avg_rating
FROM dbo.MutualFund GROUP BY risk_category;
GO
CREATE OR ALTER VIEW dbo.vw_CategoryPerformance AS
SELECT category, sub_category, COUNT(*) AS fund_count,
       AVG(returns_1yr) AS avg_1yr_return, AVG(returns_3yr) AS avg_3yr_return,
       AVG(returns_5yr) AS avg_5yr_return, AVG(sd) AS avg_volatility
FROM dbo.MutualFund GROUP BY category, sub_category;
GO
CREATE OR ALTER VIEW dbo.vw_FundDashboard AS
SELECT scheme_name, amc_name, category, sub_category, risk_category, rating,
       returns_1yr, returns_3yr, returns_5yr, sd, sharpe, sortino, expense_ratio,
       fund_size_cr, recommendation_score
FROM dbo.MutualFund;
GO
