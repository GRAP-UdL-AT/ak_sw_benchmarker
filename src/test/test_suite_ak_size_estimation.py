"""
Project: Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: February 2022
Description:
    Suit to test all classes from mass_estimation, don't forget to add new tests HERE!

Use:
    python -m unittest mass_estimation/test/test_suite_mass_estimation.py
"""

import unittest

# PARAMETERS
from camera_management_s.test.test_camera_parameters import TestCameraParameters

# BBOX
from size_estimation_s.test.test_size_estimation_px_bbox import TestSizeEstimationPxBbox
from depth_estimation_s.test.test_depth_estimation import TestDepthEstimation
from data_features_processor.test.test_features_extraction import TestDataFeatureProcessor

# MASK
from size_estimation_s.test.test_size_estimation_px_mask import TestSizeEstimationPxMask
from depth_estimation_s.test.test_depth_estimation_mask import TestDepthEstimationMask
from data_features_processor.test.test_features_extraction_mask import TestDataFeatureProcessorMask

# CALCULATIONS
from reports_management.test.test_metrics_calculated import TestMetricsCalculated
from weight_prediction_s.test.test_weight_prediction import TestWeightPredictionMethods
from data_features_processor.test.test_data_feature_config import TestDataFeatureConfig
from reports_management.test.test_comparative_reports import TestComparativeMeasuresReport


def weight_prediction_suite():
    """
        Gather all the tests to process data from detected objects in all levels
    """
    test_suite = unittest.TestSuite()

    # DATA MANAGEMENT # todo: add here tests for data management

    # TODO: 28/07/2022 add datasheet headers tests
    # PARAMETERS
    test_suite.addTest(unittest.makeSuite(TestCameraParameters))  # Camera parameters
    # TODO: ADD TESTES FOR SELECTORS HERE
    #TODO: ADD TEST FOR WEIGHT PREDICTION MODEL SELECTOR

    # BOUNDING BOX CIRCUIT
    # Here we put all test related to bounding box calculations
    test_suite.addTest(unittest.makeSuite(TestDepthEstimation))  # 17/02/2023 OK
    test_suite.addTest(unittest.makeSuite(TestSizeEstimationPxBbox))  # 17/02/2023 OK
    # todo: add here   test_weight_prediction TestWeightPredictionMethods
    test_suite.addTest(unittest.makeSuite(TestDataFeatureProcessor))  #

    # MASK CIRCUIT
    # Here we put all test related to mask calculations
    test_suite.addTest(unittest.makeSuite(TestDepthEstimationMask))  # 17/02/2023 OK
    test_suite.addTest(unittest.makeSuite(TestSizeEstimationPxMask))  # 17/02/2023 OK
    # todo: add here   test_weight_prediction TestWeightPredictionMethods
    test_suite.addTest(unittest.makeSuite(TestDataFeatureProcessorMask))  #

    # REPORTS
    test_suite.addTest(unittest.makeSuite(TestMetricsCalculated))  # Metric calculations storage
    test_suite.addTest(unittest.makeSuite(TestWeightPredictionMethods))  # Statistical models
    test_suite.addTest(unittest.makeSuite(TestDataFeatureConfig))  # 17/02/2023 OK # Check features configurations
    test_suite.addTest(unittest.makeSuite(TestComparativeMeasuresReport))  # Metrics calculations MAE, MSE, RMSE, R2

    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(weight_prediction_suite())
