clc;clear all;close all;
load('C:\Users\ajoshi\Downloads\intensity_file_temporal_8.mat');

% for jj=[1,3]
%     figure;patch('faces',faces+1,'vertices',vertices,'facevertexcdata',labels(jj,:)','facecolor','interp','edgecolor','none');material dull;view(90,0);axis equal;camlight;
%      pause(.5);hold on;
%      cent=corr_vec(1+3*(jj-1):3+3*(jj-1),:);
%      mysphere(cent,1,'r');
%      [~,ia,ib1]=intersect(cent(1,:),vertices,'rows');labels(jj,ib1)
%      [~,ia,ib2]=intersect(cent(2,:),vertices,'rows');labels(jj,ib2)
%      [~,ia,ib3]=intersect(cent(3,:),vertices,'rows');labels(jj,ib3)
%     
% end



figure;patch('faces',faces+1,'vertices',vertices,'facevertexcdata',mode(labels)','facecolor','interp','edgecolor','none');material dull;view(90,0);axis equal;camlight;

label_vert=mode(labels)';

freq=sum(labels'==repmat(label_vert,1,40),2)/40;
freq=max(0,(freq-0.33)/0.66);

colr=1-[freq.*(label_vert~=1),freq.*(label_vert~=2),freq.*(label_vert~=3)].*[(label_vert~=0),(label_vert~=0),(label_vert~=0)];

figure;patch('faces',faces+1,'vertices',vertices,'facevertexcdata',min(max(0,colr),1),'facecolor','interp','edgecolor','none');view(90,0);axis equal;material dull;camlight;

figure;patch('faces',faces+1,'vertices',vertices,'facevertexcdata',freq.*(freq<1.2),'facecolor','interp','edgecolor','none');view(90,0);axis equal;material dull;camlight;

