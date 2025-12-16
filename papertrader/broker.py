from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from .models import Candle, Fill, Order, OrderType, Side


@dataclass
class Broker:
    fee_rate: float = 0.0005
    slippage_bps: float = 2.0
    _next_id: int = 1
    open_limit_orders: List[Order] = field(default_factory=list)

    def _fee(self, notional: float) -> float:
        return notional * self.fee_rate

    def _slip(self) -> float:
        return self.slippage_bps / 10_000.0

    def submit(self, order: Order, ts: float) -> Order:
        order.id = self._next_id
        self._next_id += 1
        order.created_ts = ts

        if order.order_type == OrderType.LIMIT:
            if order.limit_price is None:
                raise ValueError("LIMIT requires limit_price")
            self.open_limit_orders.append(order)

        return order

    def try_fill_market(self, candle: Candle, order: Order) -> Fill:
        mid = candle.close
        slip = self._slip()
        px = mid * (1.0 + slip) if order.side == Side.BUY else mid * (1.0 - slip)
        fee = self._fee(order.qty * px)
        return Fill(ts=candle.ts, side=order.side, qty=order.qty, price=px, fee=fee, order_id=order.id or -1)

    def try_fill_limit_on_candle(self, candle: Candle, order: Order) -> Optional[Fill]:
        p = order.limit_price
        if p is None:
            return None

        if order.side == Side.BUY:
            if candle.low <= p:
                px = p
            else:
                return None
        else:
            if candle.high >= p:
                px = p
            else:
                return None

        fee = self._fee(order.qty * px)
        return Fill(ts=candle.ts, side=order.side, qty=order.qty, price=px, fee=fee, order_id=order.id or -1)

    def process_limits(self, candle: Candle) -> List[Fill]:
        fills: List[Fill] = []
        remaining: List[Order] = []
        for o in self.open_limit_orders:
            f = self.try_fill_limit_on_candle(candle, o)
            if f is None:
                remaining.append(o)
            else:
                fills.append(f)
        self.open_limit_orders = remaining
        return fills
