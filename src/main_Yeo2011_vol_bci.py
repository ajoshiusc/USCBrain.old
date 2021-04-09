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

subbasename = 'Yeo2011_17Networks'
bcibase = '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain'

left_mid = readdfs(bcibase + '.left.mid.cortex.dfs')
right_mid = readdfs(bcibase + '.right.mid.cortex.dfs')
left_inner = readdfs(bcibase + '.left.inner.cortex.dfs')
right_inner = readdfs(bcibase + '.right.inner.cortex.dfs')
left_pial = readdfs(bcibase + '.left.pial.cortex.dfs')
right_pial = readdfs(bcibase + '.right.pial.cortex.dfs')
left_lab = readdfs(subbasename + '.left.mid.cortex.dfs')
right_lab = readdfs(subbasename + '.right.mid.cortex.dfs')


r1_vert = (right_pial.vertices + right_mid.vertices)/2.0
r2_vert = (right_inner.vertices + right_mid.vertices)/2.0
l1_vert = (left_pial.vertices + left_mid.vertices)/2.0
l2_vert = (left_inner.vertices + left_mid.vertices)/2.0

vol_lab = image.load_img(
    '/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.dws.label.nii.gz')
vol_img = vol_lab.get_fdata()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]

X, Y, Z = np.meshgrid(np.arange(vol_lab.shape[0]), np.arange(vol_lab.shape[1]),
                      np.arange(vol_lab.shape[2]), indexing='ij')

X = X*xres
Y = Y*yres
Z = Z*zres
#vol_img = sp.mod(vol_img, 1000)
# (np.floor((vol_img/10)) == 150) | (np.floor((vol_img/10)) == 151)
ind = (vol_img >= 1000) & (vol_img != 2000)
Xc = X[ind]
Yc = Y[ind]
Zc = Z[ind]
v_lab = vol_img[ind]


class t:
    pass


class f:
    pass


t.vertices = np.concatenate((Xc[:, None], Yc[:, None], Zc[:, None]), axis=1)
f.vertices = np.concatenate((left_mid.vertices, right_mid.vertices,
                             left_inner.vertices, right_inner.vertices,
                             left_pial.vertices, right_pial.vertices,
                             l1_vert, r1_vert, l2_vert, r2_vert))

f.labels = np.concatenate((left_lab.labels, right_lab.labels,
                           left_lab.labels, right_lab.labels,
                           left_lab.labels, right_lab.labels,
                           left_lab.labels, right_lab.labels,
                           left_lab.labels, right_lab.labels))

t = interpolate_labels(fromsurf=f, tosurf=t)

# here make sure that hanns labels are not modified TBD
vol_img = vol_img * 0
vol_img[ind] = t.labels

new_img = image.new_img_like(vol_lab, vol_img)
new_img.to_filename(subbasename + '.label.nii.gz')
