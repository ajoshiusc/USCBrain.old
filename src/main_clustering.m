%% Cluster small area with tNLM
clc; clear;
addpath(genpath('C:\Users\ajoshi\Documents\coding_ground\brainreg\src'));
p_dir = 'E:\HCP-fMRI-NLM';
sub = '100307';
r_factor = 3;
ref_dir = fullfile(p_dir, 'reference');
ref = '100307';
msk = load(fullfile(ref_dir, [ref '.reduce' num2str(r_factor) '.LR_mask.mat']));

dfs_left = readdfsGz(fullfile(p_dir, 'reference', [ref '.aparc.a2009s.32k_fs.reduce3.left.dfs.gz']));
dfs_left_sm = readdfsGz(fullfile(p_dir, 'reference', [ref '.aparc.a2009s.32k_fs.reduce3.very_smooth.left.dfs.gz']));
dfs_right = readdfsGz(fullfile(p_dir, 'reference', [ref '.aparc.a2009s.32k_fs.reduce3.right.dfs.gz']));

data = load(fullfile(p_dir, sub, [sub '.rfMRI_REST1_RL.reduce3.ftdata.hvar_0.mat']));
% % 
data = load(fullfile(p_dir, sub, [sub '.rfMRI_REST1_RL.reduce3.ftdata.NLM_11N_hvar_25.mat']));


temp = data.ftdata_NLM(msk.LR_flag, :);
d=temp;
rho=corr(d');
rho(~isfinite(rho))=0;
[~,Adj]=vertices_connectivity_fast(dfs_left);
rho_mskd=rho.*((Adj>0));

patch('faces',dfs_left_sm.faces,'vertices',dfs_left_sm.vertices,'facevertexcdata',full(mean(rho_mskd,1))','facecolor','interp','edgecolor','none');view(-90,0);axis equal;axis off;camlight;material dull;
% d = temp(msk_small_region , :);
% d_corr = temp(~msk_small_region , :);
% displayTwoDFSmedial(dfs_left_sm, msk_small_region, dfs_left_sm, msk_small_region, [0 1], jet(64), 'LL', 'flat');
% clear temp
% 
% % ll = unique(dfs_left_sm.labels);
% % for k = 1:length(ll)
% %     displayTwoDFSmedial(dfs_left_sm, dfs_left_sm.labels==ll(k), dfs_left_sm, dfs_left_sm.labels==ll(k), [0 1], jet(64), 'LR', 'flat');
% %     title(num2str(ll(k)))
% % end
% 
% % make each signal mean-0 and variance-1
% m = mean(d, 2);
% d = d - m(:, ones(1, size(d, 2)));
% s = std(d, 0, 2);
% d = d./s(:, ones(1, size(d,2)));
% g_mask = ~any(isfinite(d), 2);
% d(g_mask, :) = 0;
% 
% 
% % compute correlation matrix
% rho = corr(transpose(d), transpose(d_corr));
% rho(~isfinite(rho)) = 0;
% rho_rho = corr(transpose(rho));
% 
% n_eigs = 753;
% [NcutEigenvectors, NcutEigenvalues] = ncut(rho_rho, n_eigs);
% 
% 
% n_class = [2,4,6,8,10,12,50,200];%[2 5 10 30 50 200];
% lbl = cell(length(n_class), 1);
% for n = 1:length(n_class)
%     % compute discretize Ncut vectors
%     NcutDiscrete = discretisation(NcutEigenvectors(:, 1:n_class(n)));
%     NcutDiscrete = full(NcutDiscrete);
% 
%  %   lbl{n} = kmeans(rho,n_class(n));% NcutDiscrete * transpose([1:n_class(n)]);
%     lbl{n} = NcutDiscrete * transpose([1:n_class(n)]);
% end
% 
% for n = 1:length(n_class)
%     lbl_out = dfs_left;
%     lbl_out.labels(:) = 0;
%     lbl_out.labels(msk_small_region) = lbl{n};
%     
%     h=displayTwoDFSmedial(dfs_left_sm, lbl_out.labels, dfs_left_sm, msk_small_region, [0 n_class(n)], [[1 1 1]*0.6; randCMapHue(n_class(n))], 'LL', 'flat');
%     %title(['class = ' num2str(n_class(n))])
%     saveas(h,sprintf('%s_classes%d_classes_both_hemi.png',sub,n_class(n)))
% end
% close all
% 
% 
