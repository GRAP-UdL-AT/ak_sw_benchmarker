# AKFruitYield: AK_SW_BENCHMARKER - Azure Kinect Size Estimation & Weight Prediction Benchmarker

AKFruitYield is a modular software that allows orchard data from RGB-D Azure Kinect cameras to be processed for fruit
size and fruit yield estimation. Specifically, two modules have been developed: i) [AK_SW_BENCHMARKER](https://pypi.org/project/ak-sw-benchmarker/) that makes it possible
to apply different sizing algorithms and allometric yield prediction models to manually labeled color and depth tree
images; and ii) [AK_VIDEO_ANALYSER](https://pypi.org/project/ak-video-analyser/) that analyses videos on which to automatically detect apples, estimate their size and
predict yield at the plot or per hectare scale using the appropriate algorithms. Both modules have easy-to-use
graphical interfaces and provide reports that can subsequently be used by other analysis tools.

[AK_VIDEO_ANALYSER](https://pypi.org/project/ak-video-analyser/) is part of the [AKFruitData](https://doi.org/10.1016/j.softx.2022.101231) and AKFruitYield family (Fig 1.), a suite
that offers field acquisition tools focused on the [Azure Kinect DK sensor](https://docs.microsoft.com/en/azure/kinect-dk/). Table 1-2 shows the links to the other
developed tools.

|                           |
|---------------------------|
| ![SOFTWARE_FAMILY](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/ak_fruit_family.png?raw=true) |
| Fig. 1. a) Proposed stages of data acquisition and extraction for AKFruitData and AKFruitYield. Dashed green lines correspond to processes related to acquisition, red lines to processes related to data creation and training, and black lines to processes for performance estimation. b) Interoperability between the data acquisition ([AK_ACQS](https://github.com/GRAP-UdL-AT/ak_acquisition_system); [AK_SM_RECORDER](https://pypi.org/project/ak-sm-recorder/)), data creation ([AK_FRAEX](https://pypi.org/project/ak-frame-extractor/)), algorithm benchmarking ([AK_SW_BENCHMARKER](https://pypi.org/project/ak-sw-benchmarker/)) and video analysis ([AK_VIDEO_ANALYSER](https://pypi.org/project/ak-video-analyser/)) modules. The processes proposed in Figure 1 are expanded and represented by the developed software.|

|                           | Package                   | Description            |
|---------------------------|---------------------------|-------------------------|
| ![AK_ACQS_100](https://github.com/juancarlosmiranda/juancarlosmiranda/blob/main/images/icons_992/ak_acqs_992.png?raw=true) | AK_ACQS Azure Kinect Acquisition System ([https://github.com/GRAP-UdL-AT/ak_acquisition_system](https://github.com/GRAP-UdL-AT/ak_acquisition_system)) | AK_ACQS is a software solution for data acquisition in fruit orchards using a sensor system boarded on a terrestrial vehicle. It allows the coordination of computers and sensors through the sending of remote commands via a GUI. At the same time, it adds an abstraction layer on library stack of each sensor, facilitating its integration. This software solution is supported by a local area network (LAN), which connects computers and sensors from different manufacturers ( cameras of different technologies, GNSS receiver) for in-field fruit yield testing. |
| ![AK_SM_RECORDER_100](https://github.com/juancarlosmiranda/juancarlosmiranda/blob/main/images/icons_992/ak_sm_recorder_992.png?raw=true) | AK_SM_RECORDER - Azure Kinect Standalone Mode ([https://pypi.org/project/ak-sm-recorder/](https://pypi.org/project/ak-sm-recorder/)) | A simple GUI recorder based on Python to manage Azure Kinect camera devices in a standalone mode. https://pypi.org/project/ak-sm-recorder/ |
| ![AK_FRAEX_100](https://github.com/juancarlosmiranda/juancarlosmiranda/blob/main/images/icons_992/ak_fraex_992.png?raw=true) | AK_FRAEX - Azure Kinect Frame Extractor ([https://pypi.org/project/ak-frame-extractor/](https://pypi.org/project/ak-frame-extractor/)) | AK_FRAEX is a desktop tool created for post-processing tasks after field acquisition. It enables the extraction of information from videos recorded in MKV format with the Azure Kinect camera. Through a GUI, the user can configure initial parameters to extract frames and automatically create the necessary metadata for a set of images. |
|                           | Table 1. | Modules developed under the [AKFruitData](https://doi.org/10.1016/j.softx.2022.101231) family |


|                           | Package                   | Description             |
|---------------------------|---------------------------|-------------------------|
| ![AK_SW_BENCHMARKER_100](https://github.com/juancarlosmiranda/juancarlosmiranda/blob/main/images/icons_100/ak_sw_benchmarker_100.png?raw=true) | AK_SW_BENCHMARKER - Azure Kinect Size Estimation & Weight Prediction Benchmarker ([https://pypi.org/project/ak-sw-benchmarker/](https://pypi.org/project/ak-sw-benchmarker/)) | Python based GUI tool for fruit size estimation and weight prediction. |
| ![AK_VIDEO_ANALYSER_100](https://github.com/juancarlosmiranda/juancarlosmiranda/blob/main/images/icons_100/ak_video_analyser_100.png?raw=true) | AK_VIDEO_ANALYSER - Azure Kinect Video Analyser ([https://pypi.org/project/ak-video-analyser/](https://pypi.org/project/ak-video-analyser/)) | Python based GUI tool for fruit size estimation and weight prediction from videos. |
| Table 2. | Modules developed under the AKFruitYield family |


## AK_SW_BENCHMARKER description

Python based GUI tool for fruit size estimation and weight prediction. It receives as input a data set in the format
explained by [Miranda et al., 2022](https://doi.org/10.1016/j.softx.2022.101231) and a ground truth file to display
various fruit measurements. ak-sw-benchmarker is part of the AKFruitYield family (Fig 2.), a suite that offers field
acquisition tools focused on the Azure Kinect DK sensor. Table 1 shows the links to the other developed tools. This is
the Github repository of **ak-sw-benchmarker**, an installable version can be found published on [Pypi.org](https://pypi.org/search/?q=ak-sw-benchmarker) at the following
link [https://pypi.org/project/ak-sw-benchmarker/](https://pypi.org/project/ak-sw-benchmarker/)

|                           |
|---------------------------|
| ![SOFTWARE_PRESENTATION](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/SOFTWAREX_article_04_fig_02_v1.1.png?raw=true) |
| Fig. 2. ak_sw_benchmarker module user interface. a) 'Dataset metrics' tab to select data (frames) and configure the sizing and yield prediction algorithms. b) 'Metric comparisons' tab to report results and error statistics.|


## Contents

1. Pre-requisites.
2. Functionalities.
3. Install and run.
4. Files and folder description.
5. Development tools, environment, build executables.

## 1. Pre-requisites

* [SDK Azure Kinect](https://docs.microsoft.com/es-es/azure/kinect-dk/set-up-azure-kinect-dk) installed.
* [pyk4a library](https://pypi.org/project/pyk4a/) installed. If the operating system is Windows, follow
  this [steps](https://github.com/etiennedub/pyk4a/). You can find test basic examples with
  pyk4a [here](https://github.com/etiennedub/pyk4a/tree/master/example).
* In Ubuntu 20.04, we provide a script to install the camera drivers following the instructions
  in [azure_kinect_notes](https://github.com/GRAP-UdL-AT/ak_acquisition_system/tree/main/docs/azure_kinect_notes/).
* Videos recorded with the Azure Kinect camera, optional video samples are available at [AK_FRAEX - Azure Kinect Frame Extractor demo videos](https://doi.org/10.5281/zenodo.6968103)


## 2. Functionalities

The functionalities of the software are briefly described. Supplementary material can be
found in [USER's Manual](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/USER_MANUAL_ak_sw_benchmarker_v1.md).

* **Analyse dataset** allows benchmarking to be performed with a final report of size estimates and weight prediction. The user has the option of introducing a file with values of real dimensions of fruits (ground truth) to compare with the set of images that it is desired to be analyzed. A final report with results (size and weight) grouped by image and fruit will be presented according to the selected parameters in addition to the test metrics.
* **Export images** makes it possible to visualize the geometric fitting of the ROIs on the objects (fruits) to be measured. Outputs are color images including binary masks of selected objects and fruit labeling. This functionality adds value to the software since the user can observe how sizing algorithms are applied to the images, enabling corrective adjustments in the algorithm configuration if necessary.
* **Run tests in dataset** calculates the test metrics. The user must first indicate the estimate to be analyzed (Report selector in Fig. 2b), namely the major geometric axis of the fruit (A1), the minor axis (A2) or the weight (WEIGHT). Since all sizing-yielding combinations are analyzed, this functionality allows the method with least error to be determined, also obtaining a final ranking of sizing algorithms or ranking of sizing-allometric model combinations.


## 3. Install and run

### 3.1 PIP quick install package

Create your Python virtual environment.

```
** For Linux systems **
python3 -m venv ./ak_sw_benchmarker_venv
source ./ak_sw_benchmarker_venv/bin/activate
pip install --upgrade pip
pip install python -m ak_sw_benchmarker

** execute package **
python -m ak_sw_benchmarker

** For Windows 10 systems **
python -m venv ./ak_sw_benchmarker_venv
.\ak_sw_benchmarker_venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install ak-sw-benchmarker

** execute package **
python -m ak_sw_benchmarker

```

Download the dataset with images and the file with apples groundtruth from [https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/data/](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/).


### 3.2 Install and run virtual environments using scripts provided

* [Linux]
  Enter to the folder **"ak_sw_benchmarker/"**

Create virtual environment(only first time)

```
chmod 755 *.sh; ./creating_env_ak_sw_benchmarker.sh
```

Run script.

```
./ak_sw_benchmarker_start.sh
```

* [Windows]
  Enter to the folder "ak_sw_benchmarker/"

Create virtual environment(only first time)

```
TODO_HERE
```

Run script from CMD.

```
./ak_sw_benchmarker_start.bat
```

## 4.3 Files and folder description

Folder description:

| Folders                    | Description            |
|---------------------------|-------------------------|
| [docs/](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/tree/main/docs) | Documentation |
| [src/](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/tree/main/src) | Source code |
| [data/](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/tree/main/data) | Dataset with images and the file with apples groundtruth. |
| . | . |

Python environment files:

| Files                    | Description              | OS |
|---------------------------|-------------------------|---|
| activate_env.bat | Activate environments in Windows | WIN |
| ak_sw_benchmarker_start.bat | Executing main script | WIN |
| creating_env_ak_sw_benchmarker_sim.sh | Automatically creates Python environments | Linux |
| ak_sw_benchmarker_start.sh | Executing main script | Linux |


Pypi.org PIP packages files:
| Files                    | Description              | OS |
|---------------------------|-------------------------|---|
| build_pip.bat | Build PIP package to distribution | WIN |
| /src/ak_sw_benchmarker/__main__.py | Main function used in package compilation | Supported by Python |
| setup.cfg | Package configuration PIP| Supported by Python |
| pyproject.toml | Package description PIP| Supported by Python |



## 5. Development tools, environment, build executables

Some development tools are needed with this package, listed below:

* [Opencv](https://opencv.org/).
* [7zip](https://7ziphelp.com/).

### 5.1 Notes for developers

You can use the __main__.py for execute as first time in src/ak-size-estimation/_ _ main _ _.py Configure the path of
the project, if you use Pycharm, put your folder root like this:
![ak_sw_benchmarker](https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/img/configuration_pycharm.png?raw=true)

### 5.2 Creating virtual environment Windows / Linux

```
python3 -m venv ak_size_weight_sim_venv
source ./ak_size_weight_sim_venv/bin/activate
pip install --upgrade pip
pip install -r requirements_windows.txt or pip install -r requirements_linux.txt
```

** If there are some problems in Windows, follow [this](https://github.com/etiennedub/pyk4a/) **

```
pip install pyk4a --no-use-pep517 --global-option=build_ext --global-option="-IC:\Program Files\Azure Kinect SDK v1.4.1\sdk\include" --global-option="-LC:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\lib"
```

## 5.3 Building PIP package

We are working to offer Pypi support for this package. At this time this software can be built by scripts automatically.

### 5.3.1 Build packages

```
py -m pip install --upgrade build
build_pip.bat
```

### 5.3.2 Download PIP package

```
pip install package.whl
```

### 5.3.3 Run ak_sw_benchmarker

```
python -m ak_sw_benchmarker
```

After the execution of the script, a new folder will be generated inside the project **"/dist"**. You can copy **
ak_sw_benchmarker_f/** or a compressed file **"ak_sw_benchmarker_f.zip"** to distribute.

### 5.6 Package distribution format

At this time, the current supported format for the distribution is Python packages.

| Package type | Package |  Url |  Description | 
|--------------|---------|------|------| 
| PIP          | .whl    | .whl | PIP packages are stored in build/ |

## Authorship

This project is contributed by [GRAP-UdL-AT](https://www.grap.udl.cat/en/index.html). Please contact authors to report bugs
juancarlos.miranda@udl.cat

## Citation

If you find this code useful, please consider citing:

```
@article{MIRANDA2022101231,
title = {AKFruitYield: Modular benchmarking and video analysis software for Azure Kinect cameras for fruit size and fruit yield estimation in apple orchards},
journal = {SoftwareX},
volume = {XX},
pages = {000000},
year = {2023},
issn = {0000-0000},
doi = {},
url = {},
author = {Juan Carlos Miranda and Jaume Arnó and Jordi Gené-Mola and Spyros Fountas and Eduard Gregorio},
keywords = {RGB-D camera, apple fruit sizing, yield prediction, detection and benchmarking algorithms, allometry},
abstract = {.}
}
``` 

## Acknowledgements

This work was partly funded by the Department of Research and Universities of the Generalitat de Catalunya (grants 2017
SGR 646) and by the Spanish Ministry of Science and Innovation/AEI/10.13039/501100011033/ERDF (grant
RTI2018-094222-B-I00 [PAgFRUIT project](https://www.pagfruit.udl.cat/en/) and PID2021-126648OB-I00 [PAgPROTECT project](https://www.grap.udl.cat/en/recerca/projectes-de-recerca/pagprotect/)). The Secretariat of Universities
and Research of the Department of Business and Knowledge of the [Generalitat de Catalunya](https://web.gencat.cat) and European Social Fund (ESF)
are also thanked for financing Juan Carlos Miranda’s pre-doctoral fellowship ([2020 FI_B 00586](https://agaur.gencat.cat/en/inici/index.html)). The work of Jordi
Gené-Mola was supported by the Spanish Ministry of Universities through a Margarita Salas postdoctoral grant funded by
the European Union - NextGenerationEU. The authors would also like to thank the Institut de Recerca i Tecnologia
Agroalimentàries [(IRTA)](https://www.irta.cat/es/) for allowing the use of their experimental fields, and in particular Dr. Luís Asín and Dr. Jaume
Lordán who have contributed to the success of this work.


<img src="https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/logos/logo_PAgFRUIT.png" height="60px" alt="PAgFRUIT Research Project"/>
<img src="https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/logos/logo_udl.png" height="60px" alt="Universitat de Lleida"/>
<img src="https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/logos/logo_goverment_calonia.png" height="60px" alt="Generalitat de Catalunya"/>
<img src="https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/logos/logo_min_science.png" height="60px" alt="Ministerio de Ciencia, Innovación y Universidades"/>
<img src="https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/logos/logo_UNIO_EUROPEA.png" height="60px" alt="Fons Social Europeu (FSE) "/>
<img src="https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/blob/main/docs/img/logos/logo_AGAUR.png" height="60px" alt="AGAUR"/>
