# %% This script corrects the labels of central gray structures which seem to be mislabeled in the USCBrain atlas


from dfsio import readdfs, writedfs
import matlab.engine as meng

USCBrainbaseLatest = '/ImagePTE1/ajoshi/code_farm/hybridatlas/USCBrain_9_8'

eng = meng.start_matlab()
eng.addpath(eng.genpath('/ImagePTE1/ajoshi/code_farm/svreg/MEX_Files'))
eng.addpath(eng.genpath('/ImagePTE1/ajoshi/code_farm/svreg/3rdParty'))
eng.addpath(eng.genpath('/ImagePTE1/ajoshi/code_farm/svreg/src'))
xmlf = USCBrainbaseLatest+'/brainsuite_labeldescription.xml'


for hemi in {'left', 'right'}:

    mid = USCBrainbaseLatest+'/BCI-DNI_brain.'+hemi+'.mid.cortex.dfs'
    eng.recolor_by_label(mid, '', xmlf, nargout=0)

    s = readdfs(mid)
    sin = readdfs(USCBrainbaseLatest+'/BCI-DNI_brain.' +
                  hemi+'.inner.cortex.dfs')
    spial = readdfs(USCBrainbaseLatest+'/BCI-DNI_brain.' +
                    hemi+'.pial.cortex.dfs')

    sin.vColor = s.vColor
    sin.labels = s.labels
    writedfs(USCBrainbaseLatest+'/BCI-DNI_brain.' +
             hemi+'.inner.cortex.dfs', sin)

    spial.vColor = s.vColor
    spial.labels = s.labels
    writedfs(USCBrainbaseLatest+'/BCI-DNI_brain.'+hemi+'.pial.cortex.dfs', spial)
