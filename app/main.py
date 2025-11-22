from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import sqlite3
from pathlib import Path
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.heuristic import score_claim

DB = Path(__file__).resolve().parents[1] / "data.db"
TEMPLATES = Path(__file__).resolve().parents[1] / "templates"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES)),
    autoescape=select_autoescape(["html", "xml"]),
)

app = FastAPI()


def get_db_conn():
    if not DB.exists():
        raise RuntimeError("Database not found. Run scripts/load_data.py first.")
    return sqlite3.connect(str(DB))


@app.get("/", response_class=HTMLResponse)
def dashboard():
    """Render a simple dashboard page."""
    # small metrics computed from DB
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM claims")
    total = cur.fetchone()[0]
    # detect billed-amount column name
    cur.execute("PRAGMA table_info(claims)")
    cols = [r[1] for r in cur.fetchall()]
    billed_candidates = [
        "billed_amount",
        "Amount Billed",
        "AMOUNT BILLED",
        "amount billed",
        "Amount",
        "AMOUNT",
        "amount_billed",
    ]
    billed_col = None
    for c in billed_candidates:
        if c in cols:
            billed_col = c
            break
    if billed_col is None:
        lower_map = {col.lower(): col for col in cols}
        for key in ("billed", "amount", "amt"):
            if key in lower_map:
                billed_col = lower_map[key]
                break

    if billed_col:
        safe_col = '"' + billed_col.replace('"', '""') + '"'
        try:
            cur.execute(f"SELECT AVG({safe_col}) FROM claims")
            avg_charge = cur.fetchone()[0] or 0
        except Exception:
            avg_charge = 0
        try:
            cur.execute(f"SELECT {safe_col} FROM claims")
            billed = [r[0] for r in cur.fetchall() if r[0] is not None]
        except Exception:
            billed = []
    else:
        avg_charge = 0
        billed = []
    conn.close()

    template = env.get_template("dashboard.html")
    return template.render(total=total, avg_charge=avg_charge, billed=billed)


@app.get("/claims", response_class=HTMLResponse)
def claims_page():
    """Render the claims review page."""
    template = env.get_template("claims.html")
    return template.render()


@app.get("/api/claims")
def api_claims(q: str = Query(None), limit: int = 50, offset: int = 0):
    conn = get_db_conn()
    cur = conn.cursor()
    sql = "SELECT rowid, * FROM claims"
    params: List = []
    if q:
        sql += " WHERE diagnosis LIKE ? OR patient_id LIKE ?"
        params += [f"%{q}%", f"%{q}%"]
    sql += " LIMIT ? OFFSET ?"
    params += [limit, offset]
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    raw_rows = [dict(zip(cols, r)) for r in cur.fetchall()]

    # normalize keys to canonical names used by the UI

    def normalize_row(raw: Dict) -> Dict:
        normalized = {}
        # lower-key map
        lk = {k.lower(): k for k in raw.keys()}

        def pick(*candidates):
            for c in candidates:
                if c in raw and raw[c] is not None:
                    return raw[c]
                if c.lower() in lk and raw.get(lk[c.lower()]) is not None:
                    return raw.get(lk[c.lower()])
            return None

        normalized['rowid'] = raw.get('rowid') or raw.get('id')
        # Prefer exact header matches commonly found in datasets
        # Map 'Patient ID' -> patient_id (case-insensitive) and 'Amount Billed' -> billed_amount
        normalized['patient_id'] = pick('patient_id', 'Patient ID', 'patient', 'pat_id')
        # procedure_code is optional for this dataset; do not force a placeholder
        normalized['procedure_code'] = pick('procedure_code', 'proc_code', 'procedure')
        normalized['billed_amount'] = pick('billed_amount', 'Amount Billed', 'amount_billed', 'amount', 'amt') or 0
        normalized['diagnosis'] = pick('diagnosis', 'DIAGNOSIS', 'diag', 'diagnosis_code')
        normalized['age'] = pick('age', 'patient_age', 'age_years')
        normalized['gender'] = pick('gender', 'GENDER', 'sex')
        # capture FRAUD_TYPE column if present
        normalized['fraud_type'] = pick('fraud_type', 'FRAUD_TYPE')

        # include original keys as fallback
        for k, v in raw.items():
            if k not in normalized:
                normalized[k] = v
        return normalized

    rows = [normalize_row(r) for r in raw_rows]
    conn.close()
    # compute simple avg per procedure (naively)
    avg_by_proc: Dict[str, float] = {}
    try:
        # compute averages from normalized rows
        df = rows
        sums = {}
        counts = {}
        for r in df:
            proc = r.get('procedure_code')
            try:
                amt = float(r.get('billed_amount') or 0)
            except Exception:
                amt = 0
            if proc is None:
                continue
            sums[proc] = sums.get(proc, 0) + amt
            counts[proc] = counts.get(proc, 0) + 1
        for k in sums:
            avg_by_proc[k] = sums[k] / counts[k]
    except Exception:
        avg_by_proc = {}

    for r in rows:
        r["fraud_score"] = score_claim(r, avg_by_proc)
    return {"items": rows, "count": len(rows)}
