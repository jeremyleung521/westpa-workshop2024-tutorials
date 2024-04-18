#!/usr/bin/env python

from synd.core import load_model
import numpy as np
import sys


if __name__ == '__main__':
    # Load in the synd model (for the backmapper)
    model = load_model('ntl9_folding.synd')

    # Calculate the Pcoord for the input
    pcoord = model.backmap(np.asarray([int(sys.argv[1])]), 'default')
    
    # Print it out
    print(f'{pcoord[0,0]}') 
