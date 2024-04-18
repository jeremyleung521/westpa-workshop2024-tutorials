#!/bin/bash

# if [ -n "$SEG_DEBUG" ] ; then
#   set -x
#   env | sort
# fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

# Soft-link necessary files
ln -sv $WEST_SIM_ROOT/ntl9_folding_synd/ntl9_folding.synd .
ln -sv $WEST_SIM_ROOT/ntl9_folding_synd/run_ntl9_synd.py .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  # sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.txt ./parent.txt
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  # sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  echo $(basename $WEST_PARENT_DATA_REF) > ./parent.txt
fi

python run_ntl9_synd.py

cat pcoord.txt > $WEST_PCOORD_RETURN

cat pcoord.txt > $WEST_RMSD_RETURN

cat xyz.npy > $WEST_COORD_RETURN

cat seg.txt > $WEST_STATE_INDICES_RETURN

# For HDF5 Framework, but not really necessary and/or compatible with SynD
# cp hmr.prmtop $WEST_TRAJECTORY_RETURN
# cp seg.nc $WEST_TRAJECTORY_RETURN

# cp hmr.prmtop $WEST_RESTART_RETURN
# cp seg.ncrst  $WEST_RESTART_RETURN/parent.ncrst

# cp seg.log $WEST_LOG_RETURN

# Clean Up
rm xyz.npy pcoord.txt

# if [ -n "$SEG_DEBUG" ] ; then
#   head -v $WEST_PCOORD_RETURN
# fi

