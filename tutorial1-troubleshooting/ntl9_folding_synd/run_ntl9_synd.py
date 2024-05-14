import numpy as np
import pickle
from synd.core import load_model

# Loading in the SynD Model
model = load_model('ntl9_folding.synd')

# Resetting the random number generator, so we're actually create distinct trajectories 
model.rng = np.random.default_rng()
print(f'RNG State: {model.rng.bit_generator.state}')

# This is the cluster_ids from the parent segments
restart = np.atleast_1d(np.loadtxt('parent.txt', dtype=int))

# Propagate Trajectory from the last cluster_id of the parent segment
discrete_trajectory = model.generate_trajectory(
    initial_states=np.array([restart[-1]]),
    # 1 step is 10 ps, including first frame
    n_steps=31
)[:,::3]

# print(f'discrete: {discrete_trajectory}')
#
# If you want to add additional backmappers, which are the `get` method of a dictionary,
# mapping key=cluster_id to value=anything you want.
#
# with open('synd_model/coord_map.pkl', 'rb') as infile:
#     coord_map = pickle.load(infile)
# 
# model.add_backmapper(
#     coord_map.get, 
#     name='coord'
# )

# Output pcoord
pcoord_trajectory = model.backmap(discrete_trajectory[:, :], 'default')[0] * -1

# Output xyz coordinates, multiply by 10 to turn into Angstroms
atomistic_trajectory = model.backmap(discrete_trajectory[:, :], 'full_coordinates')[0] * 10

# Output SASA, multiple by 100 to turn from nm^2 to Angstrom^2
sasa_trajectory = model.backmap(discrete_trajectory[:, :], 'sasa')[0] * 100

# If you want a trajectory file 
# import MDAnalysis as mda
# from MDAnalysis.coordinates.memory import MemoryReader

# u = mda.Universe('ntl9.pdb')
# u.load_new(atomistic_trajectory[0], format=MemoryReader)
# u.select_atoms('all').write('seg.nc', frames='all')

# Outputting clusters_ids into `seg.txt`, pcoord into `pcoord.txt`, xyz into `xyz.npy`
np.savetxt('seg.txt', discrete_trajectory[0], fmt='%d')
np.savetxt('pcoord.txt', pcoord_trajectory, fmt='%2.8f')
np.save('xyz.npy', atomistic_trajectory)
np.savetxt('sasa.dat', sasa_trajectory)

