import scipy as sp
import nibabel.freesurfer.io as fsio
from surfproc import view_patch_vtk, patch_color_labels, smooth_patch
from dfsio import writedfs, readdfs
from nibabel.gifti.giftiio import read as gread



labels,_,_=fsio.read_annot('/big_disk/ajoshi/freesurfer/subjects/sub06880/label/rh.HCP-MMP1.annot')
vert,faces=fsaverage_surf=fsio.read_geometry('/big_disk/ajoshi/freesurfer/subjects/sub06880/surf/rh.pial')

class fs:
    pass


fs.vertices=vert; fs.faces=faces;fs.labels=labels
fs = patch_color_labels(fs)
view_patch_vtk(fs,outfile='fs1.png')#, azimuth=-90, roll=90)


class bs:
    pass


bs1=readdfs('/home/ajoshi/Desktop/test/T1.right.pial.cortex.svreg.dfs')
bs=readdfs('/home/ajoshi/Desktop/test/multiparc/T1.right.mid.cortex.svreg.HCP-MMP1.dfs')
bs.vertices = bs1.vertices
bs = patch_color_labels(bs)
view_patch_vtk(bs,outfile='bst1.png')#, azimuth=-90, roll=90)




bs1=readdfs('/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/HCP-MMP1/BCI-HCP_MMP1.right.mid.cortex.dfs')
bs = readdfs('/home/ajoshi/BrainSuite19b/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.pial.cortex.dfs')
bs.labels=bs1.labels

bs = patch_color_labels(bs)
view_patch_vtk(bs,outfile='bci_bst1.png')#, azimuth=-90, roll=90)


labels,_,_=fsio.read_annot('/big_disk/ajoshi/freesurfer/subjects/BCI_DNI_Atlas/label/rh.HCP-MMP1.annot')
vert,faces=fsaverage_surf=fsio.read_geometry('/big_disk/ajoshi/freesurfer/subjects/BCI_DNI_Atlas/surf/rh.pial')

fs.vertices=vert; fs.faces=faces;fs.labels=labels
fs = patch_color_labels(fs)
view_patch_vtk(fs,outfile='bci_fs1.png')#, azimuth=-90, roll=90)


