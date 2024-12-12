# Imports.

from . import Preprocessing
from . import Utilities as util
from . import FTIR_plotting
from .. import Global_Utilities as gu
import numpy as np
from scipy.signal import savgol_filter

# Main function definition.

def FTIR_Analysis_Main( ip ):
    '''Main function for FTIR data.'''

    file_data, data, m_peaks, y_peaks, mag_m_peaks, mag_y_peaks, m_peaks_array, y_peaks_array, first_derivative_data, second_derivative_data, third_derivative_data = [], [], [], [], [], [], [], [], [], [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [x, [y]]. data[0], data[1][i] all have length 1762. Data of type lists of numpys.

    gu.print_files_read( len( data[1] ), 572 )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data, "mnfrpaeubdtv" )

    for i in range( len( file_data ) ):

        s = file_data[i][3]

        if s.find( "m" ) > -0.5:

            if file_data[i][0] == 40:

                array = np.array( data[1][i] )

                array = savgol_filter( array, 7, 3 )

                data[1][i] = array

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data now of form [x, [y], [m]]. Data of type lists of numpys.

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data )
        second_derivative_data = util.compute_derivatives( first_derivative_data )
        third_derivative_data = util.compute_derivatives( second_derivative_data )

    if ip.extract_features:

        m_peaks, m_peaks_array, y_peaks, y_peaks_array = util.extract_FTIR_features( ip.output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data, ip.peak_threshold_1, ip.peak_threshold_2, ip.peak_spacing, ip.peak_limit )

    if ip.read_and_analyse_features:

        util.read_and_analyse_FTIR_features( ip, file_data )

    if ip.plot_data:

        FTIR_plotting.plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data, m_peaks, m_peaks_array, y_peaks, y_peaks_array )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data )
