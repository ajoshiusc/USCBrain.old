# %%
"""

@author: ajoshi
"""
from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs, writedfs
import time
import scipy as sp
import nibabel as nib
from nilearn import image


left_mid = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral_corr\
/BCI-DNI_brain.left.mid.cortex.dfs')
right_mid = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral_corr\
/BCI-DNI_brain.right.mid.cortex.dfs')
left_inner = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral\
_corr/BCI-DNI_brain.left.inner.cortex.dfs')
right_inner = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral\
_corr/BCI-DNI_brain.right.inner.cortex.dfs')
left_pial = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral_\
corr/BCI-DNI_brain.left.pial.cortex.dfs')
right_pial = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral\
_corr/BCI-DNI_brain.right.pial.cortex.dfs')

r1_vert = (right_pial.vertices + right_mid.vertices)/2.0
r2_vert = (right_inner.vertices + right_mid.vertices)/2.0
l1_vert = (left_pial.vertices + left_mid.vertices)/2.0
l2_vert = (left_inner.vertices + left_mid.vertices)/2.0

vol_lab = image.load_img('/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain\
_atlas_refined_4_11_2017/BCI-DNI_brain.label.nii.gz')
vol_img = vol_lab.get_data()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]

X, Y, Z = sp.meshgrid(sp.arange(vol_lab.shape[0]), sp.arange(vol_lab.shape[1]),
                      sp.arange(vol_lab.shape[2]), indexing='ij')

X = X*xres
Y = Y*yres
Z = Z*zres
#vol_img = sp.mod(vol_img, 1000)
ind = (sp.floor((vol_img/10)) == 150) | (sp.floor((vol_img/10)) == 151)
Xc = X[ind]
Yc = Y[ind]
Zc = Z[ind]
v_lab = vol_img[ind]


class t:
    pass


class f:
    pass


t.vertices = sp.concatenate((Xc[:, None], Yc[:, None], Zc[:, None]), axis=1)
f.vertices = sp.concatenate((left_mid.vertices, right_mid.vertices,
                             left_inner.vertices, right_inner.vertices,
                             left_pial.vertices, right_pial.vertices,
                             l1_vert, r1_vert, l2_vert, r2_vert))

f.labels = sp.concatenate((left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels))

t = interpolate_labels(fromsurf=f,tosurf=t)

# here make sure that hanns labels are not modified TBD
vol_img[ind] = t.labels

new_img = image.new_img_like(vol_lab, vol_img)
new_img.to_filename('/big_disk/ajoshi/coding_ground/hbci_atlas/precentral_corr/\
BCI-DNI_brain.label.nii.gz')
