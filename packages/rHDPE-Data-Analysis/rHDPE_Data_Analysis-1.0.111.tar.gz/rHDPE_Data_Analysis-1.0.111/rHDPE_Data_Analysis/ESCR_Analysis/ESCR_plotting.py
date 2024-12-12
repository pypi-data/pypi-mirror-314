# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( ip.directory )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = samples_present
    # samples_to_plot = [1, 3, 6, 8, 9, 12, 15, 17, 24, 25]
    samples_to_plot = [17, 24, 25]

    split = False

    if not split:

        splits = [0, 96]

    if ip.shiny:

        samples_to_plot = ip.shiny_samples_to_plot

        if type( samples_to_plot ) == int:

            samples_to_plot = [samples_to_plot]

        splits = ip.shiny_split

    colours = gu.read_list_of_colours( ip.directory )

    shiny_de = []

    data_extraction_bool = False

    plt.figure( figsize = (10, 8) )

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        for i in samples_to_plot:

            mask = np.where( sample_array == i )[0]

            for j in mask:

                if file_data[j][0] == 3 or file_data[j][0] == 9:

                    hour_mask = np.where( (data[2] <= upper_bound) & (data[2] >= lower_bound) )[0]

                    plt.plot( data[2][hour_mask], data[1][j][[3, 6, 7, 8]][hour_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    shiny_de.append( data[2][hour_mask].tolist() )
                    shiny_de.append( data[1][j][[3, 6, 7, 8]][hour_mask].tolist() )

                else:

                    hour_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                    plt.plot( data[0][hour_mask], data[1][j][hour_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    shiny_de.append( data[0][hour_mask].tolist() )
                    shiny_de.append( data[1][j][hour_mask].tolist() )

        if ip.shiny:

            return shiny_de

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0, fontsize = 18 )
        # plt.legend( ncol = 2, fontsize = 18, bbox_to_anchor = ( 1.05, 1 ) )

        plt.xlabel( "Time [Hours]", fontsize = 18 )
        plt.ylabel( "Bottle Success Rate [%]", fontsize = 18 )
        plt.xticks( fontsize = 18 )
        plt.yticks( fontsize = 18 )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( ip.output_directory + "ESCR/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction_bool:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

    return shiny_de
