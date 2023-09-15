"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: November 2021
Description:

Use:
"""

import os
from os.path import expanduser
from helpers.helper_filesystem import copy_folder
from gui_benchmarking.gui_benchmarking_config import GUISimulationConfig
from gui_benchmarking.gui_tab_window import GUIAKTabWindow
# without src.

if __name__ == '__main__':
    BASE_DIR = os.path.abspath('.')

    user_path = expanduser("~")
    base_path = os.path.join(user_path)

    current_main_path_str = __file__
    package_path = os.path.join(os.path.dirname(os.path.normpath(current_main_path_str)), 'ak_sw_benchmarker')
    # ------------
    package_path_config_files = os.path.join(package_path, 'conf')
    ui_path_config_file = os.path.join(package_path, 'ui_benchmarking_settings.conf')

    # ------------
    # in the current folder of execution
    root_folder = os.path.join(BASE_DIR, 'ak_sw_benchmarker')  #
    path_user_config_files = os.path.join(root_folder, 'conf')
    path_user_input_folder = os.path.join(root_folder, 'input_folder')
    path_user_output_folder = os.path.join(root_folder, 'output_dataset')
    path_user_output_csv_folder = os.path.join(path_user_output_folder, 'output_csv')
    path_user_output_img_folder = os.path.join(path_user_output_folder, 'output_img')

    print('user_path->', user_path)
    print('BASE_DIR->', BASE_DIR)
    print('current_main_path_str', current_main_path_str)
    print('package_path', package_path)
    print('path_user_config_files->', path_user_config_files)
    print('path_user_output_folder->', path_user_output_folder)

    # -------------------------
    # if directory doesn't exist, then create
    if not os.path.exists(root_folder):
        print("Directory DOES'NT exist!!!", root_folder)
        os.mkdir(root_folder)
        os.mkdir(path_user_config_files)
        os.mkdir(path_user_input_folder)
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        pass
    # -------------------------
    ui_simulation_config = GUISimulationConfig(ui_path_config_file)
    ui_simulation_config.input_folder = path_user_input_folder
    ui_simulation_config.output_folder = path_user_output_folder
    # -------------------------
    app = GUIAKTabWindow(ui_simulation_config)
    app.mainloop()
    # -------------------------