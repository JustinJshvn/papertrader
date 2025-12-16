from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .broker import Broker
from .export import export_equity_png, export_fills_csv
from .market import MarketReplay
from .metrics import EquityCurve, max_drawdown
from .models import Candle, Order, OrderType, Side
from .portfolio import Portfolio

import matplotlib as mpl

mpl.rcParams["keymap.save"] = []
mpl.rcParams["keymap.zoom"] = []
mpl.rcParams["keymap.pan"] = []
mpl.rcParams["keymap.fullscreen"] = []
mpl.rcParams["keymap.quit"] = []
mpl.rcParams["keymap.grid"] = []
mpl.rcParams["keymap.yscale"] = []
mpl.rcParams["keymap.xscale"] = []
mpl.rcParams["keymap.home"] = []
mpl.rcParams["keymap.back"] = []
mpl.rcParams["keymap.forward"] = []


@dataclass
class UIState:
    last_key: Optional[str] = None
    limit_mode: bool = False
    pending_limit_price: str = ""


class MatplotlibUI:
    def __init__(self, market: MarketReplay, broker: Broker, portfolio: Portfolio):
        self.market = market
        self.broker = broker
        self.portfolio = portfolio

        self.fills = []
        self.equity_curve = EquityCurve(points=[])
        self.state = UIState()

        self.lookback = 250

        self.fig = plt.figure(figsize=(11, 6))
        self.ax_price = self.fig.add_axes([0.06, 0.20, 0.62, 0.74])
        self.ax_info = self.fig.add_axes([0.72, 0.20, 0.26, 0.74])
        self.ax_help = self.fig.add_axes([0.06, 0.04, 0.92, 0.12])

        self.ax_info.axis("off")
        self.ax_help.axis("off")

        c = self.market.current()
        self.equity_curve.points.append((c.ts, self.portfolio.equity(c.close)))

        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

    def on_key(self, event):
        k = event.key
        self.state.last_key = k

        if k == " ":
            self.market.paused = not self.market.paused
            return

        if k == "right":
            self._one_tick()
            return

        if k in ["+", "="]:
            self.market.speed = min(self.market.speed + 1, 30)
            return

        if k == "-":
            self.market.speed = max(self.market.speed - 1, 1)
            return

        if k == "l":
            self.state.limit_mode = not self.state.limit_mode
            self.state.pending_limit_price = ""
            return

        if self.state.limit_mode and (k.isdigit() or k == "." or k == "backspace" or k == "enter"):
            if k == "backspace":
                self.state.pending_limit_price = self.state.pending_limit_price[:-1]
            elif k == "enter":
                pass
            else:
                self.state.pending_limit_price += k
            return

        if k == "b":
            self._submit_market(Side.BUY, 1.0)
            return

        if k == "s":
            self._submit_market(Side.SELL, 1.0)
            return

        if k == "shift+b":
            self._submit_market(Side.BUY, 5.0)
            return

        if k == "shift+s":
            self._submit_market(Side.SELL, 5.0)
            return

        if k == "enter" and self.state.limit_mode:
            self._submit_limit_from_buffer()
            return

        if k == "r":
            self._export()
            return

    def _submit_market(self, side: Side, qty: float):
        c = self.market.current()
        o = self.broker.submit(Order(side=side, qty=qty, order_type=OrderType.MARKET), ts=c.ts)
        f = self.broker.try_fill_market(c, o)
        self.portfolio.apply_fill(f)
        self.fills.append(f)

    def _submit_limit_from_buffer(self):
        c = self.market.current()
        try:
            p = float(self.state.pending_limit_price)
        except ValueError:
            return
        side = Side.BUY if self.state.last_key != "enter" else Side.BUY
        o = self.broker.submit(Order(side=side, qty=1.0, order_type=OrderType.LIMIT, limit_price=p), ts=c.ts)
        self.state.limit_mode = False
        self.state.pending_limit_price = ""

    def _one_tick(self):
        c = self.market.current()

        eq = self.portfolio.equity(c.close)
        self.equity_curve.points.append((c.ts, eq))

        fills = self.broker.process_limits(c)
        for f in fills:
            self.portfolio.apply_fill(f)
            self.fills.append(f)

        if self.market.can_step():
            self.market.step()

    def _export(self):
        ts = self.equity_curve.times()
        eq = self.equity_curve.values()
        export_fills_csv("trades.csv", self.fills)
        export_equity_png("equity.png", ts, eq, title="Equity Curve (PaperTrader)")
        return

    def _render(self):
        c = self.market.current()
        start = max(0, self.market.i - self.lookback)
        candles = self.market.candles[start : self.market.i + 1]
        closes = [x.close for x in candles]
        xs = list(range(len(closes)))

        self.ax_price.clear()
        self.ax_price.plot(xs, closes)
        self.ax_price.set_title("Price (close)")
        self.ax_price.set_xlabel("Index (lookback)")
        self.ax_price.set_ylabel("Price")

        self.ax_info.clear()
        self.ax_info.axis("off")

        eq = self.portfolio.equity(c.close)
        unreal = self.portfolio.unrealized_pnl(c.close)
        mdd = max_drawdown(self.equity_curve.values()) if self.equity_curve.points else 0.0

        info_lines = [
            "PaperTrader (Non-AI)",
            "",
            f"i: {self.market.i}/{len(self.market.candles)-1}",
            f"ts: {c.ts:.0f}",
            f"price: {c.close:,.2f}",
            "",
            f"cash: {self.portfolio.cash:,.2f}",
            f"qty: {self.portfolio.qty:.4f}",
            f"avg_cost: {self.portfolio.avg_cost:,.2f}",
            f"unreal: {unreal:,.2f}",
            f"realized: {self.portfolio.realized_pnl:,.2f}",
            f"equity: {eq:,.2f}",
            f"maxDD: {mdd*100:.2f}%",
            "",
            f"paused: {self.market.paused}",
            f"speed: {self.market.speed}x",
            f"open limits: {len(self.broker.open_limit_orders)}",
            "",
            f"limit mode: {self.state.limit_mode}",
            f"limit buf: {self.state.pending_limit_price}",
        ]

        y = 0.98
        for line in info_lines:
            self.ax_info.text(0.02, y, line, va="top", fontsize=10)
            y -= 0.06 if line != "" else 0.04

        self.ax_help.clear()
        self.ax_help.axis("off")
        help_text = (
            "SPACE play/pause | RIGHT step | B/S market 1 | Shift+B/Shift+S market 5 | "
            "+/- speed | L limit input (type price, ENTER) | R export trades.csv + equity.png"
        )
        self.ax_help.text(0.01, 0.65, help_text, fontsize=10)

    def run(self):
        def tick(_):
            if not self.market.paused:
                for _ in range(min(self.market.speed, 5)):
                    self._one_tick()
            self._render()

        self._render()  # draw once immediately
        self.ani = FuncAnimation(self.fig, tick, interval=50)  # IMPORTANT: store it
        plt.show()