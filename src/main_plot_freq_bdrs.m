clc;clear all;close all;restoredefaultpath;
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/3rdParty'));
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/MEX_Files'));
addpath(genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/src'));

s = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI_brain_atlas_refined_4_18_2017/BCI-DNI_brain.left.mid.cortex.mod.dfs');
s = smooth_cortex_fast(s,.5,3000);
so = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs');
s.labels=so.labels;
h=figure
patch('faces',s.faces,'vertices',s.vertices,'facevertexcdata',s.attributes,'edgecolor','none','facecolor','interp','BackFaceLighting','unlit');
axis equal; axis off; material dull; view(90,0); camlight;colormap gray;caxis([0,1]);

tri_lab = s.labels(s.faces);
flg=max(tri_lab,[],2) == min(tri_lab,[],2);
 hold on;
for jj=1:length(tri_lab)
    if length(unique(tri_lab(jj,:))) ==2
        
       ind = find(tri_lab(jj,:) == mode(tri_lab(jj,:)));
       ind2 = setdiff([1,2,3],ind);
       v1=s.vertices(s.faces(jj, ind(1)),:);
       v2=s.vertices(s.faces(jj, ind2),:);
       VV1=(v1+v2)/2;
       
       v1=s.vertices(s.faces(jj, ind(2)),:);
       v2=s.vertices(s.faces(jj, ind2),:);
       VV2=(v1+v2)/2;
       VV=[VV1;VV2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       

    end
    
    if length(unique(tri_lab(jj,:))) ==3
        
       v1=s.vertices(s.faces(jj, 1),:);
       v2=s.vertices(s.faces(jj, 2),:);
       v3=s.vertices(s.faces(jj, 3),:);
       m=(v1+v2+v3)/3;
       
       VV=[m;(v1+v2)/2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       
       VV=[m;(v2+v3)/2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       
       VV=[m;(v1+v3)/2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       

    end        
    
end
%zoom(3);
%set (h, 'Units', 'normalized', 'Position', [0,0,1,1]);
saveas(h,'left_freq1_2.pdf');
saveas(h,'left_freq1_2.png');
view(-90,0);camlight;
saveas(h,'left_freq2_2.pdf');
saveas(h,'left_freq2_2.png');
