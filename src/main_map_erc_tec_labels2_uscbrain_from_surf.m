clc;clear all;close all;restoredefaultpath;
addpath(genpath('/home/ajoshi/projects/svreg/src'));
addpath(genpath('/home/ajoshi/projects/svreg/3rdParty'));
addpath(genpath('/home/ajoshi/projects/svreg/MEX_Files'));

BrainSuitePath = '/home/ajoshi/BrainSuite21a';
atlasbasename = fullfile(BrainSuitePath,'svreg','USCBrain','USCBrain');

%atlasbasename = fullfile(BrainSuitePath,'svreg','BrainSuiteAtlas1','mri');

sublist = dir('/deneb_disk/erc_tec/ADNI10_USCBrain_nohippo/*');

outfolder = '/deneb_disk/erc_tec/mapped_labels_nohippo';

for j = 3:length(sublist)

    sub = sublist(j).name
    
    if ~isfolder(['/deneb_disk/erc_tec/ADNI10_USCBrain/',sub])
        continue
    end
%    '002_S_1268'
    
    subbasename = ['/deneb_disk/erc_tec/ADNI10_USCBrain/',sub,'/anat/',sub,'_T1w'];    
    
    label_file = [subbasename,'-297L.label.nii.gz'];


    
    interp3()


    
    svreg_apply_map(inv_map_file,label_file,fullfile(outfolder,[sub,'.atlas.label.nii.gz']),[atlasbasename,'.bfc.nii.gz']);


end

