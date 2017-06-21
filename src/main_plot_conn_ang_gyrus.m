clc;clear all;close all;
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg/src'));
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg/3rdParty'));
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg/MEX_Files'));

s=readdfs('/big_disk/ajoshi/coding_ground/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs');
s.vcolor(s.labels~=226+1,:)=0.5;
h=figure; hold on;
%plot_outline_labels(s,'k');
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.vcolor,'facecolor','interp','edgecolor','none','backfacelighting','unlit');
axis equal; axis off; view(-90,0);material dull; camlight; lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
set(gcf, 'Position', get(0,'Screensize'));zoom(2); % Maximize figure.
saveas(h,'left_ang_gyrus.png');

%%
s=readdfs('/big_disk/ajoshi/coding_ground/svreg/USCBrain/BCI-DNI_brain.left.mid.cortex.dfs');
s.vcolor(s.labels~=236+1 &s.labels~=238+1&s.labels~=240+1,:)=0.5;
h=figure; hold on;
%plot_outline_labels(s,'k');
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.vcolor,'facecolor','interp','edgecolor','none','backfacelighting','unlit');
axis equal; axis off; view(-90,0);material dull; camlight; lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
set(gcf, 'Position', get(0,'Screensize'));zoom(2); % Maximize figure.
saveas(h,'left_ang_gyrus_USCBrain2.png');


%%
figure;
load('/home/ajoshi/Downloads/conn_files/connectivity_fileangular gyrus_left_subdivision=3_BCI.mat')
vcolor=0*vertices+.5;
vcolor(ROI_labels'>0,1)=1;vcolor(ROI_labels'>0,2)=1;vcolor(ROI_labels'>0,3)=.5;
h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',vcolor,'facecolor','interp','edgecolor','none');
axis equal; axis off;
s.faces=faces+1;
s.vertices = vertices;
view(-90,0); camlight;material dull;lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
set(gcf, 'Position', get(0,'Screensize'));%zoom(2); % Maximize figure.
saveas(h,'left_ang_gyrus_Grayordinates.png');

%%
%/home/ajoshi/Downloads/conn_files
load('/big_disk/ajoshi/coding_ground/hybridatlas/angular gyrus/connectivity_fileangular_gyrus_left_subdivision=2_BCI.mat')
vcolor=0*vertices+.5;
vcolor(ROI_labels'==1,1)=1;vcolor(ROI_labels'==1,2)=0;vcolor(ROI_labels'==1,3)=0;
vcolor(ROI_labels'==2,1)=0;vcolor(ROI_labels'==2,2)=0;vcolor(ROI_labels'==2,3)=1;
vcolor(ROI_labels'==3,1)=0;vcolor(ROI_labels'==3,2)=0;vcolor(ROI_labels'==3,3)=0;


h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',vcolor,'facecolor','interp','edgecolor','none');
axis equal; axis off;
s.faces=faces+1;
s.vertices = vertices;
view(-45,15); camlight;material dull;lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
set(gcf, 'Position', get(0,'Screensize'));%zoom(2); % Maximize figure.
saveas(h,'left_ang_gyrus_Grayordinates_subdivided2.png');

%%
%load('/home/sgaurav/Documents/git_sandbox/cortical_parcellation/src/intensity_mode_map/intensity_file_angular gyrus_227_nCluster=2_BCI.mat')
load('/big_disk/ajoshi/coding_ground/hybridatlas/angular gyrus/intensity_file_angular_gyrus_227_nCluster=3_BCI.mat')

load('/big_disk/ajoshi/coding_ground/hybridatlas/angular gyrus/connectivity_fileangular_gyrus_left_subdivision=3_BCI.mat')
h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',freq'.*(labs_all'>0)+0*(labs_all'==0),'facecolor','interp','edgecolor','none');
axis equal; axis off;colormap gray;
s.labels=labs_all;s.faces=faces+1;s.vertices=s.vertices;
plot_outline_labels(s,'k'); colormap gray; caxis([40/3,40])
view(-45,15); camlight;material dull;lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
camlight;
set(gcf, 'Position', get(0,'Screensize'));%zoom(2); % Maximize figure.
saveas(h,'left_ang_gyrus_Grayordinates_freq32.png');
%%
sl=readdfs('/big_disk/ajoshi/coding_ground/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs');
s=readdfs('/big_disk/ajoshi/coding_ground/svreg/USCBrain/BCI-DNI_brain.left.mid.cortex.mod.dfs');
s.attributes(sl.labels~=226)=0;
h=figure;
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.attributes,'facecolor','interp','edgecolor','none');
axis equal; axis off;colormap gray;
view(-90,0); camlight;material dull;lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
set(gcf, 'Position', get(0,'Screensize'));%zoom(2); % Maximize figure.
saveas(h,'left_ang_gyrus_USCBrain_freq.png');
%%
load('/home/ajoshi/Downloads/conn_files/connectivity_fileangular gyrus_left_subdivision=3_BCI.mat')

h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',corr_to_cortex','facecolor','interp','edgecolor','none');
axis equal; axis off;
s.faces=faces+1;
s.vertices = vertices;
s.labels = ROI_labels';
hold on;
plot_outline_labels(s,'k'); colormap jet; caxis([0,1])
view(-90,0); camlight;material dull;lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
set(gcf, 'Position', get(0,'Screensize'));%zoom(2); % Maximize figure.
saveas(h,'conn_ang_gyrus3_1.png');
view(-90,0); camlight;
saveas(h,'conn_ang_gyrus3_2.png');

