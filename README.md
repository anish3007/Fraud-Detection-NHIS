# Fraud-Detection-NHIS
NHIS Claims Auditor Dashboard (MVP)

Quick start

1. create venv and install deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. load CSV into SQLite

```bash
python3 scripts/load_data.py path/to/claims.csv
```

3. run the app

```bash
uvicorn app.main:app --reload
```

AI Prompt Journal (placeholder)

This repository contains a minimal web application (MVP) for auditing NHIS claims and assigning a Fraud Likelihood Score to each claim.

Assignment brief (excerpt): The NHIS Fraud Auditor Dashboard Assignment — build a minimal, functional dashboard that ingests the NHIS claims CSV, implements a simple explainable heuristic to score claims (0-100), and provides views for overall metrics and claim review. See `APEIRO_ASSIGNMENT.txt` for full requirements.

- Will include 5 best prompts and their uses (scoring function, debugging, schema design, test generation, architecture decision).

Architecture decision

- Using FastAPI + SQLite for a zero-admin MVP; switch to Postgres if scaling beyond prototype.
