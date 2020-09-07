# %% This script corrects the labels of central gray structures which seem to be mislabeled in the USCBrain atlas
import xml.etree.ElementTree as ET


from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs
import numpy as np

from nilearn import image as ni
import copy


def build_dict_rois(xmlfile):
    # Read XML for brain atlas
    xml_root = ET.parse(xmlfile).getroot()

    roi_names = list()
    roi_ids = list()

    for i in range(len(xml_root)):
        roi_names.append(xml_root[i].get('fullname'))
        roi_ids.append(int(xml_root[i].get('id')))

    roi_dict = {roi_ids[i]: roi_names[i]
                for i in range(len(roi_ids))}

    return roi_dict


def check_uscbrain_bci(uscbrain_lab_vol, uscbrain_dict, bci_lab_vol, bci_dict):
    # This checks each USCBrain ROI has only 1 BCI ROI. If not it prints a message.

    for uscbrain_lab in uscbrain_dict:

        lab_ind = np.where(uscbrain_lab_vol == uscbrain_lab)
        bci_labs, lab_counts = np.unique(
            bci_lab_vol[lab_ind], return_counts=True)

        for j, bci_lab in enumerate(bci_labs):

            if bci_dict[bci_lab] not in uscbrain_dict[uscbrain_lab]:
                print('USCBrain and BCI labels inconsistent %d(%s) vs %d(%s)' % (
                    uscbrain_lab, uscbrain_dict[uscbrain_lab], bci_lab, bci_dict[bci_lab]))

        for j, bci_lab in enumerate(bci_labs):

            if len(bci_labs) > 1:
                print('ROI %d (%s) of USCBrain has BCI rois and counts:' %
                      (uscbrain_lab, uscbrain_dict[uscbrain_lab]))
                print(bci_lab, bci_dict[bci_lab], lab_counts[j])


def check_bci_uscbrain(uscbrain_lab_vol, uscbrain_dict, bci_lab_vol, bci_dict):
    # This checks each BCI ROI has max 3 USCBrain ROIs. If not it prints a message.

    for bci_lab in bci_dict:

        lab_ind = np.where(bci_lab_vol == bci_lab)
        uscbrain_labs, lab_counts = np.unique(
            uscbrain_lab_vol[lab_ind], return_counts=True)

        for j, uscbrain_lab in enumerate(uscbrain_labs):

            if bci_dict[bci_lab] not in uscbrain_dict[uscbrain_lab]:
                print('USCBrain and BCI labels inconsistent %d(%s) vs %d(%s)' % (
                    uscbrain_lab, uscbrain_dict[uscbrain_lab], bci_lab, bci_dict[bci_lab]))

        for j, uscbrain_lab in enumerate(uscbrain_labs):
            if len(uscbrain_labs) > 3:
                print('ROI %d (%s) of BCI has USC rois and counts' %
                      (bci_lab, bci_dict[bci_lab]))

                print(uscbrain_lab,
                      uscbrain_dict[uscbrain_lab], lab_counts[j])


BCIbase = '/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas'
USCBrainbaseLatest = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_9_3_2020'

bci_dict = build_dict_rois(BCIbase+'/brainsuite_labeldescription.xml')
uscbrain_dict = build_dict_rois(
    USCBrainbaseLatest+'/brainsuite_labeldescription.xml')


# Volume check
uscbrain = ni.load_img(USCBrainbaseLatest +
                       '/BCI-DNI_brain.precent_bci_idcorr.label.nii.gz')

bci = ni.load_img(BCIbase + '/BCI-DNI_brain.label.nii.gz')

check_uscbrain_bci(uscbrain.get_fdata().flatten(),
                   uscbrain_dict, bci.get_fdata().flatten(), bci_dict)

check_bci_uscbrain(uscbrain.get_fdata().flatten(),
                   uscbrain_dict, bci.get_fdata().flatten(), bci_dict)


# Left hemisphere surface
print('=====Checking Left Hemisphere Surface=====')

uscbrain = readdfs(USCBrainbaseLatest +
                       '/BCI-DNI_brain.left.mid.cortex.dfs')

bci = readdfs(BCIbase + '/BCI-DNI_brain.left.mid.cortex.dfs')

check_uscbrain_bci(uscbrain.labels.flatten(),
                   uscbrain_dict, bci.labels.flatten(), bci_dict)

check_bci_uscbrain(uscbrain.labels.flatten(),
                   uscbrain_dict, bci.labels.flatten(), bci_dict)

# Right hemisphere surface
print('=====Checking Right Hemisphere Surface=====')

uscbrain = readdfs(USCBrainbaseLatest +
                       '/BCI-DNI_brain.right.mid.cortex.dfs')

bci = readdfs(BCIbase + '/BCI-DNI_brain.right.mid.cortex.dfs')

check_uscbrain_bci(uscbrain.labels.flatten(),
                   uscbrain_dict, bci.labels.flatten(), bci_dict)

check_bci_uscbrain(uscbrain.labels.flatten(),
                   uscbrain_dict, bci.labels.flatten(), bci_dict)



