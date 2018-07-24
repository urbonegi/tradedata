import mock
import unittest
import os

import numpy
import pandas

import lib
from lib.trades import TradesData
import lib.trades

class TradesDataTestCase(unittest.TestCase):

    def test_same_class_instance_used(self):
        trd = TradesData()
        trd2 = TradesData()
        self.assertEqual(trd, trd2)
        trd.a = 'cat'
        trd2.a = 'dog'
        self.assertEqual(trd.a, 'dog')
        self.assertEqual(trd2.a, 'dog')

    @mock.patch('lib.trades.get_csv_files', return_value=[])
    def test_none_decorator(self, mock_get_files):
        trd = TradesData()
        trd.process_trade_data('It is mocked, we do not care')
        self.assertEqual(trd.get_trade_data(), 'Trade data is not loaded.')
        self.assertEqual(trd.get_instrument_summary(), 'Trade data is not loaded.')
        self.assertEqual(trd.get_daily_summary(), 'Trade data is not loaded.')
        mock_get_files.assert_called_once_with('It is mocked, we do not care')
