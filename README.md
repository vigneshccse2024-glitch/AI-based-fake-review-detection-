# AI-Based Fake Review Detection System

A beginner-friendly final-year project that classifies review text as **Genuine** or **Potentially Fake** using TF-IDF features and machine-learning classifiers. It includes a Flask web application, SQLite database, secure authentication, review history, admin dashboard, model evaluation, downloadable CSV reports, and a reproducible training pipeline.

> **Important:** A text classifier provides an estimate based on learned patterns. It is not proof that a reviewer or review is deceptive. Use the prediction as one signal alongside source verification and other evidence.

## Features

- User registration, login, logout, and password hashing
- Review detection with calibrated confidence score
- Suspicious-pattern explanation (promotional language, repetition, excessive punctuation, short text, etc.)
- Review history and CSV download
- Admin dashboard with counts, recent analyses, and model metrics
- TF-IDF + Logistic Regression, Multinomial Naive Bayes, and Random Forest comparison
- SQLite database through SQLAlchemy
- Responsive blue/purple interface
- Architecture, data-flow, and UML diagrams in `docs/`

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python ml/train_model.py
python seed_admin.py
python run.py
```

Open http://127.0.0.1:5000. The demo admin account created by `seed_admin.py` is:

- Email: `admin@example.com`
- Password: `Admin@12345`

Change this password before deployment.

## Training with your own data

The included `data/reviews.csv` is a small educational sample, not a benchmark dataset. For a serious study, use a properly sourced and licensed labeled dataset with columns `text` and `label`, where labels are `genuine` or `fake`.

```bash
python ml/train_model.py --data data/reviews.csv
```

The script prints actual holdout accuracy, precision, recall, F1, confusion matrix, and the selected model. It writes artifacts to `ml/artifacts/`. The application will refuse to predict if the model artifact is missing, so training is explicit and reproducible.

## Project structure

```text
app/                 Flask application package, templates, CSS, JS
 data/reviews.csv    Small educational labeled dataset
 ml/train_model.py   Training and evaluation script
 ml/artifacts/       Generated model and metrics (after training)
 docs/                Mermaid architecture, DFD, UML, and report outline
tests/               Basic application tests
run.py               Development entry point
seed_admin.py        Creates the admin user
```

## Testing

```bash
pytest -q
```

Manual cases to try include genuine product experiences, promotional reviews, short text, long text, spelling mistakes, and repeated words. Record actual results from your trained model; do not substitute expected labels for measured results.

## Responsible-use notes

The classifier may reflect dataset bias, domain shift, and writing-style correlations. Do not use it as the sole basis for banning users, denying refunds, or making legal or employment decisions. Store only data necessary for the project, protect credentials, and obtain consent for any real-world review data.
