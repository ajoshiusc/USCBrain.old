#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 17:35:03 2017

@author: ajoshi
"""

from dfsio import readdfs, writedfs
from nilearn import image
import scipy as sp

so = readdfs('/big_disk/ajoshi/coding_ground/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.pial.cortex.dfs')
s = readdfs('/big_disk/ajoshi/coding_ground/svreg/USCBrain/BCI-DNI_brain.right.pial.cortex.dfs')



