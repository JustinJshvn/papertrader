from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple


def compute_returns(equity: List[float]) -> List[float]:
    if len(equity) < 2:
        return []
    out: List[float] = []
    for i in range(1, len(equity)):
        prev = equity[i - 1]
        cur = equity[i]
        if prev == 0:
            out.append(0.0)
        else:
            out.append((cur - prev) / prev)
    return out


def max_drawdown(equity: List[float]) -> float:
    if not equity:
        return 0.0
    peak = equity[0]
    mdd = 0.0
    for x in equity:
        peak = max(peak, x)
        dd = (peak - x) / peak if peak != 0 else 0.0
        mdd = max(mdd, dd)
    return mdd


@dataclass
class EquityCurve:
    points: List[Tuple[float, float]]

    def values(self) -> List[float]:
        return [e for _, e in self.points]

    def times(self) -> List[float]:
        return [t for t, _ in self.points]
