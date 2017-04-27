# %%
"""

@author: ajoshi
"""
from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs
import scipy as sp
from nilearn import image

vol = image.load_img('/big_disk/ajoshi/coding_ground/hybridatlas/\
BCI-DNI_brain_atlas_refined_4_18_2017/BCI-DNI_brain.bfc.nii.gz')

# save 1mm T1
vol1 = image.resample_img(vol, target_affine=sp.eye(4))
vol1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain-1mm.nii.gz')

# save 2mm T1
vol2 = image.resample_img(vol, target_affine=sp.eye(4)*2)
vol2.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain-2mm.nii.gz')

lab = image.load_img('/big_disk/ajoshi/coding_ground/hybridatlas/\
BCI-DNI_brain_atlas_refined_4_18_2017/BCI-DNI_brain.label.nii.gz')
lab.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain.label.nii.gz')

# save 1mm T1
lab1mm = image.resample_img(lab, target_affine=sp.eye(4),
                            interpolation='nearest', target_shape=vol1.shape)
lab1mm.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain-1mm.label.nii.gz')

# save 2mm T1
lab2mm = image.resample_img(lab, target_affine=sp.eye(4)*2,
                            interpolation='nearest', target_shape=vol2.shape)
lab2mm.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain-2mm.label.nii.gz')

# %%


right_mod = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.right.mid.cortex.mod.dfs')
left_mod = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.left.mid.cortex.mod.dfs')

right_mid = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.right.mid.cortex.dfs')
left_mid = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.left.mid.cortex.dfs')

right_inner = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.right.inner.cortex.dfs')
left_inner = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.left.inner.cortex.dfs')

right_pial = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.right.pial.cortex.dfs')
left_pial = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/BCI-DNI\
_brain_atlas_refined_4_18_2017/BCI-DNI_brain.left.pial.cortex.dfs')


vol_lab = image.load_img('/big_disk/ajoshi/coding_ground/hybridatlas/\
BCI-DNI_brain_atlas_refined_4_18_2017/BCI-DNI_brain.label.nii.gz')
vol_img = vol_lab.get_data()

xres = vol_lab.header['pixdim'][1]
yres = vol_lab.header['pixdim'][2]
zres = vol_lab.header['pixdim'][3]

X, Y, Z = sp.meshgrid(sp.arange(vol_lab.shape[0]), sp.arange(vol_lab.shape[1]),
                      sp.arange(vol_lab.shape[2]), indexing='ij')

X = X*xres
Y = Y*yres
Z = Z*zres

vol_img = sp.mod(vol_img, 1000)
ind = (vol_img >= 100) & (vol_img < 600)

Xc = X[ind]
Yc = Y[ind]
Zc = Z[ind]
v_lab = vol_img[ind]

r1_vert = (right_pial.vertices + right_mid.vertices)/2.0
r2_vert = (right_inner.vertices + right_mid.vertices)/2.0
l1_vert = (left_pial.vertices + left_mid.vertices)/2.0
l2_vert = (left_inner.vertices + left_mid.vertices)/2.0

vol_attrib = sp.zeros(vol_img.shape)


class t:
    pass


class f:
    pass


t.vertices = sp.concatenate((Xc[:, None], Yc[:, None], Zc[:, None]), axis=1)
f.vertices = sp.concatenate((left_mid.vertices, right_mid.vertices,
                             left_inner.vertices, right_inner.vertices,
                             left_pial.vertices, right_pial.vertices,
                             l1_vert, r1_vert, l2_vert, r2_vert))

f.labels = sp.concatenate((left_mod.attributes, right_mod.attributes,
                           left_mod.attributes, right_mod.attributes,
                           left_mod.attributes, right_mod.attributes,
                           left_mod.attributes, right_mod.attributes,
                           left_mod.attributes, right_mod.attributes))

t = interpolate_labels(fromsurf=f, tosurf=t)

# %% here make sure that hanns labels are not modified TBD
vol_attrib[ind] = t.labels
vol = image.load_img('/big_disk/ajoshi/coding_ground/hybridatlas/\
BCI-DNI_brain_atlas_refined_4_18_2017/BCI-DNI_brain.bfc.nii.gz')
prob_img = image.new_img_like(vol, vol_attrib)
prob_img.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain-prob.nii.gz')

msk = image.threshold_img(prob_img, threshold=.5)

lab = image.load_img('/big_disk/ajoshi/coding_ground/hybridatlas/hBCI_DNI_fsl/\
BCI-DNI_brain.label.nii.gz')

lab1 = image.new_img_like(lab, lab.get_data() * (prob_img.get_data() > 0))
lab1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr0.nii.gz')

lab1 = image.new_img_like(lab, lab.get_data() * (prob_img.get_data() > 0.5))
lab1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr50.nii.gz')

lab1 = image.new_img_like(lab, lab.get_data() * (prob_img.get_data() > 0.9))
lab1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr90.nii.gz')


# %% Threshold the image

prob_img1mm = image.resample_img(prob_img, target_affine=sp.eye(4),
                                 interpolation='nearest')
prob_img1mm.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-prob_1mm.nii.gz')


lab1mm1 = image.new_img_like(lab1mm, lab1mm.get_data()*(prob_img1mm.
                             get_data() > 0))
lab1mm1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr0-1mm.nii.gz')

lab1mm1 = image.new_img_like(lab1mm, lab1mm
                             .get_data()*(prob_img1mm.get_data() > 0.5))
lab1mm1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr50-1mm.nii.gz')

lab1mm1 = image.new_img_like(lab1mm, lab1mm.get_data()*(prob_img1mm.
                             get_data() > 0.9))
lab1mm1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr90-1mm.nii.gz')

# %%
prob_img2mm = image.resample_img(prob_img, target_affine=sp.eye(4)*2)
prob_img2mm.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-prob_2mm.nii.gz')


lab2mm1 = image.new_img_like(lab2mm, lab2mm.get_data()*(prob_img2mm.
                             get_data() > 0))
lab2mm1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr0-2mm.nii.gz')

lab2mm1 = image.new_img_like(lab2mm, lab2mm.get_data() *
                             (prob_img2mm.get_data() > 0.5))
lab2mm1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr50-2mm.nii.gz')

lab2mm1 = image.new_img_like(lab2mm, lab2mm.get_data() *
                             (prob_img2mm.get_data() > 0.9))
lab2mm1.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/\
hBCI_DNI_fsl/BCI-DNI_brain-maxprob-thr90-2mm.nii.gz')

