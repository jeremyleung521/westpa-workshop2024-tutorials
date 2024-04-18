#!/bin/bash

# if [ -n "$SEG_DEBUG" ] ; then
#     set -x
#     env | sort
# fi

cd $WEST_SIM_ROOT || exit 1

ITER=$(printf "%06d" $WEST_CURRENT_ITER)
tar -czf seg_logs/$ITER.tar.gz seg_logs/$ITER-*.log
rm  -f  seg_logs/$ITER-*.log
# rm -rf traj_segs/$ITER
