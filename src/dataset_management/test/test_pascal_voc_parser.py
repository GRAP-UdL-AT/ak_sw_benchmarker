"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/
# Author: Juan Carlos Miranda
# Date: January 2022
# Description:
  Test for PASCAL VOC format

Documentation in https://docs.python.org/3/library/unittest.html

Usage:
python -m unittest dataset_management/test/test_pascal_voc_parser.py
"""
import unittest
import os
from src.dataset_management.pascal_voc_parser import PascalVocParser


class TestPASCALVOCParser(unittest.TestCase):

    def setUp(self):
        self.root_folder = os.path.abspath('')
        # self.file_pv_to_check = '20210927_115932_k_r2_e_000_150_138_1_0_C.xml'
        self.file_pv_to_check = '20210927_114012_k_r2_e_000_150_138_2_0_C.xml'
        self.pv_folder = 'pascal_voc_files'  # HERE WE DEFINE THE NAME OF DATASET
        self.dataset_folder_pv_path = os.path.join(self.root_folder, self.pv_folder)
        print(self.root_folder)

    def test_pascal_voc_read_file(self):
        print(self.test_pascal_voc_read_file.__name__)
        # path to files for test
        a_pv_file_path = os.path.join(self.dataset_folder_pv_path, self.file_pv_to_check)
        pv_labelled_list, pv_label_list = PascalVocParser.readXMLFromFile(a_pv_file_path)  # load data to memory

        # to crop images in MATLAB us this format
        # human_labeled_MATLAB_list = [
        #    [1299, 363, 91, 91],
        #    [1236, 354, 44, 43],
        # ]

        # --------------------------
        # in PASCAL VOC format list
        # human_labeled_list = [
        #    [1299, 363, 1390, 454],
        #    [1236, 354, 1280, 397],
        # ]
        # --------------------------
        #human_labeled_list_01 = [
        #    ['1299', '363', '1390', '454'],
        #    ['1236', '354', '1280', '397'],
        #    ['1129', '419', '1172', '462'],
        #    ['1114', '161', '1165', '212'],
        #    ['1055', '33', '1117', '95'],
        #    ['923', '207', '984', '268'],
        #    ['909', '112', '969', '172'],
        #    ['1017', '667', '1071', '721'],
        #    ['1071', '677', '1114', '721'],
        #    ['1366', '513', '1419', '565'],
        #    ['1334', '539', '1391', '596'],
        #    ['1200', '581', '1252', '633'],
        #    ['840', '220', '896', '276'],
        #    ['890', '168', '932', '209'],
        #    ['981', '74', '1036', '129'],
        #    ['1110', '368', '1150', '408'],
        #    ['1106', '321', '1135', '351'],
        #    ['1098', '264', '1137', '303'],
        #    ['938', '519', '985', '566'],
        #    ['897', '513', '943', '559'],
        #    ['619', '693', '674', '749'],
        #    ['1023', '954', '1097', '1029'],
        #    ['800', '721', '853', '774']
        #]
        # 11:40
        #human_labeled_list_02 = [
        #    ['1075', '71', '1125', '129'],
        #    ['1005', '107', '1050', '161'],
        #    ['936', '145', '987', '206'],
        #    ['916', '196', '955', '235'],
        #    ['952', '230', '1002', '289'],
        #    ['871', '241', '923', '299'],
        #    ['1128', '185', '1175', '235'],
        #    ['1115', '275', '1154', '317'],
        #    ['1124', '332', '1154', '363'],
        #    ['1129', '378', '1165', '417'],
        #    ['1137', '427', '1182', '467'],
        #    ['924', '509', '969', '558'],
        #    ['958', '518', '1002', '564'],
        #    ['1028', '648', '1075', '704'],
        #    ['1074', '662', '1114', '705'],
        #    ['1198', '578', '1245', '625'],
        #    ['1033', '913', '1096', '982'],
        #    ['1240', '367', '1282', '409'],
        #    ['1301', '374', '1387', '459'],
        #    ['1360', '514', '1413', '565'],
        #    ['1335', '546', '1390', '594'],
        #    ['450', '97', '510', '155'],
        #    ['483', '311', '543', '366'],
        #    ['589', '313', '645', '374'],
        #    ['553', '361', '611', '416'],
        #    ['351', '656', '428', '723'],
        #    ['672', '678', '720', '728'],
        #    ['832', '701', '882', '751']]

        human_labeled_list_01 = [
            [1299, 363, 1390, 454],
            [1236, 354, 1280, 397],
            [1129, 419, 1172, 462],
            [1114, 161, 1165, 212],
            [1055, 33, 1117, 95],
            [923, 207, 984, 268],
            [909, 112, 969, 172],
            [1017, 667, 1071, 721],
            [1071, 677, 1114, 721],
            [1366, 513, 1419, 565],
            [1334, 539, 1391, 596],
            [1200, 581, 1252, 633],
            [840, 220, 896, 276],
            [890, 168, 932, 209],
            [981, 74, 1036, 129],
            [1110, 368, 1150, 408],
            [1106, 321, 1135, 351],
            [1098, 264, 1137, 303],
            [938, 519, 985, 566],
            [897, 513, 943, 559],
            [619, 693, 674, 749],
            [1023, 954, 1097, 1029],
            [800, 721, 853, 774]
        ]
        # 11:40
        human_labeled_list_02 = [
            [1075, 71, 1125, 129],
            [1005, 107, 1050, 161],
            [936, 145, 987, 206],
            [916, 196, 955, 235],
            [952, 230, 1002, 289],
            [871, 241, 923, 299],
            [1128, 185, 1175, 235],
            [1115, 275, 1154, 317],
            [1124, 332, 1154, 363],
            [1129, 378, 1165, 417],
            [1137, 427, 1182, 467],
            [924, 509, 969, 558],
            [958, 518, 1002, 564],
            [1028, 648, 1075, 704],
            [1074, 662, 1114, 705],
            [1198, 578, 1245, 625],
            [1033, 913, 1096, 982],
            [1240, 367, 1282, 409],
            [1301, 374, 1387, 459],
            [1360, 514, 1413, 565],
            [1335, 546, 1390, 594],
            [450, 97, 510, 155],
            [483, 311, 543, 366],
            [589, 313, 645, 374],
            [553, 361, 611, 416],
            [351, 656, 428, 723],
            [672, 678, 720, 728],
            [832, 701, 882, 751]]


        #self.assertEqual(pv_labelled_list, human_labeled_list_01)
        self.assertEqual(pv_labelled_list, human_labeled_list_02)


if __name__ == '__main__':
    unittest.main()
