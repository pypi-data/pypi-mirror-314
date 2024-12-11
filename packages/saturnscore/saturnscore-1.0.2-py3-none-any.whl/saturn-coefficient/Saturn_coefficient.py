import numpy as np
import pandas as pd
import scipy
import umap.umap_ as umap
from AdjustedRV import  AdjustedRV
from scipy.spatial import distance

def SaturnCoefficient(original_matrix, umap_output_layout):

    original_matrix_norm = original_matrix / np.max(original_matrix)
    original_matrix_norm_dist = distance.squareform(distance.pdist(original_matrix_norm))
    umap_output_layout_dist = distance.squareform(distance.pdist(umap_output_layout))

    Saturn_Python = AdjustedRV(original_matrix_norm_dist, umap_output_layout_dist, version='Maye', center=True)

    return Saturn_Python
