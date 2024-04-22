#!/usr/bin/env python

from synd.core import load_model
import numpy as np
import sys
import MDAnalysis as mda
from MDAnalysis.coordinates.memory import MemoryReader


if __name__ == '__main__':
    # Load in the synd model (for the backmapper)
    model = load_model('ntl9_folding.synd')
   
    print(f'{sys.argv}')
 
    # Return the coordinates, note in Angstroms (*10)
    atomistic_trajectory = model.backmap(np.asarray([[int(sys.argv[1])]]), 'full_coordinates')[0] * 10
    
    u = mda.Universe('ntl9.pdb')
    u.load_new(atomistic_trajectory[0], format=MemoryReader)
    u.select_atoms('all').write(f'{sys.argv[2]}.nc', frames='all')
