function [ output_args ] = plot3dDepthSpecial(surface_title, depth_apple_selected, im_3dplot_path)

% -----------------------------------
% DEPTH STATISCAL METRICS over fruit selected
% -----------------------------------
temp_depth_apple_selected=depth_apple_selected(depth_apple_selected>0); % to get statistics descriptive
meanDepth=mean2(temp_depth_apple_selected);
stdDepth=std2(temp_depth_apple_selected);
minDepth=min(temp_depth_apple_selected);
maxDepth=max(temp_depth_apple_selected);
modeDepth=mode(temp_depth_apple_selected, 'all');

fprintf('In 3D-> MEAN=%3f STD=%3f MIN=%3f MAX=%3f MOD=%3f \n', meanDepth, stdDepth, minDepth, maxDepth, modeDepth);

maxDepth=1200; % fixed to mantain the scale

%% FIGURE 03
% Create figure
figure_03_title = surface_title;
surface_title_font_size=36
axes_font_size=22

x_label_title = 'Width in px';
y_label_title = 'Height in px';
z_label_title = 'Depth in mm';
z_min_limit=minDepth;
z_max_limit=maxDepth;
MIN_L = minDepth;
MAX_L = maxDepth;
RANGE_TICKS = MAX_L - MIN_L;
STEP_TICKS = RANGE_TICKS/10;
PAR_MIN = MIN_L-(mod(MIN_L,5)); % BEGIN FROM even number
ARRAY_TICKS = [PAR_MIN:STEP_TICKS:MAX_L];

figure_03 = figure('WindowState','maximized','Name',figure_03_title);

colormap(jet(25));
axes1 = axes('Parent',figure_03,'Position',[0.147445404806389 0.107997997997998 0.618624885621344 0.815]);
hold(axes1,'on');
surface(depth_apple_selected)
view(axes1,[45.916883538365 63.3574380519591]);
xlabel(x_label_title);
ylabel(y_label_title);
zlabel(z_label_title);
zlim(axes1,[z_min_limit z_max_limit]);
%title(surface_title,26);
%title(surface_title,'FontSize',36);
%title('APPLE 2167 depth values 3D','FontSize',36);
title(surface_title,'FontSize',surface_title_font_size);

%set(axes1,'CLim',[z_min_limit z_max_limit]); % CHANGE HERE the limits
set(axes1,'CLim',[z_min_limit z_max_limit],'FontSize',22);
%colorbar(axes1,'Ticks',ARRAY_TICKS);
colorbar(axes1,'Position',...
    [0.821799457094399 0.115349063184884 0.0111111111111111 0.815],...
    'Ticks',ARRAY_TICKS,...
    'FontSize',axes_font_size);

hold(axes1,'off');



% save data
F=getframe(figure_03);
imwrite(F.cdata, im_3dplot_path);
%pause
close(figure_03);

end