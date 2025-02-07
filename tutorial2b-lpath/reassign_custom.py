import numpy
from scipy.stats import binned_statistic_2d

# These are the new binning/state definitions
# First dimension is the CA-RMSD, the second is SASA
bin_edges = [[0,1,3.5,6,8.5,10, numpy.inf], [0, 3000, 3050, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, numpy.inf]]
n_rows = len(bin_edges[0])-1
n_cols = len(bin_edges[1])-1
tot_bins = n_rows * n_cols

def reassign_custom(data, pathways, dictionary, assign_file=None):
    # "data" is the input array, "pathways" is the output file
    # We also need to provide a dictionary which maps the state_id (and integer)
    # to a unique single character for each state
    for idx, val in enumerate(data):
        val_arr = numpy.asarray(val)

        # Assigning all frames to the binning scheme we've defined above.
        _, _, _, index = binned_statistic_2d(val_arr[:,3], val_arr[:,4], val_arr[:,3], bins= bin_edges, expand_binnumbers=True)

        for idx2, val2 in enumerate(val_arr):
            if val2[2] < 2:
                # If from source or sink state, skip. We're not changing the source/target definition
                continue
            else:
                # Replace state id with the index sum, downsizing the 2D index into a unique 1D index
                val2[2] = int(index[0, idx2] * n_rows + index[1, idx2] + 2)  # Adding 2 because we want to reserve 0, 1 for our source, sink states

            # Overwriting the output "pathways"
            pathways[idx, idx2] = val2

    # Generating a dictionary mapping each state, last one is the "unknown" state
    # Unknown state is given when a frame is in a region not explicitly defined a state.
    dictionary = {0:"0", 1:"1"}  # Source, sink states
    dictionary.update({i+2: chr(50+i) for i in range(tot_bins)})  # One for each bin
    dictionary.update({74: '!'})  # The "Unknown" state, where it visited a region not defined

    return dictionary

