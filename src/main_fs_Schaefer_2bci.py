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
for hemi in {'left', 'right'}:
    if hemi == 'left':
        fshemi = 'lh'
    else:
        fshemi = 'rh'

    bci_bsti = readdfs(
        '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.' + hemi + '.inner.cortex.dfs')
    bci_bst_mid = readdfs(
        '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.' + hemi + '.mid.cortex.dfs')

    bci_bsti.vertices[:, 0] -= 96*0.8
    bci_bsti.vertices[:, 1] -= 192*0.546875
    bci_bsti.vertices[:, 2] -= 192*0.546875
    bci.vertices, bci.faces = fsio.read_geometry(
        '/big_disk/ajoshi/data/BCI_DNI_Atlas/surf/' + fshemi + '.white')
    # view_patch_vtk(bci)

    bci_bst_mid_sm = smooth_patch(bci_bst_mid, iterations=3000, relaxation=.5)

    for parcels, nets in itertools.product([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], [7, 17]):
        cmd3 = 'mri_surf2surf --hemi ' + fshemi + ' --srcsubject fsaverage --trgsubject BCI_DNI_Atlas --sval-annot /ImagePTE1/ajoshi/code_farm/hybridatlas/Schaefer2018/FreeSurfer5.3/fsaverage/label/' + fshemi + '.Schaefer2018_' + \
            str(parcels)+'Parcels_'+str(nets)+'Networks_order.annot --tval /big_disk/ajoshi/freesurfer/subjects/BCI_DNI_Atlas/label/' + \
            str(fshemi)+'.Schaefer2018_'+str(parcels) + \
            'Parcels_' + str(nets) + 'Networks_order.annot'
        #os.system(cmd1 + ';' + cmd2 + ';' + cmd3)
        os.system(cmd3)
        outfile = 'BCI-DNI_Schaefer2018_' + \
            str(parcels)+'Parcels_'+str(nets) + \
            'Networks' + '.' + hemi + '.mid.cortex.dfs'

        ''' BCI to FS processed BCI '''
        bci.labels = np.zeros(bci.vertices.shape[0])
        fslabels, label1, colortable1 = fsio.read_annot('/big_disk/ajoshi/freesurfer/subjects/BCI_DNI_Atlas/label/'+str(
            fshemi)+'.Schaefer2018_'+str(parcels)+'Parcels_' + str(nets) + 'Networks_order.annot')
        fslabels[fslabels < 0] = 0

        bci.labels = fslabels
        bci = patch_color_labels(bci)

        bci_bsti = interpolate_labels(bci, bci_bsti)
        bci_bst_mid.labels = bci_bsti.labels
        bci_bst_mid_sm.labels = bci_bst_mid.labels
        bci_bst_labels = patch_color_labels(bci_bst_mid_sm)
        #view_patch_vtk(bci_bst_labels)
        writedfs(outfile, bci_bst_labels)
