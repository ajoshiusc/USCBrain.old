# %%
"""
Created on Tue Sep  6 00:08:31 2016

@author: ajoshi
"""
from dfsio import readdfs, writedfs
from nilearn import image
import scipy as sp

rois1 = [1642, 4421, 1501]
rois2 = [1641, 4422, 1503]

left_mid = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/\
/BCI-DNI_brain_atlas_refined/BCI-DNI_brain.left.mid.cortex.dfs')

right_mid = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/\
/BCI-DNI_brain_atlas_refined/BCI-DNI_brain.right.mid.cortex.dfs')

v_lab = image.load_img('/big_disk/ajoshi/coding_ground/svreg-matlab/\
BCI-DNI_brain_atlas_refined/BCI-DNI_brain.label.nii.gz')

data1 = v_lab.get_data()
data2 = data1.copy()

left_labs = left_mid.labels.copy()
right_labs = right_mid.labels.copy()

data2 = data1.copy()


for ids in range(len(rois1)):
    data2[data1 == rois1[ids]] = rois2[ids]
    data2[data1 == rois2[ids]] = rois1[ids]
    left_labs[sp.where(left_mid.labels == rois1[ids])] = rois2[ids]
    left_labs[sp.where(left_mid.labels == rois2[ids])] = rois1[ids]
    right_labs[sp.where(right_mid.labels == rois1[ids])] = rois2[ids]
    right_labs[sp.where(right_mid.labels == rois2[ids])] = rois1[ids]

vm = image.new_img_like(v_lab, data2)
vm.to_filename('/big_disk/ajoshi/coding_ground/svreg-matlab/\
BCI-DNI_brain_atlas_refined/BCI-DNI_brain.label.corr.nii.gz')

left_mid.labels = left_labs
right_mid.labels = right_labs

writedfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas_\
refined/BCI-DNI_brain.left.mid.cortex.corr.dfs', left_mid)
writedfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas_\
refined/BCI-DNI_brain.right.mid.cortex.corr.dfs', right_mid)

left_inner = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/\
/BCI-DNI_brain_atlas_refined/BCI-DNI_brain.left.inner.cortex.dfs')
left_inner.labels = left_labs
writedfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas_\
refined/BCI-DNI_brain.left.inner.cortex.corr.dfs', left_inner)

left_pial = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/\
/BCI-DNI_brain_atlas_refined/BCI-DNI_brain.left.pial.cortex.dfs')
left_pial.labels = left_labs
writedfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas_\
refined/BCI-DNI_brain.left.pial.cortex.corr.dfs', left_pial)

right_inner = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/\
/BCI-DNI_brain_atlas_refined/BCI-DNI_brain.right.inner.cortex.dfs')
right_inner.labels = right_labs
writedfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas_\
refined/BCI-DNI_brain.right.inner.cortex.corr.dfs', right_inner)

right_pial = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/\
/BCI-DNI_brain_atlas_refined/BCI-DNI_brain.right.pial.cortex.dfs')
right_pial.labels = right_labs
writedfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI_brain_atlas_\
refined/BCI-DNI_brain.right.pial.cortex.corr.dfs', right_pial)
