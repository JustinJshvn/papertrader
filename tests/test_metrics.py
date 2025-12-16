from papertrader.metrics import compute_returns, max_drawdown


def test_returns():
    eq = [100.0, 110.0, 99.0]
    r = compute_returns(eq)
    assert len(r) == 2
    assert abs(r[0] - 0.10) < 1e-9
    assert abs(r[1] - (-0.10)) < 1e-9


def test_max_drawdown():
    eq = [100, 120, 110, 130, 90]
    dd = max_drawdown(eq)
    assert abs(dd - (40/130)) < 1e-9
