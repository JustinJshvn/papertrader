from papertrader.broker import Broker
from papertrader.models import Candle, Order, OrderType, Side


def test_market_slippage_and_fee():
    b = Broker(fee_rate=0.001, slippage_bps=10.0)
    c = Candle(ts=0, open=100, high=101, low=99, close=100)

    o = b.submit(Order(side=Side.BUY, qty=2.0, order_type=OrderType.MARKET), ts=0)
    f = b.try_fill_market(c, o)

    assert abs(f.price - 100.1) < 1e-9
    assert abs(f.fee - (2.0 * 100.1 * 0.001)) < 1e-9


def test_limit_fill_conditions():
    b = Broker(fee_rate=0.0, slippage_bps=0.0)
    buy = b.submit(Order(side=Side.BUY, qty=1.0, order_type=OrderType.LIMIT, limit_price=95.0), ts=0)
    sell = b.submit(Order(side=Side.SELL, qty=1.0, order_type=OrderType.LIMIT, limit_price=105.0), ts=0)

    c1 = Candle(ts=1, open=100, high=104, low=96, close=101)
    fills = b.process_limits(c1)
    assert len(fills) == 0

    c2 = Candle(ts=2, open=101, high=106, low=94, close=103)
    fills = b.process_limits(c2)
    assert {f.order_id for f in fills} == {buy.id, sell.id}
