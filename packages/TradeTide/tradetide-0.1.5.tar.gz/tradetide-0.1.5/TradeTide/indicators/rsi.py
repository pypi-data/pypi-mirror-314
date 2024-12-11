#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pandas
from typing import NoReturn
import matplotlib
from TradeTide.indicators.base_indicator import BaseIndicator

from dataclasses import dataclass, field


@dataclass(kw_only=True, repr=False)
class RSI(BaseIndicator):
    """
    Implements the Relative Strength Index (RSI) trading indicator as an extension of the BaseIndicator class.

    The RSI is a momentum oscillator that measures the speed and change of price movements. It oscillates between 0 and 100.
    Traditionally, the RSI is considered overbought when above 70 and oversold when below 30. Signals can be generated from
    these conditions to suggest potential buy or sell opportunities.

    Attributes:
        period (int | str): The number of periods used to calculate the RSI. Commonly set to 14.
        overbought_threshold (int): The RSI level above which the asset is considered overbought. Typically set to 70.
        oversold_threshold (int): The RSI level below which the asset is considered oversold. Typically set to 30.
        value_type (str): The column name from the input DataFrame on which the RSI calculation is based. Usually set to 'close'.

    Methods:
        add_to_ax: Plots the RSI and its thresholds on a given Matplotlib axis.
        generate_signal: Calculates the RSI values based on price changes and generates buy/sell signals.
    """
    period: int | str = 14
    overbought_threshold: int = field(default=80, repr=False)
    oversold_threshold: int = field(default=20, repr=False)
    value_type: str = field(default='close', repr=False)

    def add_to_ax(self, ax: matplotlib.axes.Axes) -> NoReturn:
        """
        Adds the RSI plot to the specified Matplotlib axis, including the overbought and oversold threshold lines.

        Parameters:
            ax (matplotlib.axes.Axes): The Matplotlib axis object where the RSI plot will be added.
        """
        ax.set_ylabel(self.__repr__())

        ax.plot(
            self.data['rsi'],
            label='RSI',
            linewidth=2,
            color='C0'
        )

        ax.axhline(
            self.overbought_threshold,
            linestyle='--',
            color='red',
            alpha=0.5,
            linewidth=2,
            label='overbought'
        )

        ax.axhline(
            self.oversold_threshold,
            linestyle='--',
            color='green',
            alpha=0.5,
            linewidth=2,
            label='oversold'
        )

    @BaseIndicator.post_generate_signal
    def generate_signal(self, market_data: pandas.DataFrame) -> pandas.DataFrame:
        """
        Calculates the RSI based on the provided DataFrame and generates buy or sell signals.

        A buy signal is generated when the RSI crosses below the oversold threshold, and a sell signal is generated
        when the RSI crosses above the overbought threshold. The signals are added to the 'signal' column in the DataFrame.

        Parameters:
            market_data (pandas.DataFrame): The input DataFrame containing price data and a column specified by `value_type`.

        Returns:
            pandas.DataFrame: The input DataFrame with an added 'rsi' column containing the RSI values and a 'signal' column
                              containing the buy/sell signals.
        """
        delta = self.data[self.value_type].diff()

        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()

        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()

        rs = gain / loss

        self.data['rsi'] = 100 - (100 / (1 + rs))

        self.data['signal'] = 0

        self.data.loc[self.data['rsi'] < self.oversold_threshold, 'signal'] = 1
        self.data.loc[self.data['rsi'] > self.overbought_threshold, 'signal'] = -1
