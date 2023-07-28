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
from surfproc import view_patch_vtk, smooth_patch, patch_color_labels
from dfsio import writedfs, readdfs

from scipy.interpolate import griddata

# Make average label atlas




#||AUM||
#||Shree Ganeshaya Namaha||

sub_list = glob('/deneb_disk/erc_tec/ADNI10_USCBrain/*_S_*')

for subdir in sub_list:

    subname = os.path.basename(subdir)

    subbasename = subdir + '/anat/' + subname + '_T1w'

    left_mid_fname = subbasename + '.left.inner.cortex.svreg.dfs'
    left_mid_atlas_fname = subdir + '/anat/atlas.left.mid.cortex.svreg.dfs'
    print(subname)

    print(left_mid_atlas_fname)

    l_atlas = readdfs(left_mid_atlas_fname)

    vol_lab_file = '/deneb_disk/erc_tec/ADNI10_hdr_corr/ADNI10_new/' + subname +'/anat/' + subname +'.EPT.label.nii.gz' #subbasename + '-297L.label.nii.gz'
    vol_lab = nib.load(vol_lab_file)
    vol_img = vol_lab.get_fdata()

    xres = vol_lab.header['pixdim'][1]
    yres = vol_lab.header['pixdim'][2]
    zres = vol_lab.header['pixdim'][3]

    l = readdfs(left_mid_fname)



    xx = np.arange(vol_lab.shape[0])*xres
    yy = np.arange(vol_lab.shape[1])*yres
    zz = np.arange(vol_lab.shape[2])*zres
    l.labels = interpn((xx, yy, zz), vol_img, l.vertices, method='nearest')


    patch_color_labels(l)
   # view_patch_vtk(l)
    writedfs('/deneb_disk/erc_tec/mapped_labels_nohippo_hdr_corr/'+subname+'.left.EPT.label.dfs',l)



    l_atlas.labels = griddata((l.u,l.v),l.labels,(l_atlas.u,l_atlas.v),'nearest')

    patch_color_labels(l_atlas)
    #view_patch_vtk(l_atlas)

    writedfs('/deneb_disk/erc_tec/mapped_labels_nohippo_hdr_corr/'+subname+'.left.USCBrain.EPT.label.dfs',l_atlas)




