"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/
Author: Juan Carlos Miranda
Date: February 2022
Description:
  Configuration of benchmarking user interface

Use:

"""
import os
import configparser


class GUIBenchmarkingConfig:
    app_title = 'ak_sw_benchmarker'
    width = 320
    height = 480
    geometry_about = '300x480'
    geometry_main = '320x480'
    file_extension_to_search = "*.csv"
    base_folder = os.path.abspath('')
    input_folder = os.path.join(base_folder)
    output_folder = os.path.join(base_folder)
    file_browser_input_folder = os.path.join(base_folder)

    def __init__(self, file_config_name=None):
        if file_config_name is not None:
            if os.path.isfile(file_config_name):
                self.f_config_name = file_config_name
                self.read_config()

    def read_config(self):
        """
        Read config from file ui_settings.conf
        :return:
        """
        f_config = configparser.ConfigParser()
        f_config.read(self.f_config_name)
        self.width = f_config['DEFAULT']['WIDTH']
        self.height = f_config['DEFAULT']['HEIGHT']
        self.geometry_about = f_config['DEFAULT']['geometry_about']
        self.geometry_main = f_config['DEFAULT']['geometry_main']
        self.file_extension_to_search = f_config['DEFAULT']['file_extension_to_search']
        self.base_folder = f_config['DEFAULT']['base_folder']
        self.input_folder = f_config['DEFAULT']['input_folder']
        self.output_folder = f_config['DEFAULT']['output_folder']
        self.file_browser_input_folder = f_config['DEFAULT']['file_browser_input_folder']
