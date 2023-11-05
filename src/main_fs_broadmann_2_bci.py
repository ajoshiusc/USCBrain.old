# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
import nibabel.freesurfer.io as fsio
from surfproc import smooth_patch, view_patch
from dfsio import writedfs, readdfs
from nibabel.gifti.giftiio import read as gread
import os
from scipy.spatial import cKDTree
from surfproc import view_patch_vtk, patch_color_labels
import numpy as np


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


broadmann = ["BA1", "BA2", "BA3a", "BA3b", "BA4a",
             "BA4p", "BA6", "BA44", "BA45", "V1", "V2", "MT"]
hemi = 'left'
fshemi = 'lh'

for hemi in {'left', 'right'}:
    if hemi == 'left':
        fshemi = 'lh'
    else:
        fshemi = 'rh'

    outfile = 'BCI-DNI_Broadmann' + '.' + hemi + '.mid.cortex.dfs'

    ''' BCI to FS processed BCI '''
    bci_bsti = readdfs(
        '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.' + hemi + '.mid.cortex.dfs')
    bci_bst = readdfs(
        '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.' + hemi + '.inner.cortex.dfs')
    bci_bst_mid = readdfs(
        '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.' + hemi + '.inner.cortex.dfs')

    bci_bst.vertices[:, 0] -= 96*0.8
    bci_bst.vertices[:, 1] -= 192*0.546875
    bci_bst.vertices[:, 2] -= 192*0.546875
    bci.vertices, bci.faces = fsio.read_geometry(
        '/big_disk/ajoshi/data/BCI_DNI_Atlas/surf/' + fshemi + '.white')
    bci.labels = np.zeros(bci.vertices.shape[0])
    for i in range(len(broadmann)):
        labind = fsio.read_label('/big_disk/ajoshi/data/BCI_DNI_Atlas/label/' +
                                 fshemi + '.' + broadmann[i] + '.thresh.label')
        bci.labels[labind] = i+1

    bci_bst = interpolate_labels(bci, bci_bst)
    bci_bst_mid.labels = bci_bst.labels
    #bci_bst_mid = smooth_patch(bci_bst_mid, 6000)
    bci_bst_labels = patch_color_labels(bci_bst_mid)
    view_patch_vtk(bci_bst_labels)
    writedfs(outfile, bci_bst_labels)
