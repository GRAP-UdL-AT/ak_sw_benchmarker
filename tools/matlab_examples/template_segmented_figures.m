% ------------------------------------------------------------------------
% Fruit Detection Project
% Author: https://github.com/juancarlosmiranda/
% Date: November 20210
% This script is used to draw plotters for the paper
% First execute scriptDepthStatistics3D, this generates cropped data from a
% frame image.
% This is an script used to show 3d plot data with details
% ------------------------------------------------------------------------

% Script to draw

%% setting environment
clc; close all; clear all;
userPath='C:/Users/Usuari/';

%% Output results paths
OutputPath=fullfile(userPath, 'development','ak_size_weight_sim','tools','data','output','/');
pathOutputResultsSegRGB=fullfile(OutputPath,'outcomesRGB','/');
pathOutputResultsSegMasks=fullfile(OutputPath,'outcomesMasks','/');
pathOutputResultsDepth=fullfile(OutputPath,'outcomesDepth','/');
pathOutputResultsHeatmap=fullfile(OutputPath,'outcomesHeatmap','/');
pathOutputResults3D=fullfile(OutputPath,'outcomes3D','/');
pathOutputResultsFeaturesFiles=fullfile(OutputPath,'outcomesFiles','/');


%% -------------------------
% CHANGE HERE TO THE IMAGE

% %% Figures 02 from one selected apple
% % load specific depth .mat
im_depth_apple = '20210927_123505_k_r2_e_000_150_138_2_0_C.png_14.mat'; % APPLE_2167
im_cropped_mask_name = '20210927_123505_k_r2_e_000_150_138_2_0_C.png_14.png'; % APPLE_2167

load(fullfile(pathOutputResultsDepth, im_depth_apple));
depth_apple_selected=cropped_depth_data; %IDepthObject;  % get channel from transformed depth matrix

im_mask_path=fullfile(pathOutputResultsSegMasks, im_cropped_mask_name);
cropped_mask_im =imread(im_mask_path);

cropped_depth_data_masked=immultiply(cropped_depth_data,cropped_mask_im); % get segmented depth data

% -----------------------------------
% DEPTH STATISCAL METRICS over fruit selected
% -----------------------------------
temp_depth_apple_selected=depth_apple_selected(depth_apple_selected>0); % to get statistics descriptive
meanDepth=mean2(temp_depth_apple_selected);
stdDepth=std2(temp_depth_apple_selected);
minDepth=min(temp_depth_apple_selected);
maxDepth=max(temp_depth_apple_selected);
modeDepth=mode(temp_depth_apple_selected, 'all');
fprintf('MEAN=%3f STD=%3f MIN=%3f MAX=%3f MOD=%3f \n', meanDepth, stdDepth, minDepth, maxDepth, modeDepth);

%% FIGURE 02 heatmap
%current_label = 'APPLE 2167'
%imageName='IMAGE_NAME_'
%title_heatmap_name = strcat(current_label,' depth');
%im_heatmap = strcat(imageName,'_h','.png');    
%im_heatmap_path = fullfile(pathOutputResultsHeatmap, im_heatmap); 
%plotHeatmapDepthSpecial(title_heatmap_name, depth_apple_selected, im_heatmap_path);
%% call to segmented image
%title_heatmap_name = strcat(current_label,' depth with mask');
%im_heatmap = strcat(imageName,'_hm','.png');    
%im_heatmap_path = fullfile(pathOutputResultsHeatmap, im_heatmap); 
%plotHeatmapDepthSpecial(title_heatmap_name, cropped_depth_data_masked, im_heatmap_path);


%% FIGURE 03 3D plot 
% only depth without mask
current_label = 'APPLE 2167'
imageName='IMAGE_NAME_'
title_3dplot_name = strcat(current_label,'- BBOX region');
im_3dplot = strcat(imageName,'_3d','.png');    
im_3dplot_path = fullfile(pathOutputResults3D, im_3dplot); 
plot3dDepthSpecial(title_3dplot_name, depth_apple_selected, im_3dplot_path)

% call to segmented image
title_3dplot_name = strcat(current_label,'- MASK region');
im_3dplot = strcat(imageName,'_3d_mask','.png');    
im_3dplot_path = fullfile(pathOutputResults3D, im_3dplot); 
plot3dDepthSpecial(title_3dplot_name, cropped_depth_data_masked, im_3dplot_path)


%% Documentation
% https://es.mathworks.com/matlabcentral/answers/513971-how-can-i-modify-the-x-and-y-axis-tick-labels-for-a-heatmap-chart
% 
