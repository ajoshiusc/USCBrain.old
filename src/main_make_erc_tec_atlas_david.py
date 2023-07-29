# %%
"""

@author: ajoshi
"""
from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs, writedfs
import time
import numpy as np
import scipy as sp
import nibabel as nib
from nilearn import image
from glob import glob
from tqdm import tqdm
from scipy.stats import mode
import time
import os
from scipy.interpolate import interpn
from surfproc import view_patch_vtk, smooth_patch, patch_color_labels, smooth_surf_function
from dfsio import writedfs, readdfs

from scipy.interpolate import griddata

# Make average label atlas

left_atlas_fname='/home/ajoshi/BrainSuite21a/svreg/USCBrain/USCBrain.left.mid.cortex.dfs'
right_atlas_fname='/home/ajoshi/BrainSuite21a/svreg/USCBrain/USCBrain.right.mid.cortex.dfs'


l = readdfs(left_atlas_fname)
r = readdfs(right_atlas_fname)
vol_lab_file = '/home/ajoshi/USCBrainMulti/EPT_Atlas/BCI-EPT.label.nii.gz'
vol_lab = nib.load(vol_lab_file)
vol_img = vol_lab.get_fdata()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]


xx = np.arange(vol_lab.shape[0])*xres
yy = np.arange(vol_lab.shape[1])*yres
zz = np.arange(vol_lab.shape[2])*zres
    
l.labels = interpn((xx, yy, zz), vol_img, l.vertices, method='nearest')
r.labels = interpn((xx, yy, zz), vol_img, r.vertices, method='nearest')

patch_color_labels(l)
patch_color_labels(r)

writedfs('/home/ajoshi/USCBrainMulti/EPT_Atlas/BCI-EPT.left.mid.cortex.dfs',l)
writedfs('/home/ajoshi/USCBrainMulti/EPT_Atlas/BCI-EPT.right.mid.cortex.dfs',r)

