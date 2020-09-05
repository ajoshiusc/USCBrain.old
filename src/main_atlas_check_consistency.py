# %%
"""

@author: ajoshi
"""
from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs, writedfs
import time
import scipy as sp
import numpy as np

import nibabel as nib
from nilearn import image as ni
import copy

BCIbase = '/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas'
USCBrainbase = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_9_3_2020'


def check_uscbrain_bci(uscbrain_lab, bci_lab):
    # This checks each USCBrain ROI has only 1 BCI ROI. If not it prints a message.
    uscbrain_labels = np.unique(uscbrain_lab)

    for lab in uscbrain_labels:
        lab_ind = np.where(uscbrain_lab == lab)
        bci_labs, lab_counts = np.unique(bci_lab[lab_ind], return_counts=True)
        if len(bci_labs) > 1:
            print('ROI %d of USCBrain has BCI rois and counts:' % lab)
            print(bci_labs)
            print(lab_counts)


def check_bci_uscbrain(uscbrain_lab, bci_lab):
    # This checks each BCI ROI has max 3 USCBrain ROIs. If not it prints a message.
    bci_labels = np.unique(bci_lab)

    for lab in bci_labels:
        uscbrain_labs, lab_counts = np.unique(
            uscbrain_lab[bci_lab == lab], return_counts=True)
        if len(uscbrain_labs) > 3:
            print('ROI %d of BCI has USC rois and counts' % lab)
            print(uscbrain_labs)
            print(lab_counts)


# Check Left Hemisphere

# Read uscbrain and bci-dni surface labels
left_mid_uscbrain = readdfs(
    USCBrainbase + '/BCI-DNI_brain.left.mid.cortex.dfs')

left_mid_bci = readdfs('/ImagePTE1/ajoshi/code_farm/svreg\
/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs')

print('Checking consistency of USCBrain and BCI-DNI boundaries')
print('Each USCBrain labels should have only one and BCI-DNI label')

print('=====Checking Left Hemisphere=====')
check_uscbrain_bci(left_mid_uscbrain.labels, left_mid_bci.labels)
check_bci_uscbrain(left_mid_uscbrain.labels, left_mid_bci.labels)

# Checking Right hemisphere
right_mid_uscbrain = readdfs(USCBrainbase + '/BCI-DNI_brain.right.mid.cortex.dfs')

right_mid_bci = readdfs(BCIbase + '/BCI-DNI_brain.right.mid.cortex.dfs')


print('=====Checking Right Hemisphere=====')
check_uscbrain_bci(right_mid_uscbrain.labels, right_mid_bci.labels)
check_bci_uscbrain(right_mid_uscbrain.labels, right_mid_bci.labels)

print('Done checking surfaces')

print('=====Checking Volume Labels=====')

lab_bci = ni.load_img(BCIbase + '/BCI-DNI_brain.label.nii.gz')
lab_uscbrain = ni.load_img(USCBrainbase + '/BCI-DNI_brain.label.nii.gz')
#lab_bci = ni.load_img('/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_online/BCI-DNI_brain.label.nii.gz')


check_uscbrain_bci(lab_uscbrain.get_fdata(), lab_bci.get_fdata())
check_bci_uscbrain(lab_uscbrain.get_fdata(), lab_bci.get_fdata())
