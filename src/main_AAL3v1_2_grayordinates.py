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


MNIVol = '/ImagePTE1/ajoshi/code_farm/hybridatlas/AAL3v1/AAL3v1_1mm.nii.gz'
BrainSuitePath = '/home/ajoshi/BrainSuite21a'

#labelhdr = '/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.svreg.label.nii.gz'
#labelhdr = '/ImagePTE1/ajoshi/code_farm/svreg/BrainSuiteAtlas1/mri.dws.label.nii.gz'

outvol = 'ICBM152-AAL3v1.label.nii.gz'
outmidl = 'ICBM152-AAL3v1.left.mid.cortex.dfs'
outmidr = 'ICBM152-AAL3v1.right.mid.cortex.dfs'


#lmid = '/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.left.mid.cortex.svreg.dfs'
#rmid = '/ImagePTE1/ajoshi/code_farm/icbm152/mni_icbm152_nlin_asym_09c/icbm152_t1.right.mid.cortex.svreg.dfs'

lmid = '/ImagePTE1/ajoshi/mni_colin27_1998/mni_colin27_BST/colin27_t1_tal_lin.left.mid.cortex.svreg.dfs'
rmid = '/ImagePTE1/ajoshi/mni_colin27_1998/mni_colin27_BST/colin27_t1_tal_lin.right.mid.cortex.svreg.dfs'


vol_lab = image.load_img(MNIVol)
vol_lab = image.new_img_like(vol_lab, np.int16(vol_lab.get_fdata()))
vol_lab.to_filename(outvol)

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

#sl = smooth_patch(sl, iterations=3000, relaxation=.5)
#sr = smooth_patch(sr, iterations=3000, relaxation=.5)

patch_color_labels(sl)
view_patch_vtk(sl)
patch_color_labels(sr)
view_patch_vtk(sr)
writedfs(outmidl, sl)
writedfs(outmidr, sr)
