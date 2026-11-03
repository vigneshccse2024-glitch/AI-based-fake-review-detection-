import argparse, json, re
from pathlib import Path
import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

ROOT=Path(__file__).resolve().parents[1]
def clean(s): return re.sub(r'[^a-zA-Z0-9!? ]',' ',str(s).lower())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data',default=str(ROOT/'data'/'reviews.csv')); args=ap.parse_args()
    df=pd.read_csv(args.data).dropna(subset=['text','label']); df['text']=df.text.map(clean); df['label']=df.label.str.lower().str.strip()
    if set(df.label)-{'fake','genuine'}: raise ValueError('Labels must be fake or genuine')
    X_train,X_test,y_train,y_test=train_test_split(df.text,df.label,test_size=.25,random_state=42,stratify=df.label)
    specs={'Logistic Regression':LogisticRegression(max_iter=2000,class_weight='balanced'),'Naive Bayes':MultinomialNB(),'Random Forest':RandomForestClassifier(n_estimators=250,random_state=42,class_weight='balanced')}
    results={}; fitted={}
    for name,clf in specs.items():
        pipe=Pipeline([('tfidf',TfidfVectorizer(stop_words='english',ngram_range=(1,2),sublinear_tf=True)),('clf',clf)])
        pipe.fit(X_train,y_train); pred=pipe.predict(X_test)
        results[name]={'accuracy':accuracy_score(y_test,pred),'precision':precision_score(y_test,pred,pos_label='fake',zero_division=0),'recall':recall_score(y_test,pred,pos_label='fake',zero_division=0),'f1':f1_score(y_test,pred,pos_label='fake',zero_division=0),'confusion_matrix':confusion_matrix(y_test,pred,labels=['genuine','fake']).tolist()}; fitted[name]=pipe
    selected=max(results,key=lambda n: results[n]['f1']); out=ROOT/'ml'/'artifacts'; out.mkdir(exist_ok=True)
    dump({'model':fitted[selected],'selected_model':selected,'labels':['genuine','fake']},out/'model.joblib')
    (out/'metrics.json').write_text(json.dumps({'selected_model':selected,'test_size':len(y_test),'training_size':len(y_train),'models':results},indent=2))
    print(json.dumps({'selected_model':selected,'test_size':len(y_test),'models':results},indent=2))
if __name__=='__main__': main()
