"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: November 2021
Description:

Use:
"""

from enum import IntEnum
class ROISelector(IntEnum):
    """
    Used to get region of fruits, could be bounding box vs bounding box coordinates and masks
    """
    BBOX = 0  # Methods based on bounding box
    MASK = 1  # Methods based on binary masks
