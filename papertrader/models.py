from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Candle:
    ts: float
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


@dataclass
class Order:
    side: Side
    qty: float
    order_type: OrderType
    limit_price: float | None = None
    created_ts: float | None = None
    id: int | None = None


@dataclass(frozen=True)
class Fill:
    ts: float
    side: Side
    qty: float
    price: float
    fee: float
    order_id: int
