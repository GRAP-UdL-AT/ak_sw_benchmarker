"""
Project: ak_simulator Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    File to extract results in a datasheet
    It is a test suite of several parameters config
    Works with all possible combinations of methods and measures calibration spheres
    All combinations of test must be updated here

Use:
        integrations_tests = IntegrationDatasheetMetrics(datetime_experiment, camera_option, comparative_report_option, dataset_manager_config, self.path_manual_measures_entry.get(), path_output_simulation)
        integrations_tests.test_run_simulation()
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
from weight_prediction_s.weight_prediction_methods import WeightPredictionModelSelector
from reports_management.prediction_metrics_framework import PredictionsMetricsFrameworkConfig
from reports_management.prediction_metrics_framework import PredictionMetricsFramework


class IntegrationDatasheetMetrics:
    def __init__(self, datetime_experiment_str, camera_option, comparative_report_option,
                 dataset_manager_config: DatasetConfig, path_manual_measures_entry, path_output_simulation):

        self.path_output_simulation = os.path.join(path_output_simulation)
        self.path_output_plots = os.path.join(self.path_output_simulation, 'plots')

        self.datetime_experiment = datetime_experiment_str
        self.day_measures_filename = self.datetime_experiment + 'comparative_by_day_all.csv'
        self.path_output_csv = os.path.join(self.path_output_simulation, 'output_csv')
        self.path_day_measures = os.path.join(self.path_output_csv, self.day_measures_filename)
        self.comparative_report_option = comparative_report_option
        # --------------
        # create optimization datasheet
        self.headers_optimization = ['camera_option', 'pixel_option', 'size_estimation_option', 'depth_option',
                                     'mass_estimation_option',
                                     'comparative_report_option', 'total_objects', 'unit_of_measurement', 'MSE', 'MAE',
                                     'RMSE', 'MAPE', 'R2']
        self.optimization_filename = self.datetime_experiment + self.comparative_report_option.name + '_' + 'ranking_ALL.csv'
        self.path_optimization = os.path.join(self.path_output_csv, self.optimization_filename)
        self.optimization_results_df = pd.DataFrame([], columns=self.headers_optimization)
        # --------------------------------------
        # LABORATORY MEASURES
        # --------------------------------------
        path_manual_measures_df = os.path.join(path_manual_measures_entry)
        manual_measures_df = pd.read_csv(path_manual_measures_df, dtype=str, sep=';')
        manual_measures_df['fruit_id'] = manual_measures_df['fruit_id'].astype(str)
        manual_measures_df['lab.axis_01_mm'] = manual_measures_df['lab.axis_01_mm'].astype(float)
        manual_measures_df['lab.axis_02_mm'] = manual_measures_df['lab.axis_02_mm'].astype(float)
        manual_measures_df['lab.weight_gr'] = manual_measures_df['lab.weight_gr'].astype(float)
        self.measures_selected_df = manual_measures_df
        # --------------------------------------
        # global parameters
        self.dataset_manager_config = dataset_manager_config
        self.camera_option = camera_option

        self.comparative_report_option = comparative_report_option
        self.roi_selector = None
        self.size_estimation_selector = None
        self.depth_option = None
        self.weight_prediction_option = WeightPredictionModelSelector.NONE # None  # MassEstimationModelSelector.D1D2_LM_MET_01
        # --------------------------------------
        self.data_features_options = None
        self.simulator_config = None

        pass

    def run_optimization_metrics(self):
        print('run_optimization_metrics -->')
        self.data_features_options = DataFeatureConfig(camera_conf=self.camera_option.rgb_sensor,
                                                       roi_selector=self.roi_selector,
                                                       size_estimation_selector=self.size_estimation_selector,
                                                       depth_selector=self.depth_option,
                                                       weight_selector=self.weight_prediction_option)
        # ----------------------
        self.simulator_config = PredictionsMetricsFrameworkConfig(self.dataset_manager_config,
                                                                  self.path_day_measures,
                                                                  self.data_features_options,
                                                                  self.weight_prediction_option,
                                                                  self.comparative_report_option)

        # -----------------------------
        simulation = PredictionMetricsFramework(self.simulator_config)
        # -----------------------------
        if self.roi_selector.name == ROISelector.BBOX.name:
            simulation.comparative_metrics_dataset_bbox(self.measures_selected_df)
        elif self.roi_selector.name == ROISelector.MASK.name:
            simulation.comparative_metrics_dataset_mask(self.measures_selected_df)

        # ----------------------
        # TODO: 28/07/2022 REVIEW THIS IS REPEATED
        # r = simulation.get_simulation_results()
        # ----------------------

        r = simulation.get_simulation_results()
        # ----------------------
        temporal_record = pd.DataFrame(
            [[self.camera_option.__name__(),
              self.roi_selector.name,
              self.size_estimation_selector.name,
              self.depth_option.name,
              self.weight_prediction_option.name,
              self.comparative_report_option.name,
              r.total_objects,
              r.unit_of_measurement,
              r.MSE,
              r.MAE,
              r.RMSE,
              r.MAPE,
              r.R2]],
            columns=self.headers_optimization)
        # ----------------------
        # self.optimization_results_df = self.optimization_results_df.append(temporal_record, ignore_index=True)
        self.optimization_results_df = pd.concat([self.optimization_results_df, temporal_record], ignore_index=True)
        pass

    # all combinations of test must be updated here

    def mask_simulation_method_1(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.AVG
        #self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_2(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.MOD
        #self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_3(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.MIN
        #self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_4(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.MAX
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_5(self):
        # TODO: 02/04/2022 disable CENTROID calculations for MASK
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.EF
        self.depth_option = DepthSelector.CENTROID
        #self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_6(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.AVG
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_7(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.MOD
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_8(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.MIN
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_9(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.MAX
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_10(self):
        # TODO: 02/04/2022 disable CENTROID calculations for MASK
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CE
        self.depth_option = DepthSelector.CENTROID
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    # --------------------------------------
    def mask_simulation_method_11(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.AVG
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_12(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.MOD
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_13(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.MIN
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_14(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.MAX
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_15(self):
        # TODO: 02/04/2022 disable CENTROID calculations for MASK
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.CF
        self.depth_option = DepthSelector.CENTROID
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    # --------------------------------------
    def mask_simulation_method_16(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.AVG
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_17(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.MOD
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_18(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.MIN
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_19(self):
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.MAX
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def mask_simulation_method_20(self):
        # TODO: 02/04/2022 disable CENTROID calculations for MASK
        self.roi_selector = ROISelector.MASK
        self.size_estimation_selector = SizeEstimationSelectorPx.RR
        self.depth_option = DepthSelector.CENTROID
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def bbox_simulation_method_1(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.AVG
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def bbox_simulation_method_2(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.MOD
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def bbox_simulation_method_3(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.MIN
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def bbox_simulation_method_4(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.MAX
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

    def bbox_simulation_method_5(self):
        self.roi_selector = ROISelector.BBOX
        self.size_estimation_selector = SizeEstimationSelectorPx.BB
        self.depth_option = DepthSelector.CENTROID
        # self.mass_estimation_option = MassEstimationModelSelector.NONE
        self.run_optimization_metrics()

#    def test_run_simulation(self):
#        print(f'test_run_simulation(self): -->{self.comparative_report_option}')
#        if self.comparative_report_option == ComparativeMeasuresReportSelector.MASS:
#            print('MASS')
#            self.test_run_simulation_mass()
#        else:
#            self.test_run_simulation_diameters()
#        pass


    def test_run_simulation_diameters(self):
        """
            This contains all methods
            :return:
        """
        # self.comparative_report_option = ComparativeMeasuresReportSelector.CALIBER
        # ------------------------
        # ELLIPSE FITTING
        self.mask_simulation_method_1()
        self.mask_simulation_method_2()
        self.mask_simulation_method_3()
        # self.mask_simulation_method_4()
        # self.mask_simulation_method_5()
        # # ------------------------
        # # CIRCLE ENCLOSING
        self.mask_simulation_method_6()
        self.mask_simulation_method_7()
        self.mask_simulation_method_8()
        # self.mask_simulation_method_9()
        # self.mask_simulation_method_10()
        # # ------------------------
        # # CIRCLE FITTING
        self.mask_simulation_method_11()
        self.mask_simulation_method_12()
        self.mask_simulation_method_13()
        # self.mask_simulation_method_14()
        # self.mask_simulation_method_15()
        # # ------------------------
        # # ROTATE RECTANGLE
        self.mask_simulation_method_16()
        self.mask_simulation_method_17()
        self.mask_simulation_method_18()
        # self.mask_simulation_method_19()
        # self.mask_simulation_method_20()
        # # ------------------------
        # # BOUNDING BOX
        self.bbox_simulation_method_1()
        self.bbox_simulation_method_2()
        self.bbox_simulation_method_3()
        # self.bbox_simulation_method_4()
        # self.bbox_simulation_method_5()
        # ------------------------
        # save final result
        self.optimization_results_df.to_csv(self.path_optimization, float_format='%.3f', sep=';')  # 03/10/2022 modified decimals from .2f to .3f
        print(self.path_optimization)
        # ------------------------
        pass

    def test_run_simulation_weight(self):
        """
            This contains all methods AND RUN SIMULATION FOR WEIGHT
            :return:
        """
        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_01
        self.test_run_simulation_diameters()

        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_02
        self.test_run_simulation_diameters()

        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
        self.test_run_simulation_diameters()

        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_04
        self.test_run_simulation_diameters()

        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_05
        self.test_run_simulation_diameters()

        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_NLM_MET_01
        self.test_run_simulation_diameters()

        self.weight_prediction_option = WeightPredictionModelSelector.D1D2_NLM_MET_02
        self.test_run_simulation_diameters()

        pass
