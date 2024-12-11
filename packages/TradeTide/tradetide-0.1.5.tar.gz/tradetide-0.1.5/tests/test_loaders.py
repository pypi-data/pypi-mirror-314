#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from TradeTide.loader import get_market_data
import pytest

currency_pairs = [
    ('eur', 'usd'),
    ('chf', 'usd'),
    ('gpb', 'usd'),
    ('jpy', 'usd'),
    ('cad', 'usd'),
]


@pytest.mark.parametrize("currency_pair", currency_pairs)
def test_load_dataframe(currency_pair: tuple) -> None:
    _ = get_market_data(*currency_pair, year=2023, spread=0)

# -
