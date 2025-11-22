from typing import Dict, Any, Iterable


def _get_billed_amount(row: Dict[str, Any]) -> float:
    candidates = [
        "billed_amount",
        "Amount Billed",
        "amount billed",
        "amount_billed",
        "Amount",
    ]
    # prefer exact candidates (case-insensitive)
    lk = {k.lower(): k for k in row.keys()}
    for c in candidates:
        # check exact key
        if c in row and row[c] is not None:
            try:
                return float(row[c])
            except Exception:
                try:
                    return float(str(row[c]).replace(",", "").strip())
                except Exception:
                    continue
        # case-insensitive match
        if c.lower() in lk and row.get(lk[c.lower()]) is not None:
            try:
                return float(row.get(lk[c.lower()]))
            except Exception:
                try:
                    return float(str(row.get(lk[c.lower()])).replace(",", "").strip())
                except Exception:
                    continue
    # no billed-like key found: return 0.0 (do not try to interpret other numeric fields like patient_id)
    return 0.0


def _get_group_key(row: Dict[str, Any]) -> str:
    for k in row.keys():
        kl = k.lower()
        if "diag" in kl:
            return str(row.get(k))
        if "proc" in kl:
            return str(row.get(k))
    return "__global__"


def score_claim(row: Dict[str, Any], avg_charge_by_group: Dict[str, float]) -> int:
    billed = _get_billed_amount(row)
    group = _get_group_key(row)

    avg = None
    if group and group in avg_charge_by_group:
        try:
            avg = float(avg_charge_by_group[group])
        except Exception:
            avg = None

    if avg is None:
        numeric_avgs: Iterable[float] = [v for v in avg_charge_by_group.values() if isinstance(v, (int, float))]
        if numeric_avgs:
            avg = sum(numeric_avgs) / len(numeric_avgs)
        else:
            avg = 1.0

    if not avg or avg <= 0:
        ratio = 0.0
    else:
        ratio = billed / avg

    # map ratio to a bounded 0-100 score using a smooth saturating function
    # score = 100 * ratio / (ratio + 1) gives 0 @ ratio=0, 50 @ ratio=1, asymptotically 100
    try:
        # prefer a smooth saturating mapping but allow a high-ratio threshold to mark clear outliers
        R_MAX = 2.5
        if ratio >= R_MAX:
            raw_score = 100
        else:
            # scale the smooth function so that ratio == R_MAX maps to 100
            base = (ratio / (ratio + 1.0))
            scale = 1.0 / (R_MAX / (R_MAX + 1.0))
            raw_score = int(round(100.0 * base * scale))
    except Exception:
        raw_score = 0
    if raw_score < 0:
        raw_score = 0
    if raw_score > 100:
        raw_score = 100
    return raw_score
