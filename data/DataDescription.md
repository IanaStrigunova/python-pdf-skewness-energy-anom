# Data Description

This folder contains input files obtained from Python scripts that compute energy anomalies. A full description can be found in Strigunova et al. (2023, 2025).
There are two types of data: reanalyses and a subset of CMIP5 models (CNRM-CM5, GFDL-CM3, MIROC5, MPI-ESM-LR) with three runs (historical, "atmosphere-only" and RCP4.5).
Each dataset represents normalised energy anomalies. 
The filenames contain information on what type of data, in particular, whether it is climatology or only during heatwaves ("extremes"). 
Each  column is a part of the 3D atmospheric circulation (Rossby modes only) divided by their zonal wavenumbers (*k*):

- entire Rossby circulation or all *k* (it depends on truncation),
- zonal-mean zonal flow (or "background") or *k0*,
- planetary-scale Rossby waves or *k1-k3*,
- synoptic-scale Rossby waves or *k4-k15*.
