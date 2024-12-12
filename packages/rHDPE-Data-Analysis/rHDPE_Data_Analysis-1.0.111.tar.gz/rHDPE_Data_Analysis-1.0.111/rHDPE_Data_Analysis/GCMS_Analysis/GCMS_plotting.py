# Imports.

import numpy as np
import matplotlib.pyplot as plt

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data, savefig = False ):

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    samples_to_plot = [18]

    specimens = True
    all_specimens = False
    specimen_mask_by_index = [6, 7, 8, 9, 10, 11]
    specimen_mask = []

    mean = False

    deriv0 = True
    deriv1 = False
    deriv2 = False
    deriv3 = False

    split = True
    # splits = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 15]
    splits = [4, 4.3]

    if not split:

        splits = [int( data[0][0] ), int( data[0][len( data[0] ) - 1] )]

    if ip.shiny:

        samples_to_plot = ip.shiny_samples_to_plot

        if type( samples_to_plot ) == int:

            samples_to_plot = [samples_to_plot]

        specimen_mask = ip.shiny_specimens_to_plot

        if type( specimen_mask ) == int:

            specimen_mask = [specimen_mask]

        splits = ip.shiny_split
        mean = ip.shiny_mean
        specimens = ip.shiny_specimen
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

                            rt_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                            plt.plot( data[0][rt_mask], data[1][j][rt_mask] / 10000000, label = file_data[j][2] )

                            shiny_de.append( data[0][rt_mask].tolist() )
                            shiny_de.append( (data[1][j][rt_mask]).tolist() )

            if mean:

                index = np.where( samples_present_array == i )[0][0]

                if deriv0:

                    rt_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                    plt.plot( data[0][rt_mask], data[2][index][rt_mask], label = i, color = colours[i] )

                    shiny_de.append( data[0][rt_mask].tolist() )
                    shiny_de.append( data[2][index][rt_mask].tolist() )

        if ip.shiny:

            return shiny_de

        plt.legend( ncol = 1, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend()

        plt.xlabel( "Retention Time [Minutes]" )
        plt.ylabel( "Absolute Intensity [x10e7]" )

        ax = plt.gca()

        plt.tight_layout()

        if savefig:

            plt.savefig( ip.output_directory + "Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction_bool:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Output/Plot_Coords/Unnamed.txt", array )

    return shiny_de
