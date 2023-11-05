# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
import nibabel.freesurfer.io as fsio
from numpy.lib.function_base import interp
from surfproc import view_patch_vtk, smooth_patch, patch_color_labels
from dfsio import writedfs, readdfs
import os
from scipy.spatial import cKDTree
import nibabel as nib
from lxml import etree
import numpy as np
from nilearn import image
from scipy.interpolate import interpn


MNIVol = '/ImagePTE1/ajoshi/code_farm/hybridatlas/ArterialAtlas/ArterialAtlas/Atlas/ArterialAtlas.nii.gz'
BrainSuitePath = '/home/ajoshi/BrainSuite21a'

applymap_exe = os.path.join(BrainSuitePath, 'svreg',
                            'bin', 'svreg_apply_map.sh')
map = os.path.join(BrainSuitePath, 'svreg',
                   'BCI-DNI_brain_atlas', 'map2mni.nii.gz')
labelhdr = os.path.join(BrainSuitePath, 'svreg',
                        'BCI-DNI_brain_atlas', 'BCI-DNI_brain.label.nii.gz')
outvol = 'BCI-Arterial.label.nii.gz'
outmidl = 'BCI-Arterial.left.mid.cortex.dfs'
outmidr = 'BCI-Arterial.right.mid.cortex.dfs'


lmid = os.path.join(BrainSuitePath, 'svreg',
                    'BCI-DNI_brain_atlas', 'BCI-DNI_brain.left.mid.cortex.dfs')
rmid = os.path.join(BrainSuitePath, 'svreg',
                    'BCI-DNI_brain_atlas', 'BCI-DNI_brain.right.mid.cortex.dfs')

cmd1 = applymap_exe + ' ' + map + ' ' + MNIVol + ' ' + outvol + ' '+labelhdr

print(cmd1)

os.system(cmd1)


vol_lab = image.load_img(outvol)
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

sl.labels[(sl.labels>=27) & (sl.labels <=30)] = 0
sr.labels[(sr.labels>=27) & (sr.labels <=30)] = 0

#sl.labels[(sl.labels>=7) & (sl.labels <=8)] = 0
#sr.labels[(sr.labels>=7) & (sr.labels <=8)] = 0

#sl = smooth_patch(sl, iterations=3000, relaxation=.5)
#sr = smooth_patch(sr, iterations=3000, relaxation=.5)

patch_color_labels(sl)
view_patch_vtk(sl)
patch_color_labels(sr)
view_patch_vtk(sr)
writedfs(outmidl, sl)
writedfs(outmidr, sr)
