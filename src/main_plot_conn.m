clc;clear all;close all;
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg/src'));
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg/3rdParty'));
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg/MEX_Files'));

s=readdfs('/big_disk/ajoshi/coding_ground/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.mid.cortex.dfs');
s.vcolor(s.labels~=184,:)=0.5;
h=figure; hold on;
%plot_outline_labels(s,'k');
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.vcolor,'facecolor','interp','edgecolor','none','backfacelighting','unlit');
axis equal; axis off; view(-90,0);material dull; camlight; lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
saveas(h,'right_cingulate.png');

%%
s=readdfs('/big_disk/ajoshi/coding_ground/svreg/USCBrain/BCI-DNI_brain.right.mid.cortex.dfs');
s.vcolor(s.labels~=186 &s.labels~=188&s.labels~=190,:)=0.75;
h=figure; hold on;
%plot_outline_labels(s,'k');
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.vcolor,'facecolor','interp','edgecolor','none','backfacelighting','unlit');
axis equal; axis off; view(-90,0);material dull; camlight; lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
saveas(h,'right_cingulate_USCBrain2.png');


%%

load('/home/ajoshi/Downloads/conn_files/connectivity_filecingulate_right_subdivision=3_BCI.mat')
vcolor=0*vertices+.5;
vcolor(ROI_labels'>0,1)=1;vcolor(ROI_labels'>0,2)=1;vcolor(ROI_labels'>0,3)=.5;
h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',vcolor,'facecolor','interp','edgecolor','none');
axis equal; axis off;
s.faces=faces+1;
s.vertices = vertices;
view(-90,0); camlight;material dull;lighting phong;
saveas(h,'right_cingulate_Grayordinates.png');

%%
load('/home/ajoshi/Downloads/conn_files/connectivity_filecingulate_right_subdivision=3_BCI.mat')
vcolor=0*vertices+.5;
vcolor(ROI_labels'==1,1)=37/255;vcolor(ROI_labels'==1,2)=124/255;vcolor(ROI_labels'==1,3)=182/255;
vcolor(ROI_labels'==2,1)=86/255;vcolor(ROI_labels'==2,2)=177/255;vcolor(ROI_labels'==2,3)=46/255;
vcolor(ROI_labels'==3,1)=240/255;vcolor(ROI_labels'==3,2)=97/255;vcolor(ROI_labels'==3,3)=97/255;

h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',vcolor,'facecolor','interp','edgecolor','none');
axis equal; axis off;
s.faces=faces+1;
s.vertices = vertices;
view(-90,0); camlight;material dull;lighting phong;
saveas(h,'right_cingulate_Grayordinates_subdivided.png');

%%
load('/home/sgaurav/Documents/git_sandbox/cortical_parcellation/src/intensity_mode_map/intensity_file_cingulate_184_nCluster=3_BCI.mat')
load('/home/ajoshi/Downloads/conn_files/connectivity_filecingulate_right_subdivision=3_BCI.mat')
h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',freq'.*(labs_all'>0)+0*(labs_all'==0),'facecolor','interp','edgecolor','none');
axis equal; axis off;colormap gray;
view(-90,0); camlight;material dull;lighting phong;
saveas(h,'right_cingulate_Grayordinates_freq.png');
%%
sl=readdfs('/big_disk/ajoshi/coding_ground/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.mid.cortex.dfs');
s=readdfs('/big_disk/ajoshi/coding_ground/svreg/USCBrain/BCI-DNI_brain.right.mid.cortex.mod.dfs');
s.attributes(sl.labels~=184)=0;
h=figure;
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.attributes,'facecolor','interp','edgecolor','none');
axis equal; axis off;colormap gray;
view(-90,0); camlight;material dull;lighting phong;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
saveas(h,'right_cingulate_USCBrain_freq.png');
%%
load('/home/ajoshi/Downloads/conn_files/connectivity_filecingulate_right_subdivision=3_BCI.mat')

h=figure;
patch('faces',faces+1,'vertices',vertices,'facevertexcdata',corr_to_cortex','facecolor','interp','edgecolor','none');
axis equal; axis off;
s.faces=faces+1;
s.vertices = vertices;
s.labels = ROI_labels';
hold on;
plot_outline_labels(s,'k'); colormap jet; caxis([0,1])
view(90,0); camlight;material dull;lighting phong;
saveas(h,'conn_cingulate3_1.png');
view(-90,0); camlight;
saveas(h,'conn_cingulate3_2.png');

