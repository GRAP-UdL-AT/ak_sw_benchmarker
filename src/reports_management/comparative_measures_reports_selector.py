"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:

Use:
"""

from enum import IntEnum
class ComparativeMeasuresReportSelector(IntEnum):
    DEPTH = 0
    A1 = 1  # todo CHANGE after
    A2 = 2
    WEIGHT = 3
    ALL = 4
    DEFAULT = 5
