from pathlib import Path
import json, re
import joblib

ARTIFACTS = Path(__file__).resolve().parents[1] / 'ml' / 'artifacts'

def explain(text):
    lower = text.lower(); flags = []
    promotional = ['buy now','best ever','five stars','limited time','must buy','click','guaranteed','amazing']
    hits = [p for p in promotional if p in lower]
    if hits: flags.append('Promotional phrases detected: ' + ', '.join(hits[:4]))
    if re.search(r'([!?])\1+', text): flags.append('Repeated punctuation detected')
    words = re.findall(r"\b\w+\b", lower)
    if len(words) < 8: flags.append('Very short review')
    if words and len(set(words))/len(words) < 0.55: flags.append('High word repetition')
    if text.count('!') >= 3: flags.append('Many exclamation marks')
    return flags or ['No simple warning pattern detected; interpret the model output cautiously.']

def predict(text):
    model_path = ARTIFACTS / 'model.joblib'
    if not model_path.exists(): raise FileNotFoundError('Model not trained. Run: python ml/train_model.py')
    bundle = joblib.load(model_path); model = bundle['model']
    pred = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    classes = list(model.classes_)
    confidence = float(max(probabilities))
    label = 'Potentially Fake' if str(pred).lower() == 'fake' else 'Genuine'
    return label, confidence, explain(text)

def metrics():
    p = ARTIFACTS / 'metrics.json'
    return json.loads(p.read_text()) if p.exists() else {}
