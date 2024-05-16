#!/bin/bash

# assign source and target states using the phi/psi angles from WE simulations
lpath discretize -we -W ./west.h5 --assign-arguments "--config-from-file --scheme CRUDE_RMSD"

# extract all successful pathways connecting source and target states
# also extract the cluster labels for matching in the next step
lpath extract -we -W ./west.h5 -A ./ANALYSIS/CRUDE_RMSD/assign.h5 -ss 1 -ts 0 -p --stride 10

# perform matching with condensing repeat pairs
# uses the cluster labels as states through reassign_custom
#lpath match -we -ra reassign_custom.reassign_custom -op succ_traj/reassigned.pickle --condense 2
