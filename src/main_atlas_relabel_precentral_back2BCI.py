# %%
"""

@author: ajoshi
"""
from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs
import numpy as np

from nilearn import image as ni
import copy

BCIbase = '/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas'
USCBrainbase = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_anand_8_29'
USCBrainbaseLatest = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_9_3_2020'

#
# %% Change Precentral to match BCI-DNI brain boundaries

left_mid = readdfs(USCBrainbase+'/BCI-DNI_brain.left.mid.cortex.dfs')
right_mid = readdfs(USCBrainbase+'/BCI-DNI_brain.right.mid.cortex.dfs')
left_inner = readdfs(USCBrainbase+'/BCI-DNI_brain.left.inner.cortex.dfs')
right_inner = readdfs(USCBrainbase+'/BCI-DNI_brain.right.inner.cortex.dfs')
left_pial = readdfs(USCBrainbase+'/BCI-DNI_brain.left.pial.cortex.dfs')
right_pial = readdfs(USCBrainbase+'/BCI-DNI_brain.right.pial.cortex.dfs')

r1_vert = (right_pial.vertices + right_mid.vertices)/2.0
r2_vert = (right_inner.vertices + right_mid.vertices)/2.0
l1_vert = (left_pial.vertices + left_mid.vertices)/2.0
l2_vert = (left_inner.vertices + left_mid.vertices)/2.0


vol_lab_new = ni.load_img(USCBrainbase+'/BCI-DNI_brain.label.nii.gz')
vol_img_new = vol_lab_new.get_fdata()


vol_lab = ni.load_img(BCIbase+'/BCI-DNI_brain.label.nii.gz')
vol_img = vol_lab.get_fdata()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]

X, Y, Z = np.meshgrid(np.arange(vol_lab.shape[0]), np.arange(vol_lab.shape[1]),
                      np.arange(vol_lab.shape[2]), indexing='ij')

X = X*xres
Y = Y*yres
Z = Z*zres

ind = (vol_img == 150)  # selects right precentral from BCI atlas
Xc = X[ind]
Yc = Y[ind]
Zc = Z[ind]


class t:
    pass


class f:
    pass


t.vertices = np.concatenate((Xc[:, None], Yc[:, None], Zc[:, None]), axis=1)
f.vertices = np.concatenate((left_mid.vertices, right_mid.vertices,
                             left_inner.vertices, right_inner.vertices,
                             left_pial.vertices, right_pial.vertices,
                             l1_vert, r1_vert, l2_vert, r2_vert))

f.labels = np.concatenate((left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels))

# selects precentral from uscbrain atlas
surf_ind = (f.labels == 144) | (f.labels == 146)

f.vertices = f.vertices[surf_ind]
f.labels = f.labels[surf_ind]


t = interpolate_labels(fromsurf=f, tosurf=t)


# here make sure that hanns labels are not modified TBD
vol_img_new[ind] = t.labels

del t, f
# Left Precentral
ind = (vol_img == 151)  # selects left precentral from BCI atlas
Xc = X[ind]
Yc = Y[ind]
Zc = Z[ind]


class t:
    pass


class f:
    pass


t.vertices = np.concatenate((Xc[:, None], Yc[:, None], Zc[:, None]), axis=1)
f.vertices = np.concatenate((left_mid.vertices, right_mid.vertices,
                             left_inner.vertices, right_inner.vertices,
                             left_pial.vertices, right_pial.vertices,
                             l1_vert, r1_vert, l2_vert, r2_vert))

f.labels = np.concatenate((left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels,
                           left_mid.labels, right_mid.labels))

# selects precentral from uscbrain atlas
surf_ind = (f.labels == 145) | (f.labels == 147)

f.vertices = f.vertices[surf_ind]
f.labels = f.labels[surf_ind]


t = interpolate_labels(fromsurf=f, tosurf=t)


# here make sure that hanns labels are not modified TBD
vol_img_new[ind] = t.labels


new_img = ni.new_img_like(vol_lab_new, vol_img_new)
new_img.to_filename(USCBrainbaseLatest +
                    '/BCI-DNI_brain.precent_bci.label.nii.gz')
