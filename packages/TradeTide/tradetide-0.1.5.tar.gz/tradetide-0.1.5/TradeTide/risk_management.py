#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pandas
from TradeTide.tools import percent_to_float
from TradeTide.indicators import ATR
from TradeTide import position


class RiskBase:
    """
    Base class for managing loss and profit calculations for trading strategies.

    This class defines the interface for calculating loss and profit prices
    based on different strategies. Subclasses should implement the
    get_loss_profit_price method according to their specific calculation logic.
    """

    def get_loss_profit_price(self, position_type: str, entry_price: float) -> tuple[float, float]:
        """
        Abstract method to calculate the loss and profit prices.

        Parameters:
            position_type (str): The type of trading position ('long' or 'short').
            entry_price (float): The entry price for the trading position.

        Returns:
            tuple[float, float]: The calculated stop loss and take profit prices.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement this method.")


class DirectLossProfit(RiskBase):
    """
    A class to manage loss and profit calculations for trading positions using direct or percentage-based stop_loss and take_profit values, incorporating broker leverage.
    Inherits from RiskBase to leverage foundational risk management functionalities.
    """

    def __init__(
            self,
            market: pandas.DataFrame,
            stop_loss: float | str,
            take_profit: float | str,
            leverage: int = 1) -> None:
        """
        Initializes the DirectLossProfit instance with market data, stop loss, take profit levels, and broker leverage.

        Parameters:
            market (pandas.DataFrame): Market data, used to determine the pip value based on the currency pair.
            stop_loss (float | str): The stop loss level, can be a direct value (float) or a percentage (str, e.g., "1.5%").
            take_profit (float | str): The take profit level, can be a direct value (float) or a percentage (str, e.g., "2%").
            leverage (int): The leverage provided by the broker, influencing the size of the position that can be controlled.
        """
        super().__init__()  # Initialize the base class, if necessary.
        self.market = market
        self.pip_value = self._determine_pip_value(market)
        self.stop_loss = self._parse_input(stop_loss)
        self.take_profit = self._parse_input(take_profit)
        self.leverage = leverage
        self.reward_risk_ratio = self._calculate_reward_risk_ratio()

    def _determine_pip_value(self, market: pandas.DataFrame) -> float:
        """
        Determines the pip value based on the currency pair in the market data.

        Parameters:
            market (pandas.DataFrame): Market data containing currency information.

        Returns:
            float: The pip value for calculations.
        """
        if market.attrs['currencies'] == {'usd', 'jpy'}:
            return 1e-2
        else:
            return 1e-4

    def _parse_input(self, value: float | str) -> float:
        """
        Parses the input value for stop loss or take profit to determine its pip value.

        Parameters:
            value (float | str): Input value as either a percentage string or direct float value.

        Returns:
            float: The value converted to pip value if specified in pips or remains as is if already a float.
        """
        if isinstance(value, str) and 'pip' in value:
            return float(value.strip('pip')) * self.pip_value
        elif isinstance(value, str) and '%' in value:
            # Assuming some default percentage-to-pip conversion if needed; needs clarification.
            return float(value.strip('%')) * self.pip_value
        elif isinstance(value, float):
            return value
        else:
            raise ValueError("Invalid input for stop loss or take profit.")

    def _calculate_reward_risk_ratio(self) -> float:
        """
        Calculates the risk-reward ratio based on the stop loss and take profit pip values.

        Returns:
            float: The risk-reward ratio.
        """
        return self.take_profit / self.stop_loss if self.stop_loss else float('inf')

    def calculate_margin_requirement(self, position_size: float) -> float:
        """
        Calculates the margin requirement for a given position size using the broker's leverage.

        Parameters:
            position_size (float): The size of the position in units of the base currency.

        Returns:
            float: The required margin to open the position, based on the broker's leverage.
        """
        return position_size / self.leverage


class ATRLossProfit(RiskBase):
    """
    Manages loss and profit calculations based on the Average True Range (ATR) indicator.

    This class utilizes the ATR indicator to dynamically calculate stop loss and take profit
    levels based on market volatility. It requires market data to calculate the ATR value,
    which is then adjusted by a multiplier to set the stop loss and take profit levels.
    """

    def __init__(self, market: pandas.DataFrame, ATR_multiplier: float, periods: float | str) -> None:
        """
        Initializes the class with market data for ATR calculation and parameters for loss/profit levels.

        Parameters:
            market (pandas.DataFrame): The market data used to calculate the ATR.
            ATR_multiplier (float): The multiplier applied to the ATR value for stop loss/take profit calculations.
            periods (float | str): The number of periods used for the ATR calculation.
        """
        self.ATR_indicator = ATR(periods=periods)
        self.ATR_value = self.ATR_indicator.generate_signal(market)['ATR']
        self.ATR_multiplier = ATR_multiplier

    def get_loss_profit_price(self, pos: str, entry_price: float) -> tuple[float, float]:
        """
        Calculates and returns stop loss and take profit prices based on the ATR indicator.

        Parameters:
            position_type (position.Long | position.Short): The type of trading position ('long' or 'short').
            entry_price (float): The entry price for the trading position.

        Returns:
            tuple[float, float]: The calculated stop loss and take profit prices, adjusted for market volatility.
        """
        adjustment = self.ATR_value * self.ATR_multiplier

        if isinstance(pos, position.Long):
            stop_loss_price = entry_price - adjustment
            take_profit_price = entry_price + adjustment

        else:
            stop_loss_price = entry_price + adjustment
            take_profit_price = entry_price - adjustment

        return stop_loss_price, take_profit_price


class TrailingStopLoss(RiskBase):
    """
    Manages loss and profit calculations using dynamic trailing stop loss and take profit approaches for both long and short positions.

    This class allows for dynamically adjusting the stop loss and take profit levels as the market moves in favor of the trade.
    """

    def __init__(self, trailing_stop: float, trailing_profit: float) -> None:
        """
        Initializes the management class with trailing stop and take profit levels.

        Parameters:
            trailing_stop (float): The trailing stop level, specified in pips or as a percentage.
            trailing_profit (float): The trailing take profit level, specified in pips or as a percentage.
        """
        self.trailing_stop = percent_to_float(trailing_stop)  # Convert to float if given as a percentage
        self.trailing_profit = percent_to_float(trailing_profit)  # Convert to float if given as a percentage
        self.initial_stop_loss = None
        self.initial_take_profit = None
        self.extreme_price = None  # Extreme price since entry: highest for long, lowest for short

    def set_initial_conditions(self, position_type: str, entry_price: float):
        """
        Sets the initial conditions for the trade, including the initial stop loss, take profit, and the extreme price seen based on position type.

        Parameters:
            position_type (str): The type of trading position ('long' or 'short').
            entry_price (float): The entry price for the trade.
        """
        if position_type == 'long':
            self.initial_stop_loss = entry_price - self.trailing_stop
            self.initial_take_profit = entry_price + self.trailing_profit
            self.extreme_price = entry_price
        elif position_type == 'short':
            self.initial_stop_loss = entry_price + self.trailing_stop
            self.initial_take_profit = entry_price - self.trailing_profit
            self.extreme_price = entry_price
        else:
            raise ValueError("position_type must be 'long' or 'short'")

    def update_extreme_price(self, position_type: str, current_price: float):
        """
        Updates the extreme price seen since the trade was opened, if the current price is more favorable.

        Parameters:
            position_type (str): The type of trading position ('long' or 'short').
            current_price (float): The current market price.
        """
        if position_type == 'long' and current_price > self.extreme_price:
            self.extreme_price = current_price
        elif position_type == 'short' and current_price < self.extreme_price:
            self.extreme_price = current_price

    def get_loss_profit_price(self, position_type: str, entry_price: float) -> tuple[float, float]:
        """
        Calculates and returns the dynamically adjusted stop loss and take profit prices for a trading position.

        Parameters:
            position_type (str): The type of trading position ('long' or 'short').
            entry_price (float): The entry price for the trading position.

        Returns:
            tuple[float, float]: The dynamically adjusted stop loss and take profit prices.
        """
        if position_type == 'long':
            adjusted_stop_loss = self.extreme_price - self.trailing_stop
            stop_loss_price = max(self.initial_stop_loss, adjusted_stop_loss)
            adjusted_take_profit = self.extreme_price + self.trailing_profit
            take_profit_price = max(self.initial_take_profit, adjusted_take_profit)
        elif position_type == 'short':
            adjusted_stop_loss = self.extreme_price + self.trailing_stop
            stop_loss_price = min(self.initial_stop_loss, adjusted_stop_loss)
            adjusted_take_profit = self.extreme_price - self.trailing_profit
            take_profit_price = min(self.initial_take_profit, adjusted_take_profit)
        else:
            raise ValueError("position_type must be 'long' or 'short'")

        return stop_loss_price, take_profit_price

# -
