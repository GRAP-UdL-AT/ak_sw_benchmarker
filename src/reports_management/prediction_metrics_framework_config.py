"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: November 2021
Description:

Use:
"""

from dataset_management.dataset_config import DatasetConfig
from dataset_management.dataset_manager import DatasetManager
from data_features_processor.data_features_config import DataFeatureConfig
from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector
from reports_management.comparative_measures_reports_selector import ComparativeMeasuresReportSelector


class PredictionsMetricsFrameworkConfig:
    """
    Set of parameters for configuration used in MassEstimationMetricsFramework class
    """
    dataset_manager = None
    path_day_measures = None
    data_features_options = None
    weight_prediction_option = None  # todo: change name
    comparative_report_option = None
    # ---------------------------------
    header_day_measures = ['date_capture', 'time_capture', 'fruit_id', 'pred.obj_detection', 'pred.axis_01_px',
                            'pred.axis_02_px', 'pred.depth_mm', 'pred.axis_01_mm', 'pred.axis_02_mm', 'pred.weight_gr']

    # create pandas dataframe with columns
    header_day_comparative = [
        'date_capture', 'time_capture', 'fruit_id',
        'lab.tree', 'lab.fruit_label', 'lab.depth_mm', 'lab.o_caliber_mm', 'lab.o_height_mm', 'lab.axis_01_mm', 'lab.axis_02_mm', 'lab.weight_gr', 'lab.observations',
        'pred.obj_detection', 'pred.axis_01_px', 'pred.axis_02_px', 'pred.depth_mm', 'pred.axis_01_mm',
        'pred.axis_02_mm', 'pred.weight_gr'
    ]

    # ---------------------------------

    def __init__(self, dataset_manager_config: DatasetConfig, path_day_measures,
                 data_features_options: DataFeatureConfig, weight_prediction_selector: WeightPredictionModelSelector,
                 comparative_report_option: ComparativeMeasuresReportSelector):
        self.dataset_manager = DatasetManager(dataset_manager_config)
        self.path_day_measures = path_day_measures
        self.data_features_options = data_features_options
        self.weight_prediction_option = weight_prediction_selector
        self.comparative_report_option = comparative_report_option
