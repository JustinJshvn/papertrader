from __future__ import annotations
import csv
import math
import random
from dataclasses import dataclass
from typing import List, Protocol

from .models import Candle


class DataSource(Protocol):
    def load(self) -> List[Candle]:
        ...


@dataclass(frozen=True)
class CSVDataSource:
    path: str

    def load(self) -> List[Candle]:
        out: List[Candle] = []
        with open(self.path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                out.append(
                    Candle(
                        ts=float(row["ts"]),
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row.get("volume", 0.0) or 0.0),
                    )
                )
        if not out:
            raise ValueError("CSVDataSource loaded 0 rows.")
        return out


@dataclass(frozen=True)
class SyntheticDataSource:
    n: int = 2500
    start_price: float = 120.0
    seed: int = 7

    def load(self) -> List[Candle]:
        random.seed(self.seed)
        candles: List[Candle] = []
        price = self.start_price
        t = 0.0

        for i in range(self.n):
            drift = 0.00025
            cyc = 0.0022 * math.sin(i / 34.0)
            shock = random.gauss(0, 0.010)

            ret = drift + cyc + shock
            new_price = max(0.1, price * (1.0 + ret))

            o = price
            c = new_price
            hi = max(o, c) * (1.0 + abs(random.gauss(0, 0.003)))
            lo = min(o, c) * (1.0 - abs(random.gauss(0, 0.003)))
            vol = abs(random.gauss(1000, 250))

            candles.append(Candle(ts=t, open=o, high=hi, low=lo, close=c, volume=vol))
            price = new_price
            t += 1.0

        return candles
