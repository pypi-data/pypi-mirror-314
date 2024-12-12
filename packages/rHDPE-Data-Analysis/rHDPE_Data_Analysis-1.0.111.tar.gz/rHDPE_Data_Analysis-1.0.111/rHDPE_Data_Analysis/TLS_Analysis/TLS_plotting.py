# Imports.

import numpy as np
import matplotlib.pyplot as plt

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( ip.directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    samples_to_plot = samples_present
    # samples_to_plot = [3, 1, 12, 15, 6, 9]

    specimens = True
    all_specimens = False
    specimen_mask_by_index = [0]
    specimen_mask = []

    mean = False

    deriv0 = True
    deriv1 = False
    deriv2 = False

    split = False

    if not split:

        splits = [0, 100]

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

                            displacement_mask = np.where( (data[1][j] <= upper_bound) & (data[1][j] >= lower_bound) )[0]

                            plt.plot( data[1][j][displacement_mask], data[2][j][displacement_mask], label = file_data[j][2], color = colours[i] )

                            shiny_de.append( data[1][j][displacement_mask].tolist() )
                            shiny_de.append( data[2][j][displacement_mask].tolist() )

                        if deriv1:

                            plt.plot( first_derivative_data[1][j], first_derivative_data[2][j], label = file_data[j][2], color = colours[i] )

                        if deriv2:

                            plt.plot( second_derivative_data[1][j], second_derivative_data[2][j], label = file_data[j][2], color = colours[i] )

        if ip.shiny:

            return shiny_de

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend( ncol = 2 )

        plt.xlabel( "Compressive Displacement [mm]" )
        plt.ylabel( "Force [N]" )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( ip.output_directory + "TLS/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction_bool:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

    return shiny_de
