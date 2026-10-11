"""Train and evaluate the project's risk classifier and clustering pipeline."""
from pathlib import Path
import json, warnings
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'; MODELS=ROOT/'models'
FEATURES=['expense_ratio','fund_size_cr','fund_age_yr','sortino','alpha','sd','beta','sharpe','returns_1yr','returns_3yr','returns_5yr','rating']

def main():
    df=pd.read_csv(OUT/'mutual_funds_clean.csv')
    # The original project uses XGBoost. Fall back to sklearn if the package is unavailable.
    try:
        from xgboost import XGBClassifier
        model=XGBClassifier(objective='multi:softprob', n_estimators=250, max_depth=4, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, eval_metric='mlogloss', random_state=42)
        model_name='XGBoost'
    except Exception:
        model=RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42)
        model_name='RandomForest fallback'
    X=df[FEATURES].apply(pd.to_numeric, errors='coerce')
    y_text=df['risk_category'].astype(str)
    label_encoder=LabelEncoder()
    y=label_encoder.fit_transform(y_text)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)
    pipe=Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler()),('model',model)])
    pipe.fit(X_train,y_train); pred_encoded=pipe.predict(X_test)
    y_test_text=label_encoder.inverse_transform(y_test)
    pred=label_encoder.inverse_transform(pred_encoded.astype(int))
    acc=float(accuracy_score(y_test_text,pred))
    report=classification_report(y_test_text,pred,output_dict=True,zero_division=0)
    labels=['Low','Medium','High']
    cm=confusion_matrix(y_test_text,pred,labels=labels)
    pd.DataFrame(cm,index=[f'actual_{x}' for x in labels],columns=[f'predicted_{x}' for x in labels]).to_csv(OUT/'confusion_matrix.csv')
    pd.DataFrame(classification_report(y_test_text,pred,labels=labels,target_names=labels,output_dict=True,zero_division=0)).T.to_csv(OUT/'classification_report.csv')
    metrics={'model':model_name,'rows':int(len(df)),'train_rows':int(len(X_train)),'test_rows':int(len(X_test)),'accuracy':acc,
             'macro_precision':float(report['macro avg']['precision']),'macro_recall':float(report['macro avg']['recall']),
             'macro_f1':float(report['macro avg']['f1-score']), 'target_definition':'risk_level 1-2=Low, 3-4=Medium, 5-6=High',
             'caveat':'Risk labels are derived from the source risk_level field. Results measure reproduction of these labels, not independently verified investment risk or future returns.'}
    (OUT/'model_metrics.json').write_text(json.dumps(metrics,indent=2))
    pd.DataFrame({'scheme_name':df.loc[X_test.index,'scheme_name'].values,'actual_risk':y_test_text,'predicted_risk':pred}).to_csv(OUT/'test_predictions.csv',index=False)
    MODELS.mkdir(exist_ok=True); joblib.dump({'pipeline':pipe,'features':FEATURES,'model_name':model_name,'classes':list(label_encoder.classes_),'label_encoder':label_encoder},MODELS/'risk_classifier.joblib')
    # KMeans + PCA clustering for exploratory fund segmentation.
    scaler=StandardScaler(); X_scaled=scaler.fit_transform(X)
    pca=PCA(n_components=2,random_state=42); coords=pca.fit_transform(X_scaled)
    km=KMeans(n_clusters=3,n_init=20,random_state=42); clusters=km.fit_predict(coords)
    pd.DataFrame({'scheme_name':df.scheme_name,'amc_name':df.amc_name,'category':df.category,'risk_category':df.risk_category,'cluster':clusters,'pca_1':coords[:,0],'pca_2':coords[:,1]}).to_csv(OUT/'fund_clusters.csv',index=False)
    print(json.dumps(metrics,indent=2))
if __name__=='__main__': main()
