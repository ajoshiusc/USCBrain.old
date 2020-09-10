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


def check_uscbrain_bci(uscbrain_lab_vol, uscbrain_dict, bci_lab_vol, bci_dict, tiny_threhsold=100):
    print(' This checks each USCBrain ROI has only 1 BCI ROI. If not it prints a message.')
    print(' It returns indices of overlap of rois with tiny overlapping regions.')

    error_indicator = np.zeros(len(uscbrain_lab_vol))

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

            error_indicator += (lab_counts[j] < tiny_threhsold) & (bci_lab_vol ==
                                                                   bci_lab) & (uscbrain_lab_vol == uscbrain_lab)

    return error_indicator


def check_bci_uscbrain(uscbrain_lab_vol, uscbrain_dict, bci_lab_vol, bci_dict, tiny_threhsold=100):
    print(' We will check if each BCI ROI has max 3 USCBrain ROIs. If not it prints a message.')
    print(' It returns indices of overlap of rois with tiny overlapping regions.')

    error_indicator = np.zeros(len(uscbrain_lab_vol))

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

            error_indicator += (lab_counts[j] < tiny_threhsold) & (bci_lab_vol ==
                                                                   bci_lab) & (uscbrain_lab_vol == uscbrain_lab)

    return error_indicator


def surf_lab_match_bci_uscbrain(uscbrain, uscbrain_dict, bci, bci_dict, error_ind):

    uscbrain_new = copy.deepcopy(uscbrain)

    class from_surf:
        pass

    class to_surf:
        pass

    for bci_lab in bci_dict:

        lab_ind = (bci.labels == bci_lab)

        error_ind = np.array(error_ind, dtype=bool)

        to_ind = lab_ind & error_ind
        from_ind = lab_ind & (~error_ind)

        from_surf.vertices = uscbrain.vertices[from_ind, :]
        to_surf.vertices = uscbrain.vertices[to_ind, :]
        from_surf.labels = uscbrain.labels[from_ind]

        to_surf = interpolate_labels(from_surf, to_surf)
        uscbrain_new.labels[to_ind] = to_surf.labels

    return uscbrain_new


if __name__ == "__main__":

    BCIbase = '/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas'
    USCBrainbaseLatest = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_9_8_2020'

    bci_dict = build_dict_rois(BCIbase+'/brainsuite_labeldescription.xml')
    uscbrain_dict = build_dict_rois(
        USCBrainbaseLatest+'/brainsuite_labeldescription.xml')

    # Volume check
    uscbrain = ni.load_img(USCBrainbaseLatest +
                           '/BCI-DNI_brain.label.nii.gz')

    bci = ni.load_img(BCIbase + '/BCI-DNI_brain.label.nii.gz')

    error_indicator1 = check_uscbrain_bci(uscbrain.get_fdata().flatten(),
                                          uscbrain_dict, bci.get_fdata().flatten(), bci_dict, tiny_threhsold=80)

    error_indicator2 = check_bci_uscbrain(uscbrain.get_fdata().flatten(),
                                          uscbrain_dict, bci.get_fdata().flatten(), bci_dict, tiny_threhsold=80)

    v = ni.new_img_like(bci, error_indicator1.reshape(bci.shape))
    v.to_filename('errorvol.nii.gz')
    print('Tiny region overlaps: %d or %d ' %
          (np.sum(error_indicator1), np.sum(error_indicator2)))

    class error_surf:
        pass

    # Left hemisphere surface
    print('=====Checking Left Hemisphere Surface=====')

    uscbrain = readdfs(USCBrainbaseLatest +
                       '/BCI-DNI_brain.left.mid.cortex.dfs')

    bci = readdfs(BCIbase + '/BCI-DNI_brain.left.mid.cortex.dfs')

    error_indicator1 = check_uscbrain_bci(uscbrain.labels.flatten(),
                                          uscbrain_dict, bci.labels.flatten(), bci_dict)

    error_indicator2 = check_bci_uscbrain(uscbrain.labels.flatten(),
                                          uscbrain_dict, bci.labels.flatten(), bci_dict)

    error_surf.vertices = bci.vertices
    error_surf.faces = bci.faces
    error_surf.attributes = 255.0*error_indicator1
    error_surf.labels = error_indicator1

    writedfs('error_left.dfs', error_surf)

    out_surf = surf_lab_match_bci_uscbrain(
        uscbrain, uscbrain_dict, bci, bci_dict, error_indicator1)

    writedfs(USCBrainbaseLatest +
             '/BCI-DNI_brain.left.mid.cortex_bci_consistent.dfs', out_surf)

    print('Tiny region overlaps: %d or %d ' %
          (np.sum(error_indicator1), np.sum(error_indicator2)))
    # Right hemisphere surface
    print('=====Checking Right Hemisphere Surface=====')

    uscbrain = readdfs(USCBrainbaseLatest +
                       '/BCI-DNI_brain.right.mid.cortex.dfs')

    bci = readdfs(BCIbase + '/BCI-DNI_brain.right.mid.cortex.dfs')

    error_indicator1 = check_uscbrain_bci(uscbrain.labels.flatten(),
                                          uscbrain_dict, bci.labels.flatten(), bci_dict)

    error_indicator2 = check_bci_uscbrain(uscbrain.labels.flatten(),
                                          uscbrain_dict, bci.labels.flatten(), bci_dict)

    error_surf.vertices = bci.vertices
    error_surf.faces = bci.faces
    error_surf.attributes = 255.0*error_indicator1
    error_surf.labels = error_indicator1

    writedfs('error_right.dfs', error_surf)

    out_surf = surf_lab_match_bci_uscbrain(
        uscbrain, uscbrain_dict, bci, bci_dict, error_indicator1)

    writedfs(USCBrainbaseLatest +
             '/BCI-DNI_brain.right.mid.cortex_bci_consistent.dfs', out_surf)

    print('Tiny region overlaps: %d or %d' %
          (np.sum(error_indicator1), np.sum(error_indicator2)))
