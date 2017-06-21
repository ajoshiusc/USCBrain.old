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
import matlab.engine as meng

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


class s:
    pass


class bci:
    pass

subbasename = '/big_disk/ajoshi/fs_dir/co20050723_\
090747MPRAGET1Coronals002a001'
USCBrainpath = '/big_disk/ajoshi/coding_ground/svreg/USCBrain'
#'/big_disk/ajoshi/fs_sub/co20050723_110235Flash3Dt1CORONALs002a001'
hemi = 'right'
fshemi = 'rh'

for hi in range(2):
    if hi == 0:
        hemi = 'right'
        fshemi = 'rh'
    else:
        hemi = 'left'
        fshemi = 'lh'

    ''' USCBrain to FS processed BCI '''
    bci_bsti = readdfs(USCBrainpath +
                       '/BCI-DNI_brain.' + hemi + '.mid.cortex.dfs')
    bci_bst = readdfs(USCBrainpath + '/BCI-DNI_brain.' +
                      hemi + '.inner.cortex.dfs')
    bci_bst.labels = bci_bsti.labels
    bci_bst.vertices[:, 0] -= 96*0.8
    bci_bst.vertices[:, 1] -= 192*0.546875
    bci_bst.vertices[:, 2] -= 192*0.546875
    bci.vertices, bci.faces = fsio.read_geometry('/big_disk/ajoshi/data/BCI_\
DNI_Atlas/surf/' + fshemi + '.white')
    bci = interpolate_labels(bci_bst, bci)

    ''' FS_BCI to FS BCI Sphere'''
    bci.vertices, bci.faces = fsio.read_geometry('/big_disk/ajoshi/data/BCI_\
DNI_Atlas/surf/' + fshemi + '.sphere.reg')

    ''' FS BCI Sphere to SUB FS Sphere'''

    s.vertices, s.faces = fsio.read_geometry(subbasename +
                                             '/surf/' + fshemi + '.sphere.reg')
    s = interpolate_labels(bci, s)
    fslabels, _, _ = fsio.read_annot(subbasename +
                                     '/label/' + fshemi + '.aparc.annot')
    s.labels = s.labels * sp.int16(fslabels > 0)
    s.vertices, _ = fsio.read_geometry(subbasename + '/surf/' +
                                       fshemi + '.pial')
    so, _ = fsio.read_geometry(subbasename + '/surf/' + fshemi + '.white')
    s.vertices = (s.vertices + so)/2.0
#    view_patch_vtk(s)
    s.faces = s.faces[:, (0, 2, 1)]
    writedfs(subbasename + '/' + hemi + '.mid.dfs', s)
    eng = meng.start_matlab()
    eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/MEX_Files'))
    eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/3rdParty'))
    eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/src'))
    xmlf = USCBrainpath + '/brainsuite_\
labeldescription.xml'
    eng.recolor_by_label(subbasename + '/' + hemi + '.mid.dfs',
                         '', xmlf, nargout=0)
