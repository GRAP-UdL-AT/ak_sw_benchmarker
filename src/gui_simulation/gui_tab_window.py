"""
Project: ak_simulator Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: November 2021
Description:
    Simulation user interface. This GUI contains parameters to run experiments
Use:
"""
import os
import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from tkinter import Frame, LabelFrame, Label, Menu, Entry, Button, Spinbox, Text
from tkinter import ttk

from gui_simulation.about_simulation_window import AboutSimulationWindow
from gui_simulation.help_simulation_window import HelpSimulationWindow

from dataset_management.dataset_config import DatasetConfig
from dataset_management.dataset_manager import DatasetManager

from size_estimation_s.roi_selector import ROISelector
from depth_estimation_s.depth_estimation_methods_selector import DepthSelector
from size_estimation_s.size_estimation_methods_selector import SizeEstimationSelectorPx

from camera_management_s.camera_parameters_selector import CameraModelSelector
from camera_management_s.camera_parameters import AzureKinect, KinectV2

from data_features_processor.data_features_config import DataFeatureConfig

from weight_prediction_s.weight_prediction_methods_selector import WeightPredictionModelSelector
from reports_management.comparative_measures_reports_selector import ComparativeMeasuresReportSelector

from reports_management.prediction_metrics_framework import PredictionsMetricsFrameworkConfig
from reports_management.prediction_metrics_framework import PredictionMetricsFramework
from screen_layout_s.draw_screen_helpers import DrawScreenManager

from gui_simulation.gui_simulation_config import GUISimulationConfig

from reports_management.integration_datasheet_metrics import IntegrationDatasheetMetrics
from reports_management.integration_detail_metrics import IntegrationDetailMetrics


class GUIAKTabWindow(tk.Tk):
    app_config = None
    dataset_config = None
    frames_extractor_config = None

    # Add here options to display on screen to the user
    camera_list = (
        CameraModelSelector.AK.name,
        CameraModelSelector.KINECT_V2.name
    )

    roi_list = (
        ROISelector.BBOX.name,
        ROISelector.MASK.name
    )
    size_estimation_list_bbox = (
        SizeEstimationSelectorPx.BB.name
    )

    size_estimation_list_mask = (
        SizeEstimationSelectorPx.EF.name,
        SizeEstimationSelectorPx.CE.name,
        SizeEstimationSelectorPx.CF.name,
        SizeEstimationSelectorPx.RR.name
    )

    depth_list = (
        DepthSelector.AVG.name,
        DepthSelector.MOD.name,
        DepthSelector.MIN.name
    )

    weight_prediction_list = (
        # ------------------
        # based on caliber and height
        WeightPredictionModelSelector.CH_LM_MET_01.name,
        WeightPredictionModelSelector.CH_LM_MET_02.name,
        WeightPredictionModelSelector.CH_LM_MET_03.name,
        WeightPredictionModelSelector.CH_LM_MET_04.name,
        WeightPredictionModelSelector.CH_LM_MET_05.name,
        # nonlinear models
        WeightPredictionModelSelector.CH_NLM_MET_01.name,
        WeightPredictionModelSelector.CH_NLM_MET_02.name,
        # ------------------
        # based on major diameter and minor diameter
        WeightPredictionModelSelector.D1D2_LM_MET_01.name,
        WeightPredictionModelSelector.D1D2_LM_MET_02.name,
        WeightPredictionModelSelector.D1D2_LM_MET_03.name,
        WeightPredictionModelSelector.D1D2_LM_MET_04.name,
        WeightPredictionModelSelector.D1D2_LM_MET_05.name,
        # nonlinear models
        WeightPredictionModelSelector.D1D2_NLM_MET_01.name,
        WeightPredictionModelSelector.D1D2_NLM_MET_02.name,
        # ------------------
        WeightPredictionModelSelector.MODEL_BY_DEFAULT.name,
        WeightPredictionModelSelector.NONE.name,
    )

    report_list = (
        ComparativeMeasuresReportSelector.A1.name,
        ComparativeMeasuresReportSelector.A2.name,
        ComparativeMeasuresReportSelector.WEIGHT.name
    )

    # --------------------------------------------
    TAB_TITLE_1 = 'Dataset metrics'
    TAB_TITLE_2 = 'Metric comparisons'
    # TAB_TITLE_3 = 'Tab 03'

    def __init__(self, r_config: GUISimulationConfig, master=None):
        super().__init__(master)
        # ---------------------------
        # configuration parameters
        self.app_config = r_config  # assign config
        # ---------------------------
        self.title(r_config.app_title)
        # ---------------------------
        # ---------------------------
        assets_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(assets_path, 'assets', 'icon_app.png')
        self.iconphoto(False, tk.PhotoImage(file=img_path))
        # ---------------------------
        # --------------------------------------------
        # option vars
        self.scanning_mode_radio_var = tk.StringVar()
        # ---------------------------
        self.create_menu_bars()
        # ---------------------------
        self.create_tabs()  # creates tabs
        self.create_widgets_tab_1()  # define tabs elements
        self.create_widgets_tab_2()
        # ---------------------------
        self.create_status_bar()
        # self.create_message_info()
        # ---------------------------
        # configurations
        self.input_file_path = None
        self.offset_in_seconds = None
        self.number_of_frames = None
        self.video_analyser_config_obj = None
        # ---------------------------

    def create_tabs(self):
        """
        Creates tabs here, calling
        :return:
        """
        self.tab_group = ttk.Notebook(self.master)
        # add tab forms HERE
        self.tab_1 = Frame(self.tab_group)
        self.tab_2 = Frame(self.tab_group)
        # self.tab_3 = tk.Frame(self.tab_group)
        # load tab forms
        self.tab_group.add(self.tab_1, text=self.TAB_TITLE_1)
        self.tab_group.add(self.tab_2, text=self.TAB_TITLE_2)
        # self.tab_group.add(self.tab_3, text=self.TAB_TITLE_3)
        self.tab_group.pack(expand=1, fill="both")
        pass

    def create_widgets_tab_1(self):
        """
        Define tabs elements here
        :return:
        """
        # Create some room around all the internal frames
        self['padx'] = 5
        self['pady'] = 5

        self.t1_dataset_groundtruth_frame = ttk.LabelFrame(self.tab_1, text="Labelled dataset & groundtruth data",
                                                           relief=tk.RIDGE)
        self.t1_dataset_groundtruth_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.t1_size_weight_frame = ttk.LabelFrame(self.tab_1, text="Size estimation and weight prediction",
                                                   relief=tk.RIDGE)
        self.t1_size_weight_frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.t1_labelled_data_frame = ttk.LabelFrame(self.tab_1, text=" ", relief=tk.RIDGE)
        self.t1_labelled_data_frame.grid(row=2, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.t1_message_frame = ttk.LabelFrame(self.tab_1, text="User info", relief=tk.RIDGE)
        self.t1_message_frame.grid(row=3, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.control_bar_frame = ttk.LabelFrame(self.tab_1, text="Control bar", relief=tk.RIDGE)
        self.control_bar_frame.grid(row=4, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        ############### CREATE HIERARCHY ######################
        # insert default values
        # extract from a folder
        self.t1_dataset_path_label = tk.Label(self.t1_dataset_groundtruth_frame, text='Folder path:')
        self.t1_dataset_path_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.t1_dataset_root_folder_path_entry = tk.Entry(self.t1_dataset_groundtruth_frame, state="readonly")
        self.t1_dataset_root_folder_path_entry.grid(row=0, column=1, sticky=tk.W + tk.N)

        self.t1_select_folder_button = tk.Button(self.t1_dataset_groundtruth_frame, text='Browse',
                                                 command=self.t1_select_folder_data)
        self.t1_select_folder_button.grid(row=0, column=2, sticky=tk.W + tk.N)
        ########################################################
        # extract from one file
        self.t1_an_input_file_label = tk.Label(self.t1_dataset_groundtruth_frame, text='File selected:')
        self.t1_an_input_file_label.grid(row=1, column=0, sticky=tk.W, pady=3)
        # # -----------------------
        self.t1_path_manual_measures_entry = tk.Entry(self.t1_dataset_groundtruth_frame, state="readonly")
        self.t1_path_manual_measures_entry.grid(row=1, column=1, sticky=tk.W + tk.N)
        # -----------------------
        # insert default values
        self.t1_select_file_button = tk.Button(self.t1_dataset_groundtruth_frame, text='Browse',
                                               command=self.t1_select_file_data)
        self.t1_select_file_button.grid(row=1, column=2, sticky=tk.W + tk.N)

        # --------------
        self.t1_camera_label = tk.Label(self.t1_size_weight_frame, text='Camera:')
        self.t1_camera_label.grid(row=0, column=0, sticky=tk.W, pady=3)
        self.t1_camera_box = ttk.Combobox(self.t1_size_weight_frame, state="readonly")
        self.t1_camera_box['values'] = self.camera_list
        self.t1_camera_box.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.t1_camera_box.current(0)
        # --------------
        self.t1_roi_selector_label = tk.Label(self.t1_size_weight_frame, text='ROI selector:')
        self.t1_roi_selector_label.grid(row=1, column=0, sticky=tk.W, pady=3)
        self.t1_roi_selector_box = ttk.Combobox(self.t1_size_weight_frame, state="readonly")
        self.t1_roi_selector_box['values'] = self.roi_list
        self.t1_roi_selector_box.grid(row=1, column=1, sticky=tk.W + tk.N)
        self.t1_roi_selector_box.current(0)
        self.t1_roi_selector_box.bind("<<ComboboxSelected>>", self.t1_roi_selector_changed)  # add event callback here
        # --------------
        self.t1_size_estimation_selector_label = tk.Label(self.t1_size_weight_frame, text='Size estimation selector:')
        self.t1_size_estimation_selector_label.grid(row=2, column=0, sticky=tk.W, pady=3)
        self.t1_size_estimation_selector_box = ttk.Combobox(self.t1_size_weight_frame, state="readonly")
        self.t1_size_estimation_selector_box['values'] = self.size_estimation_list_bbox  # default bbox methods
        self.t1_size_estimation_selector_box.grid(row=2, column=1, sticky=tk.W + tk.N)
        self.t1_size_estimation_selector_box.current(0)
        # --------------
        self.t1_depth_selector_label = tk.Label(self.t1_size_weight_frame, text='Depth selector:')
        self.t1_depth_selector_label.grid(row=3, column=0, sticky=tk.W, pady=3)

        self.t1_depth_selector_box = ttk.Combobox(self.t1_size_weight_frame, state="readonly")
        self.t1_depth_selector_box['values'] = self.depth_list
        self.t1_depth_selector_box.grid(row=3, column=1, sticky=tk.W + tk.N)
        self.t1_depth_selector_box.current(0)
        # ---------------
        self.t1_comparative_report_label = tk.Label(self.t1_size_weight_frame, text='Report selector:')
        self.t1_comparative_report_label.grid(row=4, column=0, sticky=tk.W, pady=3)

        self.t1_comparative_report_selector_box = ttk.Combobox(self.t1_size_weight_frame, state="readonly")
        self.t1_comparative_report_selector_box['values'] = self.report_list
        self.t1_comparative_report_selector_box.grid(row=4, column=1, sticky=tk.W + tk.N)
        self.t1_comparative_report_selector_box.current(0)  # SELECTED BY DEFAULT caliber/diameter_01
        self.t1_comparative_report_selector_box.bind("<<ComboboxSelected>>",
                                                     self.t1_comparative_report_selector_changed)  # add event callback here
        # --------------
        self.t1_weight_prediction_selector_label = tk.Label(self.t1_size_weight_frame, text='Weight prediction method:')
        self.t1_weight_prediction_selector_label.grid(row=5, column=0, sticky=tk.W, pady=3)
        self.t1_weight_prediction_selector_box = ttk.Combobox(self.t1_size_weight_frame,
                                                              state="disabled")  # readonly active
        self.t1_weight_prediction_selector_box['values'] = self.weight_prediction_list
        self.t1_weight_prediction_selector_box.grid(row=5, column=1, sticky=tk.W + tk.N)
        self.t1_weight_prediction_selector_box.current(0)
        # --------------
        self.t1_simulation_button = tk.Button(self.t1_labelled_data_frame, text='Analyse dataset',
                                              command=self.t1_run_simulation_experiment)
        self.t1_simulation_button.grid(row=0, column=0, sticky=tk.W + tk.N)

        self.t1_img_button = tk.Button(self.t1_labelled_data_frame, text='Export images', command=self.t1_run_img_experiment)
        self.t1_img_button.grid(row=0, column=1, sticky=tk.W + tk.N)

        #  button check to print labels on images
        self.print_labels_check_var = tk.IntVar()
        self.print_labels_check_var.set(1)
        self.t1_labels_check = tk.Checkbutton(self.t1_labelled_data_frame, text='Print labels',
                                              variable=self.print_labels_check_var)
        self.t1_labels_check.grid(row=0, column=2, sticky=tk.W + tk.N)

        self.t1_quitButton = tk.Button(self.control_bar_frame, text='Quit', command=self.quit_app)
        self.t1_quitButton.grid(row=0, column=0, sticky=tk.W + tk.E)

        ################
        self.t1_messages_label = tk.Label(self.t1_message_frame, text='Messages:')
        self.t1_messages_label.grid(row=0, column=0, sticky=tk.W + tk.N)
        self.t1_messages_info = tk.Text(self.t1_message_frame, width=40, height=5)
        self.t1_messages_info.grid(row=1, column=0, sticky=tk.W + tk.N)

        self.t1_results_label = tk.Label(self.t1_message_frame, text='Results:')
        self.t1_results_label.grid(row=2, column=0, sticky=tk.W + tk.N)

        self.t1_results_info = tk.Text(self.t1_message_frame, width=40, height=5)
        self.t1_results_info.grid(row=3, column=0, sticky=tk.W + tk.N)
        ################
        # -------------------------------------------------------
        pass
        # -------------------------------------------------------

    def create_widgets_tab_2(self):
        """
        Define tabs elements here
        :return:
        """
        # self.tab_2_label = Label(self.tab_2, text='Label example in TAB_2:')
        # self.tab_2_label.grid(row=1, column=1, sticky=tk.W, ipadx=3, ipady=3)

        # Create some room around all the internal frames
        self['padx'] = 5
        self['pady'] = 5

        self.t2_dataset_groundtruth_frame = ttk.LabelFrame(self.tab_2, text="Labelled dataset & groundtruth data",
                                                           relief=tk.RIDGE)
        self.t2_dataset_groundtruth_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.t2_size_weight_frame = ttk.LabelFrame(self.tab_2, text="Size estimation and weight prediction",
                                                   relief=tk.RIDGE)
        self.t2_size_weight_frame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.t2_labelled_data_frame = ttk.LabelFrame(self.tab_2, text=" ", relief=tk.RIDGE)
        self.t2_labelled_data_frame.grid(row=2, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.t2_message_frame = ttk.LabelFrame(self.tab_2, text="User info", relief=tk.RIDGE)
        self.t2_message_frame.grid(row=3, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        ############### CREATE HIERARCHY ######################
        # insert default values
        # extract from a folder
        self.t2_dataset_path_label = tk.Label(self.t2_dataset_groundtruth_frame, text='Folder path:')
        self.t2_dataset_path_label.grid(row=0, column=0, sticky=tk.W, pady=3)

        self.t2_dataset_root_folder_path_entry = tk.Entry(self.t2_dataset_groundtruth_frame, state="readonly")
        self.t2_dataset_root_folder_path_entry.grid(row=0, column=1, sticky=tk.W + tk.N)

        self.t2_select_folder_button = tk.Button(self.t2_dataset_groundtruth_frame, text='Browse',
                                                 command=self.t2_select_folder_data)
        self.t2_select_folder_button.grid(row=0, column=2, sticky=tk.W + tk.N)
        ########################################################
        # extract from one file
        self.t2_an_input_file_label = tk.Label(self.t2_dataset_groundtruth_frame, text='File selected:')
        self.t2_an_input_file_label.grid(row=1, column=0, sticky=tk.W, pady=3)
        # # -----------------------
        self.t2_path_manual_measures_entry = tk.Entry(self.t2_dataset_groundtruth_frame, state="readonly")
        self.t2_path_manual_measures_entry.grid(row=1, column=1, sticky=tk.W + tk.N)

        self.t2_select_file_button = tk.Button(self.t2_dataset_groundtruth_frame, text='Browse',
                                               command=self.t2_select_file_data)
        self.t2_select_file_button.grid(row=1, column=2, sticky=tk.W + tk.N)
        # --------------
        self.t2_camera_label = tk.Label(self.t2_size_weight_frame, text='Camera:')
        self.t2_camera_label.grid(row=0, column=0, sticky=tk.W, pady=3)
        self.t2_camera_box = ttk.Combobox(self.t2_size_weight_frame, state="readonly")
        self.t2_camera_box['values'] = self.camera_list
        self.t2_camera_box.grid(row=0, column=1, sticky=tk.W + tk.N)
        self.t2_camera_box.current(0)
        # --------------
        # --------------
        self.t2_comparative_report_label = tk.Label(self.t2_size_weight_frame, text='Report selector:')
        self.t2_comparative_report_label.grid(row=5, column=0, sticky=tk.W, pady=3)
        self.t2_comparative_report_selector_box = ttk.Combobox(self.t2_size_weight_frame, state="readonly")
        self.t2_comparative_report_selector_box['values'] = self.report_list
        self.t2_comparative_report_selector_box.grid(row=5, column=1, sticky=tk.W + tk.N)
        self.t2_comparative_report_selector_box.current(2)
        # -----------------------
        self.t2_simulation_button = tk.Button(self.t2_labelled_data_frame, text='Run tests in dataset',
                                              command=self.t2_run_simulation_experiment)
        self.t2_simulation_button.grid(row=0, column=0, sticky=tk.W + tk.N)

        self.t2_quitButton = tk.Button(self.t2_labelled_data_frame, text='Quit', command=self.quit_app)
        self.t2_quitButton.grid(row=0, column=1, sticky=tk.W + tk.N)

        ################
        self.t2_messages_label = tk.Label(self.t2_message_frame, text='Messages:')
        self.t2_messages_label.grid(row=0, column=0, sticky=tk.W + tk.N)

        self.t2_messages_info = tk.Text(self.t2_message_frame, width=40, height=5)
        self.t2_messages_info.grid(row=1, column=0, sticky=tk.W + tk.N)

        self.t2_results_label = tk.Label(self.t2_message_frame, text='Results:')
        self.t2_results_label.grid(row=2, column=0, sticky=tk.W + tk.N)

        self.t2_results_info = tk.Text(self.t2_message_frame, width=40, height=5)
        self.t2_results_info.grid(row=3, column=0, sticky=tk.W + tk.N)
        ################

    def create_widgets_tab_3(self):
        """
        Define tabs elements here
        :return:
        """
        self.tab_3_label = Label(self.tab_3, text='Label example in TAB_3:', width=self.LABEL_WIDTH)
        self.tab_3_label.grid(row=1, column=1, sticky=tk.W, ipadx=3, ipady=3)
        pass

    def create_menu_bars(self):
        """
        Add menu to the UI
        :return:
        :return:
        """
        # Create some room around all the internal frames

        self.menubar = Menu(self)
        self.menu_file = Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(label="Quit", command=self.quit_app)

        self.menu_help = Menu(self.menubar, tearoff=False)
        self.menu_help.add_command(label="Help...", command=self.open_help_data)
        self.menu_help.add_command(label="About...", command=self.open_about_data)

        self.menubar.add_cascade(menu=self.menu_file, label='File', underline=0)
        self.menubar.add_cascade(menu=self.menu_help, label='About', underline=0)
        self.config(menu=self.menubar)  # add menu to window

    def open_about_data(self):
        about_windows = AboutSimulationWindow(self)
        about_windows.grab_set()

    def open_help_data(self):
        help_windows = HelpSimulationWindow(self)
        help_windows.grab_set()

    def not_implemented_yet(self):
        print("Not implemented yet!!!")

    def clean_text_widgets(self):
        self.t1_messages_info.delete("1.0", "end")
        self.t1_results_info.delete("1.0", "end")

    def create_status_bar(self):
        self.status_bar = Label(self, text=".", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def t1_select_folder_data(self):
        analyze_status_str = ""
        results_info_str = ""
        directory_selected = filedialog.askdirectory(initialdir=self.app_config.input_folder)

        if directory_selected == "":
            analyze_status_str = "A directory has not been selected " + "\n"
            print(analyze_status_str)
        else:
            self.t1_dataset_root_folder_path_entry['state'] = "normal"
            self.t1_dataset_root_folder_path_entry.delete(0, "end")
            self.t1_dataset_root_folder_path_entry.insert(0, os.path.join(directory_selected))
            self.t1_dataset_root_folder_path_entry['state'] = "readonly"
        # ----------------------------------------
        analyze_status_str = directory_selected + "\n"
        self.t1_messages_info.insert("1.0", analyze_status_str)
        # ----------------------------------------

    def t1_select_file_data(self):
        analyze_status_str = ""
        results_info_str = ""
        path_filename_selected = filedialog.askopenfilename(initialdir=self.app_config.file_browser_input_folder, title="Select a File", filetypes=(("Text files", self.app_config.file_extension_to_search), ("all files", "*.csv")))

        if path_filename_selected == "":
            analyze_status_str = "A file has not been selected " + "\n"
        else:
            #################################
            an_input_file = os.path.join(path_filename_selected)
            #################################
            self.t1_path_manual_measures_entry['state'] = "normal"
            self.t1_path_manual_measures_entry.delete(0, "end")
            self.t1_path_manual_measures_entry.insert(0, os.path.join(an_input_file))
            self.t1_path_manual_measures_entry['state'] = "readonly"
            #################################
        # ----------------------------------------
        analyze_status_str = path_filename_selected + "\n"
        self.t1_messages_info.insert("1.0", analyze_status_str)

    def t1_roi_selector_changed(self, event):
        """
        Used to restrict access to non-mask methods
        :param event:
        :return:
        """
        if self.t1_roi_selector_box.get() == ROISelector.BBOX.name:
            self.t1_size_estimation_selector_box['values'] = self.size_estimation_list_bbox
        elif self.t1_roi_selector_box.get() == ROISelector.MASK.name:
            self.t1_size_estimation_selector_box['values'] = self.size_estimation_list_mask
            # action here
        self.t1_size_estimation_selector_box.current(0)  # select default option

    def t1_comparative_report_selector_changed(self, event):
        """
        Used to restrict access to non-mask methods
        :param event:
        :return:
        """
        if self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.A1.name:  # d1 y d2
            self.t1_weight_prediction_selector_box['state'] = 'disabled'
        elif self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.A2.name:  # d1 y d2
            self.t1_weight_prediction_selector_box['state'] = 'disabled'
        elif self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.WEIGHT.name:  # d1 and  d2
            self.t1_weight_prediction_selector_box['state'] = 'readonly'
            self.t1_weight_prediction_selector_box.current(0)  # select default option

    def t1_run_img_experiment(self):
        """
        It is used to draw on images the application of ROI selectors.
        Results are visualized in folder /output/output_img/
        :return:
        """
        if self.t1_dataset_root_folder_path_entry.get() == "" or self.t1_path_manual_measures_entry.get() == "":
            self.t1_messages_info.insert("1.0", f'Select a dataset and a groundtruth file!!!')
            self.t1_results_info.insert("1.0", "Results can't be processed")
        else:
            print("proces enabled")
            print('run_img_experiment -->')
            dataset_name = os.path.basename(self.t1_dataset_root_folder_path_entry.get())
            dataset_parent_folder_path = os.path.abspath(os.path.join(self.t1_dataset_root_folder_path_entry.get(), os.pardir))
            #
            path_output_simulation = os.path.join(self.app_config.output_folder)
            path_output_img = os.path.join(path_output_simulation, 'output_img')  # TODO: add this to global variable config
            # # get database
            # # get path to open manual measures
            # # ---------------------
            dataset_manager_config = DatasetConfig(dataset_parent_folder_path, dataset_name)
            dataset_manager_obj = DatasetManager(dataset_manager_config)
            result_pair_list = dataset_manager_obj.get_labeled_mask_list_files()
            # # ---------------------
            # # TODO: 03/03/2023 this is repeated in many places, it must be replaced
            manual_measures_df = pd.read_csv(self.t1_path_manual_measures_entry.get(), dtype=str, sep=';')
            manual_measures_df['fruit_id'] = manual_measures_df['fruit_id'].astype(str)
            manual_measures_df['lab.axis_01_mm'] = manual_measures_df['lab.axis_01_mm'].astype(float)
            manual_measures_df['lab.axis_02_mm'] = manual_measures_df['lab.axis_02_mm'].astype(float)
            manual_measures_df['lab.weight_gr'] = manual_measures_df['lab.weight_gr'].astype(float)
            # # measures_selected_df = manual_measures_df # todo: 03/03/2023 to clean this.
            selected_fruits_list = pd.Series.tolist(manual_measures_df['fruit_id'])
            #
            # # -------------------------------
            if self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.BB.name:
                size_estimation_selector = SizeEstimationSelectorPx.BB
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.EF.name:
                size_estimation_selector = SizeEstimationSelectorPx.EF
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.CE.name:
                size_estimation_selector = SizeEstimationSelectorPx.CE
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.CF.name:
                size_estimation_selector = SizeEstimationSelectorPx.CF
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.RR.name:
                size_estimation_selector = SizeEstimationSelectorPx.RR
            # # -------------------------------
            #
            # # ---------------------
            # # todo: 14/10/2022 review parameters, could be made using parameter in constructor
            # print("print_labels", self.print_labels_check_var.get())
            screen_layout = DrawScreenManager()
            screen_layout.loop_over_frames(result_pair_list, selected_fruits_list, path_output_img, size_estimation_selector, self.print_labels_check_var.get())
            print(f"Images generated at {path_output_img}")
            # ---------------------
        pass

    def t1_run_simulation_experiment(self):
        """
        Create details of measurements from each labelled object
        """
        if self.t1_dataset_root_folder_path_entry.get() == "" or self.t1_path_manual_measures_entry.get() == "":
            self.t1_messages_info.insert("1.0", f'Select a dataset and a groundtruth file!!!')
            self.t1_results_info.insert("1.0", "Results can't be processed")
        else:
            print("proces enabled")
            print('run_img_experiment -->')
            print('run_simulation_experiment -->')
            dataset_name = os.path.basename(self.t1_dataset_root_folder_path_entry.get())
            dataset_parent_folder_path = os.path.abspath(
                os.path.join(self.t1_dataset_root_folder_path_entry.get(), os.pardir))

            camera_option = None  # TODO: 02/11/2022, at this time it seems not used
            depth_option = None
            weight_prediction_option = None
            comparative_report_option = None
            # -------------------------------
            if self.t1_camera_box.get() == CameraModelSelector.AK.name:
                camera_option = AzureKinect()
            elif self.t1_camera_box.get() == CameraModelSelector.KINECT_V2.name:
                camera_option = KinectV2()
            else:
                camera_option = AzureKinect()
            # -------------------------------
            # ROI selectors options
            # -------------------------------
            if self.t1_roi_selector_box.get() == ROISelector.BBOX.name:
                roi_selector = ROISelector.BBOX
            elif self.t1_roi_selector_box.get() == ROISelector.MASK.name:
                roi_selector = ROISelector.MASK
            # -------------------------------
            # Size estimation selector options:
            # -------------------------------
            if self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.BB.name:
                size_estimation_selector = SizeEstimationSelectorPx.BB
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.EF.name:
                size_estimation_selector = SizeEstimationSelectorPx.EF
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.CE.name:
                size_estimation_selector = SizeEstimationSelectorPx.CE
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.CF.name:
                size_estimation_selector = SizeEstimationSelectorPx.CF
            elif self.t1_size_estimation_selector_box.get() == SizeEstimationSelectorPx.RR.name:
                size_estimation_selector = SizeEstimationSelectorPx.RR
            # -------------------------------
            # Depth estimation selector
            # -------------------------------
            if self.t1_depth_selector_box.get() == DepthSelector.AVG.name:
                depth_option = DepthSelector.AVG
            elif self.t1_depth_selector_box.get() == DepthSelector.MOD.name:
                depth_option = DepthSelector.MOD
            elif self.t1_depth_selector_box.get() == DepthSelector.MIN.name:
                depth_option = DepthSelector.MIN
            # -------------------------------
            # caliber and height models
            # -------------------------------
            if self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_LM_MET_01.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_LM_MET_01
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_LM_MET_02.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_LM_MET_02
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_LM_MET_03.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_LM_MET_03
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_LM_MET_04.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_LM_MET_04
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_LM_MET_05.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_LM_MET_05
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_NLM_MET_01.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_NLM_MET_01
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.CH_NLM_MET_02.name:
                weight_prediction_option = WeightPredictionModelSelector.CH_NLM_MET_02
            # diameter and height models
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_01.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_01
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_02.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_02
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_03.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_03
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_04.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_04
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_LM_MET_05.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_LM_MET_05
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_NLM_MET_01.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_NLM_MET_01
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.D1D2_NLM_MET_02.name:
                weight_prediction_option = WeightPredictionModelSelector.D1D2_NLM_MET_02
            # option by default
            elif self.t1_weight_prediction_selector_box.get() == WeightPredictionModelSelector.MODEL_BY_DEFAULT.name:
                weight_prediction_option = WeightPredictionModelSelector.MODEL_BY_DEFAULT

            # ---------------------------------
            if self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.DEPTH.name:  # todo: 02/11/2022 it is not used in this research
                comparative_report_option = ComparativeMeasuresReportSelector.DEPTH
            elif self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.A1.name:
                comparative_report_option = ComparativeMeasuresReportSelector.A1
            elif self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.A2.name:
                comparative_report_option = ComparativeMeasuresReportSelector.A2
            elif self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.WEIGHT.name:
                comparative_report_option = ComparativeMeasuresReportSelector.WEIGHT
            elif self.t1_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.ALL.name:  # todo: 02/11/2022 it is not used in this research
                comparative_report_option = ComparativeMeasuresReportSelector.ALL

            # --------------------------------
            # PREPARING FILE NAME
            now = datetime.now()
            datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
            print(
                f'{datetime_experiment}, '
                f'{camera_option.__name__()}, '
                f'{roi_selector.name}, '
                f'{size_estimation_selector.name}, '
                f'{depth_option.name}, '
                f'{comparative_report_option.name},'
                f'{weight_prediction_option.name}')

            # --------------------------------
            # todo: 02/11/2022 add here a fix for the filename in case of mass and method
            root_folder = os.path.abspath('')
            day_measures_filename = datetime_experiment + camera_option.__name__() + '_' + roi_selector.name + '_' + size_estimation_selector.name + '_' + depth_option.name + '_' + comparative_report_option.name + '.csv'  # todo: add in parameters
            day_measures_filename_2 = datetime_experiment + 'comparative_by_day_2.csv'  # todo: add in parameters
            # todo: add additive file with results
            # todo: add ancillary columns
            path_output_simulation = os.path.join(self.app_config.output_folder)
            path_output_csv = os.path.join(path_output_simulation, 'output_csv')
            path_day_measures = os.path.join(path_output_csv, day_measures_filename)
            # ADD HERE SPECIFIC COLUMNS to use
            manual_measures_df = pd.read_csv(self.t1_path_manual_measures_entry.get(), dtype=str, sep=';')
            manual_measures_df['fruit_id'] = manual_measures_df['fruit_id'].astype(str)
            manual_measures_df['lab.depth_mm'] = manual_measures_df['lab.depth_mm'].astype(float)
            manual_measures_df['lab.o_caliber_mm'] = manual_measures_df['lab.o_caliber_mm'].astype(float)
            manual_measures_df['lab.o_height_mm'] = manual_measures_df['lab.o_height_mm'].astype(float)
            manual_measures_df['lab.axis_01_mm'] = manual_measures_df['lab.axis_01_mm'].astype(float)
            manual_measures_df['lab.axis_02_mm'] = manual_measures_df['lab.axis_02_mm'].astype(float)
            manual_measures_df['lab.weight_gr'] = manual_measures_df['lab.weight_gr'].astype(float)
            measures_selected_df = manual_measures_df

            dataset_manager_config = DatasetConfig(dataset_parent_folder_path, dataset_name)

            data_features_options = DataFeatureConfig(camera_conf=camera_option.rgb_sensor,
                                                      roi_selector=roi_selector,
                                                      size_estimation_selector=size_estimation_selector,
                                                      depth_selector=depth_option,
                                                      weight_selector=weight_prediction_option)

            simulator_config = PredictionsMetricsFrameworkConfig(dataset_manager_config, path_day_measures,
                                                                 data_features_options, weight_prediction_option,
                                                                 comparative_report_option)
            simulator_metrics = PredictionMetricsFramework(simulator_config)
            # -----------------------------
            # todo: 30/03/2022, this could be improved with only one function and internal parameters
            if self.t1_roi_selector_box.get() == ROISelector.BBOX.name:
                # start simulation with ground truth file selected by the user
                simulator_metrics.comparative_metrics_dataset_bbox(measures_selected_df)
            elif self.t1_roi_selector_box.get() == ROISelector.MASK.name:
                simulator_metrics.comparative_metrics_dataset_mask(measures_selected_df)  # start simulation
            # -----------------------------
            simulator_metrics.export_csv_results(path_day_measures)
            results_simulation_metrics = simulator_metrics.get_simulation_results()  # todo: this is common for comparative
            # results_simulation_metrics.print_metrics()  # todo: measures units must be equal to report selector
            # print(results_simulation_metrics.__str__())
            print(results_simulation_metrics.print_metrics_02())
            self.t1_results_info.insert("1.0", datetime_experiment + results_simulation_metrics.print_metrics_02())
            # todo: 30/03/2022 add here option to draw apples selected
            pass
        # --------------------------------

    def clean_text_widgets(self):
        self.t1_messages_info.delete("1.0", "end")
        self.t1_results_info.delete("1.0", "end")

    def t1_roi_selector_changed(self, event):
        """
        Used to restrict access to non-mask methods
        :param event:
        :return:
        """
        if self.t1_roi_selector_box.get() == ROISelector.BBOX.name:
            self.t1_size_estimation_selector_box['values'] = self.size_estimation_list_bbox
        elif self.t1_roi_selector_box.get() == ROISelector.MASK.name:
            self.t1_size_estimation_selector_box['values'] = self.size_estimation_list_mask
            # action here
        self.t1_size_estimation_selector_box.current(0)  # select default option

    def t2_select_folder_data(self):
        analyze_status_str = ""
        results_info_str = ""
        directory_selected = filedialog.askdirectory(initialdir=self.app_config.input_folder)

        if directory_selected == "":
            analyze_status_str = "A directory has not been selected " + "\n"
            print(analyze_status_str)
        else:
            self.t2_dataset_root_folder_path_entry['state'] = "normal"
            self.t2_dataset_root_folder_path_entry.delete(0, "end")
            self.t2_dataset_root_folder_path_entry.insert(0, os.path.join(directory_selected))
            self.t2_dataset_root_folder_path_entry['state'] = "readonly"
        # ----------------------------------------
        analyze_status_str = directory_selected + "\n"
        self.t2_messages_info.insert("1.0", analyze_status_str)
        # ----------------------------------------

    def t2_select_file_data(self):
        # self.clean_text_widgets
        analyze_status_str = ""
        results_info_str = ""
        path_filename_selected = filedialog.askopenfilename(initialdir=self.app_config.file_browser_input_folder,
                                                            title="Select a File", filetypes=(
            ("Text files", self.app_config.file_extension_to_search), ("all files", "*.csv")))

        if path_filename_selected == "":
            analyze_status_str = "A file has not been selected " + "\n"
        else:
            #################################
            an_input_file = os.path.join(path_filename_selected)
            #################################
            self.t2_path_manual_measures_entry['state'] = "normal"
            self.t2_path_manual_measures_entry.delete(0, "end")
            self.t2_path_manual_measures_entry.insert(0, os.path.join(an_input_file))
            self.t2_path_manual_measures_entry['state'] = "readonly"
            #################################
        # ----------------------------------------
        analyze_status_str = path_filename_selected + "\n"
        self.t2_messages_info.insert("1.0", analyze_status_str)

    def t2_run_simulation_experiment(self):

        if self.t2_dataset_root_folder_path_entry.get() == "" or self.t2_path_manual_measures_entry.get() == "":
            self.t2_messages_info.insert("1.0", f'Select a dataset and a groundtruth file!!!')
            self.t2_results_info.insert("1.0", "Results can't be processed")
        else:
            print("proces enabled")
            print('run_simulation_experiment -->')
            dataset_name = os.path.basename(self.t2_dataset_root_folder_path_entry.get())
            dataset_parent_folder_path = os.path.abspath(
                os.path.join(self.t2_dataset_root_folder_path_entry.get(), os.pardir))

            camera_option = None
            depth_option = None
            weight_prediction_option = None
            comparative_report_option = None

            if self.t2_camera_box.get() == CameraModelSelector.AK.name:
                camera_option = AzureKinect()
            elif self.t2_camera_box.get() == CameraModelSelector.KINECT_V2.name:
                camera_option = KinectV2()
            else:
                camera_option = AzureKinect()
            # -------------------------------
            # -------------------------------
            # -------------------------------
            if self.t2_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.DEPTH.name:
                comparative_report_option = ComparativeMeasuresReportSelector.DEPTH
            elif self.t2_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.A1.name:
                comparative_report_option = ComparativeMeasuresReportSelector.A1
            elif self.t2_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.A2.name:
                comparative_report_option = ComparativeMeasuresReportSelector.A2
            elif self.t2_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.WEIGHT.name:
                comparative_report_option = ComparativeMeasuresReportSelector.WEIGHT
            elif self.t2_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.ALL.name:  # TODO; 28/07/2022 THIS OPTION IS REDUNDANT
                comparative_report_option = ComparativeMeasuresReportSelector.ALL
            # -------------------------------

            # --------------------------------
            now = datetime.now()
            datetime_experiment = now.strftime("%Y%m%d_%H%M%S_")
            # --------------------------------
            path_output_simulation = os.path.join(self.app_config.output_folder)
            dataset_manager_config = DatasetConfig(dataset_parent_folder_path, dataset_name)

            # --------------------------------
            # get comparative measures
            integrations_tests = IntegrationDatasheetMetrics(datetime_experiment, camera_option,
                                                             comparative_report_option, dataset_manager_config,
                                                             self.t2_path_manual_measures_entry.get(),
                                                             path_output_simulation)
            # TODO: temporal solution 28/07/2022, WE HAVE TO ORGANIZE THIS AS AN OPTION AND IMPROVE IT.
            if self.t2_comparative_report_selector_box.get() == ComparativeMeasuresReportSelector.WEIGHT.name:
                integrations_tests.test_run_simulation_weight()
            else:
                integrations_tests.test_run_simulation_diameters()
                integrations_detail_tests = IntegrationDetailMetrics(datetime_experiment, camera_option,
                                                                     comparative_report_option, dataset_manager_config,
                                                                     self.t2_path_manual_measures_entry.get(),
                                                                     path_output_simulation)
                integrations_detail_tests.test_run_simulation_masks()
            # --------------------------------
            # get details
            # integrations_detail_tests = IntegrationDetailMetrics(datetime_experiment, camera_option, comparative_report_option, dataset_manager_config, self.path_manual_measures_entry.get(), path_output_simulation)
            # integrations_detail_tests.test_run_simulation_masks()
            # --------------------------------
            pass

        # --------------------------------

    def quit_app(self):
        # ---------------------------------------------
        self.destroy()
        pass
