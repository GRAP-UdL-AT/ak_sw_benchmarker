"""
# Project: Fruit Size Estimation
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Test for methods used for size estimation of fruits

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_size_estimation.py

"""
import unittest
from reports_management.metrics_calculations import MetricsCalculations


class TestMetricsCalculated(unittest.TestCase):

    def setUp(self):
        self.metrics_calculated = MetricsCalculations('gr.')
        pass

    def test_print_metrics(self):
        print(self.test_print_metrics.__name__)
        # ----------------------------------
        self.metrics_calculated.print_metrics()
        # ----------------------------------
        self.assertEqual('OK', 'OK')

    def test_str_metrics(self):
        print(self.test_print_metrics.__name__)
        # ----------------------------------
        str_print = self.metrics_calculated
        print(str_print)
        exp_str_print = '0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0'
        # ----------------------------------
        # todo: add check here
        #self.assertEqual(str_print, exp_str_print)
        self.assertEqual('OK', 'OK')

if __name__ == '__main__':
    unittest.main()
