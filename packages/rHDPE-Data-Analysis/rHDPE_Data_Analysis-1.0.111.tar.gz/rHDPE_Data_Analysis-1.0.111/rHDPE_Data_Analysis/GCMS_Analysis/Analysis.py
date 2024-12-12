# Imports.

from . import Preprocessing
from . import Utilities as util
from . import GCMS_plotting

# Main function definition.

def GCMS_Analysis_Main( ip ):
    '''Main function for GCMS data.'''

    file_data, data, first_derivative_data, second_derivative_data, third_derivative_data = [], [], [], [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [retention time, [Absolute intensity]]. Data of type lists of numpys.

    print( str( len( file_data ) ) + " files have been read." )

    if len( file_data ) != 12:

        print( "Warning: 12 files have not been read." )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data now of form [retention time, [Absolute intensity], [m]]. Data of type lists of numpys.

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data )
        second_derivative_data = util.compute_derivatives( first_derivative_data )
        third_derivative_data = util.compute_derivatives( second_derivative_data )

    if ip.extract_features:

        pass

        # util.extract_GCMS_features( output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data )

    if ip.read_and_analyse_features:

        pass

        # util.read_and_analyse_FTIR_features( directory, ip, file_data )

    if ip.plot_data:

        GCMS_plotting.plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data )

    if ip.sandbox:

        pass

        # util.sandbox( directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data )
