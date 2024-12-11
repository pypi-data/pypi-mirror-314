#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from typing import NoReturn
import pandas
import numpy
from TradeTide.position import Short, Long
from TradeTide.risk_management import DirectLossProfit, ATRLossProfit
from TradeTide.time_state import TimeState


class CapitalManagement:
    """
    A base class for managing capital in a trading environment. It defines common properties
    and methods used by subclasses for specific capital management strategies.
    """

    def __init__(
            self,
            risk_management: DirectLossProfit | ATRLossProfit,
            max_cap_per_trade: float,
            limit_of_positions: int = numpy.inf,
            max_spread: float = numpy.inf,
            micro_lot: int = 1000):
        """
        Initializes the CapitalManagement object with common trading parameters.

        Parameters:
            - stop_loss (float): The stop loss percentage, indicating the maximum loss acceptable before closing a position.
            - take_profit (float): The take profit percentage, indicating the target profit to close a position.
            - max_cap_per_trade (float): The maximum capital allocated for each trade.
            - limit_of_positions (int): The maximum number of positions that can be open at any time.
        """
        self.max_cap_per_trade = max_cap_per_trade
        self.limit_of_positions = limit_of_positions
        self.risk_management = risk_management
        self.micro_lot = micro_lot
        self.max_spread = max_spread

    def manage(self, backtester: object, market: pandas.DataFrame) -> NoReturn:
        """
        Manages trading positions based on the strategy's signals, market data, and the subclass's
        specific capital management strategy. This method should be implemented by subclasses.

        Parameters:
            - backtester (object): The backtesting framework instance.
            - market (pandas.DataFrame): The market data containing historical price information.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class LimitedCapital(CapitalManagement):
    """
    Manages trading capital with a limitation on the initial capital and the maximum number of open positions.
    """

    def __init__(
            self,
            risk_management: DirectLossProfit | ATRLossProfit,
            initial_capital: float,
            max_cap_per_trade: float,
            limit_of_positions: int = numpy.inf,
            max_spread: float = numpy.inf,
            micro_lot: int = 1_000):
        """
        Initializes the LimitedCapital object with trading parameters and limitations on capital and positions.

        Parameters:
            - initial_capital (float): The initial capital available for trading.
        """
        super().__init__(
            risk_management=risk_management,
            max_cap_per_trade=max_cap_per_trade,
            limit_of_positions=limit_of_positions,
            micro_lot=micro_lot,
            max_spread=max_spread
        )

        self.initial_capital = initial_capital
        self.limit_of_positions = limit_of_positions

    def manage(self, backtester: object, market: pandas.DataFrame) -> NoReturn:
        """
        Implements the capital management strategy for a trading scenario with limited capital and positions.

        Parameters:
            - backtester (object): The backtesting framework instance.
            - market (pandas.DataFrame): The market data containing historical price information.
        """
        self.market = market

        # Initialize or clear the list to store Position objects
        self.time_state = TimeState(initial_capital=self.initial_capital)
        backtester.position_list = []

        # Iterate over signals and open new positions where indicated
        for idx, row in market[backtester.strategy.signal != 0].iterrows():
            self.time_state.update_date(row.date)

            if self.time_state.active_positions >= self.limit_of_positions:
                continue

            if row.spread > self.max_spread:
                continue

            available_cash: float = min(self.time_state.cash, self.max_cap_per_trade)

            position_class = Long if backtester.strategy.signal[idx] == 1 else Short
            size = numpy.floor((available_cash - row.spread) / row.close)
            cost = size * row.close + row.spread

            if size < self.micro_lot:
                continue

            position = position_class(
                start_date=row.date,
                market=market,
                risk_management=self.risk_management,
                entry_price=row.close,
                size=size,
                cost=cost
            )

            self.time_state.add_position(position)

            backtester.position_list.append(position)


class UnlimitedCapital(CapitalManagement):
    """
    Manages trading capital without limitations on the initial capital or the number of open positions.
    """

    def __init__(
            self,
            risk_management: DirectLossProfit | ATRLossProfit,
            max_cap_per_trade: float,
            limit_of_positions: int = numpy.inf,
            max_spread: float = numpy.inf):
        """
        Initializes the UnlimitedCapital object with trading parameters.
        """
        super().__init__(
            risk_management=risk_management,
            max_cap_per_trade=max_cap_per_trade,
            limit_of_positions=limit_of_positions,
            max_spread=max_spread
        )

    def manage(self, backtester: object, market: pandas.DataFrame) -> NoReturn:
        """
        Implements the capital management strategy for a trading scenario with limited capital and positions.

        Parameters:
            - backtester (object): The backtesting framework instance.
            - market (pandas.DataFrame): The market data containing historical price information.
        """
        self.market = market

        # Initialize or clear the list to store Position objects
        self.time_state = TimeState(initial_capital=self.initial_capital)
        backtester.position_list = []

        # Iterate over signals and open new positions where indicated
        for idx, row in market[backtester.strategy.signal != 0].iterrows():
            self.time_state.update_date(row.date)

            if self.time_state.active_positions >= self.limit_of_positions:
                continue

            if row.spread > self.max_spread:
                continue

            position_class = Long if backtester.strategy.signal[idx] == 1 else Short
            size = numpy.floor((self.max_cap_per_trade - row.spread) / row.close)
            cost = size * row.close + row.spread

            if size < self.micro_lot:
                continue

            position = position_class(
                start_date=row.date,
                market=market,
                risk_management=self.risk_management,
                entry_price=row.close,
                size=size,
                cost=cost
            )

            self.time_state.add_position(position)

            backtester.position_list.append(position)

# -
