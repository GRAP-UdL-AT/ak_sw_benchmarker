%
% Project: ak-size-estimation Azure Kinect Size Estimation & Weight Prediction Benchmarker https://github.com/GRAP-UdL-AT/ak_sw_benchmarker/
%
% * PAgFRUIT http://www.pagfruit.udl.cat/en/
% * GRAP http://www.grap.udl.cat/
%
% Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
% Date: November 2021
% Description:
%
% Use:
%
% ------------------------------------------------------------------------
% Segmentation using depth information and thresholds
% ===================================================
% This example shows how to load data extracted from videos in .mkv format 
% using AK_FRAME_EXTRACTOR and its further use in MATLABs scripts as .mat files.
% Using frames (RGB and depth data) extracted from video files, it is filtered 
% by depth threshold values avoiding zero values to obtain an RGB fruit image.
% In this script two types of thresholds are applied, the first mask is
% segmented with one threshold, and the second with two types of limits.
%
%% setting environment
clc; close all; clear all;
home_user=fullfile('C:','Users', 'Usuari')  % POINT TO "..user root" folder
dataset_root_folder = fullfile(home_user, 'development', 'ak_size_weight_sim', 'tools', 'data')
script_path=fullfile(home_user, 'development', 'ak_size_weight_sim', 'tools','matlab_examples')

% input data examples
test_images_path=fullfile(dataset_root_folder);
path_test_depth=fullfile(dataset_root_folder);

% output data
output_images_path=fullfile(script_path,'output_threshold_depth');

% data names: images and DEPTH
image_base_name='20210927_114012_k_r2_e_000_150_138_2_0';
rgb_image_name=strcat(image_base_name,'_C.png');

depth_image_name=strcat(image_base_name,'_D.mat');
image_heatmap_orig=strcat(depth_image_name,'_h_orig.jpg');

% images names for mask 1
image_segmented_mask_name_1=strcat(rgb_image_name,'_mask1.jpg');
image_heatmap_name_2_1=strcat(depth_image_name,'_h_2_1.jpg');

% images names for mask 2
image_segmented_mask_name_2=strcat(rgb_image_name,'_mask2.jpg');
image_name_heatmap_2_2=strcat(depth_image_name,'_h_2_2.jpg');


%% load RGB image
rgb_data_path=fullfile(test_images_path, rgb_image_name);
rgb_data=imread(rgb_data_path);

%% load DEPTH
load(fullfile(path_test_depth, depth_image_name));
depth_data=transformed_depth; % load from file
% -----------------------

%% configure thresholds and getting masks
threshold_distance=500;
depth_logic_mask_1=depth_data(:,:)>threshold_distance;

threshold_distance_min=1400;
threshold_distance_max=1500;
depth_logic_mask_2=(depth_data(:,:) >= threshold_distance_min ) & (depth_data(:,:) <= threshold_distance_max);

%% segmentation with mask 1 single threshold
rgb_data_segmented_1(:,:,1)=immultiply(rgb_data(:,:,1),depth_logic_mask_1);
rgb_data_segmented_1(:,:,2)=immultiply(rgb_data(:,:,2),depth_logic_mask_1);
rgb_data_segmented_1(:,:,3)=immultiply(rgb_data(:,:,3),depth_logic_mask_1);


%% segmentation with mask 2 appliying two thresholds at each end
rgb_data_segmented_2(:,:,1)=immultiply(rgb_data(:,:,1),depth_logic_mask_2);
rgb_data_segmented_2(:,:,2)=immultiply(rgb_data(:,:,2),depth_logic_mask_2);
rgb_data_segmented_2(:,:,3)=immultiply(rgb_data(:,:,3),depth_logic_mask_2);


%% Figures
%fo_1=figure('Name','Original RGB Image', 'Position', get(0, 'Screensize')); figure(fo_1); imshow(rgb_data); title(['Original RGB Image']);

%% Mask 1
%f1_1=figure('Name','RGB single threshold'); figure(f1_1); imshow(rgb_data_segmented_1); title(['RGB single threshold']);

%% Saving segmented images
imwrite(rgb_data_segmented_1, fullfile(output_images_path, image_segmented_mask_name_1), 'png');
imwrite(rgb_data_segmented_2, fullfile(output_images_path, image_segmented_mask_name_2), 'png');

%% depth statistics
depth_selected=depth_data(depth_data>0); % to get statistics descriptive
meanDepth=mean2(depth_selected);
stdDepth=std2(depth_selected);
minDepth=min(depth_selected);
maxDepth=max(depth_selected);
modeDepth=mode(depth_selected, 'all');
fprintf('Original depth = mean=%3f std=%3f min=%3f max=%3f mode=%3f \n', meanDepth, stdDepth, minDepth, maxDepth, modeDepth);

