# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 00:08:31 2016

@author: ajoshi
"""
from fmri_methods_sipi import reduce3_to_bci_lh, interpolate_labels
from dfsio import readdfs, writedfs
import scipy.io
import matlab.engine as meng
import os
from surfproc import patch_color_labels, view_patch_vtk, patch_color_attrib
# smooth_patch
import scipy as sp

outputfile = 'gaurav_bci.dfs'
# initialize the structures


class ts:
    pass


class fs:
    pass

p_dir = '/big_disk/ajoshi/coding_ground/hbci_atlas/precentral_intensity_mod_map'
nSub = 40
lst = os.listdir(p_dir)
bci_bst = readdfs('100307.BCI2reduce3.very_smooth.left.dfs')
bci_bst_sm = readdfs('100307.BCI2reduce3.very_smooth.left.dfs')

bci_bst.vertices = bci_bst_sm.vertices

freq = sp.zeros(bci_bst.vertices.shape[0])
bci_bst.labels *= 10
for fname in lst:
    if not (fname.endswith('.mat')):
        continue

    s = fname.find('_nCluster')

    roino = int(fname[s-3:s])
    print roino
    if sp.mod(roino, 2) == 0:
        continue

    data1 = scipy.io.loadmat(os.path.join(p_dir, fname))

    labs = data1['labels'].squeeze()
    freq1 = data1['freq'].squeeze()
    freq1 = freq1/nSub
    freq1[labs == 0] = 0
#    bci_labs = reduce3_to_bci_lh(labs)
#    freq1 = reduce3_to_bci_lh(freq1)
    bci_labs = labs.squeeze().copy()
    bci_labs_orig = bci_labs.copy()

    if sp.amax(bci_labs) > 0:
        bci_labs[bci_bst.labels != roino*10] = 0      
        indt = (bci_bst.labels == roino*10) & (bci_labs == 0)
        ts.vertices = bci_bst.vertices[indt, :]
        ind = (bci_bst.labels == roino*10) & (bci_labs != 0)
        fs.vertices = bci_bst.vertices[ind, :]
        fs.labels = bci_labs[ind]
        ts = interpolate_labels(fs, ts)
        bci_labs[indt] = ts.labels

    freq1[(bci_labs > 0) & (freq1 == 0)] = \
        sp.amin(freq1[(bci_labs_orig > 0) & (freq1 != 0)])

    freq[(bci_bst.labels == roino*10)] += freq1[(bci_bst.labels == roino*10)]
    bci_bst.labels += sp.uint16(bci_labs)


freq[freq == 0] = 1
bci_bst.attributes = freq
bci_bst = patch_color_labels(bci_bst, freq=freq, cmap='Paired')
# bci_bst = smooth_patch(bci_bst, iterations=90, relaxation=10.8)
view_patch_vtk(bci_bst, show=1)
####writedfs('/home/ajoshi/data/BCI-DNI_brain_atlas/BCI-DNI_brain.left.\
####mid.cortex_refined_labs_uncorr.dfs', bci_bst)
bci_bst = patch_color_attrib(bci_bst, bci_bst.attributes)
view_patch_vtk(bci_bst, show=1)

bci_bst = patch_color_labels(bci_bst, freq=freq, cmap='Paired')
view_patch_vtk(bci_bst, show=1)
####writedfs('/home/ajoshi/data/BCI-DNI_brain_atlas/BCI-DNI_brain.left.\
####mid.cortex_refined_labs_mod_freq_uncorr.dfs', bci_bst)

bci_labs = reduce3_to_bci_lh(bci_bst.labels)
bci_freq = reduce3_to_bci_lh(bci_bst.attributes)

bci_bst = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_\
atlas_refined_4_11_2017/BCI-DNI_brain.left.mid.cortex.dfs')

bci_bst_sm = readdfs('/big_disk/ajoshi/data/BCI-DNI_brain_atlas/BCI-DNI_brain.\
left.mid.cortex_smooth10.dfs')
bci_bst.vertices = bci_bst_sm.vertices


# clean bci_labs for the labels based on bci_bst 
# we want precentral label in all these vertices

oldids = sp.floor(bci_bst.labels/10)# precent in 711 atlas
oldidsbst = sp.floor(bci_labs/10) # precent in new subdiv
ind = ((oldids == 150) | (oldids == 151)) & ((oldidsbst != 150) & (oldidsbst != 151)) # precent in new subdiv but not in old atlas

oldids = sp.floor(bci_bst.labels/10)  # precent in 711 atlas
indlabs = (oldidsbst == 150) | (oldidsbst == 151) # precent in new subdiv

fs.vertices = bci_bst.vertices[indlabs, :] # we are given values here
fs.labels = bci_labs[indlabs]
ts.vertices = bci_bst.vertices[ind, :] # we need values here

ts = interpolate_labels(fromsurf=fs, tosurf=ts)
bci_labs[ind]=ts.labels    
    
bci_freq[ind]=1 #maybe

oldids = sp.floor(bci_bst.labels/10)
ind = ((oldids ==150) | (oldids==151)) 

bci_bst.labels[ind] = bci_labs[ind]

bci_freq1 = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_\
atlas_refined_4_11_2017/BCI-DNI_brain.left.mid.cortex.mod.dfs')

bci_bst.attributes = bci_freq1.attributes
bci_bst.attributes[ind] = bci_freq[ind]


bci_bst = patch_color_labels(bci_bst, cmap='Paired')
view_patch_vtk(bci_bst, show=1)
writedfs('../tmp/BCI-DNI_brain.left.\
mid.cortex_refined_labs_uncorr.dfs', bci_bst)

bci_bst = patch_color_labels(bci_bst, freq=bci_bst.attributes, cmap='Paired')
# bci_bst = smooth_patch(bci_bst, iterations=90, relaxation=10.8)
view_patch_vtk(bci_bst, show=1)
writedfs('../tmp/BCI-DNI_brain.left.\
mid.cortex_refined_labs_mod_freq_uncorr.dfs', bci_bst)


surfname = '../tmp/BCI-DNI_brain.left.\
mid.cortex_refined_labs_uncorr.dfs'
sub_out = '../tmp/BCI-DNI_brain.left.\
mid.cortex_refined_labs_corr.dfs'

eng = meng.start_matlab()
eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/MEX_Files'))
eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/3rdParty'))
eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg-matlab/src'))

eng.corr_topology_labels(surfname, sub_out)

bci_bst = readdfs(sub_out)
#bci_bst = patch_color_labels(bci_bst, freq=bci_bst.attributes, cmap='Paired')
bci_bst = patch_color_attrib(bci_bst,cmap='gray',clim=[0,1])

# bci_bst = smooth_patch(bci_bst, iterations=90, relaxation=10.8)
view_patch_vtk(bci_bst, show=1)

writedfs('../precentral_corr/BCI-DNI_brain.left.mid.cortex.mod.dfs', bci_bst)
xmlf='/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_atlas_refined_4_11_2017/brainsuite_labeldescription.xml'
#eng.recolor_by_label('../precentral_corr/BCI-DNI_brain.left.mid.cortex.mod.dfs','',xmlf,nargout=0)

bci_lab = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_\
atlas_refined_4_11_2017/BCI-DNI_brain.left.mid.cortex.dfs')
bci_lab.labels = bci_bst.labels
delattr(bci_lab,'attributes')
writedfs('../precentral_corr/BCI-DNI_brain.left.mid.cortex.dfs', bci_lab)
eng.recolor_by_label('../precentral_corr/BCI-DNI_brain.left.mid.cortex.dfs','',xmlf,nargout=0)

bci_lab = readdfs('../precentral_corr/BCI-DNI_brain.left.mid.cortex.dfs')
li = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_\
atlas_refined_4_11_2017/BCI-DNI_brain.left.inner.cortex.dfs')
li.labels=bci_lab.labels
li.vColor=bci_lab.vColor
#delattr(li,'attributes')
writedfs('../precentral_corr/BCI-DNI_brain.left.inner.cortex.dfs', li)

lp = readdfs('/big_disk/ajoshi/coding_ground/hbci_atlas/BCI-DNI_brain_\
atlas_refined_4_11_2017/BCI-DNI_brain.left.pial.cortex.dfs')
lp.labels=bci_lab.labels
lp.vColor=bci_lab.vColor
#delattr(lp,'attributes')
writedfs('../precentral_corr/BCI-DNI_brain.left.pial.cortex.dfs', lp)



#bci_bst = patch_color_labels(bci_bst, freq=bci_bst.attributes, cmap='Paired')
#view_patch_vtk(bci_bst, show=1)
#
#writedfs('BCI-DNI_brain.left.\
#mid.cortex_refined_labs.dfs', bci_bst)
