from papertrader.models import Fill, Side
from papertrader.portfolio import Portfolio


def test_buy_sell_pnl():
    p = Portfolio(starting_cash=1000.0)

    p.apply_fill(Fill(ts=0, side=Side.BUY, qty=1.0, price=100.0, fee=0.0, order_id=1))
    assert abs(p.cash - 900.0) < 1e-9
    assert abs(p.qty - 1.0) < 1e-9
    assert abs(p.avg_cost - 100.0) < 1e-9

    p.apply_fill(Fill(ts=1, side=Side.SELL, qty=1.0, price=120.0, fee=0.0, order_id=2))
    assert abs(p.qty - 0.0) < 1e-9
    assert abs(p.cash - 1020.0) < 1e-9
    assert abs(p.realized_pnl - 20.0) < 1e-9
