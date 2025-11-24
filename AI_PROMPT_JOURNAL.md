# AI Prompt Journal

This file stores the exact prompts and LLM outputs used during development for traceability.

How to use
- Each entry contains: prompt, model used, date, and the raw output. Paste the exact LLM output under each prompt.

1) Prompt: "Propose a simple, explainable heuristic to assign a fraud likelihood score (0-100) for healthcare claims using fields like billed_amount, procedure_code, and provider_id. Return a clear formula and edge-case handling."
Output:
```
Core Idea

A claim is more suspicious if:
 - The billed amount is unusually high for that procedure.
 - The same provider frequently bills above normal.
 - Certain high-risk procedures appear unusually often.

Final Scoring Formula
Let:
B = billed_amount
P_avg = average billed_amount for that procedure_code
Prov_avg = average billed_amount by that provider_id
Proc_freq = number of times this procedure appears per provider 

ProcedureScore = min(50, (B / P_avg) * 50)
ProviderScore = min(30, (B / Prov_avg) * 30)
FrequencyScore = 0 if Proc_freq < 5
FrequencyScore = 10 if 5 ≤ Proc_freq < 10
FrequencyScore = 20 if Proc_freq ≥ 10

Fraud Score = min(100, ProcedureScore + ProviderScore + FrequencyScore)
```

2) Prompt: "Generate a step-by-step plan to follow to build the NHIS Fraud Auditor Dashboard MVP within the assignment constraints (8 hours), plus concrete implementation tips, code snippets, deployment commands, testing checklist"
Output:
```
Recommended approach (fastest, robust)

Stack (Rapid + production-feasible): Python + FastAPI (backend API) + SQLite (local) or Redis for TTL + Pandas for ingestion + React (create-react-app) for frontend with Chart.js or Recharts.

Alternative fastest (single repo, minimal dev): Streamlit app (UI + logic in one place) — great if you need to finish quickly and deploy to Streamlit Cloud. But if you need REST endpoints / and /claims, use FastAPI (small code) + a tiny React UI.

Deploy to: Render / Railway for backend, Vercel for frontend (or single Render for both). Dockerize if you prefer.
```

3) Prompt: "Recommend a minimal FastAPI project structure for an MVP that serves a dashboard and a paginated claims API; include endpoints and data flow."
Output:
```
apeiro_fraud_mvp/
├── app/
│   ├── main.py                # FastAPI app, mounts routers, static, templates
│   ├── heuristic.py           # Business logic (fraud score, filters)
├── scripts/
│   └── load_data.py           # Loads data from *.csv to SQLite
├── templates/
│   └── dashboard.html         # Basic HTML UI with JS fetching /api/claims
├── tests/
│   └── test_scoring.py        # Unit test the claims api
├── data.db                    # SQLite Database layer
└── README.md
```

4) Prompt: "Write a pytest unit test for the fraud scoring function that verifies low/medium/high buckets and edge-case values."
Output:
```
from app.heuristic import score_claim

def test_score_basic():
    avg = {'PROC1': 100.0}
    claim = {'billed_amount': 250, 'procedure_code': 'PROC1'}
    s = score_claim(claim, avg)
    assert isinstance(s, int)
    assert 0 <= s <= 100
    assert s == 100  # 250% -> clamped to 100


def test_score_zero_avg():
    avg = {}
    claim = {'billed_amount': 50, 'procedure_code': None}
    s = score_claim(claim, avg)
    assert s >= 0 and s <= 100
```

5) Prompt: "Compare SQLite vs Postgres for a prototype claims auditor dashboard and recommend which to use for quick MVP deployment."
Model: <model>
Date: <YYYY-MM-DD>
Output:
```
1. SQLite
Pros
---
 - Zero configuration – no server setup required
 - File-based, lightweight, very fast for small/medium datasets
 - Perfect for local development and demos
 - Excellent for rapid prototyping
 - Minimal operational overhead
 - Easy to bundle with FastAPI

Cons
---
 - Limited concurrency handling
 - Not ideal for high write volume or multi-user production loads
 - No native user roles or complex analytics features

 2. PostgreSQL

Pros
---
 - Enterprise-grade relational database
 - Strong concurrency and transaction support
 - Better for production-scale usage
 - Supports advanced analytics (window functions, indexing, partitions)
 - Scales well with multiple users and services

Cons
---
 - Requires setup and maintenance
 - Slightly heavier configuration
 - Slower to initialize for quick MVPs
 - Overkill for a minimal proof-of-concept
```
