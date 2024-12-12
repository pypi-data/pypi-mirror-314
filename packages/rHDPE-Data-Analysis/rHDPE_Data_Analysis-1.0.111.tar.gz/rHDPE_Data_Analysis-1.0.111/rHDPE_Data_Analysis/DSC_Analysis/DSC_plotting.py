# Imports.

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, savefig = True ):

    resin_data = gu.get_list_of_resins_data( ip.directory )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = samples_present[:-7]
    samples_to_plot = [23]

    specimens = False
    all_specimens = False
    specimen_mask_by_index = [1, 3]
    specimen_mask = []

    mean = True

    deriv0 = True
    deriv1 = False
    deriv2 = False

    cryst = True
    melt = True

    split = False
    num_splits = 15
    split_length = 10
    splits = [split_length * (i + 2) for i in range( num_splits )]
    splits = [130, 145]

    if not split:

        splits = [int( data[2][0] ), int( data[2][len( data[2] ) - 1] )]

    if ip.shiny:

        samples_to_plot = ip.shiny_samples_to_plot

        if type( samples_to_plot ) == int:

            samples_to_plot = [samples_to_plot]

        specimen_mask = ip.shiny_specimens_to_plot

        if type( specimen_mask ) == int:

            specimen_mask = [specimen_mask]

        splits = ip.shiny_split
        melt = ip.shiny_melt
        cryst = ip.shiny_cryst
        mean = ip.shiny_mean
        specimens = ip.shiny_specimen
        all_specimens = False

    colours = gu.read_list_of_colours( ip.directory )

    shiny_de = []

    data_extraction_bool = True

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

                            if cryst:

                                temp_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                                plt.plot( data[0][temp_mask], data[1][j][temp_mask], label = file_data[j][2] )

                                shiny_de.append( data[0][temp_mask].tolist() )
                                shiny_de.append( data[1][j][temp_mask].tolist() )

                            if melt:

                                temp_mask = np.where( (data[2] <= upper_bound) & (data[2] >= lower_bound) )[0]

                                plt.plot( data[2][temp_mask], data[3][j][temp_mask], label = file_data[j][2] )

                                shiny_de.append( data[2][temp_mask].tolist() )
                                shiny_de.append( data[3][j][temp_mask].tolist() )

                        if deriv1:

                            if cryst:

                                temp_mask = np.where( (first_derivative_data[0] <= upper_bound) & (first_derivative_data[0] >= lower_bound) )[0]

                                plt.plot( first_derivative_data[0][temp_mask], first_derivative_data[1][j][temp_mask], label = file_data[j][2] )

                            if melt:

                                temp_mask = np.where( (first_derivative_data[2] <= upper_bound) & (first_derivative_data[2] >= lower_bound) )[0]

                                plt.plot( first_derivative_data[2][temp_mask], first_derivative_data[3][j][temp_mask], label = file_data[j][2] )

                        if deriv2:

                            if cryst:

                                temp_mask = np.where( (second_derivative_data[0] <= upper_bound) & (second_derivative_data[0] >= lower_bound) )[0]

                                plt.plot( second_derivative_data[0][temp_mask], second_derivative_data[1][j][temp_mask], label = file_data[j][2] )

                            if melt:

                                temp_mask = np.where( (second_derivative_data[2] <= upper_bound) & (second_derivative_data[2] >= lower_bound) )[0]

                                plt.plot( second_derivative_data[2][temp_mask], second_derivative_data[3][j][temp_mask], label = file_data[j][2] )

            if mean:

                index = np.where( samples_present_array == i )[0][0]

                if deriv0:

                    if cryst:

                        temp_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                        plt.plot( data[0][temp_mask], data[4][index][temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                        shiny_de.append( data[0][temp_mask].tolist() )
                        shiny_de.append( data[4][index][temp_mask].tolist() )

                        data_extraction.append( data[0][temp_mask] )
                        data_extraction.append( data[4][index][temp_mask] )

                    if melt:

                        temp_mask = np.where( (data[2] <= upper_bound) & (data[2] >= lower_bound) )[0]

                        plt.plot( data[2][temp_mask], data[5][index][temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                        shiny_de.append( data[2][temp_mask].tolist() )
                        shiny_de.append( data[5][index][temp_mask].tolist() )

                        data_extraction.append( data[2][temp_mask] )
                        data_extraction.append( data[5][index][temp_mask] )

                if deriv1:

                    if cryst:

                        temp_mask = np.where( (first_derivative_data[0] <= upper_bound) & (first_derivative_data[0] >= lower_bound) )[0]

                        plt.plot( first_derivative_data[0][temp_mask], first_derivative_data[4][index][temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if melt:

                        temp_mask = np.where( (first_derivative_data[2] <= upper_bound) & (first_derivative_data[2] >= lower_bound) )[0]

                        plt.plot( first_derivative_data[2][temp_mask], first_derivative_data[5][index][temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv2:

                    if cryst:

                        temp_mask = np.where( (second_derivative_data[0] <= upper_bound) & (second_derivative_data[0] >= lower_bound) )[0]

                        plt.plot( second_derivative_data[0][temp_mask], second_derivative_data[4][index][temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if melt:

                        temp_mask = np.where( (second_derivative_data[2] <= upper_bound) & (second_derivative_data[2] >= lower_bound) )[0]

                        plt.plot( second_derivative_data[2][temp_mask], second_derivative_data[5][index][temp_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

        if ip.shiny:

            return shiny_de

        # plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend()

        plt.xlabel( "Temperature °C" )
        plt.ylabel( "Heat Flow" )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( ip.output_directory + "DSC/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction_bool:

            data_extraction[0] = np.pad( data_extraction[0], (0, 500) )
            data_extraction[1] = np.pad( data_extraction[1], (0, 500) )

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

        return shiny_de

def plot_variance( directory, output_directory, data, mask, s, std_c, std_m ):

    resin_data = gu.get_list_of_resins_data( directory )

    plt.gca().set_prop_cycle( cycler( color = ['c', 'c', 'm', 'm', 'y', 'y', 'k', 'k', 'g', 'g'] ) )

    for i in mask:

        plt.plot( data[0], data[1][i], linewidth = 1 )
        plt.plot( data[2], data[3][i], linewidth = 1, label = i )

    x_axis_1 = np.linspace( 0, 0, len( data[0] ) )
    x_axis_2 = np.linspace( 0, 0, len( data[2] ) )

    plt.gca().set_prop_cycle( cycler( color = ['c', 'm'] ) )

    plt.fill_between( data[0], std_c, x_axis_1, linewidth = 1.5 )
    plt.fill_between( data[2], -np.array( std_m ), x_axis_2, linewidth = 1.5 )

    plt.title( resin_data.loc[s]["Label"] )
    plt.xlabel( "Temperature (°C)" )
    plt.ylabel( "Normalised Heat Flow" )
    plt.legend()
    plt.savefig( output_directory + resin_data.loc[s]["Label"] + ".pdf" )
    plt.close()
