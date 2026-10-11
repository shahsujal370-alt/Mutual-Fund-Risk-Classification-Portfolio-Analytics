USE MutualFundAnalytics;
GO
-- 1. Funds by risk category
SELECT risk_category, COUNT(*) AS fund_count, AVG(returns_3yr) AS avg_3yr_return, AVG(sd) AS avg_volatility, AVG(CAST(rating AS FLOAT)) AS avg_rating
FROM dbo.MutualFund GROUP BY risk_category ORDER BY fund_count DESC;
-- 2. Category-level performance
SELECT category, COUNT(*) AS fund_count, AVG(returns_1yr) AS avg_1yr_return, AVG(returns_3yr) AS avg_3yr_return, AVG(returns_5yr) AS avg_5yr_return
FROM dbo.MutualFund GROUP BY category ORDER BY avg_3yr_return DESC;
-- 3. Top funds per risk category (transparent historical score; not investment advice)
WITH ranked AS (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY risk_category ORDER BY recommendation_score DESC, returns_3yr DESC, rating DESC) AS rn
 FROM dbo.MutualFund
)
SELECT risk_category, scheme_name, amc_name, category, rating, returns_3yr, sd, sharpe, recommendation_score
FROM ranked WHERE rn <= 5 ORDER BY risk_category, rn;
-- 4. High volatility and weak 3-year returns: review list, not a buy/sell signal
SELECT scheme_name, amc_name, category, risk_category, sd, returns_3yr, rating
FROM dbo.MutualFund WHERE sd >= (SELECT AVG(sd) FROM dbo.MutualFund)
 AND returns_3yr < (SELECT AVG(returns_3yr) FROM dbo.MutualFund)
ORDER BY sd DESC;
GO
