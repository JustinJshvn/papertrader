from __future__ import annotations
import sys

from .broker import Broker
from .datasource import CSVDataSource, SyntheticDataSource
from .market import MarketReplay
from .portfolio import Portfolio
from .ui_matplotlib import MatplotlibUI


def main():
    if len(sys.argv) > 1:
        candles = CSVDataSource(sys.argv[1]).load()
    else:
        candles = SyntheticDataSource().load()

    market = MarketReplay(candles=candles)
    broker = Broker()
    portfolio = Portfolio(starting_cash=10_000.0)

    ui = MatplotlibUI(market=market, broker=broker, portfolio=portfolio)
    ui.run()


if __name__ == "__main__":
    main()
