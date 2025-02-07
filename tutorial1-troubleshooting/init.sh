#!/bin/bash

# Set up simulation environment
source env.sh

# Clean up from previous/ failed runs
rm -rf traj_segs seg_logs istates west.h5
mkdir   seg_logs traj_segs istates

# Note all states from the "clusters" in bstates.txt are from RMSD > 10.2 Ang
# The tstate would be structures with RMSD < 1 Ang
#--sstate-file "sbstates/sstates.txt" \

w_init --bstate-file "sbstates/bstates.txt" \
        --tstate 'folded,10' \
	--segs-per-state 1 \
	--work-manager=threads "$@" |& tee init.log
