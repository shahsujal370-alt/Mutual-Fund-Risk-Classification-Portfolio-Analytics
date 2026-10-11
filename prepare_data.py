"""Clean mutual fund data and produce SQL/Power BI-ready tables."""
from pathlib import Path
import pandas as pd
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data' / 'comprehensive_mutual_funds_data.csv'
OUT = ROOT / 'outputs'
NUMERIC = ['min_sip','min_lumpsum','expense_ratio','fund_size_cr','fund_age_yr','sortino','alpha','sd','beta','sharpe','risk_level','rating','returns_1yr','returns_3yr','returns_5yr']

def main():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(SOURCE)
    original_rows = len(df)
    df.columns = [c.strip().lower() for c in df.columns]
    for c in NUMERIC:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    # Do not invent values for missing business identifiers; remove exact duplicate rows.
    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    numeric_cols = df.select_dtypes(include='number').columns
    for c in numeric_cols:
        df[c] = df[c].fillna(df[c].median())
    for c in ['scheme_name','amc_name','category','sub_category','fund_manager']:
        if c in df: df[c] = df[c].fillna('Unknown').astype(str).str.strip()
    df['risk_category'] = pd.cut(df['risk_level'], bins=[0,2,4,6], labels=['Low','Medium','High'], include_lowest=True).astype(str)
    df['risk_category'] = df['risk_category'].replace('nan','Unknown')
    # Portfolio score is a transparent ranking proxy, not a guaranteed-return forecast.
    df['recommendation_score'] = (df['returns_3yr'].rank(pct=True)*0.70 + df['rating'].rank(pct=True)*0.30).round(6)
    # Basic validation summary
    quality = pd.DataFrame([
        ['source_rows', original_rows], ['rows_after_deduplication', len(df)], ['exact_duplicate_rows_removed', duplicate_rows],
        ['columns', len(df.columns)], ['rows_with_missing_values_after_cleaning', int(df.isna().any(axis=1).sum())],
        ['unique_funds', int(df['scheme_name'].nunique())], ['low_risk_funds', int((df.risk_category=='Low').sum())],
        ['medium_risk_funds', int((df.risk_category=='Medium').sum())], ['high_risk_funds', int((df.risk_category=='High').sum())]
    ], columns=['check_name','value'])
    df.to_csv(OUT/'mutual_funds_clean.csv', index=False)
    quality.to_csv(OUT/'data_quality_summary.csv', index=False)
    df[['scheme_name','amc_name','category','sub_category','risk_level','risk_category','rating','returns_1yr','returns_3yr','returns_5yr','sd','sharpe','sortino','recommendation_score']].to_csv(OUT/'powerbi_fund_summary.csv', index=False)
    df.groupby(['category','risk_category'], dropna=False).agg(fund_count=('scheme_name','count'), avg_return_1yr=('returns_1yr','mean'), avg_return_3yr=('returns_3yr','mean'), avg_volatility=('sd','mean'), avg_rating=('rating','mean')).reset_index().to_csv(OUT/'powerbi_category_risk_summary.csv', index=False)
    print(f'Prepared {len(df)} rows (source {original_rows}; removed {duplicate_rows} exact duplicates).')
    print(quality.to_string(index=False))
if __name__ == '__main__': main()
