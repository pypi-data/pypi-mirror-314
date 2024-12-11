#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pytest
import pandas
from TradeTide.backtester import BackTester
from TradeTide.loader import get_market_data
from TradeTide.capital_management import LimitedCapital
from TradeTide.risk_management import DirectLossProfit


class MockStrategy:
    def __init__(self):
        pass

    def generate_signal(self, market_data: pandas.DataFrame):
        self.data = pandas.DataFrame(index=market_data.index)

        # Initialize the signal column with no signal
        self.data['signal'] = 0

        # Set a buy signal (1) on even days and a sell signal (-1) on odd days
        self.data[market_data.date.dt.day_name() == 'Monday'] = +1

        self.signal = self.data['signal']


@pytest.fixture
def mock_data() -> pandas.DataFrame:
    market_data = get_market_data('eur', 'usd', time_span='3day', year=2023, spread=0)
    return market_data


@pytest.fixture
def backtester(mock_data: pandas.DataFrame) -> BackTester:
    strategy = MockStrategy()
    strategy.generate_signal(mock_data)
    backtester = BackTester(strategy=strategy, market=mock_data)
    return backtester


@pytest.fixture
def capital_management(mock_data):
    loss_profit_managment = DirectLossProfit(
        market=mock_data,
        stop_loss='.1%',
        take_profit='.1%',
    )

    capital_management = LimitedCapital(
        initial_capital=1_000,
        max_cap_per_trade=100,
        limit_of_positions=3,
        risk_management=loss_profit_managment
    )

    return capital_management


def test_signal_generation(backtester, mock_data):
    for index, row in backtester.strategy.data.iterrows():
        day = mock_data.iloc[index].date.day_name()
        expected_signal = 1 if day == 'Monday' else 0
        assert row['signal'] == expected_signal, "Signal generation failed."


def test_backtest_execution(backtester, capital_management):
    portfolio = backtester.backtest(capital_management=capital_management)
    assert isinstance(portfolio, pandas.DataFrame), "Backtest didn't return a DataFrame."
    assert not portfolio.empty, "Backtest returned an empty DataFrame."


def test_performance_metrics(backtester, capital_management):

    backtester.backtest(capital_management=capital_management)
    # Mock the performance calculation to simplify the test
    backtester.metrics.print()
    assert 'Returns' in backtester.metrics.performance_dict, "Performance metrics calculation failed."
    assert backtester.metrics.performance_dict['Returns'] == '0.00%', "Incorrect total return calculated."

# -
