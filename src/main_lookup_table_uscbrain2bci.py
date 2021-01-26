# %% This script checks consistency of BCI and USCBrain labels. The BCI label should be substring of USCBrain label
import xml.etree.ElementTree as ET


from fmri_methods_sipi import interpolate_labels
from dfsio import readdfs, writedfs
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


def uscbrain2bci(uscbrain_lab_vol, uscbrain_dict, bci_lab_vol, bci_dict, tiny_threhsold=100):
    print(' This checks each USCBrain ROI has only 1 BCI ROI. If not it prints a message.')
    print(' For each uscbrain roi it outputs corresponding BCI ROI.')

    error_indicator = np.zeros(len(uscbrain_lab_vol))

    f = open('uscbrain2bci.csv', 'w')

    for uscbrain_lab in uscbrain_dict:

        lab_ind = np.where(uscbrain_lab_vol == uscbrain_lab)[0]
        bci_labs, lab_counts = np.unique(
            bci_lab_vol[lab_ind], return_counts=True)

        count_sort_ind = np.argsort(-lab_counts)

        bci_labs = bci_labs[count_sort_ind]
        lab_counts = lab_counts[count_sort_ind]

        if len(lab_ind) > 0:
            print('%d, %s, %d, %s' % (
                uscbrain_lab, uscbrain_dict[uscbrain_lab], bci_labs[0], bci_dict[bci_labs[0]]))

            f.write('%d, %s, %d, %s\n' % (
                uscbrain_lab, uscbrain_dict[uscbrain_lab], bci_labs[0], bci_dict[bci_labs[0]]))

        for j, bci_lab in enumerate(bci_labs):

            if bci_dict[bci_lab] not in uscbrain_dict[uscbrain_lab]:
                print('USCBrain and BCI labels inconsistent %d(%s) vs %d(%s)' % (
                    uscbrain_lab, uscbrain_dict[uscbrain_lab], bci_lab, bci_dict[bci_lab]))

        for j, bci_lab in enumerate(bci_labs):

            if len(bci_labs) > 1:
                print('ROI %d (%s) of USCBrain has BCI rois and counts:' %
                      (uscbrain_lab, uscbrain_dict[uscbrain_lab]))
                print(bci_lab, bci_dict[bci_lab], lab_counts[j])

            error_indicator += (lab_counts[j] < tiny_threhsold) & (bci_lab_vol ==
                                                                   bci_lab) & (uscbrain_lab_vol == uscbrain_lab)

    f.close()

    return error_indicator


if __name__ == "__main__":

    BCIbase = '/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas'
    USCBrainbaseLatest = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_online'

    bci_dict = build_dict_rois(BCIbase+'/brainsuite_labeldescription.xml')
    uscbrain_dict = build_dict_rois(
        USCBrainbaseLatest+'/brainsuite_labeldescription.xml')

    # Volume check
    uscbrain = ni.load_img(USCBrainbaseLatest +
                           '/BCI-DNI_brain.label.nii.gz')

    bci = ni.load_img(BCIbase + '/BCI-DNI_brain.label.nii.gz')

    error_indicator1 = uscbrain2bci(uscbrain.get_fdata().flatten(
    ), uscbrain_dict, bci.get_fdata().flatten(), bci_dict, tiny_threhsold=80)
