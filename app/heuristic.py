from typing import Dict, Any, Iterable


def _get_billed_amount(row: Dict[str, Any]) -> float:
    candidates = [
        "billed_amount",
        "Amount Billed",
        "amount billed",
        "amount_billed",
        "Amount",
    ]
    for k in candidates:
        if k in row and row[k] is not None:
            try:
                return float(row[k])
            except Exception:
                try:
                    return float(str(row[k]).replace(",", ""))
                except Exception:
                    continue
    for v in row.values():
        try:
            return float(v)
        except Exception:
            continue
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

    raw_score = int(round(100 * ratio))
    if raw_score < 0:
        raw_score = 0
    if raw_score > 100:
        raw_score = 100
    return raw_score
