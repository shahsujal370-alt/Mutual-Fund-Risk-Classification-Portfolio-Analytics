/* Run in SQL Server Management Studio (SSMS). Creates the project database and reporting tables. */
IF DB_ID('MutualFundAnalytics') IS NULL CREATE DATABASE MutualFundAnalytics;
GO
USE MutualFundAnalytics;
GO
IF OBJECT_ID('dbo.MutualFund','U') IS NOT NULL DROP TABLE dbo.MutualFund;
GO
CREATE TABLE dbo.MutualFund (
    fund_id INT IDENTITY(1,1) PRIMARY KEY,
    scheme_name NVARCHAR(300) NOT NULL,
    min_sip DECIMAL(18,2) NULL,
    min_lumpsum DECIMAL(18,2) NULL,
    expense_ratio DECIMAL(10,4) NULL,
    fund_size_cr DECIMAL(20,4) NULL,
    fund_age_yr INT NULL,
    fund_manager NVARCHAR(200) NULL,
    sortino FLOAT NULL,
    alpha FLOAT NULL,
    sd FLOAT NULL,
    beta FLOAT NULL,
    sharpe FLOAT NULL,
    risk_level INT NULL,
    amc_name NVARCHAR(250) NULL,
    rating INT NULL,
    category NVARCHAR(100) NULL,
    sub_category NVARCHAR(200) NULL,
    returns_1yr FLOAT NULL,
    returns_3yr FLOAT NULL,
    returns_5yr FLOAT NULL,
    risk_category NVARCHAR(20) NULL,
    recommendation_score FLOAT NULL,
    loaded_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
CREATE INDEX IX_MutualFund_RiskCategory ON dbo.MutualFund(risk_category);
CREATE INDEX IX_MutualFund_Category ON dbo.MutualFund(category);
GO
