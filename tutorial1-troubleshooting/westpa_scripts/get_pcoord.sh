#!/bin/bash

# if [ -n "$SEG_DEBUG" ] ; then
#   set -x
#   env | sort
# fi

cd $WEST_SIM_ROOT/ntl9_folding_synd

# Make temporary files
PCOORD=$(mktemp)
TEMP_NAME=$(basename $(mktemp -u))

# Grab Cluster ID
CLUSTERID=$(basename $WEST_STRUCT_DATA_REF)

# Calculate Pcoord
python map_pcoord.py $CLUSTERID > $PCOORD

# Backmap for a coordinate file
python map_coord.py $CLUSTERID $TEMP_NAME

# Return Pcoord
cat $PCOORD > $WEST_PCOORD_RETURN
rm $PCOORD

# For HDF5 Framework
cp ntl9.pdb $WEST_TRAJECTORY_RETURN
cp $TEMP_NAME.nc $WEST_TRAJECTORY_RETURN/seg.nc

# cp ntl9.pdb $WEST_RESTART_RETURN
cat $CLUSTERID > $WEST_RESTART_RETURN/parent.txt
rm $TEMP_NAME.nc

#if [ -n "$SEG_DEBUG" ] ; then
#  head -v $WEST_PCOORD_RETURN
#fi
