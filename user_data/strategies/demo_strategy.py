import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from typing import Optional, Union
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class DemoStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short: bool = False  # Can this strategy go short?
    # Minimal ROI designed for the strategy.
    minimal_roi = {
        # Exit when 1% profit was reached (in effect after 60 minutes)
        "60": 0.01,
        # Exit when 2% profit was reached (in effect after 30 minutes)
        "30": 0.02,
        "0": 0.04  # Exit whenever 4% profit was reached
    }

    stoploss = -0.05  # Exit whenever 5% loss reached
    # The stoploss will be adjusted to be always -10% of the highest observed price.
    trailing_stop = True

    timeframe = '5m'  # The time frame of each candle

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }

    # Get data about other coins or time interval except for the default keypair this strategy runs on
    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Get into a Long position whenever rsi cross above 70 and the volume isn't 0
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 70)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Exit the position whenever rsi cross below 50 and the volume isn't 0
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['rsi'], 50)) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),

            'exit_long'] = 1

        return dataframe
