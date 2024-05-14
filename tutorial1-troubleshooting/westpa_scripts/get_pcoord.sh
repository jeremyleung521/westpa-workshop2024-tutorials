#!/bin/bash

cd $WEST_SIM_ROOT/ntl9_folding_synd

# Grab Cluster ID
CLUSTERID=$(basename $WEST_STRUCT_DATA_REF)

# >>>>> Calculate Pcoord <<<<<
# This takes in a cluster number as argument and returns the pcoord.
python map_pcoord.py $CLUSTERID > pcoord.dat

# >>>>> Backmap for a coordinate file <<<<<
# This takes in cluster number and file name as arguments
# and outputs a {file name}.nc coordinate file.
python map_coord.py $CLUSTERID seg

# >>>>> Return Pcoord <<<<<
cat pcoord.dat > $WEST_PCOORD_RETURN

# >>>>> For HDF5 Framework <<<<<
cp ntl9.pdb $WEST_TRAJECTORY_RETURN
cp seg.nc $WEST_TRAJECTORY_RETURN/seg.nc
rm seg.nc

# cp ntl9.pdb $WEST_RESTART_RETURN
cat $CLUSTERID > $WEST_RESTART_RETURN/parent.txt

