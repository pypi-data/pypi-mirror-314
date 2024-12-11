#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from typing import NoReturn

import numpy
from TradeTide.position import Short, Long
from datetime import date as DateTime


class TimeState:
    def __init__(self, initial_capital: float):
        self.open_positions = []
        self.closed_positions = []
        self.cash = initial_capital

    def update_cash(self, date: DateTime):
        # Assuming profits/losses from closed positions are realized immediately
        total_cost_open_positions = sum(pos.cost for pos in self.open_positions)
        total_returns_closed_positions = sum(pos.return_ for pos in self.closed_positions)  # Replace pos.return_ with your actual return attribute
        self.time_info.loc[date, 'cash'] = self.initial_capital - total_cost_open_positions + total_returns_closed_positions

    def add_position(self, position: Long | Short) -> NoReturn:
        self.open_positions.append(position)
        self.cash -= position.cost

    def update_date(self, date) -> NoReturn:
        closing_position = list(
            filter(lambda x: x.stop_date < date, self.open_positions)
        )

        self.open_positions = list(
            filter(lambda x: x.stop_date >= date, self.open_positions)
        )

        add_cash = numpy.sum(
            [p.exit_value for p in closing_position]
        )

        self.cash += add_cash

    @property
    def active_positions(self) -> int:
        return len(self.open_positions)
