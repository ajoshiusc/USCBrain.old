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
from glob import glob
from tqdm import tqdm
from scipy.stats import mode
import time
import os
from scipy.interpolate import interpn
from surfproc import view_patch_vtk, smooth_patch, patch_color_labels
from dfsio import writedfs, readdfs

# Make average label atlas


outvol = "BCI-ERC-TEC.label.nii.gz"
outvol_prob = "BCI-ERC-TEC.prob.nii.gz"

outmidl = "BCI-ERC-TEC.left.mid.cortex.dfs"
outmidr = "BCI-ERC-TEC.right.mid.cortex.dfs"


lab_list = glob("/deneb_disk/erc_tec/mapped_labels_no_hippo/*.nii.gz")


vol_lab = image.load_img(
    "/home/ajoshi/BrainSuite21a/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.dws.label.nii.gz"
)
vol_img = vol_lab.get_fdata()

xres = vol_lab.header["pixdim"][1]
yres = vol_lab.header["pixdim"][2]
zres = vol_lab.header["pixdim"][3]


all_labs = np.zeros(
    (vol_lab.shape[0], vol_lab.shape[1], vol_lab.shape[2], len(lab_list)),
    dtype=np.int16,
)

for i, sub in enumerate(tqdm(lab_list)):
    all_labs[..., i] = nib.load(sub).get_fdata()


# vals, counts = np.unique(all_labs, return_counts=True, axis=3)


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

# atlas_labs, counts = mode(all_labs, axis=3, keepdims=False)
# np.savez('mode_labs.npz',atlas_labs=atlas_labs,counts=counts)

print(
    "Loading from presaved mode, if the file does not exist then uncomment the above twoo lines"
)
v = np.load("mode_labs.npz")
atlas_labs = v["atlas_labs"]
counts = v["counts"]

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)


out_img = nib.Nifti1Image(atlas_labs, vol_lab.affine, vol_lab.header)
out_img.to_filename(outvol)

prob_img = nib.Nifti1Image(
    np.float64(counts) / len(lab_list), vol_lab.affine, vol_lab.header
)
prob_img.set_data_dtype("float32")
prob_img.to_filename(outvol_prob)


BrainSuitePath = "/home/ajoshi/BrainSuite21a"

lmid = os.path.join(
    BrainSuitePath, "svreg", "BCI-DNI_brain_atlas", "BCI-DNI_brain.left.mid.cortex.dfs"
)
rmid = os.path.join(
    BrainSuitePath, "svreg", "BCI-DNI_brain_atlas", "BCI-DNI_brain.right.mid.cortex.dfs"
)

vol_img = vol_lab.get_fdata()

xres = vol_lab.header["pixdim"][1]
yres = vol_lab.header["pixdim"][2]
zres = vol_lab.header["pixdim"][3]

sl = readdfs(lmid)
sr = readdfs(rmid)

xx = np.arange(vol_lab.shape[0]) * xres
yy = np.arange(vol_lab.shape[1]) * yres
zz = np.arange(vol_lab.shape[2]) * zres

sl.labels = interpn((xx, yy, zz), vol_img, sl.vertices, method="nearest")
sr.labels = interpn((xx, yy, zz), vol_img, sr.vertices, method="nearest")

sl = smooth_patch(sl, iterations=3000, relaxation=0.5)
sr = smooth_patch(sr, iterations=3000, relaxation=0.5)

patch_color_labels(sl)
view_patch_vtk(sl)
patch_color_labels(sr)
view_patch_vtk(sr)
writedfs(outmidl, sl)
writedfs(outmidr, sr)
