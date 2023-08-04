#!/bin/bash
# HEADER FOR BASH SCRIPTS
# Project: ak-size-estimation Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/
#
# * PAgFRUIT http://www.pagfruit.udl.cat/en/
# * GRAP http://www.grap.udl.cat/
#
# Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/

# commands definitions
PYTHON_CMD='python3'

# folders names definitions
DEVELOPMENT_ENV_PATH='development_env'
COMMON_ENV_PATH='bin/activate'


# files extensions names
EXT_SCRIPTS_SH='*.sh'
EXT_ZIP='.zip'

# folders names definitions
DEVELOPMENT_PATH='development'
DEVELOPMENT_ENV_PATH='development_env'
COMMON_ENV_PATH='bin/activate'


# software folders names
SIZE_ESTIMATION_NAME='ak_simulator'


# project folders
ROOT_FOLDER_F=$HOME/$DEVELOPMENT_PATH/ #$ROOT_FOLDER_NAME/
SIZE_ESTIMATION_NAME_F=$ROOT_FOLDER_F$SIZE_ESTIMATION_NAME/

# environment folders
ENV_NAME='_venv'
ROOT_ENV_F=$HOME/$DEVELOPMENT_ENV_PATH/ #$ROOT_FOLDER_NAME$ENV_NAME/
SIZE_ESTIMATION_NAME_ENV_F=$ROOT_ENV_F$SIZE_ESTIMATION_NAME$ENV_NAME/

# activating environments
source $SIZE_ESTIMATION_NAME_ENV_F$COMMON_ENV_PATH

python ak_size_weight_sim_main.py
deactivate
