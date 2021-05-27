# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:51:16 2016

@author: ajoshi
"""
from scipy.io import savemat
import nibabel.freesurfer.io as fsio
from surfproc import view_patch_vtk, patch_color_labels, smooth_patch
from dfsio import writedfs, readdfs
import nibabel as nib
import os
from scipy.spatial import cKDTree
import numpy as np

p_dir_ref='/home/ajoshi/HCP_data'
ref_dir = os.path.join(p_dir_ref, 'reference')
outbasename = 'Yeo2011_17Networks'



def interpolate_labels(fromsurf=[], tosurf=[]):
    ''' interpolate labels from surface to to surface'''
    tree = cKDTree(fromsurf.vertices)
    d, inds = tree.query(tosurf.vertices, k=1, p=2)
    tosurf.labels = fromsurf.labels[inds]
    return tosurf


inputfile_R='/big_disk/ajoshi/freesurfer/subjects/fsaverage/label/rh.Yeo2011_17Networks_N1000.annot'
fsAve_sph_R='/big_disk/ajoshi/freesurfer/subjects/fsaverage/surf/rh.sphere.reg.avg'
fsAve_sph_32k_R='/big_disk/ajoshi/data/standard_mesh_atlases/resample_fsaverage/fs_LR-deformed_to-fsaverage.R.sphere.32k_fs_LR.surf.gii'
fsAve_32k_R ='/data_disk/HCP_data/reference.old/100307/MNINonLinear/fsaverage_LR32k/100307.R.inflated.32k_fs_LR.surf.gii'

inputfile_L='/big_disk/ajoshi/freesurfer/subjects/fsaverage/label/lh.Yeo2011_17Networks_N1000.annot'
fsAve_sph_L='/big_disk/ajoshi/freesurfer/subjects/fsaverage/surf/lh.sphere.reg.avg'
fsAve_sph_32k_L='/big_disk/ajoshi/data/standard_mesh_atlases/resample_fsaverage/fs_LR-deformed_to-fsaverage.L.sphere.32k_fs_LR.surf.gii'
fsAve_32k_L ='/ImagePTE1/ajoshi/BrainnetomeAtlas/BN_Atlas_freesurfer/fsaverage/32k/fsaverage.L.inflated.32k_fs_LR.surf.gii'

gord_labels = np.zeros(96854) # initialize grayordinate vector

class lh_sph:
    pass
class rh_sph:
    pass
class lh:
    pass
class rh:
    pass
class lh32k:
    pass
class rh32k:
    pass


# Process left hemisphere
yeomapL,_,_=fsio.read_annot(inputfile_L)
vert, faces = fsio.read_geometry(fsAve_sph_L)
gL = nib.load(fsAve_sph_32k_L)
vert32k = gL.darrays[0].data 
faces32k = gL.darrays[1].data
lh_sph.vertices = vert; lh_sph.faces = faces; lh_sph.labels = yeomapL
lh32k.vertices = vert32k
lh32k.faces = faces32k
lh32k = interpolate_labels(lh_sph, lh32k)
gL = nib.load(fsAve_32k_L)
lh32k.vertices = gL.darrays[0].data
lh32k.faces = gL.darrays[1].data
lh32k = patch_color_labels(lh32k)
view_patch_vtk(lh32k)

# process right hemisphere
yeomapR,_,_=fsio.read_annot(inputfile_R)
vert, faces = fsio.read_geometry(fsAve_sph_R)
gR = nib.load(fsAve_sph_32k_R)
vert32k = gR.darrays[0].data 
faces32k = gR.darrays[1].data
rh_sph.vertices = vert; rh_sph.faces = faces; rh_sph.labels = yeomapR
rh32k.vertices = vert32k
rh32k.faces = faces32k
rh32k = interpolate_labels(rh_sph, rh32k)
gR = nib.load(fsAve_32k_R)
rh32k.vertices = gR.darrays[0].data
rh32k.faces = gR.darrays[1].data
rh32k = patch_color_labels(rh32k)
view_patch_vtk(rh32k)


gord_labels[:len(lh32k.labels)]=lh32k.labels # right hemisphere labels
gord_labels[len(rh32k.labels):len(rh32k.labels)*2]=rh32k.labels # right hemisphere labels

savemat('Yeo2011_17Networks_N1000_grayordinate_labels.mat',{'labels':gord_labels})

