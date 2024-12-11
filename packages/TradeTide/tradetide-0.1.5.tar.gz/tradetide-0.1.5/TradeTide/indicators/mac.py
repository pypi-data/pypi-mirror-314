#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pandas
import numpy
from typing import NoReturn
import matplotlib
from TradeTide.indicators.base_indicator import BaseIndicator

from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class MAC(BaseIndicator):
    """
    Implements a Moving Average Crossing (MAC) indicator as an extension of the BaseIndicator class.

    This indicator involves two moving averages of a series: a "short" and a "long" moving average. A typical trading signal
    is generated when the short moving average crosses above (bullish signal) or below (bearish signal) the long moving average.
    The indicator is commonly used to identify the momentum and direction of a trend.

    Attributes:
        short_window (int | str): The window size of the short moving average.
        long_window (int | str): The window size of the long moving average.
        min_period (int): The minimum number of observations in the window required to have a value (otherwise result is NA).
        value_type (str): The type of price data to use for the moving average calculation. Typically one of ['high', 'low', 'open', 'close'].

    Methods:
        add_to_ax: Plots the short and long moving averages on a given Matplotlib axis.
    """
    short_window: int | str = 30
    long_window: int | str = 150
    min_period: int = 10
    value_type: str = 'close'

    def add_to_ax(self, ax: matplotlib.axes.Axes) -> NoReturn:
        """
        Adds the short and long moving average plots to the specified Matplotlib axis.

        This method visualizes the short and long moving averages on a plot, which is useful for identifying potential
        crossover points that might indicate trading signals.

        Parameters:
            ax (matplotlib.axes.Axes): The Matplotlib axis object where the moving averages will be plotted.
        """
        ax.set_ylabel(self.__repr__())

        ax.plot(
            self.data['short_window_array'],
            linewidth=2,
            label='short window'
        )

        ax.plot(
            self.data['long_window_array'],
            label='long window',
            linewidth=2,
        )

    @BaseIndicator.post_generate_signal
    def generate_signal(self, market_data: pandas.DataFrame) -> pandas.DataFrame:
        """
        Generates trading signals based on the crossover of short-term and long-term moving averages.

        This method applies a rolling mean calculation to a specified column (`self.value_type`) in the input DataFrame,
        creating two new columns: 'long_window_array' and 'short_window_array', representing the long-term and short-term
        moving averages, respectively. A trading signal is generated when the short-term moving average crosses above the
        long-term moving average, indicated by a value of 1 in the 'signal' column; otherwise, the 'signal' value is set to 0.

        The method is decorated with `@BaseIndicator.post_generate_signal`, suggesting it may perform additional operations
        or checks defined in the `BaseIndicator` class after the signal generation.

        Parameters:
            market_data (pandas.DataFrame): The input DataFrame containing market data. It must include a column named
                                          as specified by `self.value_type`, which is used for calculating moving averages.

        Returns:
            pandas.DataFrame: The original DataFrame is modified in-place to include three new columns:
                              'long_window_array', 'short_window_array', and 'signal'. The 'signal' column contains
                              the generated trading signals based on the moving average crossover indicator.
        """
        self.data['long_window_array'] = self.data[self.value_type].rolling(
            window=self.long_window,
            min_periods=self.min_period
        ).mean()

        self.data['short_window_array'] = self.data[self.value_type].rolling(
            window=self.short_window,
            min_periods=self.min_period
        ).mean()

        self.data['signal'] = numpy.where(self.data['short_window_array'] > self.data['long_window_array'], 1, -1)
# -
