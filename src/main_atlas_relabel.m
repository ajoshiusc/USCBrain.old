clc;clear all;close all;
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/src'))
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/3rdParty'))

out_atlas='/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_atlas_refined_4_12_2017/BCI-DNI_brain';
out_atlas_dir=fileparts(out_atlas);
in_atlas='/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_atlas_refined_4_11_2017/BCI-DNI_brain';
in_atlas_dir=fileparts(in_atlas);

vin=load_nii_BIG_Lab([in_atlas,'.label.nii.gz']);
aa=load('/big_disk/ajoshi/coding_ground/hbci_atlas/relabel_lut_aaj.txt');
vout=vin;

for jj=1:length(aa)
    vout.img(vin.img==aa(jj,1))=aa(jj,2);
end

%== Soyoungs edits based on figures_compile.pptx
% Swap 126 and 124 (superior and inferior branches of pars opercularis)
roi1=vout.img==124; roi2=vout.img==126;
vout.img(roi1)=126;vout.img(roi2)=124;

% Swap 338 and 340 (superior and inferior branches of pars opercularis)
roi1=vout.img==338; roi2=vout.img==340;
vout.img(roi1)=340;vout.img(roi2)=338;

% Gyrus rectus: Silhoutte scores look good but very tiny ROI on the left
% hemisphere, therefore merged the two subdivisions
roi=vout.img==160 | vout.img==162; vout.img(roi)=158;
roi=vout.img==161 | vout.img==163; vout.img(roi)=159;


save_untouch_nii_gz(vout, [out_atlas,'.label.nii.gz']);
copyfile('../brainsuite_labels_func_v1.xml',[out_atlas_dir,'/brainsuite_labeldescription.xml']);

%== ',hemi,' Hemisphere
for hemi1={'left','right'}
    hemi=hemi1{1};
    inlmid = [in_atlas,'.',hemi,'.mid.cortex.dfs'];
    sin=readdfs(inlmid);sout=sin;
    for jj=1:length(aa)
        sout.labels(sin.labels==aa(jj,1))=aa(jj,2);
    end

    %== Soyoungs edits based on figures_compile.pptx
    % Swap 126 and 124 (superior and inferior branches of pars opercularis)
    roi1=sout.labels==124; roi2=sout.labels==126;
    sout.labels(roi1)=126;sout.labels(roi2)=124;

    % Swap 338 and 340 (superior and inferior branches of pars opercularis)
    roi1=sout.labels==338; roi2=sout.labels==340;
    sout.labels(roi1)=340;sout.labels(roi2)=338;

    % Gyrus rectus: Silhoutte scores look good but very tiny ROI on the left
    % hemisphere, therefore merged the two subdivisions
    roi=sout.labels==160 | sout.labels==162; sout.labels(roi)=158;
    roi=sout.labels==161 | sout.labels==163; sout.labels(roi)=159;


    sout = rmfield(sout, 'vcolor');
    sout = rmfield(sout, 'attributes');
    outlmid = [out_atlas,'.',hemi,'.mid.cortex.dfs'];
    writedfs(outlmid,sout);

    xmlf=[out_atlas_dir,'/brainsuite_labeldescription.xml'];
    recolor_by_label(outlmid, out_atlas, xmlf);
    sout=readdfs(outlmid);

    inlin = [in_atlas,'.',hemi,'.inner.cortex.dfs'];
    sin=readdfs(inlin);souti=sin;
    souti.vcolor= sout.vcolor;
    souti.labels= sout.labels;
    writedfs([out_atlas,'.',hemi,'.inner.cortex.dfs'],souti);

    inlpial = [in_atlas,'.',hemi,'.pial.cortex.dfs'];
    sin = readdfs(inlin); soutp = sin;  % There is a bug here reading inner surface!!
    soutp.vcolor = sout.vcolor;
    soutp.labels = sout.labels;
    outlin = [out_atlas,'.',hemi,'.pial.cortex.dfs'];
    writedfs([out_atlas,'.',hemi,'.pial.cortex.dfs'],soutp);
end

%====================


