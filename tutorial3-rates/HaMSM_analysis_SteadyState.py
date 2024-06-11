import msm_we
import numpy as np
import pickle
import h5py
from msm_we._logging import log
import ray


#ModelName
model_name = 'NTL9_SynMD_WEfolding'
#west.h5 file location
h5file_paths = ['../ntl9_sample_files/completed_files/west.h5']
# Reference structure
ref_file = '../ntl9_sample_files/ntl9_folding_synd/ntl9.pdb'


#DimReduction method
dimreduce_method = 'vamp'
# Number of MSM microstates to initially put in each stratum/WE bin
clusters_per_stratum = 3
# Boundaries of the basis/target, in progress coordinate space Unit
pcoord_bounds = { 'basis':[[10.0, 1000]], 'target':[[0, 1.0]] }
# WESTPA resampling time:
tau = 3e-10 


import Coordinate_Processing
msm_we.modelWE.processCoordinates = Coordinate_Processing.processCoordinates

ray.init(num_cpus=2)
RAY_DISABLE_IMPORT_WARNING = 1

model = msm_we.modelWE()
model.initialize(fileSpecifier=h5file_paths,refPDBfile=ref_file,modelName=model_name,basis_pcoord_bounds=pcoord_bounds['basis'],target_pcoord_bounds=pcoord_bounds['target'],dim_reduce_method=dimreduce_method,tau=tau,pcoord_ndim=1)

model.get_iterations()
model.get_coordSet(last_iter = model.maxIter)

model.dimReduce(variance_cutoff=0.05,use_weights=False)
with open('Outputs/Dim_Reduce_Vamp_05.obj', 'wb') as outfile:
    pickle.dump(model, outfile)


model.cluster_coordinates(n_clusters=clusters_per_stratum,use_ray=True,stratified=True,random_state=1337,max_iter=200)
with open('Outputs/Clusters_3perStratum_200iter.obj', 'wb') as outfile:
    pickle.dump(model, outfile)


model.get_fluxMatrix(n_lag=0)
with open('Outputs/FluxMatrixRaw.obj', 'wb') as outfile:
    pickle.dump(model, outfile)


model.organize_fluxMatrix()
with open('Outputs/FluxMatrixOrganized.obj', 'wb') as outfile:
    pickle.dump(model, outfile)



model.get_Tmatrix()
model.get_steady_state()
model.get_steady_state_target_flux()
with open('Outputs/SteadyState_Flux.obj', 'wb') as outfile:
    pickle.dump(model, outfile)

model.get_flux()

with open('Outputs/Anlysis_Done.obj', 'wb') as outfile:
    pickle.dump(model, outfile)
