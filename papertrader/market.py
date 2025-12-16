from __future__ import annotations
from dataclasses import dataclass
from typing import List

from .models import Candle


@dataclass
class MarketReplay:
    candles: List[Candle]
    i: int = 0
    speed: int = 1
    paused: bool = True

    def __post_init__(self) -> None:
        if len(self.candles) < 50:
            raise ValueError("Need at least 50 candles.")

    def current(self) -> Candle:
        return self.candles[self.i]

    def can_step(self) -> bool:
        return self.i < len(self.candles) - 1

    def step(self) -> Candle:
        self.i = min(self.i + self.speed, len(self.candles) - 1)
        return self.current()
