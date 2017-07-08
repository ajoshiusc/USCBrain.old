#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
% Copyright (C) 2017 The Regents of the University of California and the University of Southern California
% Created by Anand A. Joshi, David W. Shattuch and Richard M. Leahy
%
% This program is free software; you can redistribute it and/or
% modify it under the terms of the GNU General Public License
% as published by the Free Software Foundation; version 2.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program; if not, write to the Free Software
% Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
% USA.
"""
__author__ = "Anand A Joshi"
__copyright__ = "Copyright 2017, University of Southern California"
__email__ = "ajoshi@usc.edu"

import nibabel.freesurfer.io as fsio
from dfsio import writedfs, readdfs
import os
from scipy.spatial import cKDTree
import scipy as sp
import sys
import getopt


def interpolate_labels_colors(fromsurf=[], tosurf=[], skipzero=0):
    ''' interpolate labels from surface to to surface'''
    tree = cKDTree(fromsurf.vertices)
    d, inds = tree.query(tosurf.vertices, k=1, p=2)
    if skipzero == 0:
        tosurf.labels = fromsurf.labels[inds]
        tosurf.vColor = fromsurf.vColor[inds, :]
        indz = (tosurf.labels == 0)
        tosurf.vColor[indz, :] = 0.5

    else:
        indz = (tosurf.labels == 0)
        tosurf.labels = fromsurf.labels[inds]
        tosurf.vColor = fromsurf.vColor[inds, :]
        tosurf.vColor[indz, :] = 0.5
    return tosurf


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hf:a:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('python freesurfer_label_USCBrain.py -f <freesurfer_sub>\
-a <USCBrain>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python freesurfer_label_USCBrain.py -f \
<freesurfer_sub> -a <USCBrain>')
            sys.exit()
        elif opt in ("-f", "--ffile"):
            subbasename = arg
        elif opt in ("-a", "--afile"):
            USCBrainpath = arg
    print('FreeSurfer subid is :' + subbasename)
    print('USCBrain dir is :' + USCBrainpath)
    hemi = 'right'
    fshemi = 'rh'

    class s:
        pass

    class bci:
        pass

    for hi in range(2):
        if hi == 0:
            hemi = 'right'
            fshemi = 'rh'
        else:
            hemi = 'left'
            fshemi = 'lh'

        ''' USCBrain to FS processed BCI '''
        bci_bsti = readdfs(USCBrainpath +
                           '/BCI-DNI_brain.' + hemi + '.mid.cortex.dfs')
        bci_bst = readdfs(USCBrainpath + '/BCI-DNI_brain.' +
                          hemi + '.inner.cortex.dfs')
        bci_bst.labels = bci_bsti.labels
        bci_bst.vertices[:, 0] -= 96*0.8
        bci_bst.vertices[:, 1] -= 192*0.546875
        bci_bst.vertices[:, 2] -= 192*0.546875
        bci.vertices, bci.faces = fsio.read_geometry(fshemi + '.white')
        bci = interpolate_labels_colors(bci_bst, bci)

        ''' FS_BCI to FS BCI Sphere'''
        bci.vertices, bci.faces = fsio.read_geometry(fshemi + '.sphere.reg')

        ''' FS BCI Sphere to SUB FS Sphere'''
        s.vertices, s.faces = fsio.read_geometry(subbasename +
                                                 '/surf/' + fshemi +
                                                 '.sphere.reg')
        s = interpolate_labels_colors(bci, s)
        fslabels, _, _ = fsio.read_annot(subbasename +
                                         '/label/' + fshemi + '.aparc.annot')
        s.labels = s.labels * sp.int16(fslabels > 0)
        s.vColor[fslabels <= 0, :] = 0.5
        s.vertices, _ = fsio.read_geometry(subbasename + '/surf/' +
                                           fshemi + '.pial')
        so, _ = fsio.read_geometry(subbasename + '/surf/' + fshemi + '.white')
        s.vertices = (s.vertices + so)/2.0
        s.faces = s.faces[:, (0, 2, 1)]
        outfilename = subbasename + '/' + hemi + '.mid.cortex.fs.dfs'
        writedfs(outfilename, s)
        print('output file is : ' + outfilename)

if __name__ == "__main__":
    main(sys.argv[1:])
    print('Done')




#    eng = meng.start_matlab()
#    eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/MEX_Files'))
#    eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/3rdParty'))
#    eng.addpath(eng.genpath('/big_disk/ajoshi/coding_ground/svreg/src'))
#    xmlf = USCBrainpath + '/brainsuite_\
#labeldescription.xml'
#    eng.recolor_by_label(subbasename + '/' + hemi + '.mid.dfs',
#                         '', xmlf, nargout=0)
