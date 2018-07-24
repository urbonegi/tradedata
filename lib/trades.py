import json
import os

from enum import Enum
import pandas as pd
from utils import get_csv_files, is_none_decorator


TRADE_COLUMN_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../trade_data_conf.json')
with open(TRADE_COLUMN_CONFIG, 'r') as f:
    trade_col_data = json.load(f)
    INITIAL_COLUMNS = sorted(trade_col_data, key=trade_col_data.__getitem__)


class TradeDataColumns(Enum):
    # For data reprentation
    market_val = 1
    instr_market_val = 2
    instr_closing_val = 3
    instr_average_price = 4

names = INITIAL_COLUMNS + [m.name for m in TradeDataColumns]
TradeDataColumns = Enum('TradeDataColumns', names)


class TradePanda(object):
    def __init__(self, trade_df):
        self.df = trade_df
        self._clean()
        self._add_additional_data_col()
        self._add_additional_attributes()

    def _add_additional_attributes(self):
        self.trade_days = self.df[TradeDataColumns.date.name].unique()
        # Daily df
        self.daily_df = self.df.groupby(TradeDataColumns.date.name).agg({TradeDataColumns.market_val.name: ['sum', 'count']})
        # Instrument df
        instr_markt_val = self.df.groupby([TradeDataColumns.instrument.name, TradeDataColumns.date.name,
                                           TradeDataColumns.instr_closing_val.name,
                                           TradeDataColumns.instr_average_price.name])[TradeDataColumns.market_val.name].sum()
        self.instrument_df = pd.DataFrame({'instrument_daily_market_val' : instr_markt_val}).reset_index()

    def _clean(self):
        self.df.drop_duplicates()
        self.df = self.df.reset_index(drop=True)
        self.df[TradeDataColumns.date.name] = self.df[TradeDataColumns.date.name].apply(str)
        self.df[TradeDataColumns.quantity.name] = self.df[TradeDataColumns.quantity.name].apply(int)
        self.df[TradeDataColumns.time_in_milsec.name] = self.df[TradeDataColumns.time_in_milsec.name].apply(int)
        self.df[TradeDataColumns.price.name] = self.df[TradeDataColumns.price.name].apply(float)

    def _add_additional_data_col(self):
        self.df[TradeDataColumns.market_val.name] = self.df.apply(self.get_market_value, axis=1)
        self.df[[TradeDataColumns.instr_closing_val.name, TradeDataColumns.instr_average_price.name]] = \
            self.df.apply(self.get_closing_value_average_price, axis=1, result_type="expand")

    def get_market_value(self, x):
        """
        Pandas apply
        Calculate market value for each trade
        """
        return int(x[TradeDataColumns.quantity.name])*float(x[TradeDataColumns.price.name])

    def get_closing_value_average_price(self, x):
        """
        Pandas apply
        Filter by date and instrument,
        get last traded price and
        average price per day
        """
        instr = str(x[TradeDataColumns.instrument.name])
        date = str(x[TradeDataColumns.date.name])
        condition = (self.df[TradeDataColumns.instrument.name] == instr) & (self.df[TradeDataColumns.date.name] == date)
        # Instrument closing value is last traded price
        instr_closing_value = self.df[condition].nlargest(1, TradeDataColumns.time_in_milsec.name)[TradeDataColumns.price.name].values[0]
        # Instrument average price is all instrument trades market values divided by total instrument quantity traded
        avg_price = self.df[condition][TradeDataColumns.market_val.name].sum()/self.df[condition][TradeDataColumns.quantity.name].sum()
        return instr_closing_value, avg_price


class TradesData(object):
    """
    Controller Class loads trading data, stores main trade dataframe
    in-memory for further processing, usage and representation
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Using Singleton pattern to share loaded dataframe in the app
        """
        print('In new')
        if not cls._instance:
            print('Assigning new instance')
            instance = super(TradesData, cls).__new__(cls, *args, **kwargs)
            cls._instance = instance
        return cls._instance

    def process_trade_data(self, dir):
        pd_dfs = []
        csv_files = get_csv_files(dir)
        for file in csv_files:
            df = pd.read_csv(file, sep=',', names=INITIAL_COLUMNS)
            pd_dfs.append(df)
        self.trades = None
        if pd_dfs:
            print('Loading trade data into memory... Takes time... Wait for it...')
            df = pd.concat(pd_dfs)
            self.trades = TradePanda(df)

    @is_none_decorator('trades')
    def get_trade_data(self, reference=None):
        """
        Controller to get trades dataframe
        """
        if reference is not None:
            res_df = self.trades.df.loc[self.trades.df[TradeDataColumns.trade_ref.name]==reference]
        else:
            res_df = self.trades.df
        return res_df[[TradeDataColumns.instrument.name, TradeDataColumns.date.name,
                               TradeDataColumns.time_in_milsec.name, TradeDataColumns.price.name,
                               TradeDataColumns.quantity.name, TradeDataColumns.market_val.name,
                               TradeDataColumns.trade_ref.name]]

    @is_none_decorator('trades')
    def get_instrument_summary(self, instrument=None):
        """
        Controller to get instrument summary dataframe
        """
        if instrument is not None:
            return self.trades.instrument_df.loc[self.trades.instrument_df[TradeDataColumns.instrument.name]==instrument]
        return self.trades.instrument_df

    @is_none_decorator('trades')
    def get_daily_summary(self):
        return self.trades.daily_df
