#!/bin/bash

# if [ -n "$SEG_DEBUG" ] ; then
#   set -x
#   env | sort
# fi

cd $WEST_SIM_ROOT/ntl9_folding_synd

PCOORD=$(mktemp)

# Calculate pcoord

CLUSTERID=$(basename $WEST_STRUCT_DATA_REF)
python map_pcoord.py $CLUSTERID > $PCOORD

cat $PCOORD > $WEST_PCOORD_RETURN

rm $PCOORD

#if [ -n "$SEG_DEBUG" ] ; then
#  head -v $WEST_PCOORD_RETURN
#fi
