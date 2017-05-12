### Using the USCBrain atlas with BrainSuite
test.
### Using the USCBrain atlas with FreeSurfer
The USCBrain atlas can be used with FreeSurfer for surface labeling of a given subject. This can be done in the following steps:

1. Process the subjct data using freesurfer recon-all pipeline.
2. Run the following python code.
``` 
freesurfer_label_USCBrain.py <path-to-freesurfer-subject-dir> <path-to-freesurfer-atlas-dir-sphere-map>
```
Where <path-to-freesurfer-atlas-dir-sphere-map> is shared with this package.
The output of the registration is stored as a dfs file that can be visualized in BrainSuite.

### Using the USCBrain atlas with FSL

FSL can be used with the new atlas to warp atlas labels to the subject labels. This can be done by using [FNIRT](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FNIRT), the nonlinear registration program that is part of FSL package. 

```
fnirt --ref=<path-to-anat-img>anat.nii.gz --in=<path-to-atlas>/hBCI-DNI_brain_atlas/BCI-DNI_brain.nii.gz --iout=fnirtwarpedimg.nii.gz
```
Note that execution time for fnirt can be upto 1-2 hours.
