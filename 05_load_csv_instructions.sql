/* Recommended beginner workflow:
1) Run 01_create_schema.sql in SSMS.
2) In SSMS Object Explorer, right-click MutualFundAnalytics > Tasks > Import Flat File.
3) Select outputs/mutual_funds_clean.csv, set table name to dbo.MutualFund_Stage, and inspect inferred data types.
4) The staging CSV has additional columns risk_category and recommendation_score but no fund_id or loaded_at.
5) Insert into dbo.MutualFund using an explicit column list, then run 02_data_quality_checks.sql and 04_create_views.sql.

Example insert (run only after importing to dbo.MutualFund_Stage):
INSERT INTO dbo.MutualFund
(scheme_name,min_sip,min_lumpsum,expense_ratio,fund_size_cr,fund_age_yr,fund_manager,sortino,alpha,sd,beta,sharpe,risk_level,amc_name,rating,category,sub_category,returns_1yr,returns_3yr,returns_5yr,risk_category,recommendation_score)
SELECT scheme_name,min_sip,min_lumpsum,expense_ratio,fund_size_cr,fund_age_yr,fund_manager,sortino,alpha,sd,beta,sharpe,risk_level,amc_name,rating,category,sub_category,returns_1yr,returns_3yr,returns_5yr,risk_category,recommendation_score
FROM dbo.MutualFund_Stage;
*/
