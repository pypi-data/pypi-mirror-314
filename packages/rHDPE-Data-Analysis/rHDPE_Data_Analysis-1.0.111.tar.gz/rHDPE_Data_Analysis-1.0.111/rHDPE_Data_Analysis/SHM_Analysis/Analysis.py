# Imports.

from . import Preprocessing
from . import Utilities as util
from . import SHM_plotting
from .. import Global_Utilities as gu

# Main function definition.

def SHM_Analysis_Main( ip ):

    file_data, data = [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [[Draw Ratio], [True Stress], [Neo-Hookean Strain Measure: Draw Ratio^2 - 1 / Draw Ratio]]. Data of type lists of numpys.

    gu.print_files_read( len( data[0] ), 120 )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data, "s" )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data still of form [[Draw Ratio], [True Stress], [Neo-Hookean Strain Measure: Draw Ratio^2 - 1 / Draw Ratio]]. Data of type lists of numpys.

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data, width = 200 )

    if ip.extract_features:

        util.extract_SHM_features( ip.output_directory, file_data, data, first_derivative_data )

    if ip.read_and_analyse_features:

        util.read_and_analyse_SHM_features( ip, file_data )

    if ip.plot_data:

        SHM_plotting.plot_data( ip, file_data, data, first_derivative_data )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data, first_derivative_data )
