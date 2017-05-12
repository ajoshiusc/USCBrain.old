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
flirt -ref <anat-image BFC file> -in <uscbrain BFC file> -omat <out-mat file>
fnirt --ref=<anat-image BFC file> --in=<uscbrain BFC file> --aff=<out-mat file> --cout=<fnirtcoeff coeff file>
applyxfm --ref=<anat-image BFC file> --in=<uscbrain BFC file> --out=<warped-labels> --coef=<fnirtcoeff coeff file> --premat=<out-mat file>
```
Note that execution time for flirt is 5-10 min and fnirt can take upto 1-2 hours. 
###Refrences
* [FNIRT](http://web.mit.edu/fsl_v5.0.8/fsl/doc/wiki/FNIRT(2f)UserGuide.html#Now_what.3F_--_applywarp.21) User guide
