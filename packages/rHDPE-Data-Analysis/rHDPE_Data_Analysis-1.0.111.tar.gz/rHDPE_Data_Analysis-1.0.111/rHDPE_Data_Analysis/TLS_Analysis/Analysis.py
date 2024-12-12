# Imports.

from . import Preprocessing
from . import Utilities as util
from . import TLS_plotting
from .. import Global_Utilities as gu

# Main function definition.

def TLS_Analysis_Main( ip ):

    file_data, data = [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [[Time], [Displacement], [Force], [Compressive Displacement], [Compressive Stress], [Force]]. Data of type lists of numpys.

    gu.print_files_read( len( data[2] ), 130 )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data, "e" )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data still of form [[Time], [Displacement], [Force], [Compressive Displacement], [Compressive Stress], [Force]]. Data of type lists of numpys.

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data )
        second_derivative_data = util.compute_derivatives( first_derivative_data )

    if ip.extract_features:

        util.extract_tls_features( ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    if ip.read_and_analyse_features:

        util.read_and_analyse_features( ip, file_data )

    if ip.plot_data:

        TLS_plotting.plot_data( ip, file_data, data, first_derivative_data, second_derivative_data )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )
