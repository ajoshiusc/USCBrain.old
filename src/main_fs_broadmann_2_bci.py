# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
import nibabel.freesurfer.io as fsio
from surfproc import view_patch
from dfsio import writedfs, readdfs
from nibabel.gifti.giftiio import read as gread
import os
from scipy.spatial import cKDTree
from surfproc import view_patch_vtk, patch_color_labels
import scipy as sp

p_dir_ref = '/big_disk/ajoshi/HCP_data'
ref_dir = os.path.join(p_dir_ref, 'reference')
ref = '100307'


def interpolate_labels(fromsurf=[], tosurf=[], skipzero=0):
    ''' interpolate labels from surface to to surface'''
    tree = cKDTree(fromsurf.vertices)
    d, inds = tree.query(tosurf.vertices, k=1, p=2)
    if skipzero == 0:
        tosurf.labels = fromsurf.labels[inds]
    else:
        indz = (tosurf.labels == 0)
        tosurf.labels = fromsurf.labels[inds]
        tosurf.labels[indz] = 0
    return tosurf


class bci:
    pass

subbasename = '/big_disk/ajoshi/fs_dir/co20050723_090747MPRAGET1\
Coronals002a001'
broadmann = ["BA1", "BA2", "BA3a", "BA3b", "BA4a", "BA4p", "BA6", "BA44",
             "BA45", "V1", "V2", "MT"]
#'/big_disk/ajoshi/fs_sub/co20050723_110235Flash3Dt1CORONALs002a001'
hemi = 'left'
fshemi = 'lh'

''' BCI to FS processed BCI '''
bci_bsti = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI\
_brain_atlas_refined/BCI-DNI_brain.' + hemi + '.mid.cortex.dfs')
bci_bst = readdfs('/big_disk/ajoshi/coding_ground/svreg-matlab/BCI-DNI\
_brain_atlas_refined/BCI-DNI_brain.' + hemi + '.inner.cortex.dfs')
bci_bst.vertices[:, 0] -= 96*0.8
bci_bst.vertices[:, 1] -= 192*0.546875
bci_bst.vertices[:, 2] -= 192*0.546875
bci.vertices, bci.faces = fsio.read_geometry('/big_disk/ajoshi/data/BCI_\
DNI_Atlas/surf/' + fshemi + '.white')
bci.labels = sp.zeros(bci.vertices.shape[0])
for i in range(len(broadmann)):
    labind = fsio.read_label('/big_disk/ajoshi/data/BCI_DNI_Atlas/label/' +
                             fshemi + '.' + broadmann[i] + '.thresh.label')
    bci.labels[labind] = i+1

bci_bst = interpolate_labels(bci, bci_bst)
s = bci_bst
s = patch_color_labels(s)
view_patch_vtk(s)
