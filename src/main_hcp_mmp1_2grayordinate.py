# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
from scipy.io import savemat
import nibabel.freesurfer.io as fsio
from surfproc import view_patch_vtk, patch_color_labels, smooth_patch
from dfsio import writedfs, readdfs
import nibabel as nib
import os
from scipy.spatial import cKDTree
import numpy as np


class lh32k:
    pass

class rh32k:
    pass


gord_labels = np.empty(96854,dtype=np.int16) # initialize grayordinate vector
gord_labels[:] = -1 # Initialize the array with 


inputfile = '/big_disk/ajoshi/data/Glasser_et_al_2016_HCP_MMP1.0_RVVG/HCP_Phase\
Two/Q1-Q6_RelatedParcellation210/MNINonLinear/fsaverage_LR32k/Q1-Q6_Related\
Parcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii'

labs = nib.load(inputfile)
aa = labs.nifti_header.extensions[0].get_content()
idxs = aa.get_axis(1).vertex
labels = np.squeeze(labs.get_fdata())
g_surf = nib.load('/data_disk/HCP5-fMRI-NLM/reference/100307/MNINonLinear/fsaverage_LR32k/100307.L.very_inflated.32k_fs_LR.surf.gii')
lh32k.vertices = g_surf.darrays[0].data
lh32k.faces = g_surf.darrays[1].data
lh32k.labels = np.zeros(lh32k.vertices.shape[0])
lh32k.labels[idxs] = labels
lh32k = patch_color_labels(lh32k)


inputfile = '/big_disk/ajoshi/data/Glasser_et_al_2016_HCP_MMP1.0_RVVG/HCP_Phase\
Two/Q1-Q6_RelatedParcellation210/MNINonLinear/fsaverage_LR32k/Q1-Q6_Related\
Parcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii'

labs = nib.load(inputfile)
aa = labs.nifti_header.extensions[0].get_content()
idxs = aa.get_axis(1).vertex
labels = np.squeeze(labs.get_fdata())
g_surf = nib.load('/data_disk/HCP5-fMRI-NLM/reference/100307/MNINonLinear/fsaverage_LR32k/100307.R.very_inflated.32k_fs_LR.surf.gii')
rh32k.vertices = g_surf.darrays[0].data
rh32k.faces = g_surf.darrays[1].data
rh32k.labels = np.zeros(rh32k.vertices.shape[0])
rh32k.labels[idxs] = labels
rh32k = patch_color_labels(rh32k)




gord_labels[:len(lh32k.labels)]=lh32k.labels # right hemisphere labels
gord_labels[len(rh32k.labels):len(rh32k.labels)*2]=rh32k.labels # right hemisphere labels




savemat('HCP-MMP1_grayordinate_labels.mat',{'labels':gord_labels})

