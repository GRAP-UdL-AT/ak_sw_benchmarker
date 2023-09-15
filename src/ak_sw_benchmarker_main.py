import os
from os.path import expanduser
import sys
sys.path.append(os.path.join(os.path.abspath('.'), 'src'))

from helpers.helper_filesystem import copy_folder
from gui_benchmarking.gui_benchmarking_config import GUISimulationConfig
from gui_benchmarking.gui_tab_window import GUIAKTabWindow
# without src.

if __name__ == '__main__':
    BASE_DIR = os.path.join(os.path.abspath('.'), 'ak_sw_benchmarker')
    path_config_file = os.path.join(BASE_DIR, 'conf', 'ui_benchmarking_settings.conf')

    user_path = expanduser("~")
    base_path = os.path.join(user_path)

    current_main_path_str = __file__
    package_path = os.path.dirname(os.path.normpath(current_main_path_str))
    package_path_config_files = os.path.join(package_path, 'conf')
    path_user_config_files = os.path.join(BASE_DIR, 'conf')
    path_user_input_folder = os.path.join(BASE_DIR, 'input_folder')
    path_user_output_folder = os.path.join(BASE_DIR, 'output_dataset')
    path_user_output_csv_folder = os.path.join(BASE_DIR, path_user_output_folder, 'output_csv')
    path_user_output_img_folder = os.path.join(BASE_DIR, path_user_output_folder, 'output_img')

    print('BASE_DIR->', BASE_DIR)
    print('user_path->', user_path)
    print('current_main_path_str', current_main_path_str)
    print('package_path', package_path)
    print('path_user_config_files->', path_user_config_files)
    print('path_user_output_folder->', path_user_output_folder)

    # if directory doesn't exist, then create
    if os.path.exists(path_user_output_folder):
        print('Directory exist!!!', path_user_output_folder)
    else:
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        pass
    # -------------------------
    if os.path.exists(path_user_config_files):
        print('Directory exist!!!', path_user_config_files)
    else:
        # ---------------------
        print('Directory doesnt exist!!!', path_user_config_files)
        print('Creating directory ', path_user_config_files)
        os.mkdir(path_user_config_files)
        os.mkdir(path_user_input_folder)
        os.mkdir(path_user_output_folder)
        os.mkdir(path_user_output_csv_folder)
        os.mkdir(path_user_output_img_folder)
        # ---------------------
        copy_folder(package_path_config_files, path_user_config_files)
    # -------------------------
    ui_simulation_config = GUISimulationConfig(path_config_file)
    ui_simulation_config.input_folder = path_user_input_folder
    ui_simulation_config.output_folder = path_user_output_folder
    app = GUIAKTabWindow(ui_simulation_config)
    app.mainloop()
    # -------------------------