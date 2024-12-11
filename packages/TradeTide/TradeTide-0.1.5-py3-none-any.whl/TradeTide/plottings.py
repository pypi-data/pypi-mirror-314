#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import matplotlib.pyplot as plt
import pandas
from TradeTide.strategy import Strategy
from typing import NoReturn
import MPSPlots.render2D
# plt.style.use('ggplot')


class PlotTrade():
    """
    This class is designed to visualize trading strategies by plotting the market data,
    portfolio metrics, and trading signals based on a specified trading strategy. It integrates
    market price data, portfolio performance, and strategy indicators into a coherent set of
    matplotlib plots to provide a comprehensive overview of trading activity and strategy effectiveness.

    Attributes:
        market (pandas.DataFrame): DataFrame containing market data with at least 'date' and 'close' columns.
        portfolio (pandas.DataFrame): DataFrame containing portfolio metrics and trading signals,
                                      must include 'date', 'total', 'positions', 'opened_positions',
                                      'stop_loss_price', and 'take_profit_price' columns.
        strategy (Strategy): An instance of a strategy class that implements an `add_to_ax` method,
                                 which adds strategy-specific metrics or indicators to a matplotlib axis.
    """

    def __init__(
            self,
            backtester: object,
            market: pandas.DataFrame,
            portfolio: pandas.DataFrame,
            strategy: Strategy):
        """
        Initializes the PlotTrade object with market data, portfolio information, and a trading strategy.

        Parameters:
            market (pandas.DataFrame): The market data to be plotted, including dates and prices.
            portfolio (pandas.DataFrame): The portfolio data including dates, asset totals, and trading positions.
            strategy (Strategy): The trading strategy object which contains logic to add strategy-specific
                                     indicators to the plot.
        """
        self.backtester = backtester
        self.market = market
        self.portfolio = portfolio
        self.strategy = strategy

    def plot_trading_strategy(
            self,
            show_price: bool = False,
            show_total: bool = True,
            show_metric: bool = False,
            show_assets: bool = False,
            show_units: bool = False,
            show_positions: bool = False) -> NoReturn:
        """
        Constructs and displays a comprehensive figure that visualizes various aspects of the trading strategy,
        including market prices, trading signals, portfolio metrics, and specific indicators related to assets
        and positions. This visualization aids in analyzing the strategy's performance and decision-making process over time.

        Parameters:
            show_price (bool, optional): If True, includes a plot of market prices and trading signals. Default is True.
            show_metric (bool, optional): If True, includes a plot of strategy-specific performance metrics. Default is False.
            show_assets (bool, optional): If True, includes a plot of assets over time, reflecting the portfolio's composition. Default is False.
            show_positions (bool, optional): If True, includes a plot of the trading positions over time, showing when and how the strategy enters or exits trades. Default is False.
            show_units (bool, optional): If True, includes a plot of the trading units over time, showing when and how the strategy enters or exits trades. Default is False.
            show_positions (bool, optional): If True, includes a plot of the position over time.

        Returns:
            None: This method does not return a value. Instead, it displays the constructed matplotlib figure directly.

        Notes:
            - The method organizes the selected plots into subplots within a single figure, with each subplot dedicated to one of the specified components (price, metric, assets, positions).
            - The subplots share the x-axis, which typically represents time, to facilitate comparative analysis across different aspects of the trading strategy.
            - Additional customization options for each subplot, such as legends, axes labels, and plot styles, can be specified within the respective plotting methods called within this method.
        """
        plots_count = sum([show_price, show_metric, show_assets, show_positions, show_units, show_total])

        title: str = 'Trading Strategy Overview'

        figure, axis = plt.subplots(
            nrows=plots_count,
            ncols=1,
            figsize=(12, 2.5 * plots_count),
            sharex=True,
            squeeze=False
        )

        figure.suptitle(title)

        plot_methods = [
            (show_price, self._add_price_and_signal_to_ax),
            (show_metric, self._add_strategy_to_ax),
            (show_positions, self._add_position_to_ax),
            (show_assets, self._add_asset_to_ax),
            (show_units, self._add_units_to_ax),
            (show_total, self._add_portfolio_value_to_ax)
        ]

        axis_number = 0
        for show, method in plot_methods:
            if show:
                ax = axis[axis_number, 0]
                method(ax=ax)
                ax.set_axisbelow(True)
                self._format_legend(ax=ax)
                axis_number += 1

        plt.subplots_adjust(wspace=0, hspace=0.15)

        plt.xticks(rotation=45)
        plt.show()
        plt.tight_layout()

        return figure

    def _add_position_to_ax(self, ax: plt.Axes) -> None:
        """
        Visualizes the cumulative positions held over time on a specified Matplotlib axis. This visualization
        helps in understanding how the trading strategy's positions change throughout the trading period.

        The cumulative positions are calculated by summing up individual holdings from all positions in the
        portfolio at each point in time. This aggregated view provides insight into the overall exposure of
        the trading strategy at any given moment.

        Parameters:
            ax (plt.Axes): The Matplotlib Axes object where the positions data will be plotted.

        Note:
            This method assumes that each position in the portfolio has a 'holding' attribute, which is a
            DataFrame or Series indicating the holding status (1 for holding, 0 for not holding) over time.
        """
        ax.set_ylabel('Positions')

        # Plot the cumulative positions over time
        ax.plot(
            self.portfolio.date,
            self.portfolio.long_positions,
            linewidth=2,
            color='C0',
            label='Long positions'
        )

        ax.plot(
            self.portfolio.date,
            self.portfolio.short_positions,
            linewidth=2,
            color='C1',
            label='Short positions'
        )

    def _add_units_to_ax(self, ax: plt.Axes) -> None:
        """
        Visualizes the total units held in the trading portfolio over time on a specified Matplotlib axis. This plot
        aggregates the units from all positions in the portfolio, providing insight into the portfolio's exposure in
        terms of quantity over the trading period.

        Parameters:
            ax (plt.Axes): The Matplotlib Axes object where the units data will be plotted.

        Note:
            This method assumes that each position in the 'position_list' has a 'holding' attribute indicating
            whether the position is held (1 for holding, 0 for not holding) and a 'units' attribute representing
            the number of units held in each position. The 'holding' attribute should align with the 'market' index.
        """
        ax.set_ylabel('Units')

        # Plot the total units over time
        ax.plot(
            self.portfolio.date,
            self.portfolio.holdings,
            linewidth=2,
            color='C0',
            label='Total Units'
        )

    def _add_portfolio_value_to_ax(self, ax: plt.Axes) -> None:
        """
        Visualizes the composition of the trading portfolio over time on a specified Matplotlib axis. This includes
        plots for the total portfolio value, cash component, and holdings value, providing a comprehensive view of
        the portfolio's financial status throughout the trading period.

        Parameters:
            ax (plt.Axes): The Matplotlib Axes object where the portfolio components will be plotted.

        Note:
            This method assumes the portfolio DataFrame contains 'total', 'cash', and 'holdings' columns,
            representing the total portfolio value, cash amount, and value of holdings over time, respectively.
        """
        ax.set_ylabel('Portfolio Value')

        ax.plot(
            self.portfolio.date,
            self.portfolio.total,
            label='Total',
            linewidth=2,
            color='black'
        )

        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_scientific(False)

        ax.get_yaxis().get_major_formatter().offset = self.backtester.capital_management.initial_capital

    def _add_asset_to_ax(self, ax: plt.Axes) -> None:
        """
        Visualizes the composition of the trading portfolio over time on a specified Matplotlib axis. This includes
        plots for the total portfolio value, cash component, and holdings value, providing a comprehensive view of
        the portfolio's financial status throughout the trading period.

        Parameters:
            ax (plt.Axes): The Matplotlib Axes object where the portfolio components will be plotted.

        Note:
            This method assumes the portfolio DataFrame contains 'total', 'cash', and 'holdings' columns,
            representing the total portfolio value, cash amount, and value of holdings over time, respectively.
        """
        ax.set_ylabel('Assets Value and Cash')

        ax.plot(
            self.portfolio.date,
            self.portfolio.total,
            label='Total',
            linewidth=2,
            color='black'
        )

        ax.plot(
            self.portfolio.date,
            self.portfolio.cash,
            label='Cash',
            linewidth=2,
            color='C1'
        )

    def _add_strategy_to_ax(self, ax: plt.Axes) -> NoReturn:
        """
        Adds strategy-specific metrics or indicators to a specified matplotlib axis. This method utilizes the
        `add_to_ax` method of the strategy object, allowing for flexible integration of various strategy indicators.

        Parameters:
            ax (plt.Axes): The matplotlib axis object to which the strategy metrics will be added.
        """
        self.strategy.add_to_ax(ax)

        self._add_buy_sell_signal_to_ax(ax=ax)

    def _add_price_and_signal_to_ax(self, ax: plt.Axes) -> NoReturn:
        """
        Plots the market closing prices and trading signals (buy/sell) on a specified matplotlib axis. This method
        provides a visual representation of when trades were opened or closed in relation to the market price movements.

        Parameters:
            ax (plt.Axes): The matplotlib axis object to which the price and signal information will be added.
        """
        ax.set_ylabel('Price')

        # Price and signals plot
        ax.plot(
            self.market.date,
            self.market.close,
            label='Close Price',
            color='C0',
            linewidth=2
        )

        ax.fill_between(
            x=self.market.date,
            y1=self.market.high,
            y2=self.market.low,
            color='grey',
            alpha=0.2,
        )

        # # Aggregate units from all positions in the portfolio
        for position in self.backtester.position_list:
            position._add_stop_loss_to_ax(ax=ax)
            position._add_triggers_to_ax(ax=ax)

            ax.vlines(
                x=position.start_date,
                ymin=0,
                ymax=1,
                transform=ax.get_xaxis_transform(),
                alpha=0.2,
                label='Open position',
                color='black'
            )

    def _add_buy_sell_signal_to_ax(self, ax: plt.Axes) -> NoReturn:
        ax.fill_between(
            x=self.market.date,
            y1=0,
            y2=1,
            where=self.strategy.data['signal'] == -1,
            color='red',
            label='Sell signal',
            alpha=0.2,
            transform=ax.get_xaxis_transform(),
        )

        ax.fill_between(
            x=self.market.date,
            y1=0,
            y2=1,
            where=self.strategy.data['signal'] == +1,
            color='green',
            label='Buy signal',
            alpha=0.2,
            transform=ax.get_xaxis_transform(),
        )

    def _format_legend(self, ax: plt.Axes) -> NoReturn:
        """
        Removes duplicate entries from the legend of a given matplotlib axis. This method ensures that each
        legend entry is unique, improving the clarity of the plot.

        Parameters:
            ax (plt.Axes): The matplotlib axis object from which to remove duplicate legend entries.
        """
        handles, labels = ax.get_legend_handles_labels()
        if len(labels) <= 1:
            return
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        ax.legend(*zip(*unique), loc='upper right', facecolor='white', framealpha=1)


# -
