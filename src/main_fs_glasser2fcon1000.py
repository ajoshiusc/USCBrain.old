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
import itertools
import glob
from tqdm import tqdm

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


# These commands need to be in .bashrc
#cmd1 = 'export FREESURFER_HOME=/big_disk/ajoshi/freesurfer'
#cmd2 = 'source /big_disk/ajoshi/freesurfer/SetUpFreeSurfer.sh'
#

subslist = glob.glob('/big_disk/ajoshi/freesurfer/subjects/sub*')


for s in tqdm(subslist):
    a, subname = os.path.split(s)

    for hemi in {'left', 'right'}:
        if hemi == 'left':
            fshemi = 'lh'
        else:
            fshemi = 'rh'

        cmd3 = 'mri_surf2surf --hemi ' + fshemi + ' --srcsubject fsaverage --trgsubject ' + subname + ' --sval-annot /big_disk/ajoshi/data/HCP_MMP1.0_fsaverage/3498446/' + \
            str(fshemi)+'.HCP-MMP1.annot --tval /big_disk/ajoshi/freesurfer/subjects/' + \
            subname+'/label/' + str(fshemi)+'.HCP-MMP1.annot'
        os.system(cmd3)
