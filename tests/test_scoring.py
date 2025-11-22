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
