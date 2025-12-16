# Trading Simulation (Python)

## Overview

This project is a **non-AI trading simulation** developed using Python. The application simulates a financial market using historical or synthetic price data and allows users to interactively place trades while observing portfolio performance in real time.

The system focuses on market replay, order execution, portfolio management, and performance analysis. It is designed to demonstrate object-oriented programming, modular software architecture, and deterministic algorithmic decision-making **without the use of artificial intelligence or machine learning**.

---

## Objectives

- Simulate realistic trading behavior in a controlled environment  
- Apply object-oriented design principles in a medium-scale Python project  
- Visualize market data and portfolio performance interactively  
- Implement and test deterministic trading mechanics  
- Practice software documentation, testing, and presentation  

---

## Features

- Market replay with play, pause, step, and speed control  
- Market and limit order execution  
- Portfolio management:
  - Cash balance  
  - Position size  
  - Average entry cost  
- Profit and loss tracking:
  - Realized PnL  
  - Unrealized PnL  
- Equity curve and maximum drawdown visualization  
- Interactive data visualization using **Matplotlib**  
- Trade log and performance export (CSV and PNG)  
- Fully deterministic, rule-based logic (no AI, no prediction models)

---

## Dependencies

- Python 3.x  
- Matplotlib  
- Pytest (for automated testing)

Install required dependencies using:

```bash
pip install matplotlib pytest
```

## How to Run

1. Ensure Python 3 is installed.  
2. Install the required dependencies.  
3. Navigate to the project root directory.  
4. Run the application using:
```
python -m papertrader.app
```

---

## Controls

### Market Replay
- **SPACE** — Play / Pause market replay  
- **RIGHT ARROW** — Advance one time step (one candle)  
- **+ / =** — Increase replay speed  
- **-** — Decrease replay speed  

### Trading Actions
- **B** — Market Buy (quantity = 1)  
- **S** — Market Sell (quantity = 1)  
- **Shift + B** — Market Buy (quantity = 5)  
- **Shift + S** — Market Sell (quantity = 5)  

### Limit Orders
- **L** — Enter limit order input mode  
- **0–9 / .** — Input limit price  
- **BACKSPACE** — Delete last character  
- **ENTER** — Submit limit order  

### Export
- **R** — Export:
  - `trades.csv` (trade history)  
  - `equity.png` (equity curve)

---

## Project Structure
papertrader/
app.py — Application entry point
datasource.py — Market data loading (CSV / synthetic)
market.py — Market replay and timing logic
broker.py — Order execution, fees, and slippage
portfolio.py — Portfolio and PnL management
models.py — Core data models (orders, fills, candles)
metrics.py — Performance calculations
ui_matplotlib.py — Visualization and user interaction
export.py — Data and report export utilities

tests/
test_portfolio.py — Portfolio logic tests
test_broker.py — Broker execution tests
test_metrics.py — Performance metric tests

---

## Testing Strategy

### Manual Testing
- Verified correct order execution for market and limit orders  
- Confirmed portfolio balance updates after trades  
- Tested replay controls (pause, step, speed adjustment)  
- Validated export outputs for trades and equity curve  

### Automated Testing
Automated tests were implemented using **Pytest** to verify:
- Portfolio profit and loss calculations  
- Broker execution logic, including fees and slippage  
- Limit order fill conditions  
- Performance metric calculations (returns and drawdown)  

Run tests using:
```
python -m pytest
```

---

## Design Overview

The system is structured using modular, object-oriented components:

- **MarketReplay** controls time progression and replay logic  
- **Broker** simulates order execution and transaction costs  
- **Portfolio** manages capital, positions, and PnL  
- **Metrics** computes performance statistics  
- **UI Layer** handles visualization and user interaction  

This separation of concerns improves readability, maintainability, and testability.

---

## Limitations

- No short selling or leverage (long-only simulation)  
- No real-time market data  
- No AI-based strategy or predictive modeling  

These limitations are intentional to maintain deterministic behavior and focus on core simulation mechanics.

---

## AI Usage Declaration

AI tools were used only for brainstorming, architectural discussion, and debugging assistance during early development stages.

All final implementation decisions, feature extensions, testing, documentation, and system integration were independently completed and verified by the author. No AI-generated code or content was submitted without substantial modification, validation, and understanding.

AI usage complied fully with the course policy regarding permitted and prohibited activities.

---

## Future Improvements

- Support for multiple assets  
- Candlestick chart visualization  
- Risk management tools (stop-loss, take-profit)  
- Advanced reporting and analytics  
- Session saving and replay bookmarks  