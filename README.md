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

AI Prompt Journal

Below are the five most useful prompts used while building this MVP and a short note on how each response was used.

1) "Propose a simple, explainable heuristic to assign a fraud likelihood score (0-100) for healthcare claims using fields like billed_amount, procedure_code, and provider_id. Return a clear formula and edge-case handling." — Used to define the initial Fraud Likelihood Score heuristic and edge-case rules.

2) "Generate a Python function that implements the heuristic: inputs are a claim row dict, and output is an integer score between 0 and 100. Include docstring and unit-test example." — Used to produce the scoring function and a unit test scaffold.

3) "Recommend a minimal FastAPI project structure for an MVP that serves a dashboard and a paginated claims API; include endpoints and data flow." — Used to design the `app/` layout and API endpoints.

4) "Write a pytest unit test for the fraud scoring function that verifies low/medium/high buckets and edge-case values." — Used to generate the test in `tests/test_scoring.py`.

5) "Compare SQLite vs Postgres for a prototype claims auditor dashboard and recommend which to use for quick MVP deployment." — Used to justify SQLite for local zero-admin prototype and to document the tradeoffs.

AI-generated test prompt example

Prompt: "Write a pytest function that asserts the fraud_score function returns 0 for a legitimate small claim, >75 for a clearly suspicious claim, and handles missing billed_amount by returning 0." — The generated test was adapted and included in `tests/test_scoring.py`.

Notes

- Prompts were iteratively refined (temperature, constraints, and expected return types) to produce concise, testable code snippets.
- The final submission will include the exact prompts used and the final LLM outputs in the repository `README` before delivery.
