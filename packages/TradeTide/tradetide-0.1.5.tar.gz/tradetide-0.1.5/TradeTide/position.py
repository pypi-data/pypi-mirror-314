#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from typing import NoReturn
import pandas
import numpy
import matplotlib.pyplot as plt

from dataclasses import dataclass
from TradeTide.risk_management import RiskBase


@dataclass
class BasePosition:
    """
    Represents a financial trading position with functionality for risk management,
    performance analysis, and visualization. It incorporates both long and short positions,
    taking into account entry and exit strategies based on predefined risk management parameters.

    Attributes:
        start_date: Initialization date of the position.
        market: Market data DataFrame with 'close', 'spread', and other relevant columns.
        risk_management: Strategy for risk management.
        entry_price: Price at which the position is entered.
        size: Number of units in the position.
        cost: Total cost of entering the position.

    The class requires market data and a risk management strategy to initialize. It calculates
    the entry price, number of units (size), and cost at initiation. It also computes the precise levels
    for stop loss and take profit based on the provided strategy and market conditions at the start date.

    Methods:
        initialize(): Prepares the position by setting stop loss and take profit prices based on the risk management strategy.
        update_portfolio_dataframe(dataframe: pd.DataFrame): Updates a given portfolio DataFrame with the position's details.
        compute_exit_info(): Calculates the exit price based on market data and updates the cash balance accordingly.
        compute_triggers(): Identifies trigger points for stop loss and take profit based on market movements post-entry.
        plot(): Visualizes the position lifecycle on a price chart, highlighting key events and levels.

    This class simplifies the management of trading positions by automating risk calculations and providing
    visual insights into the trading strategy's execution, making it an essential tool for backtesting trading strategies.
    """
    start_date: pandas.Timestamp
    market: pandas.DataFrame
    risk_management: RiskBase
    entry_price: float
    size: int
    cost: float

    def __post_init__(self):
        # Initial setup: validates position feasibility.
        self.initialize()

    def initialize(self) -> NoReturn:
        self.set_stop_profit_prices()
        self.compute_triggers()
        self.determine_outcome()
        self.calculate_holding_period()
        self.compute_exit_info()
        self.calculate_profit_loss()

    def compute_exit_info(self) -> NoReturn:
        """
        Determines and sets the exit price of the position based on market data and the position type.
        This is a placeholder method; the actual implementation should compute the exit price.
        """
        if self.stop_date == self.market.date.iloc[-1]:
            self.exit_price = self.market.close.iloc[-1]

        else:
            self.exit_price = self.take_profit_price if self.is_win else self.stop_loss_price

        self.exit_value = self.exit_price * self.size

    def update_portfolio_dataframe(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Updates the given portfolio DataFrame with details about the trading position, including size held, holding value,
        position status (long or short), and cash balance adjustments.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with the trading position's details.
        """
        self.add_holding_to_dataframe(dataframe=dataframe)
        self.add_position_to_dataframe(dataframe=dataframe)
        self.add_units_to_dataframe(dataframe=dataframe)
        self.update_cash(dataframe=dataframe)

    def add_total_position_to_dataframe(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Marks the trading position as either long or short in the specified portfolio DataFrame during the holding period.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with the position type information.
        """
        dataframe.loc[self.start_date:self.stop_date, 'open_positions'] += 1

    def add_units_to_dataframe(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Marks the trading position as either long or short in the specified portfolio DataFrame during the holding period.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with the position type information.
        """
        dataframe['units'] += self.holding * self.size

    def add_holding_to_dataframe(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Adds the holding value of the trading position to the specified portfolio DataFrame during the holding period.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with holding value information.
        """
        dataframe['holdings'] += self.holding * (self.size * self.market.close)

    def update_cash(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Updates the cash balance within a portfolio DataFrame based on the entry and exit of the trading position.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with cash balance changes.
        """
        dataframe.loc[self.market.date > self.start_date, 'cash'] -= self.cost

        dataframe.loc[self.market.date > self.stop_date, 'cash'] += self.exit_value

    def set_stop_profit_prices(self) -> NoReturn:
        """Sets stop loss and take profit prices based on risk management strategy."""
        raise NotImplementedError("Must be implemented by subclass.")

    def compute_triggers(self) -> NoReturn:
        """Identifies the market conditions triggering stop loss or take profit."""
        raise NotImplementedError("Must be implemented by subclass.")

    def calculate_profit_loss(self) -> NoReturn:
        """Calculates the profit or loss from the position."""
        raise NotImplementedError("Must be implemented by subclass.")

    def determine_outcome(self) -> NoReturn:
        """
        Determines the outcome of the position.

        Returns:
            int: 0 if neither stop loss nor take profit is triggered,
                 +1 if take profit is triggered first,
                 -1 if stop loss is triggered first.
        """
        # Ensure both triggers are computed, they could be None if not triggered
        self.stop_loss_trigger_idx = len(self.market) if self.stop_loss_trigger_idx is None else self.stop_loss_trigger_idx
        self.take_profit_trigger_idx = len(self.market) if self.take_profit_trigger_idx is None else self.take_profit_trigger_idx

        self.is_win = (self.take_profit_trigger_idx < self.stop_loss_trigger_idx)

    def calculate_holding_period(self) -> NoReturn:
        """
        Generates a holding period series for the trading position, marking the period from the start date to the stop date
        within the market data timeframe. This series is used for visualization and analysis purposes.
        """
        self.holding = pandas.Series(0, index=self.market.index)
        period = (self.market.date > self.start_date) & (self.market.date <= self.stop_date)
        self.holding[period] = 1

    def _add_stop_loss_to_ax(self, ax: plt.Axes) -> NoReturn:
        """
        Adds a horizontal line to a matplotlib axis to visualize the stop-loss level of the trading position.

        Parameters:
            ax (plt.Axes): The matplotlib axis object where the stop-loss level will be visualized.
        """
        ax.fill_between(
            x=self.market.date,
            y1=self.stop_loss_price,
            y2=self.market.close,
            where=self.holding == 1,
            alpha=0.3,
            color='red',
            label='Stop-loss',
        )

        ax.fill_between(
            x=self.market.date,
            y1=self.take_profit_price,
            y2=self.market.close,
            where=self.holding == 1,
            alpha=0.3,
            color='green',
            label='Take-profit',
        )

    def get_is_open_at_date(self, date: object) -> bool:
        if (date < self.start_date) or (date > self.stop_date):
            return False

        return True

    def _add_triggers_to_ax(self, ax: plt.Axes) -> NoReturn:
        """
        Marks the triggers for stop-loss and take-profit on a given matplotlib axis with scatter points.

        Parameters:
            ax (plt.Axes): The matplotlib axis object where the trigger events will be visualized.
        """
        match self.is_win:
            case 1:
                ax.scatter(
                    x=self.market.at[self.take_profit_trigger_idx, 'date'],
                    y=self.take_profit_price,
                    color='green',
                    s=10,
                    label='Take-profit Triggered',
                    zorder=5
                )

            case -1:
                ax.scatter(
                    x=self.market.at[self.stop_loss_trigger_idx, 'date'],
                    y=self.stop_loss_price,
                    color='red',
                    s=10,
                    label='Stop-loss Triggered',
                    zorder=5
                )

    def _add_holding_area_to_ax(self, ax: plt.Axes) -> NoReturn:
        """
        Highlights the holding period of the trading position on a given matplotlib axis using a fill_between operation.

        Parameters:
            ax (plt.Axes): The matplotlib axis object where the holding period will be visualized.
        """
        ax.fill_between(
            self.market['date'].values,
            y1=0,
            y2=1,
            where=self.holding != 0,
            transform=ax.get_xaxis_transform(),
            color='gray',
            alpha=0.3,
            label='Holding Period'
        )

    def plot(self) -> NoReturn:
        """
        Visualizes the trading position on a price chart. Highlights include the entry and exit points,
        stop loss and take profit levels, and the duration of the position. This method provides a graphical
        overview of the position's performance within the market context.
        """
        ax = self.market.plot(
            x='date',
            y='close',
            figsize=(10, 6),
            title=f'Position Overview [{self.type}]',
            label='Market Close'
        )

        self.market.plot(
            x='date',
            y='high',
            ax=ax,
            label='Market High'
        )

        self.market.plot(
            x='date',
            y='low',
            ax=ax,
            label='Market Low'
        )

        self._add_holding_area_to_ax(ax=ax)
        self._add_triggers_to_ax(ax=ax)
        self._add_stop_loss_to_ax(ax=ax)
        plt.legend()
        plt.show()

    def _compute_stop_date(self) -> NoReturn:
        self.stop_date_idx = min(
            filter(pandas.notna, [self.stop_loss_trigger_idx, self.take_profit_trigger_idx, len(self.market) - 1])
        )

        self.stop_date = self.market.date.iloc[self.stop_date_idx]


class Long(BasePosition):
    type = 'long'

    def set_stop_profit_prices(self) -> NoReturn:
        self.stop_loss_price = self.entry_price - self.risk_management.stop_loss
        self.take_profit_price = self.entry_price + self.risk_management.take_profit

    def compute_triggers(self) -> NoReturn:
        """
        Computes the trigger levels and dates for stop-loss and take-profit based on the market data and the position type.
        Sets the respective attributes for stop-loss and take-profit prices, as well as the earliest trigger date.
        """
        self.stop_loss_trigger_idx = self.market.close \
            .where(self.market.date > self.start_date) \
            .where(self.market.low.le(self.stop_loss_price)).first_valid_index()

        self.take_profit_trigger_idx = self.market.close \
            .where(self.market.date > self.start_date) \
            .where(self.market.high.ge(self.take_profit_price)).first_valid_index()

        self._compute_stop_date()

    def add_position_to_dataframe(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Marks the trading position as either long or short in the specified portfolio DataFrame during the holding period.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with the position type information.
        """
        dataframe['long_positions'] += self.holding

    def calculate_profit_loss(self) -> NoReturn:
        """ Return the cash value that this position made over time """
        self.profit_loss = -(self.cost - self.exit_value)


class Short(BasePosition):
    type = 'short'

    def set_stop_profit_prices(self) -> NoReturn:
        self.stop_loss_price = self.entry_price + self.risk_management.stop_loss
        self.take_profit_price = self.entry_price - self.risk_management.take_profit

    def add_position_to_dataframe(self, dataframe: pandas.DataFrame) -> NoReturn:
        """
        Marks the trading position as either long or short in the specified portfolio DataFrame during the holding period.

        Parameters:
            dataframe (pandas.DataFrame): The portfolio DataFrame to be updated with the position type information.
        """
        dataframe['short_positions'] += self.holding

    def compute_triggers(self) -> NoReturn:
        """
        Computes the trigger levels and dates for stop-loss and take-profit based on the market data and the position type.
        Sets the respective attributes for stop-loss and take-profit prices, as well as the earliest trigger date.
        """
        self.stop_loss_trigger_idx = self.market.close \
            .where(self.market.date > self.start_date) \
            .where(self.market.high.ge(self.stop_loss_price)).first_valid_index()

        self.take_profit_trigger_idx = self.market.close \
            .where(self.market.date > self.start_date) \
            .where(self.market.high.le(self.take_profit_price)).first_valid_index()

        self._compute_stop_date()

    def calculate_profit_loss(self) -> NoReturn:
        """ Return the cash value that this position made over time """
        self.profit_loss = (self.cost - self.exit_value)

# -
