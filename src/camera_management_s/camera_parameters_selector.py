"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    Configuration of cameras
Use:
"""

from enum import IntEnum
class CameraModelSelector(IntEnum):
    AK = 0  # For Azure Kinect parameters
    KINECT_V2 = 1  # For Kinect V2 parameters