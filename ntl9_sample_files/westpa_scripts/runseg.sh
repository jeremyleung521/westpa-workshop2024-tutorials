#!/bin/bash

# if [ -n "$SEG_DEBUG" ] ; then
#   set -x
#   env | sort
# fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

# Soft-link necessary files
ln -sv $WEST_SIM_ROOT/ntl9_folding_synd/ntl9_folding_mod.synd ./ntl9_folding.synd
ln -sv $WEST_SIM_ROOT/ntl9_folding_synd/run_ntl9_synd.py .
ln -sv $WEST_SIM_ROOT/ntl9_folding_synd/ntl9.pdb .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  # sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.txt ./parent.txt
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  # sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  echo $(basename $WEST_PARENT_DATA_REF) > ./parent.txt
fi

# Running SynD Propagation
python run_ntl9_synd.py

# Returning Pcoord and Auxdata
cat pcoord.txt > $WEST_PCOORD_RETURN
cat pcoord.txt > $WEST_RMSD_RETURN
cat xyz.npy > $WEST_COORD_RETURN
cat seg.txt > $WEST_STATE_INDICES_RETURN
cat sasa.dat > $WEST_SASA_RETURN

# For HDF5 Framework, Note "restart" file is a text file (of cluster id) for SynD
cp ntl9.pdb $WEST_TRAJECTORY_RETURN
cp seg.nc $WEST_TRAJECTORY_RETURN

# cp ntl9.pdb $WEST_RESTART_RETURN
cp seg.txt  $WEST_RESTART_RETURN/parent.txt

# cp seg.log $WEST_LOG_RETURN

# Clean Up
rm xyz.npy pcoord.txt

# if [ -n "$SEG_DEBUG" ] ; then
#   head -v $WEST_PCOORD_RETURN
# fi

