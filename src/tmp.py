# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
import nibabel.freesurfer.io as fsio
from numpy.lib.function_base import interp
from surfproc import view_patch_vtk, smooth_patch, patch_color_labels
from dfsio import writedfs, readdfs
from nibabel.gifti.giftiio import read as gread
import os
from scipy.spatial import cKDTree
import nibabel as nib
from lxml import etree
import numpy as np
from nilearn import image
from scipy.interpolate import interpn


MNIVol = '/ImagePTE1/ajoshi/brain_development_atlases/Hammers_mith-n30r95-maxprob-MNI152-SPM12/Hammers_mith-n30r95-MaxProbMap-full-MNI152-SPM12.nii.gz'

hammervol = image.resample_to_img(
    MNIVol, '/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.svreg.label.nii.gz', interpolation='nearest')
hammervol.set_data_dtype('int16')    
hammervol.to_filename('hammer.nii.gz')
MNIVol = 'hammer.nii.gz'


BrainSuitePath = '/home/ajoshi/BrainSuite19b'



lmid = '/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.left.inner.cortex.svreg.dfs'
rmid = '/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.right.inner.cortex.svreg.dfs'



vol_lab = image.load_img(MNIVol)

vol_img = vol_lab.get_fdata()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]

sl = readdfs(lmid)
sr = readdfs(rmid)

xx = np.arange(vol_lab.shape[0])*xres
yy = np.arange(vol_lab.shape[1])*yres
zz = np.arange(vol_lab.shape[2])*zres

sl.labels = interpn((xx, yy, zz), vol_img, sl.vertices, method='nearest')
sr.labels = interpn((xx, yy, zz), vol_img, sr.vertices, method='nearest')

sl = smooth_patch(sl, iterations=3000, relaxation=.5)
sr = smooth_patch(sr, iterations=3000, relaxation=.5)

patch_color_labels(sl)
view_patch_vtk(sl)
patch_color_labels(sr)
view_patch_vtk(sr)
