import unittest
import os

import numpy
import pandas

import lib
from lib.trades import TradePanda, setup_columns

class TradePandaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TEST_TRADE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/test_trade_data.csv')
        cls.INITIAL_COLUMNS, cls.TradeDataColumns = setup_columns()
        trade_df = pandas.read_csv(TEST_TRADE_FILE, sep=',', names=cls.INITIAL_COLUMNS)
        cls.trd_panda = TradePanda(trade_df)

    def test_trade_panda_data_clean(self):
        self.assertEqual(type(self.trd_panda.df[self.TradeDataColumns.date.name].iloc[0]), str)
        self.assertEqual(type(self.trd_panda.df[self.TradeDataColumns.quantity.name].iloc[0]), numpy.int64)
        self.assertEqual(type(self.trd_panda.df[self.TradeDataColumns.time_in_milsec.name].iloc[0]), numpy.int64)
        self.assertEqual(type(self.trd_panda.df[self.TradeDataColumns.price.name].iloc[0]), numpy.float64)

    def test_trade_panda_additional_col(self):
        self.assertIsNotNone(self.trd_panda.df[self.TradeDataColumns.market_val.name])
        self.assertIsNotNone(self.trd_panda.df[self.TradeDataColumns.instr_average_price.name])
        self.assertIsNotNone(self.trd_panda.df[self.TradeDataColumns.instr_closing_val.name])

    def test_trade_panda_additional_attributes(self):
        for d in self.trd_panda.trade_days:
            self.assertIn(str(d), ["20110624", "20110623"])
        self.assertIsNotNone(self.trd_panda.instrument_df)
        for count in self.trd_panda.daily_df["market_val"]["count"]:
            self.assertIn(int(count), [20, 30])


class TradePandaIncompleFileTestCase(TradePandaTestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TRADE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/test_trade_data2.csv')
        cls.INITIAL_COLUMNS, cls.TradeDataColumns = setup_columns()
        trade_df = pandas.read_csv(TEST_TRADE_FILE, sep=',', names=cls.INITIAL_COLUMNS)
        cls.trd_panda = TradePanda(trade_df)

    def test_assert_missing_fields(self):
        for instrument_type in self.trd_panda.df[self.TradeDataColumns.instrument_type.name]:
            self.assertTrue(pandas.isnull(instrument_type))
        for underlying_asset in self.trd_panda.df[self.TradeDataColumns.underlying_asset.name]:
            self.assertTrue(pandas.isnull(underlying_asset))
        for cl_ref in self.trd_panda.df[self.TradeDataColumns.client_ref.name]:
            self.assertTrue(pandas.isnull(cl_ref))



class TradePandaDifferentColOrderTestCase(TradePandaTestCase):

    @classmethod
    def setUpClass(cls):
        TEST_TRADE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/test_trade_data3.csv')
        PANDAS_COL_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/test_trade_data_conf.json')
        cls.INITIAL_COLUMNS, cls.TradeDataColumns = setup_columns(data_column_config=PANDAS_COL_CONFIG)
        trade_df = pandas.read_csv(TEST_TRADE_FILE, sep=',', names=cls.INITIAL_COLUMNS)
        cls.trd_panda = TradePanda(trade_df)

    def test_check_different_data_col_order(self):
        self.assertEqual(self.INITIAL_COLUMNS[0], u'date')
        self.assertEqual(self.INITIAL_COLUMNS[1], u'instrument')
