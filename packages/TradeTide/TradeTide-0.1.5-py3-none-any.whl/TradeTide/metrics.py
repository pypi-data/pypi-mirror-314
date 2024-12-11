#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from typing import NoReturn

import pandas
import numpy
from datetime import timedelta
from tabulate import tabulate


class Metrics():
    def __init__(self, portfolio: pandas.DataFrame, position_list: list, capital_management, market: pandas.DataFrame):
        self.portfolio = portfolio
        self.position_list = position_list
        self.capital_management = capital_management
        self.market = market

        self.calculate_performance_metrics()

    def get_final_portfolio_value(self) -> float:
        """
        Retrieves the final total value of the portfolio at the end of the backtesting period.

        This method calculates the final value of the portfolio, considering all open and closed positions, and prints
        this value to the console. It is a useful metric for assessing the absolute performance of the trading strategy.

        Returns:
            float: The final total value of the portfolio, represented as a monetary amount.

        Note:
            This method should be called after completing the backtest to ensure the portfolio contains the final trading results.
        """
        final_portfolio_value = self.portfolio['total'].iloc[-1]

        print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")

        return final_portfolio_value

    def calculate_total_return(self) -> float:
        """
        Calculates the total return of the trading strategy.

        Returns:
            float: The total return as a percentage.
        """
        return (self.portfolio['total'].iloc[-1] / self.capital_management.initial_capital) - 1

    def calculate_annualized_return(self, total_return: float) -> float:
        """
        Calculates the annualized return given the total return.

        Args:
            total_return (float): The total return of the strategy.

        Returns:
            float: The annualized return as a percentage.
        """
        trading_seconds = self.market.attrs['time_span'].seconds

        if trading_seconds == 0:
            return numpy.nan

        year = timedelta(days=365)

        return ((1 + total_return) ** (year.total_seconds() / trading_seconds)) - 1

    def calculate_max_drawdown(self) -> float:
        """
        Calculates the maximum drawdown of the portfolio.

        Returns:
            float: The maximum drawdown as a percentage.
        """
        rolling_max = self.portfolio['total'].cummax()
        drawdown = self.portfolio['total'] / rolling_max - 1.0
        return drawdown.min()

    def calculate_sharpe_ratio(self) -> float:
        """
        Calculates the Sharpe ratio, which measures the performance of an investment
        compared to a risk-free asset, after adjusting for its risk.

        Returns:
            float: The Sharpe ratio. A higher value indicates better risk-adjusted return.
        """
        daily_returns = self.portfolio['returns']
        return daily_returns.mean() / daily_returns.std() * numpy.sqrt(252)

    def calculate_win_loss_ratio(self) -> float:
        """
        Calculates the win-loss ratio of the trading positions.

        Returns:
            float: The ratio of wins to losses. A value of numpy.inf indicates no losses.
        """
        wins = sum(1 for pos in self.position_list if pos.is_win)
        losses = sum(1 for pos in self.position_list if not pos.is_win)

        return wins / losses if losses != 0 else numpy.inf

    def calculate_equity(self) -> float:
        """
        Calculates the final equity of the portfolio.

        Returns:
            float: The ending equity value.
        """
        return self.portfolio['total'].iloc[-1]

    def calculate_duration(self) -> int:
        """
        Calculates the duration of the backtest in days.

        Returns:
            int: The duration of the backtest.
        """
        return (self.market.date.iloc[-1] - self.market.date.iloc[0])

    def calculate_volatility(self) -> float:
        """
        Calculates the volatility of daily returns, which measures the dispersion of returns.

        Returns:
            float: The annualized volatility as a percentage.
        """
        return self.portfolio['returns'].std() * numpy.sqrt(252)

    def calculate_sortino_ratio(self) -> float:
        """
        Calculates the Sortino ratio, similar to the Sharpe ratio but only considers downside volatility,
        which provides a better measure of the risk-adjusted return for asymmetrical return distributions.

        Returns:
            float: The Sortino ratio. A higher value indicates a better return per unit of bad risk taken.
        """
        daily_returns = self.portfolio['returns']
        negative_returns = daily_returns[daily_returns < 0]
        downside_std = numpy.sqrt((negative_returns ** 2).mean()) * numpy.sqrt(252)
        annualized_return = self.calculate_annualized_return(self.calculate_total_return())
        return annualized_return / downside_std if downside_std != 0 else numpy.inf

    def calculate_performance_metrics(self) -> dict:
        """
        Calculates and compiles key performance metrics for the trading strategy.

        This includes total return, annualized return, maximum drawdown, Sharpe ratio, Sortino ratio,
        win-loss ratio, equity, duration, and volatility. These metrics quantify the strategy's
        effectiveness and risk characteristics.

        Returns:
            dict: A dictionary containing all calculated performance metrics.
        """
        if self.portfolio is None:
            print("Backtest the strategy first before calculating performance metrics.")
            return {}

        total_return = self.calculate_total_return()
        annualized_return = self.calculate_annualized_return(total_return)
        max_drawdown = self.calculate_max_drawdown()
        sharpe_ratio = self.calculate_sharpe_ratio()
        sortino_ratio = self.calculate_sortino_ratio()
        win_loss_ratio = self.calculate_win_loss_ratio()
        equity = self.calculate_equity()
        duration = self.calculate_duration()
        volatility = self.calculate_volatility()

        self.performance_dict = {
            "Start Date": self.market.date.iloc[0],
            "Stop Date": self.market.date.iloc[-1],
            "Duration": duration,
            "Reward-Risk ratio": self.capital_management.risk_management.reward_risk_ratio,
            "Returns": f"{total_return * 100:.2f}%",
            "Returns [annualized]": f"{annualized_return * 100:.2f}%",
            "Maximum drawdown": f"{max_drawdown * 100:.2f}%",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Sortino Ratio": f"{sortino_ratio:.2f}",
            "Number of Trades": f"{len(self.position_list)}",
            "Win-Loss Ratio": f"{win_loss_ratio:.2f}",
            "Equity": f"${equity:,.2f}",
            "Volatility": f"{volatility * 100:.2f}%"
        }

        return self.performance_dict

    def print(self) -> NoReturn:

        property_dict = {
            "Property": self.performance_dict.keys(), "value": self.performance_dict.values()
        }

        table = tabulate(
            property_dict,
            headers="keys"
        )

        print(table)

# -
