# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, first_derivative_data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( ip.directory )

    # For overall pipeline figure.
    
    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = [1, 3, 6, 8, 9, 12, 13, 15, 17, 18, 20]
    # samples_to_plot = samples_present
    samples_to_plot = [3, 15, 1, 12, 6, 9]

    specimens = True
    all_specimens = True
    specimen_mask_by_index = [0, 1, 3]
    specimen_mask = []

    mean = False

    deriv0 = True
    deriv1 = False
    deriv2 = False

    split = False
    num_splits = 25
    split_length = 20
    splits = [split_length * (i + 5) for i in range( num_splits )]
    splits = [20, 100]

    step = 100

    if not split:

        splits = [0, 250]

    if ip.shiny:

        samples_to_plot = ip.shiny_samples_to_plot

        if type( samples_to_plot ) == int:

            samples_to_plot = [samples_to_plot]

        specimen_mask = ip.shiny_specimens_to_plot

        if type( specimen_mask ) == int:

            specimen_mask = [specimen_mask]

        splits = ip.shiny_split
        all_specimens = False

    colours = gu.read_list_of_colours( ip.directory )

    shiny_de = []

    data_extraction_bool = False

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        for i in samples_to_plot:

            if specimens:

                mask = np.where( sample_array == i )[0]

                if not ip.shiny:

                    if all_specimens:

                        specimen_mask = [file_data[mask[j]][2] for j in range( len( mask ) )]

                    else:

                        specimen_mask = [file_data[mask[j]][2] for j in specimen_mask_by_index]

                for j in mask:

                    if file_data[j][2] in specimen_mask:

                        if deriv0:

                            strain_mask = np.where( (data[2][j] <= upper_bound) & (data[2][j] >= lower_bound) )[0]

                            plt.plot( data[2][j][strain_mask], data[1][j][strain_mask], label = file_data[j][2], color = colours[i] )

                            shiny_de.append( data[2][j][strain_mask].tolist() )
                            shiny_de.append( data[1][j][strain_mask].tolist() )

                        if deriv1:

                            strain_mask = np.where( (first_derivative_data[2][j] <= upper_bound) & (first_derivative_data[2][j] >= lower_bound) )[0]

                            plt.plot( first_derivative_data[2][j][strain_mask][::step], first_derivative_data[1][j][strain_mask][::step], label = file_data[j][2], color = colours[i] )

        if ip.shiny:

            return shiny_de

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend( ncol = 2 )

        plt.xlabel( "Neo-Hookean Strain Measure" )
        plt.ylabel( "True Stress [MPa]" )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( ip.output_directory + "SHM/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction_bool:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

    return shiny_de
