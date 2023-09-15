"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/
Author: Juan Carlos Miranda
Date: February 2022
Description:
  Test for methods used to check automatic metrics against a data calculated by a system.
  This assumes an example datasheet and obtains metrics from a fixed method
  The columns pred.caliber_mm, pred.height_mm, pred.mass_gr contains known dummy values to check metrics procedures
  The procedures were checked at 22/02/2022, each measures was compared against an datasheet program
  There are results calculated with sklearn library to check values.
  The .csv with anciliary columns is used to see intermediate steps.

  All metrics were checked against
Usage:
python -m unittest $HOME/development/KA_detector/mass_estimation/test/test_comparative_reports.py
"""
import unittest
import os
import pandas as pd
from math import sqrt
from sklearn.metrics import mean_squared_error, median_absolute_error, mean_absolute_percentage_error, r2_score
from reports_management.metrics_calculations import MetricsCalculations
from reports_management.comparative_measures_reports import ComparativeMeasuresReport
from reports_management.comparative_measures_reports_selector import ComparativeMeasuresReportSelector


class TestComparativeMeasuresReport(unittest.TestCase):

    def setUp(self):
        """
        It assumes a pre-created comparative datashet format
        LABORATORY MEASURES vs  system measures
        :return:
        """
        self.BASE_FOLDER = os.path.abspath('')
        self.day_measures_filename = 'pre_comparative_by_frame_4.csv'
        self.path_input_df = os.path.join(self.BASE_FOLDER, 'test_input_csv')
        self.path_comparative_by_frame = os.path.join(self.path_input_df, self.day_measures_filename)


        self.day_measures_filename_out = 'comparative_by_frame_out.csv'
        self.path_output_df = os.path.join(self.BASE_FOLDER, 'test_output_csv')
        self.path_comparative_by_frame_o = os.path.join(self.path_output_df, self.day_measures_filename_out)

        # at this time this test assumes a merged datasheet by another procedure
        self.comparative_by_frame_df = pd.read_csv(self.path_comparative_by_frame, dtype=str, sep=';')
        self.comparative_by_frame_df['lab.depth_mm'] = self.comparative_by_frame_df['lab.depth_mm'].astype(float)
        self.comparative_by_frame_df['lab.axis_01_mm'] = self.comparative_by_frame_df['lab.axis_01_mm'].astype(float)
        self.comparative_by_frame_df['lab.axis_02_mm'] = self.comparative_by_frame_df['lab.axis_02_mm'].astype(float)
        self.comparative_by_frame_df['lab.weight_gr'] = self.comparative_by_frame_df['lab.weight_gr'].astype(float)

        self.comparative_by_frame_df['pred.depth_mm'] = self.comparative_by_frame_df['pred.depth_mm'].astype(float)
        self.comparative_by_frame_df['pred.axis_01_mm'] = self.comparative_by_frame_df['pred.axis_01_mm'].astype(float)
        self.comparative_by_frame_df['pred.axis_02_mm'] = self.comparative_by_frame_df['pred.axis_02_mm'].astype(float)
        self.comparative_by_frame_df['pred.weight_gr'] = self.comparative_by_frame_df['pred.weight_gr'].astype(float)
        self.a_report = None

    def test_comparative_metrics_selector_mass(self):
        # here we test reports
        # an assembled datasheet with lab measures and system measures
        report_selector = ComparativeMeasuresReportSelector.WEIGHT
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        self.a_report.print_metrics()
        self.assertEqual('OK', 'OK')

    def test_comparative_metrics_selector_depth(self):
        """
        here we test reports an assembled datasheet with lab measures and system measures
        :return:
        """
        report_selector = ComparativeMeasuresReportSelector.DEPTH
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        self.a_report.print_metrics()
        self.assertEqual('OK', 'OK')

    def test_comparative_metrics_selector_caliber(self):
        """
        here we test reports an assembled datasheet with lab measures and system measures
        :return:
        """
        report_selector = ComparativeMeasuresReportSelector.A1
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        self.a_report.print_metrics()
        self.assertEqual('OK', 'OK')

    def test_comparative_metrics_selector_height(self):
        """
        here we test reports an assembled datasheet with lab measures and system measures
        :return:
        """
        report_selector = ComparativeMeasuresReportSelector.A2
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        self.a_report.print_metrics()
        self.assertEqual('OK', 'OK')


    def test_get_calculate_weight_metrics(self):
        """
        Check mass measures
        :return:
        """
        exp_weight_metrics = MetricsCalculations('gr.')
        exp_weight_metrics.total_objects = 17  # CHECKED
        exp_weight_metrics.sum_predict_objects = 2946.0  # CHECKED
        exp_weight_metrics.mean_predict_objects = 173.2941176470588  # CHECKED
        exp_weight_metrics.sum_measured_objects = 2955.2  # CHECKED
        exp_weight_metrics.mean_measured_objects = 173.83529411764704  # CHECKED
        exp_weight_metrics.MSE = 0.372941176470587  # CHECKED
        exp_weight_metrics.MAE = 0.5411764705882329  # TODO: 22/02/2022 This is not the correct result
        exp_weight_metrics.RMSE = 0.6106890996821435  # CHECKED
        exp_weight_metrics.MAPE = 0.0033182835232287125  # CHECKED
        exp_weight_metrics.R2 = 0.9998457573997165  # CHECKED
        # -------------------------
        report_selector = ComparativeMeasuresReportSelector.WEIGHT
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        result_weight_metrics = self.a_report.get_weight_metrics()
        # -------------------------
        # ------------------------
        # using sklearn library
        # ------------------------
        y_true = self.comparative_by_frame_df['lab.weight_gr']
        y_pred = self.comparative_by_frame_df['pred.weight_gr']
        mse_weight = mean_squared_error(y_true, y_pred)
        rmse_weight = sqrt(mse_weight)
        mae_weight = median_absolute_error(y_true, y_pred)
        mape_weight = mean_absolute_percentage_error(y_true, y_pred)
        r2_weight = r2_score(y_true, y_pred)
        print(f'mse_weight={mse_weight}')
        print(f'rmse_weight={rmse_weight}')
        print(f'mae_weight={mae_weight} gr.')
        print(f'mape_weight={mape_weight} %')
        print(f'r2_weight={r2_weight}')
        # -------------------------
        self.assertEqual(exp_weight_metrics.total_objects, result_weight_metrics.total_objects)
        self.assertEqual(exp_weight_metrics.sum_predict_objects, result_weight_metrics.sum_predict_objects)
        self.assertEqual(exp_weight_metrics.mean_predict_objects, result_weight_metrics.mean_predict_objects)
        self.assertEqual(exp_weight_metrics.sum_measured_objects, result_weight_metrics.sum_measured_objects)
        self.assertEqual(exp_weight_metrics.mean_measured_objects, result_weight_metrics.mean_measured_objects)
        self.assertEqual(exp_weight_metrics.MSE, result_weight_metrics.MSE)
        self.assertEqual(exp_weight_metrics.MAE, result_weight_metrics.MAE)
        self.assertEqual(exp_weight_metrics.RMSE, result_weight_metrics.RMSE)
        self.assertEqual(exp_weight_metrics.MAPE, result_weight_metrics.MAPE)
        self.assertEqual(exp_weight_metrics.R2, result_weight_metrics.R2)
        # CHECK sklearn library
        self.assertEqual(exp_weight_metrics.MSE, mse_weight)
        #self.assertEqual(exp_mass_metrics.MAE, mae_weight)
        self.assertEqual(exp_weight_metrics.RMSE, rmse_weight)
        self.assertEqual(exp_weight_metrics.MAPE, mape_weight)
        self.assertEqual(exp_weight_metrics.R2, r2_weight)

    def test_get_calculate_depth_metrics(self):
        exp_depth_metrics = MetricsCalculations('mm.')
        exp_depth_metrics.total_objects = 17  # CHECKED
        exp_depth_metrics.sum_predict_objects = 25093.0  # CHECKED
        exp_depth_metrics.mean_predict_objects = 1476.0588235294117  # CHECKED
        exp_depth_metrics.sum_measured_objects = 25188.0  # CHECKED
        exp_depth_metrics.mean_measured_objects = 1481.6470588235295  # CHECKED
        exp_depth_metrics.MSE = 61.0  # CHECKED
        exp_depth_metrics.MAE = 5.588235294117647  # TODO: 22/02/2022 This is not the correct result
        exp_depth_metrics.RMSE = 7.810249675906654  # CHECKED
        exp_depth_metrics.MAPE = 0.0038493908608176215  # CHECKED
        exp_depth_metrics.R2 = 0.9986873050206022  # CHECKED
        # -------------------------
        report_selector = ComparativeMeasuresReportSelector.DEPTH
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        result_depth_metrics = self.a_report.get_depth_metrics()
        # -------------------------
        # ------------------------
        # using sklearn library
        # ------------------------
        y_true = self.comparative_by_frame_df['lab.depth_mm']
        y_pred = self.comparative_by_frame_df['pred.depth_mm']
        mse_depth = mean_squared_error(y_true, y_pred)
        rmse_depth = sqrt(mse_depth)
        mae_depth = median_absolute_error(y_true, y_pred)
        mape_depth = mean_absolute_percentage_error(y_true, y_pred)
        r2_depth = r2_score(y_true, y_pred)
        print(f'mse_depth={mse_depth}')
        print(f'rmse_depth={rmse_depth}')
        print(f'mae_depth={mae_depth} mm.')
        print(f'mape_depth={mape_depth} %')
        print(f'r2_depth={r2_depth}')
        # -------------------------
        self.assertEqual(exp_depth_metrics.total_objects, result_depth_metrics.total_objects)
        self.assertEqual(exp_depth_metrics.sum_predict_objects, result_depth_metrics.sum_predict_objects)
        self.assertEqual(exp_depth_metrics.mean_predict_objects, result_depth_metrics.mean_predict_objects)
        self.assertEqual(exp_depth_metrics.sum_measured_objects, result_depth_metrics.sum_measured_objects)
        self.assertEqual(exp_depth_metrics.mean_measured_objects, result_depth_metrics.mean_measured_objects)
        self.assertEqual(exp_depth_metrics.MSE, result_depth_metrics.MSE)
        self.assertEqual(exp_depth_metrics.MAE, result_depth_metrics.MAE)
        self.assertEqual(exp_depth_metrics.RMSE, result_depth_metrics.RMSE)
        self.assertEqual(exp_depth_metrics.MAPE, result_depth_metrics.MAPE)
        self.assertEqual(exp_depth_metrics.R2, result_depth_metrics.R2)
        # CHECK sklearn library
        self.assertEqual(exp_depth_metrics.MSE, mse_depth)
        self.assertEqual(exp_depth_metrics.RMSE, rmse_depth)
        self.assertEqual(exp_depth_metrics.MAPE, mape_depth)
        self.assertEqual(exp_depth_metrics.R2, r2_depth)

    def test_get_calculate_axis_01_metrics(self):
        exp_axis_01_metrics = MetricsCalculations('mm.')
        exp_axis_01_metrics.total_objects = 17  # CHECKED
        exp_axis_01_metrics.sum_predict_objects = 1210.0  # CHECKED
        exp_axis_01_metrics.mean_predict_objects = 71.17647058823529  # CHECKED
        exp_axis_01_metrics.sum_measured_objects = 1218.6000000000001  # CHECKED
        exp_axis_01_metrics.mean_measured_objects = 71.68235294117648  # CHECKED
        exp_axis_01_metrics.MSE = 0.3135411764705905  # CHECKED
        exp_axis_01_metrics.MAE = 0.5058823529411782  # TODO: 22/02/2022 This is not the correct result
        exp_axis_01_metrics.RMSE = 0.5599474765284602  # CHECKED
        exp_axis_01_metrics.MAPE = 0.006972017508493307  # CHECKED
        exp_axis_01_metrics.R2 = 0.9924911415617047  # CHECKED
        # -------------------------
        report_selector = ComparativeMeasuresReportSelector.A1
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        result_axis_01_metrics = self.a_report.get_axis_01_metrics()
        # -------------------------
        # ------------------------
        # using sklearn library
        # ------------------------
        y_true = self.comparative_by_frame_df['lab.axis_01_mm']
        y_pred = self.comparative_by_frame_df['pred.axis_01_mm']
        mse_axis_01 = mean_squared_error(y_true, y_pred)
        rmse_axis_01 = sqrt(mse_axis_01)
        mae_axis_01 = median_absolute_error(y_true, y_pred)
        mape_axis_01 = mean_absolute_percentage_error(y_true, y_pred)
        r2_axis_01 = r2_score(y_true, y_pred)
        print(f'mse_axis_01={mse_axis_01}')
        print(f'rmse_axis_01={rmse_axis_01}')
        print(f'mae_axis_01={mae_axis_01} mm.')
        print(f'mape_axis_01={mape_axis_01} %')
        print(f'r2_axis_01={r2_axis_01}')
        # -------------------------
        self.assertEqual(exp_axis_01_metrics.total_objects, result_axis_01_metrics.total_objects)
        self.assertEqual(exp_axis_01_metrics.sum_predict_objects, result_axis_01_metrics.sum_predict_objects)
        self.assertEqual(exp_axis_01_metrics.mean_predict_objects, result_axis_01_metrics.mean_predict_objects)
        self.assertEqual(exp_axis_01_metrics.sum_measured_objects, result_axis_01_metrics.sum_measured_objects)
        self.assertEqual(exp_axis_01_metrics.mean_measured_objects, result_axis_01_metrics.mean_measured_objects)
        self.assertEqual(exp_axis_01_metrics.MSE, result_axis_01_metrics.MSE)
        self.assertEqual(exp_axis_01_metrics.MAE, result_axis_01_metrics.MAE)
        self.assertEqual(exp_axis_01_metrics.RMSE, result_axis_01_metrics.RMSE)
        self.assertEqual(exp_axis_01_metrics.MAPE, result_axis_01_metrics.MAPE)
        self.assertEqual(exp_axis_01_metrics.R2, result_axis_01_metrics.R2)
        # CHECK sklearn library
        self.assertEqual(exp_axis_01_metrics.MSE, mse_axis_01)
        #self.assertEqual(exp_caliber_metrics.MAE, mae_caliber)
        self.assertEqual(exp_axis_01_metrics.RMSE, rmse_axis_01)
        self.assertEqual(exp_axis_01_metrics.MAPE, mape_axis_01)
        self.assertEqual(exp_axis_01_metrics.R2, r2_axis_01)


    def test_get_calculate_axis_02_metrics(self):
        exp_axis_02_metrics = MetricsCalculations('mm.')
        exp_axis_02_metrics.total_objects = 17  # CHECKED
        exp_axis_02_metrics.sum_predict_objects = 1158.0  # CHECKED
        exp_axis_02_metrics.mean_predict_objects = 68.11764705882354  # CHECKED
        exp_axis_02_metrics.sum_measured_objects = 1164.1599999999999  # CHECKED
        exp_axis_02_metrics.mean_measured_objects = 68.47999999999999  # CHECKED
        exp_axis_02_metrics.MSE = 0.19058823529411814  # CHECKED
        exp_axis_02_metrics.MAE = 0.3623529411764712  # TODO: 22/02/2022 This is not the correct result
        exp_axis_02_metrics.RMSE = 0.43656412506539993  # CHECKED
        exp_axis_02_metrics.MAPE = 0.005549650350799257  # CHECKED
        exp_axis_02_metrics.R2 = 0.9975255902841844  # CHECKED
        # -------------------------
        report_selector = ComparativeMeasuresReportSelector.A2
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        result_height_metrics = self.a_report.get_axis_02_metrics()
        # -------------------------
        y_true = self.comparative_by_frame_df['lab.axis_02_mm']
        y_pred = self.comparative_by_frame_df['pred.axis_02_mm']

        mse_axis_02 = mean_squared_error(y_true, y_pred)
        rmse_axis_02 = sqrt(mse_axis_02)
        mae_axis_02 = median_absolute_error(y_true, y_pred)
        mape_axis_02 = mean_absolute_percentage_error(y_true, y_pred)
        r2_axis_02 = r2_score(y_true, y_pred)

        print(f'mse_axis_02={mse_axis_02}')
        print(f'rmse_axis_02={rmse_axis_02}')
        print(f'mae_axis_02={mae_axis_02} mm.')
        print(f'mape_axis_02={mape_axis_02} %')
        print(f'r2_axis_02={r2_axis_02}')
        # -------------------------
        self.assertEqual(exp_axis_02_metrics.total_objects, result_height_metrics.total_objects)
        self.assertEqual(exp_axis_02_metrics.sum_predict_objects, result_height_metrics.sum_predict_objects)
        self.assertEqual(exp_axis_02_metrics.mean_predict_objects, result_height_metrics.mean_predict_objects)
        self.assertEqual(exp_axis_02_metrics.sum_measured_objects, result_height_metrics.sum_measured_objects)
        self.assertEqual(exp_axis_02_metrics.mean_measured_objects, result_height_metrics.mean_measured_objects)
        self.assertEqual(exp_axis_02_metrics.MSE, result_height_metrics.MSE)
        self.assertEqual(exp_axis_02_metrics.MAE, result_height_metrics.MAE)
        self.assertEqual(exp_axis_02_metrics.RMSE, result_height_metrics.RMSE)
        self.assertEqual(exp_axis_02_metrics.MAPE, result_height_metrics.MAPE)
        self.assertEqual(exp_axis_02_metrics.R2, result_height_metrics.R2)
        # CHECK sklearn library
        self.assertEqual(exp_axis_02_metrics.MSE, mse_axis_02)
        #self.assertEqual(exp_height_metrics.MAE, mae_height)
        self.assertEqual(exp_axis_02_metrics.RMSE, rmse_axis_02)
        self.assertEqual(exp_axis_02_metrics.MAPE, mape_axis_02)
        self.assertEqual(exp_axis_02_metrics.R2, r2_axis_02)


    def test_export_data_CSV(self):
        report_selector = ComparativeMeasuresReportSelector.WEIGHT
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        self.a_report.export_data_csv(self.path_comparative_by_frame_o)
        exp_file_created = True
        file_created = os.path.isfile(self.path_comparative_by_frame_o)
        self.assertEqual(exp_file_created, file_created)

    def test_get_comparative_df(self):
        report_selector = ComparativeMeasuresReportSelector.WEIGHT
        self.a_report = ComparativeMeasuresReport(self.comparative_by_frame_df, report_selector)
        a_comparative_df = self.a_report.get_comparative_df()
        exp_comparative_df = (17, 29)  # this check if columns changed
        self.assertEqual(exp_comparative_df, a_comparative_df.shape)


if __name__ == '__main__':
    unittest.main()



