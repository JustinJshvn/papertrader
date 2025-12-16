from __future__ import annotations
import csv
from dataclasses import dataclass
from typing import List

from .models import Fill


def export_fills_csv(path: str, fills: List[Fill]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts", "side", "qty", "price", "fee", "order_id"])
        for x in fills:
            w.writerow([x.ts, x.side.value, x.qty, x.price, x.fee, x.order_id])


def export_equity_png(path: str, ts: List[float], eq: List[float], title: str = "Equity Curve") -> None:
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(ts, eq)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
