#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pytest
import TradeTide.strategy
from TradeTide.loader import get_market_data

strategy_list = TradeTide.indicators.__all__


@pytest.mark.parametrize("strategy", strategy_list, ids=strategy_list)
def test_strategy(strategy):
    market_data = get_market_data('eur', 'usd', year=2023, spread=0)

    market_data = market_data[:10_000].copy()

    strat = getattr(TradeTide.indicators, strategy)()

    strat.generate_signal(market_data)
