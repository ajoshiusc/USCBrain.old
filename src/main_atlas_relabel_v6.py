# %%
"""
Created on Tue Sep  6 00:08:31 2016

@author: ajoshi
"""
from dfsio import readdfs, writedfs
from nilearn import image
import scipy as sp
import pandas as pd
import matlab.engine as meng
from shutil import copyfile

xl = pd.ExcelFile("/big_disk/ajoshi/coding_ground/hybridatlas/hybrid_atlas\
_adjusted_labels_13June2017.xlsx")

df = xl.parse("Sheet1")

oldID = df['oldID']
newID = df['newID']

left_mid = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/\
USCBrain_06_17_2017/BCI-DNI_brain.left.mid.cortex.dfs')

right_mid = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/\
USCBrain_06_17_2017/BCI-DNI_brain.right.mid.cortex.dfs')

v_lab = image.load_img('/big_disk/ajoshi/coding_ground/hybridatlas/\
USCBrain_06_17_2017/BCI-DNI_brain.label.nii.gz')

data1 = v_lab.get_data()
data2 = data1.copy()

left_labs = left_mid.labels.copy()
right_labs = right_mid.labels.copy()


for ids in range(len(oldID)):
    data2[data1 == oldID[ids]] = newID[ids]
    left_labs[sp.where(left_mid.labels == oldID[ids])] = newID[ids]
    right_labs[sp.where(right_mid.labels == oldID[ids])] = newID[ids]

vm = image.new_img_like(v_lab, data2)
vm.to_filename('/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain\
/BCI-DNI_brain.label.nii.gz')

left_mid.labels = left_labs
right_mid.labels = right_labs


lmid = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain\
/BCI-DNI_brain.left.mid.cortex.dfs'
rmid = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain\
/BCI-DNI_brain.right.mid.cortex.dfs'
writedfs(lmid, left_mid)
writedfs(rmid, right_mid)

left_inner = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas\
/USCBrain_06_17_2017/BCI-DNI_brain.left.inner.cortex.dfs')
left_inner.labels = left_labs

lin = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain/\
BCI-DNI_brain.left.inner.cortex.dfs'
writedfs(lin, left_inner)

lpial = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain/\
BCI-DNI_brain.left.pial.cortex.dfs'
left_pial = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas\
/USCBrain_06_17_2017/BCI-DNI_brain.left.pial.cortex.dfs')
left_pial.labels = left_labs
writedfs(lpial, left_pial)

rin = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain/\
BCI-DNI_brain.right.inner.cortex.dfs'
right_inner = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/\
USCBrain_06_17_2017/BCI-DNI_brain.right.inner.cortex.dfs')
right_inner.labels = right_labs
writedfs(rin, right_inner)

rpial = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain/\
BCI-DNI_brain.right.pial.cortex.dfs'
right_pial = readdfs('/big_disk/ajoshi/coding_ground/hybridatlas/\
USCBrain_06_17_2017/BCI-DNI_brain.right.pial.cortex.dfs')
right_pial.labels = right_labs
writedfs(rpial, right_pial)

eng = meng.start_matlab()
eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/MEX_Files'))
eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/3rdParty'))
eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/src'))
xmlf = '/big_disk/ajoshi/coding_ground/hybridatlas/brainsuite_hybrid_atlas_\
labeldescription_14June2017.xml'
eng.recolor_by_label(rmid, '', xmlf, nargout=0)
eng.recolor_by_label(lmid, '', xmlf, nargout=0)
eng.recolor_by_label(rin, '', xmlf, nargout=0)
eng.recolor_by_label(lin, '', xmlf, nargout=0)
eng.recolor_by_label(rpial, '', xmlf, nargout=0)
eng.recolor_by_label(lpial, '', xmlf, nargout=0)

xmlfout = '/big_disk/ajoshi/coding_ground/hybridatlas/USCBrain/brainsuite_\
labeldescription.xml'

copyfile(xmlf, xmlfout)
