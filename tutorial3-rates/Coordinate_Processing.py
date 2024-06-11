import mdtraj as md
import numpy as np
from itertools import combinations


def processCoordinates(self, coords):
    
    xt = md.Trajectory(xyz=coords, topology=self.reference_structure.topology)

    #  C-alpha atoms indices 
    ca_ind = self.reference_structure.topology.select("name CA")

    pairs = np.asarray(list(combinations(ca_ind, 2)))
    
    dist_nm = md.compute_distances(xt, pairs, periodic=True, opt=True)

    dist_Ang = dist_nm*10.0
    
    return dist_Ang