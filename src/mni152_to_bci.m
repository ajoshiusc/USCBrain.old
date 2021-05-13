%clc;clear all;close all;restoredefaultpath;

%addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/src'));
%addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/3rdParty'));
%addpath(genpath('/ImagePTE1/ajoshi/code_farm/svreg/MEX_Files'));
function mni152_to_bci(atlas_name)
% left hemi
sub_label = readdfs(['MNI152-',atlas_name,'.left.mid.cortex.dfs']);
sub = readdfs('/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.left.mid.cortex.svreg.dfs');
tar = readdfs('/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/atlas.left.mid.cortex.svreg.dfs');
sub.labels = sub_label.labels;

tar.labels=map_data_flatmap(sub,sub.labels,tar,'nearest',[]);

outfile = ['BCI-',atlas_name,'.left.mid.cortex.dfs'];
writedfs(outfile,tar);
recolor_by_label(outfile,[],[]);

% right hemi
sub_label = readdfs(['MNI152-',atlas_name,'.right.mid.cortex.dfs']);
sub = readdfs('/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.right.mid.cortex.svreg.dfs');
tar = readdfs('/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/atlas.right.mid.cortex.svreg.dfs');
sub.labels = sub_label.labels;

tar.labels=map_data_flatmap(sub,sub.labels,tar,'nearest',[]);

outfile = ['BCI-',atlas_name,'.right.mid.cortex.dfs'];
writedfs(outfile,tar);
recolor_by_label(outfile,[],[]);


  