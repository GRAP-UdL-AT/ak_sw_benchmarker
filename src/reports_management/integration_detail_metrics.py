"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    This file extracts details of each combination of parameters and executes methods
    All combinations of test must be updated here
        # TODO: these test are implemented in class integration_detail_metrics.py. This is an integration test
            replace test saved in ./method_all
Use:
        integrations_detail_tests = IntegrationDetailMetrics(datetime_experiment, camera_option, comparative_report_option, dataset_manager_config, self.path_manual_measures_entry.get(), path_output_simulation)
        integrations_detail_tests.test_run_simulation_masks()

"""
import os
import pandas as pd
# ------------------
from dataset_management.dataset_config import DatasetConfig
# ------------------
from data_features_processor.data_features_config import DataFeatureConfig
from data_features_processor.data_features_config import ROISelector
from size_estimation_s.size_estimation_methods import SizeEstimationSelectorPx
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from reports_management.prediction_metrics_framework import PredictionsMetricsFrameworkConfig
from reports_management.prediction_metrics_framework import PredictionMetricsFramework


class IntegrationDetailMetrics:
    def __init__(self, datetime_experiment_str, camera_option, comparative_report_option,
                 dataset_manager_config: DatasetConfig, path_manual_measures_entry, path_output_simulation):

        self.path_output_simulation = os.path.join(path_output_simulation)
        self.path_output_plots = os.path.join(self.path_output_simulation, 'plots')

        self.datetime_experiment = datetime_experiment_str
        self.base_filename = 'comp_'
        self.extension_csv = '.csv'
        self.path_output_csv = os.path.join(self.path_output_simulation, 'output_csv')

        # --------------------------------------
        # LABORATORY MEASURES
        # --------------------------------------
        path_manual_measures_df = os.path.join(path_manual_measures_entry)
        manual_measures_df = pd.read_csv(path_manual_measures_df, dtype=str, sep=';')
        manual_measures_df['fruit_id'] = manual_measures_df['fruit_id'].astype(str)
        manual_measures_df['lab.axis_01_mm'] = manual_measures_df['lab.axis_01_mm'].astype(float)
        manual_measures_df['lab.axis_02_mm'] = manual_measures_df['lab.axis_02_mm'].astype(float)
        manual_measures_df['lab.weight_gr'] = manual_measures_df['lab.weight_gr'].astype(float)
        self.measures_selected_df = manual_measures_df  # global parameter
        # --------------------------------------
        # global parameters
        self.dataset_manager_config = dataset_manager_config
        self.camera_option = camera_option

        self.comparative_report_option = comparative_report_option
        self.roi_selector = None
        self.size_estimation_selector = None
        self.depth_option = None
        self.weight_prediction_option = None
        # --------------------------------------

    def mask_comparative_1(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.AVG
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_2(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.MOD
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_3(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.MIN
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_4(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.MAX
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_5(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.CENTROID
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_6(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.AVG
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_7(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.MOD
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_8(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.MIN
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_9(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.MAX
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_10(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.CENTROID
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------
    # -------------------------------
    def mask_comparative_11(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.AVG
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_12(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.MOD
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_13(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.MIN
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_14(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.MAX
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_15(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.CENTROID
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    # -------------------------------
    def mask_comparative_16(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.AVG
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_17(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.MOD
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_18(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.MIN
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_19(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.MAX
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def mask_comparative_20(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.CENTROID
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def bbox_comparative_1(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.AVG
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def bbox_comparative_2(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.MOD
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def bbox_comparative_3(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.MIN
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def bbox_comparative_4(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.MAX
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def bbox_comparative_5(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.CENTROID
        self.weight_prediction_option = None

        self.day_measures_filename = self.datetime_experiment + \
                                     self.base_filename + \
                                     self.roi_selector.name + '_' + \
                                     self.size_estimation_selector.name + '_' + \
                                     self.depth_option.name + '_' + \
                                     self.comparative_report_option.name + \
                                     self.extension_csv
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        # ------ run
        self.run_comparative()
        # ----------

    def run_comparative(self):
        """
        Here are grouped all methods to run simulation
        :return:
        """
        data_features_options = DataFeatureConfig(camera_conf=self.camera_option.rgb_sensor,
                                                  roi_selector=self.roi_selector,
                                                  size_estimation_selector=self.size_estimation_selector,
                                                  depth_selector=self.depth_option,
                                                  weight_selector=self.weight_prediction_option)
        # -----------------------------
        self.simulator_config = PredictionsMetricsFrameworkConfig(self.dataset_manager_config,
                                                                  self.path_day_measures,
                                                                  data_features_options,
                                                                  self.weight_prediction_option,
                                                                  self.comparative_report_option)
        # -----------------------------
        simulator_metrics = PredictionMetricsFramework(self.simulator_config)
        # -----------------------------
        if self.roi_selector.name == ROISelector.BBOX.name:
            simulator_metrics.comparative_metrics_dataset_bbox(self.measures_selected_df)
        elif self.roi_selector.name == ROISelector.MASK.name:
            simulator_metrics.comparative_metrics_dataset_mask(self.measures_selected_df)
        # -----------------------------
        results_simulation_metrics = simulator_metrics.get_simulation_results()
        print(
            f'{self.camera_option.__name__()}, {self.comparative_report_option.name},{self.roi_selector.name}, {self.size_estimation_selector.name}')
        results_simulation_metrics.print_metrics()
        simulator_metrics.export_csv_results(self.path_day_measures)

    def test_run_simulation_masks(self):
        """
        output_data/
        | --- \ reports_by_frame
        | --- \ images
        | --- \ reports_by_dataset
        | --- \ masks

        """
        # ------------------------
        # ELLIPSE FITTING
        self.mask_comparative_1()
        self.mask_comparative_2()
        self.mask_comparative_3()
        # self.mask_comparative_4()
        # self.mask_comparative_5()
        # # ------------------------
        # # CIRCLE ENCLOSING
        self.mask_comparative_6()
        self.mask_comparative_7()
        self.mask_comparative_8()
        # self.mask_comparative_9()
        # self.mask_comparative_10()
        # # ------------------------
        # # CIRCLE FITTING
        self.mask_comparative_11()
        self.mask_comparative_12()
        self.mask_comparative_13()
        # self.mask_comparative_14()
        # self.mask_comparative_15()

        # # ------------------------
        # # ROTATE RECTANGLE
        self.mask_comparative_16()
        self.mask_comparative_17()
        self.mask_comparative_18()
        # self.mask_comparative_19()
        # self.mask_comparative_20()
        # ------------------------
        # BOUNDING BOX
        self.bbox_comparative_1()
        self.bbox_comparative_2()
        self.bbox_comparative_3()
        # self.bbox_comparative_4()
        # self.bbox_comparative_5()
        # ------------------------
