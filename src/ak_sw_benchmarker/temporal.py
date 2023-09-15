# if directory doesn't exist, then create
if os.path.exists(path_user_output_folder):
    print('Directory exist!!!', path_user_output_folder)
else:
    os.mkdir(path_user_output_folder)
    os.mkdir(path_user_output_csv_folder)
    os.mkdir(path_user_output_img_folder)
    pass
# -------------------------

# if directory doesn't exist, then create
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