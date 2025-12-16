from __future__ import annotations
from dataclasses import dataclass

from .models import Fill, Side


@dataclass
class Portfolio:
    starting_cash: float = 10_000.0
    cash: float = 10_000.0
    qty: float = 0.0
    avg_cost: float = 0.0
    realized_pnl: float = 0.0

    def __post_init__(self) -> None:
        self.cash = float(self.starting_cash)

    def equity(self, mark: float) -> float:
        return self.cash + self.qty * mark

    def unrealized_pnl(self, mark: float) -> float:
        if self.qty <= 0:
            return 0.0
        return (mark - self.avg_cost) * self.qty

    def apply_fill(self, fill: Fill) -> None:
        if fill.qty <= 0:
            raise ValueError("Fill qty must be > 0")

        if fill.side == Side.BUY:
            cost = fill.qty * fill.price + fill.fee
            if cost > self.cash + 1e-9:
                raise ValueError("Insufficient cash")
            new_qty = self.qty + fill.qty
            self.avg_cost = (
                (self.avg_cost * self.qty + fill.price * fill.qty) / new_qty
                if new_qty > 0
                else 0.0
            )
            self.qty = new_qty
            self.cash -= cost

        elif fill.side == Side.SELL:
            if fill.qty > self.qty + 1e-9:
                raise ValueError("Insufficient position")
            self.realized_pnl += (fill.price - self.avg_cost) * fill.qty - fill.fee
            self.qty -= fill.qty
            self.cash += fill.qty * fill.price - fill.fee
            if self.qty <= 1e-12:
                self.qty = 0.0
                self.avg_cost = 0.0

        else:
            raise ValueError("Unknown side")
