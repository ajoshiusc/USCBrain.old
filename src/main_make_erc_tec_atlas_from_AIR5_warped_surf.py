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

left_atlas_fname='/home/ajoshi/BrainSuite21a/svreg/USCBrain/USCBrain.left.inner.cortex.dfs'
right_atlas_fname='/home/ajoshi/BrainSuite21a/svreg/USCBrain/USCBrain.right.inner.cortex.dfs'


l = readdfs(left_atlas_fname)
r = readdfs(right_atlas_fname)
sub_list = glob('/deneb_disk/erc_tec/AIR5_warped/*_S_*')

union_label_l = np.zeros(l.vertices.shape[0])
union_label_r = np.zeros(r.vertices.shape[0])

labels = [290,291,293,294,295]

for subdir in sub_list:

    subname = os.path.basename(subdir)

    subbasename = subdir + '/' + subname + '_T1w'


    vol_lab_file = '/deneb_disk/erc_tec/AIR5_warped/'+subname+'/'+subname+'_T1w.warped.label.nii.gz'
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

    writedfs('/deneb_disk/erc_tec/mapped_labels_air5/'+subname+'.left.EPT.label.dfs',l)
    writedfs('/deneb_disk/erc_tec/mapped_labels_air5/'+subname+'.right.EPT.label.dfs',r)

    union_label_l += np.int16(l.labels > 0)
    union_label_r += np.int16(r.labels > 0)


l.attributes = union_label_l/len(sub_list)
r.attributes = union_label_r/len(sub_list)

l=smooth_patch(l,iterations=1500)
r=smooth_patch(r,iterations=1500)

writedfs('uscbrain.left.union.dfs',l)
writedfs('uscbrain.right.union.dfs',r)

l.attributes = smooth_surf_function(l,l.attributes,a1=.3,a2=.3)
r.attributes = smooth_surf_function(r,r.attributes,a1=.3,a2=.3)

writedfs('uscbrain.left.union.smoothp3.dfs',l)
writedfs('uscbrain.right.union.smoothp3.dfs',r)



l.attributes = smooth_surf_function(l,l.attributes)
r.attributes = smooth_surf_function(r,r.attributes)

writedfs('uscbrain.left.union.smooth.dfs',l)
writedfs('uscbrain.right.union.smooth.dfs',r)

l.attributes = smooth_surf_function(l,l.attributes)
r.attributes = smooth_surf_function(r,r.attributes)

writedfs('uscbrain.left.union.smooth2.dfs',l)
writedfs('uscbrain.right.union.smooth2.dfs',r)


