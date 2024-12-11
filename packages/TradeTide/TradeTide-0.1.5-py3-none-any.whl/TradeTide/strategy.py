#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from typing import NoReturn
import pandas
import numpy
from TradeTide.indicators.base_indicator import BaseIndicator
import matplotlib.pyplot as plt
from mpl_interactions import ioff, panhandler, zoom_factory


class Strategy:
    """
    Generates combined trading signals based on signals from multiple strategies using weighted voting.
    If weights are not provided, they are initialized randomly.

    Attributes:
        data (pd.DataFrame): Historical market data.
        strategies (list): List of strategy instances implementing the StrategyInterface.
        weights (list): List of weights corresponding to each strategy. Randomly initialized if not provided.
    """

    value_type: str = 'close'

    def __init__(self, *indicators: BaseIndicator, weights: list = None) -> numpy:
        """
        Initializes the CombinedSignalStrategy with market data, strategy instances, and optional weights.

        Args:
            strategies (list): List of strategy instances, each adhering to the StrategyInterface.
            weights (list, optional): List of weights corresponding to each strategy. If None, weights are initialized randomly.
        """
        self.indicators = indicators
        self.weights = weights if weights is not None else numpy.random.rand(len(indicators))
        self.weights /= numpy.sqrt(numpy.square(self.weights).sum())

        if len(indicators) != len(self.weights):
            raise ValueError("The number of indicators must be equal to the number of weights.")

    @BaseIndicator.post_generate_signal
    def generate_signal(self, market_data: pandas.DataFrame) -> pandas.DataFrame:
        """
        Aggregates signals from individual indicators based on assigned weights to generate final combined signals.

        Returns:
            pd.Series: Final combined signals where 1 represents a 'buy' signal, -1 represents a 'sell' signal,
                       and 0 represents no action.
        """
        signals_df = pandas.DataFrame(index=market_data.index)

        # Collect signals from each strategy
        for i, indicator in enumerate(self.indicators):
            signals_df[f'signal_{i}'] = indicator.generate_signal(market_data)

        # Apply weights to the signals
        weighted_signals = signals_df.mul(self.weights, axis=1)

        # Aggregate weighted signals to produce a final signal
        self.signal = self.data['signal'] = weighted_signals.sum(axis=1).apply(numpy.sign)

    def add_to_ax(self, ax) -> NoReturn:
        pass

    def plot(self) -> NoReturn:
        n_strategy = len(self.indicators)

        title: str = 'Trading Indicators Overview'

        with ioff:
            self.figure, self.axis = plt.subplots(
                nrows=(n_strategy + 1),
                ncols=1,
                figsize=(10, 3 * n_strategy + 1),
                sharex=True,
            )

        self.axis = numpy.atleast_1d(self.axis)

        self.figure.suptitle(title)

        self.axis[0].plot(
            self.data.close,
            linewidth=2,
        )

        y_min, y_max = self.axis[0].get_ylim()

        self.axis[0].fill_between(
            self.data.index,
            y1=y_min,
            y2=y_max,
            where=self.signal == 1,
            color='green',
            alpha=0.2
        )

        self.axis[0].fill_between(
            self.data.index,
            y1=y_min,
            y2=y_max,
            where=self.signal == -1,
            color='red',
            alpha=0.2
        )

        self.axis[0].set_ylabel('Close value')
        self.axis[-1].set_xlabel('Date')

        for indicator, ax in zip(self.indicators, self.axis[1:]):
            indicator.add_to_ax(ax)

        plt.subplots_adjust(wspace=0, hspace=0.1)
        plt.legend()

        for ax in self.axis:
            zoom_factory(ax)

        _ = panhandler(self.figure)

        plt.show()

# -
