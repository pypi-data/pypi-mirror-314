"""
Strategy
========
"""

# Import necessary modules and classes from the TradeTide package
from TradeTide import BackTester, indicators, get_market_data, Strategy
from TradeTide import capital_management, risk_management


# Load historical market data for EUR/USD pair for the year 2023 and limit to 4000 data points
market_data = get_market_data('eur', 'usd', year=2023, time_span='3day', spread=0)

# Initialize a Moving Average Crossing indicator with specific window settings and minimum period
indicator_0 = indicators.BB()
indicator_1 = indicators.RMI()

strategy = Strategy(
    indicator_0, indicator_1
)

# Generate trading signals based on the market data
strategy.generate_signal(market_data)

# Plot the indicator signals overlaid on the market data
strategy.plot()

# Create the BackTester instance, linking it with the market data and chosen strategy
backtester = BackTester(market=market_data, strategy=strategy)

# Set up loss and profit management with specified stop loss and take profit percentages
risk = risk_management.DirectLossProfit(
    market=market_data,
    stop_loss='10pip',
    take_profit='10pip',
)

# Configure capital management strategy with initial capital, spread, and trading constraints
capital_management = capital_management.LimitedCapital(
    initial_capital=100_000,
    risk_management=risk,
    max_cap_per_trade=10_000,
    limit_of_positions=1,
    micro_lot=1_000
)

# Execute the backtest using the configured capital management strategy
backtester.backtest(capital_management=capital_management)

# %%
# Visualize the backtest results, showing the strategy's performance against the market price
backtester.plot(show_price=True)

# Calculate and display key performance metrics for the trading strategy
metrics = backtester.metrics


# Retrieve and print the final total value of the portfolio after completing the backtest
metrics.print()



# -
