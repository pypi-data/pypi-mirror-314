#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from typing import NoReturn
import pandas
import numpy
import matplotlib.pyplot as plt
from TradeTide.indicators.base_indicator import BaseIndicator

from dataclasses import dataclass, field


@dataclass(kw_only=True, repr=False)
class ATR(BaseIndicator):
    """
    Implements the Average True Range (ATR) trading indicator as an extension of the BaseIndicator class.

    The ATR is a technical analysis indicator that measures market volatility by decomposing the entire range of an asset for that period,
    including the gap from the previous close if it falls outside of the current range. The ATR is typically used to understand the volatility
    in the price of an asset over a certain period of time.

    Attributes:
        periods (int | str): The number of periods over which the ATR is calculated, typically 14.
        value_type (str): The column names from the input DataFrame on which the ATR calculation is based, usually 'high', 'low', and 'close'.

    Methods:
        add_to_ax: Plots the ATR on a given Matplotlib axis.
        generate_signal: Calculates the ATR based on price movements.
    """
    periods: int | str = 14
    value_type: str = field(default='close', repr=False)

    def add_to_ax(self, ax: plt.Axes) -> NoReturn:
        """
        Adds the ATR plot to the specified Matplotlib axis.

        This method plots the ATR of the trading indicator, providing a visual representation of market volatility over time.

        Parameters:
            ax (matplotlib.axes.Axes): The Matplotlib axis object where the ATR plot will be added.
        """
        ax.set_ylabel(self.__repr__())

        ax.plot(
            self.data.index,
            self.data.ATR,
            label='ATR',
            linewidth=1,
            color='C1'
        )

    def generate_signal(self, market_data: pandas.DataFrame) -> pandas.DataFrame:
        """
        Calculates the ATR based on the provided DataFrame.

        The method computes the true range and then the average true range over the specified period. The calculated ATR is
        added to the DataFrame, allowing analysis of the market's volatility.

        Parameters:
            market_data (pandas.DataFrame): The input DataFrame containing price data including 'high', 'low', and 'close' columns.

        Returns:
            pandas.DataFrame: The input DataFrame with an added column for the ATR ('ATR').
        """
        high_low = market_data['high'] - market_data['low']
        high_close = numpy.abs(market_data['high'] - market_data['close'].shift())
        low_close = numpy.abs(market_data['low'] - market_data['close'].shift())
        true_ranges = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        market_data['ATR'] = true_ranges.rolling(window=self.periods).mean()

        self.data = market_data

        return self.data
