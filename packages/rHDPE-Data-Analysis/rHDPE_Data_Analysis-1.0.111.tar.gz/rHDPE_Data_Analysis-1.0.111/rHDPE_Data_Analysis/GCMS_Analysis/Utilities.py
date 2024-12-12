# Imports.

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [data[0][width: -width], [], [], []]

    for i in range( len( data[1] ) ):

        derivative_data[1].append( np.array( gu.derivative( data[0], data[1][i], width ) ) )

    for i in range( len( data[3] ) ):

        derivative_data[3].append( np.array( gu.derivative( data[0], data[3][i], width ) ) )

    return derivative_data

def extract_GCMS_features( output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data ):

    pass

def read_and_analyse_FTIR_features( directory, ip, file_data ):

    pass

def sandbox( directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data ):

    pass
