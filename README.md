# Enhanced Risk-Based Mutual Fund Classification & Portfolio Analytics

**Stack:** Python · XGBoost · scikit-learn · SQL Server · Power BI · pandas

An end-to-end portfolio project built from a dataset of 814 mutual funds. It combines data cleaning and quality checks, supervised risk-category classification, unsupervised clustering, risk-profile fund screening, SQL reporting assets, and a Power BI dashboard specification.

> **Transparency note:** SQL scripts and Power BI assets are included for local execution. Do not claim the SQL Server layer or a `.pbix` dashboard is deployed until you have run the SQL scripts and built/saved the report in Power BI Desktop. The risk labels are derived from the source dataset's `risk_level`; model scores measure reproduction of those labels, not independent future-risk prediction.

## Project features

- Standardise column names and convert numeric-like fields.
- Remove exact duplicate rows and impute missing numeric values with medians.
- Create Low / Medium / High categories from source `risk_level` (1–2 / 3–4 / 5–6).
- Train and evaluate an XGBoost classifier (Random Forest fallback if XGBoost is unavailable).
- Report accuracy, macro precision/recall/F1, classification report and confusion matrix.
- Apply K-Means and PCA for exploratory fund segmentation.
- Generate transparent risk-profile shortlists using a score based on 70% percentile rank of historical 3-year return and 30% percentile rank of rating. This is a simple screening heuristic, not financial advice.
- Provide SQL Server table definitions, data-quality checks, analysis queries, views and CSV-load instructions.
- Provide Power BI DAX measures and a dashboard layout guide.

## Repository structure

```text
MutualFund-ML-Project/
├── data/                         # source CSV
├── notebooks/                    # original notebook
├── src/
│   ├── prepare_data.py            # cleaning, validation, reporting extracts
│   ├── train_model.py              # model evaluation, clustering, saved model
│   ├── recommend.py                # risk-profile shortlist exports
│   └── run_pipeline.py             # runs the Python workflow
├── sql/                           # SQL Server schema, checks, queries, views
├── powerbi/                       # DAX measures and dashboard guide
├── outputs/                       # reproducible output examples and model metrics
├── models/                        # serialized model output
├── reports/                       # original project report
├── docs/                           # data dictionary, architecture, GitHub guide
├── requirements.txt
└── README.md
```

## Run the Python pipeline (Windows)

1. Install Python 3.10 or later.
2. Open PowerShell in this project folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Run the pipeline:

   ```powershell
   python src/run_pipeline.py
   ```

Generated files are saved under `outputs/` and the trained model under `models/`.

## SQL Server setup

1. Install SQL Server and SQL Server Management Studio (SSMS).
2. Run `sql/01_create_schema.sql` in SSMS.
3. Import `outputs/mutual_funds_clean.csv` into `dbo.MutualFund` using the instructions in `sql/05_load_csv_instructions.sql` (check column mappings and types before importing).
4. Run `sql/02_data_quality_checks.sql`.
5. Run `sql/03_analysis_queries.sql`.
6. Run `sql/04_create_views.sql`.

The scripts use SQL Server T-SQL. Always inspect the target table and row counts after import.

## Power BI setup

1. Open Power BI Desktop.
2. Choose **Get Data → SQL Server** and connect to the instance/database `MutualFundAnalytics`.
3. Load `dbo.vw_FundDashboard`, `dbo.vw_RiskCategorySummary`, and `dbo.vw_CategoryPerformance` after creating them in SQL Server.
4. Follow `powerbi/Dashboard_Build_Guide.md` and add measures from `powerbi/DAX_Measures.dax` via **Modeling → New measure**.
5. Create and save your report as `powerbi/MutualFund_Analytics.pbix`.

If SQL Server is not ready, you can prototype the report by importing `outputs/mutual_funds_clean.csv` directly, then reconnect to SQL Server later.

## Results

The included run's metrics are in `outputs/model_metrics.json`. With the saved run included here, XGBoost achieved **88.96% test accuracy** on a stratified 20% test split (163 test rows). Review the metrics generated on your own environment after rerunning the pipeline; exact values can vary by library versions and setup.

## Limitations and responsible interpretation

- The data is a static snapshot, not a live market feed.
- Source risk_level is mapped to the target classes, so this is a label-reproduction classification exercise.
- Historical returns and ratings are not guarantees of future performance.
- The recommendation score is a simple ranking proxy and does not account for investor goals, time horizon, taxes, liquidity, costs, or suitability.
- The original notebook/report are retained as project materials; use their results only after reviewing and rerunning the relevant cells.

## Bullets 

- Built a Python data-preparation workflow for 814 mutual fund records, including numeric conversion, duplicate handling, missing-value treatment, and reporting exports.
- Trained and evaluated an XGBoost model to reproduce source-defined Low/Medium/High risk categories, reaching 88.96% test accuracy in the included run.
- Applied K-Means clustering and PCA to explore fund segments and generated risk-profile shortlists using historical 3-year returns and ratings.
- Prepared SQL Server schema, analytical queries, reusable views, data-quality checks, and Power BI DAX/report specifications for fund analytics.

Only say that you **implemented SQL Server reporting** or **built a Power BI dashboard** after executing the scripts and saving the `.pbix` report yourself.
