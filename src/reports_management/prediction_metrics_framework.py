"""
Project: ak_simulator Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    Configuration of simulation user interface
    Read images, depth and IR from a dataset, extract labelled data and print metrics.

Use:

"""
import cv2
import scipy.io as sio
import pandas as pd
# ------------------
from dataset_management.pascal_voc_parser import PascalVocParser
# ------------------
from data_features_processor.features_extraction import DataFeatureProcessor
# ------------------
from reports_management.comparative_measures_reports_selector import ComparativeMeasuresReportSelector
from reports_management.comparative_measures_reports import ComparativeMeasuresReport
from size_estimation_s.image_processing import ImageProcessing
from reports_management.prediction_metrics_framework_config import PredictionsMetricsFrameworkConfig

# ------------------

"""
TITLE: CASE1, 
INPUT:
    DATASET LABELLED
    CAMERA PARAMETERS
    LAB MEASURES .csv
    SELECTOR TO CALCULATE SIZE
    SELECTOR TO ESTIMATE MASS
    SELECTOR FOR METRICS TO APPLY
    OUTPUT PATH FILENAME TO SAVE RESULTS


OUTPUT:
    ON SCREEN REPORT OF METRICS
    IF FILE IS SELECTED, SAVE .CSV DATASHEET.
    plot of data estimated    
"""

"""
TITLE: CASE2, 
INPUT:
    DATASET LABELLED
    CAMERA PARAMETERS
    LAB MEASURES .csv
    SELECTOR TO CALCULATE SIZE
    SELECTOR TO ESTIMATE MASS
    SELECTOR FOR METRICS TO APPLY
    OUTPUT PATH FILENAME TO SAVE RESULTS
OUTPUT:
    ON SCREEN REPORT OF METRICS
    IF FILE IS SELECTED, SAVE .CSV DATASHEET.
"""


class PredictionMetricsFramework:
    conf = None
    a_report = None

    def __init__(self, pred_metrics_conf: PredictionsMetricsFrameworkConfig):
        self.conf = pred_metrics_conf

    def comparative_metrics_dataset_bbox(self, measures_df):
        """
        This method loop over frames of a dataset, get each file and its correspondence with depth and IR data.
        At this time, IR data is not used.
        Depth data and IR data are coded in .mat format. This format can be openened from MATLAB.

        :param measures_df:
        :return:
        """
        result_pair_list = self.conf.dataset_manager.get_labeled_list_files()
        day_comparative_df = pd.DataFrame([], columns=self.conf.header_day_comparative)

        for a_register in result_pair_list:
            # this follows the folder structure explained in ./dataset_management/dataset_manager.py
            date_record = a_register[0]
            times_record = a_register[1]
            rgb_file_path = a_register[2]
            depth_mat_file_path = a_register[3]
            # Enable this if you need IR data, but we are not using it in this research
            # ir_mat_file_path = a_register[4]
            pv_file_path = a_register[5]  # .XML file PASCAL VOC format

            # select from list image paths previously selected
            # open image and related data
            rgb_frame = cv2.imread(rgb_file_path)  # load data from .png file to memory
            depth_mat_data = sio.loadmat(depth_mat_file_path)  # load from .mat file to memory
            depth_frame = depth_mat_data['transformed_depth']  # get data from inner section of .mat file
            # Enable this if you need IR data, but in this research we are not using it
            # ir_mat_data = sio.loadmat(ir_mat_file_path)  # load data from IR to memory
            # ir_frame = ir_mat_data['transformed_ir']  # get data from inner section of .mat file
            # ----------------------------------------------------
            # detections simulated from RGB color images, reading PASCAL VOC files to get bounding boxes and labels
            pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(pv_file_path)  # load data to memory
            # ----------------------------------------------------
            # conf_features = self.conf.data_features_options
            data_feature_processor = DataFeatureProcessor(self.conf.data_features_options, rgb_frame, depth_frame)
            results_by_frame_df = data_feature_processor.roi_selector_loop_bbox(pv_labelled_list, pv_label_list)

            # add results by frame to a list
            temporal_record = results_by_frame_df
            temporal_record['fruit_id'] = results_by_frame_df['fruit_id'].astype(str)
            temporal_record['date_capture'] = date_record
            temporal_record['time_capture'] = times_record
            # ---------------
            # merge data from manual labelled and selected
            temporal_record_merged = pd.merge(measures_df, temporal_record, left_on='fruit_id', right_on='fruit_id', how='inner')
            # ---------------------------
            # create a summative record with calculated data for each frame (each picture/image)
            #day_comparative_df = day_comparative_df.append(temporal_record_merged, ignore_index=True)
            day_comparative_df = pd.concat([day_comparative_df, temporal_record_merged], ignore_index=True)
            # -----------------
        day_comparative_df.drop(columns=day_comparative_df.columns[0], axis=1, inplace=True)
        # day_comparative_df is used by metrics by frame, there is an intermediate result called results_by_frame
        self.a_report = ComparativeMeasuresReport(day_comparative_df, self.conf.comparative_report_option)
        # writes results to a global parameter

    def comparative_metrics_dataset_mask(self, measures_df):
        """
        This method loop over frames of a dataset, get each file and its correspondence with depth and IR data.
        At this time, IR data is not used.
        Depth data and Ir data are code in .mat format.
        This uses a .png file to get a mask. The file was made using MATLAB Image Segmenter

        :param measures_df:
        :return:
        """
        result_pair_list = self.conf.dataset_manager.get_labeled_mask_list_files()
        day_comparative_df = pd.DataFrame([], columns=self.conf.header_day_comparative)
        # cycle per frame
        for a_register in result_pair_list:
            date_record = a_register[0]
            times_record = a_register[1]
            rgb_file_path = a_register[2]
            depth_mat_file_path = a_register[3]
            # Enable this if you need IR data, but we are not using it in this research
            # an_ir_mat_file_path = a_register[4]
            pv_file_path = a_register[5]
            mask_file_path = a_register[6]
            # select from list image paths previously selected
            # open image and related data # TODO: 01/04/2022 replace hardcoded string .png
            rgb_frame = cv2.imread(rgb_file_path + '.png')  # load data to memory
            depth_mat_frame = sio.loadmat(depth_mat_file_path)  # load depth data into memory
            depth_frame = depth_mat_frame['transformed_depth']
            # Enable this if you need IR data, but we are not using it in this research
            # ir_mat_data = sio.loadmat(an_ir_mat_file_path)
            # ir_frame = an_ir_mat_data['transformed_ir']  # get data from inner section of .mat file
            mask_frame = cv2.imread(mask_file_path, cv2.IMREAD_GRAYSCALE)  # load into memory the binary mask
            # detections simulated from RGB color images, reading PASCAL VOC files, with bounding boxes and labels
            # ----------------------------------------------------
            pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(pv_file_path)  # load data to memory
            # ----------------------------------------------------
            # IMAGE PROCESSING INSTRUCTIONS HERE
            imp = ImageProcessing()
            ip_1 = imp.im_method_1(mask_frame)
            # ----------------------------------------------------
            # get measures by frame using PASCAL-VOC coordinates rgb frames, depth data and binary masks
            data_feature_processor = DataFeatureProcessor(self.conf.data_features_options, rgb_frame, depth_frame)
            results_by_frame_df = data_feature_processor.roi_selector_loop_mask(pv_labelled_list, pv_label_list, ip_1)
            # TODO: 09/03/2022 add here data images
            # TODO: use the selected option to draw objects
            # add results by frame to a list
            temporal_record = results_by_frame_df
            temporal_record['fruit_id'] = results_by_frame_df['fruit_id'].astype(str)
            temporal_record['date_capture'] = date_record
            temporal_record['time_capture'] = times_record
            # ---------------
            # merge data from manual labelled and selected
            temporal_record_merged = pd.merge(measures_df, temporal_record, left_on='fruit_id', right_on='fruit_id', how='inner')
            # ---------------------------
            #day_comparative_df = day_comparative_df.append(temporal_record_merged, ignore_index=True)
            day_comparative_df = pd.concat([day_comparative_df, temporal_record_merged], ignore_index=True)
            # ---------------------------
        # -----------------
        day_comparative_df.drop(columns=day_comparative_df.columns[0], axis=1, inplace=True)
        # day_comparative_df is used by metrics by frame, there is an intermediate result called results_by_frame
        self.a_report = ComparativeMeasuresReport(day_comparative_df, self.conf.comparative_report_option)
        # writes results to a global parameter

    def print_results(self):
        print(type(self).__name__)
        print('PRINT RESULTS based on configurations -->')
        if self.conf.comparative_report_option == ComparativeMeasuresReportSelector.DEPTH:
            print('DEPTH -->')
            self.a_report.print_depth_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.A1:
            print('D1 -->')
            self.a_report.print_axis_01_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.A2:
            print('D2 -->')
            self.a_report.print_axis_02_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.WEIGHT:
            print('WEIGHT -->')
            self.a_report.print_weight_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.ALL:
            print('ALL -->')
            self.a_report.print_metrics()
        else:
            print('DEFAULT -->')
            self.a_report.print_weight_metrics()

    def export_csv_results(self, export_path_simulations):
        print(type(self).__name__)
        print('SAVING WITH SELECTED NAME BY USER')
        print(f'Saving data in file {export_path_simulations} -->')
        self.a_report.export_data_csv(self.conf.path_day_measures)

    def get_simulation_results(self):
        results_metrics = None

        if self.conf.comparative_report_option == ComparativeMeasuresReportSelector.DEPTH:
            print('DEPTH -->')
            results_metrics = self.a_report.get_depth_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.A1:
            print('A1 -->')
            results_metrics = self.a_report.get_axis_01_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.A2:
            print('A2 -->')
            results_metrics = self.a_report.get_axis_02_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.WEIGHT:
            print('WEIGH -->')
            results_metrics = self.a_report.get_weight_metrics()
        elif self.conf.comparative_report_option == ComparativeMeasuresReportSelector.ALL:
            print('ALL -->')
            self.a_report.print_metrics()
        else:
            print('DEFAULT -->')
            results_metrics = self.a_report.get_weight_metrics()

        return results_metrics
