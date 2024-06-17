#!/bin/bash

cd $WEST_SIM_ROOT/ntl9_folding_synd

# >>>>> Make temporary files <<<<<
PCOORD=$(mktemp)
TEMP_NAME=$(basename $(mktemp -u))

# Grab Cluster ID
CLUSTERID=$(basename $WEST_STRUCT_DATA_REF)
 
# >>>>> Calculate Pcoord <<<<<
# This takes in a cluster number as argument and returns the pcoord.
#python map_pcoord.py $CLUSTERID > $PCOORD
python map_sasa.py $CLUSTERID > $PCOORD
 
# >>>>> Backmap for a coordinate file <<<<<
# This takes in cluster number and file name as arguments
# and outputs a {file name}.nc coordinate file.
python map_coord.py $CLUSTERID $TEMP_NAME

# >>>>> Return Pcoord <<<<<
cat $PCOORD > $WEST_PCOORD_RETURN
rm $PCOORD
 
# >>>>> For HDF5 Framework <<<<<
cp ntl9.pdb $WEST_TRAJECTORY_RETURN
cp $TEMP_NAME.nc $WEST_TRAJECTORY_RETURN/seg.nc
rm $TEMP_NAME.nc

# cp ntl9.pdb $WEST_RESTART_RETURN
cat $CLUSTERID > $WEST_RESTART_RETURN/parent.txt

