# Imports.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data, m_peaks, m_peaks_array, y_peaks, y_peaks_array, savefig = False ):

    # for i in range( len( data[1] ) ):
    #
    #     # data[1][i] = (data[1][i] / data[1][i].max())
    #     data[1][i] = ((data[1][i] - data[1][i].min()) / (data[1][i].max() - data[1][i].min()))
    #
    # for i in range( len( data[2] ) ):
    #
    #     # data[1][i] = (data[1][i] / data[1][i].max())
    #     data[2][i] = ((data[2][i] - data[2][i].min()) / (data[2][i].max() - data[2][i].min()))

    resin_data = gu.get_list_of_resins_data( ip.directory, ip.name_appendage )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 3 #4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    # samples_to_plot = samples_present
    samples_to_plot = [1, 2, 3, 4, 701]

    specimens = False
    all_specimens = True
    specimen_mask_by_index = [0, 1, 3]
    specimen_mask = []

    mean = True

    plot_mean_peaks = False
    plot_specimen_peaks = False

    deriv0 = True
    deriv1 = False
    deriv2 = False
    deriv3 = False

    split = True
    # splits = [int( data[0][len( data[0] ) - 1] ), 800, 1400, 1500, 2000, 2700, 3000, int( data[0][0] )]
    # splits = [600, 650, 700, 750, 800, 850, 900, 950, 1000]
    # splits = [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]
    # splits = [2000, 2050, 2100, 2150, 2200, 2250, 2300, 2350, 2400, 2450, 2500, 2550, 2600, 2650, 2700, 2750, 2800, 2850, 2900, 2950, 3000]
    # splits = [3000, 3050, 3100, 3150, 3200, 3250, 3300, 3350, 3400, 3450, 3500, 3550, 3600, 3650, 3700, 3750, 3800, 3850, 3900, 3950, 4000]
    # splits = [3000, 4000]
    # splits = [600, 1000, 1400, 1800, 2200, 2600, 3000]
    splits = [800, 1000]

    if not split:

        splits = [int( data[0][len( data[0] ) - 1] ), int( data[0][0] )]

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

            if plot_mean_peaks:

                index = np.where( samples_present_array == i )[0][0]

                for p in range( len( m_peaks ) ):

                    if m_peaks[p] > lower_bound and m_peaks[p] < upper_bound:

                        if m_peaks_array[index][p] > 0.0001:

                            plt.axvline( x = m_peaks[p], color = colours[samples_present[index]] )

            if specimens:

                mask = np.where( sample_array == i )[0]

                if not ip.shiny:

                    if all_specimens:

                        specimen_mask = [file_data[mask[j]][2] for j in range( len( mask ) )]

                    else:

                        specimen_mask = [file_data[mask[j]][2] for j in specimen_mask_by_index]

                for j in mask:

                    if file_data[j][2] in specimen_mask:

                        if plot_specimen_peaks:

                            for p in range( len( y_peaks ) ):

                                if y_peaks[p] > lower_bound and y_peaks[p] < upper_bound:

                                    if y_peaks_array[j][p] > 0.0001:

                                        plt.axvline( x = y_peaks[p] )

                        if deriv0:

                            wn_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                            plt.plot( data[0][wn_mask], data[1][j][wn_mask], label = file_data[j][2] )

                            shiny_de.append( data[0][wn_mask].tolist() )
                            shiny_de.append( data[1][j][wn_mask].tolist() )

                        if deriv1:

                            wn_mask = np.where( (first_derivative_data[0] <= upper_bound) & (first_derivative_data[0] >= lower_bound) )[0]

                            plt.plot( first_derivative_data[0][wn_mask], first_derivative_data[1][j][wn_mask], label = file_data[j][2] )

                        if deriv2:

                            wn_mask = np.where( (second_derivative_data[0] <= upper_bound) & (second_derivative_data[0] >= lower_bound) )[0]

                            plt.plot( second_derivative_data[0][wn_mask], second_derivative_data[1][j][wn_mask], label = file_data[j][2] )

                        if deriv3:

                            wn_mask = np.where( (third_derivative_data[0] <= upper_bound) & (third_derivative_data[0] >= lower_bound) )[0]

                            plt.plot( third_derivative_data[0][wn_mask], third_derivative_data[1][j][wn_mask], label = file_data[j][2] )

            if mean:

                index = np.where( samples_present_array == i )[0][0]

                if deriv0:

                    wn_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                    plt.plot( data[0][wn_mask], data[2][index][wn_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    shiny_de.append( data[0][wn_mask].tolist() )
                    shiny_de.append( data[2][index][wn_mask].tolist() )

                if deriv1:

                    wn_mask = np.where( (first_derivative_data[0] <= upper_bound) & (first_derivative_data[0] >= lower_bound) )[0]

                    plt.plot( first_derivative_data[0][wn_mask], first_derivative_data[2][index][wn_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv2:

                    wn_mask = np.where( (second_derivative_data[0] <= upper_bound) & (second_derivative_data[0] >= lower_bound) )[0]

                    plt.plot( second_derivative_data[0][wn_mask], second_derivative_data[2][index][wn_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                if deriv3:

                    wn_mask = np.where( (third_derivative_data[0] <= upper_bound) & (third_derivative_data[0] >= lower_bound) )[0]

                    plt.plot( third_derivative_data[0][wn_mask], third_derivative_data[2][index][wn_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    # data_extraction.append( third_derivative_data[0][wn_mask] )
                    # data_extraction.append( third_derivative_data[2][index][wn_mask] )

        if ip.shiny:

            return shiny_de

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )
        # plt.legend( ncol = 2, loc = 'upper right', borderaxespad = 0, fontsize = 20 )
        # plt.legend()

        plt.xlabel( "Wavenumber [cm\u207b\u00b9]", fontsize = 20 )
        plt.ylabel( "Absorbance", fontsize = 20 )
        plt.xticks( fontsize = 20 )
        plt.yticks( fontsize = 20 )

        ax = plt.gca()
        ax.invert_xaxis()

        plt.tight_layout()

        # For overall pipeline figure.

        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( ip.output_directory + "FTIR/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction_bool:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

    return shiny_de
