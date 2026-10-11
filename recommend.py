"""Risk-profile filter and transparent ranking-based fund shortlist."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def recommend(risk_profile='Medium', top_n=5):
    df=pd.read_csv(ROOT/'outputs'/'mutual_funds_clean.csv')
    risk_profile=risk_profile.title()
    if risk_profile not in {'Low','Medium','High'}: raise ValueError('risk_profile must be Low, Medium, or High')
    subset=df[df.risk_category==risk_profile].copy()
    subset=subset.sort_values(['recommendation_score','returns_3yr','rating'],ascending=False).head(top_n)
    cols=['scheme_name','amc_name','category','sub_category','risk_category','rating','returns_1yr','returns_3yr','returns_5yr','sd','sharpe','recommendation_score']
    return subset[cols]
if __name__=='__main__':
    for risk in ['Low','Medium','High']:
        result=recommend(risk,5); result.to_csv(ROOT/'outputs'/f'recommendations_{risk.lower()}.csv',index=False)
        print(f'\n{risk} risk shortlist\n',result.to_string(index=False))
