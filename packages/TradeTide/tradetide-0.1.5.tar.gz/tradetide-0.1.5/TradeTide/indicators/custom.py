#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-


import pandas as pd
import numpy as np
from TradeTide.indicators.base_indicator import BaseIndicator

from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class Custom(BaseIndicator):
    """
    A custom trading signal generator that integrates user-defined signals into market data.

    This class allows for the incorporation of arbitrary, pre-computed trading signals into a trading strategy.
    It assumes that the custom signals are aligned with the market data in terms of the sequence and count.

    Attributes:
        custom_signal (np.ndarray): An array of custom trading signals corresponding to each data point in the market data.

    Methods:
        generate_signal(market_data): Integrates custom signals into the provided market data DataFrame and returns it.
    """

    def __init__(self, custom_signal: np.ndarray):
        """
        Initializes the Custom signal generator with a user-defined array of trading signals.

        Args:
            custom_signal (np.ndarray): An array containing the custom trading signals. Each element in the array should
                                        correspond to a trading signal (-1, 0, 1) for each data point in the market data,
                                        where -1 indicates a 'sell' signal, 1 indicates a 'buy' signal, and 0 indicates
                                        no action.
        """
        self.custom_signal = custom_signal

    def __repr__(self) -> str:
        return "Custom indicator"

    @BaseIndicator.post_generate_signal
    def generate_signal(self, market_data: pd.DataFrame) -> pd.DataFrame:
        """
        Integrates the custom trading signals into the provided market data DataFrame.

        This method adds a 'signal' column to the `market_data` DataFrame, containing the custom trading signals.
        It ensures that the length of the `custom_signal` array matches the number of rows in `market_data`.

        Args:
            market_data (pd.DataFrame): The market data into which the custom signals will be integrated. This DataFrame
                                        should have the same number of rows as the length of the `custom_signal` array.

        Returns:
            pd.DataFrame: The `market_data` DataFrame with an additional 'signal' column containing the custom signals.

        Raises:
            AssertionError: If the length of the `custom_signal` array does not match the number of rows in `market_data`.
        """
        assert len(market_data) == len(self.custom_signal), 'Mismatch between the custom signal and market_data'

        # Create a copy of the market_data to avoid modifying the original DataFrame
        data_with_signals = market_data.copy()
        data_with_signals['signal'] = self.custom_signal

        return data_with_signals
