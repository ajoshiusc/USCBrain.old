# %% This script corrects the labels of central gray structures which seem to be mislabeled in the USCBrain atlas
import xml.etree.ElementTree as ET

"""

@author: ajoshi
"""
from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs
import numpy as np

from nilearn import image as ni
import copy

BCIbase = '/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas'
USCBrainbaseLatest = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_9_3_2020'


old_labs = [612, 613, 614, 615, 620, 621, 680, 681, 690, 691]
new_labs = [620, 621, 630, 631, 650, 651, 696, 697, 698, 699]

v = ni.load_img(USCBrainbaseLatest+'/BCI-DNI_brain.precent_bci.label.nii.gz')

old_vol = v.get_fdata()
new_vol = old_vol.copy()

for i, l in enumerate(old_labs):
    new_vol[old_vol == l] = new_labs[i]


v = ni.new_img_like(v,new_vol)

v.to_filename(USCBrainbaseLatest+'/BCI-DNI_brain.precent_bci_idcorr.label.nii.gz')

