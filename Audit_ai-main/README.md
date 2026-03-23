# AuditAI — Anomaly-Driven Audit Assistant

Detects suspicious journal entries using
rule-based detection and ML (K-Means + DBSCAN).

## Team
- Member 1: [Name] — Database
- Member 2: [Name] — Flask API
- Member 3: [Name] — K-Means ML
- Member 4: [Name] — DBSCAN + Risk Scoring
- Member 5: [Name] — React Frontend
- Member 6: [Name] — Charts + Rules

## How to Run

### Backend
    cd backend
    python -m venv venv
    venv\Scripts\activate     # Windows
    source venv/bin/activate  # Mac/Linux
    pip install -r requirements.txt
    python database.py
    python seed_data.py
    python app.py

### Frontend
    cd frontend
    npm install
    npm start

Open http://localhost:3000 in browser.