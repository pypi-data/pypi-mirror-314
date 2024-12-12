# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_crossover_points( directory, output_directory, resin_data, file_data, sample_array, samples_to_plot, specimens, mean, data_extraction_bool, savefig ):

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( output_directory + "Rheology/Features/Features.csv" )

    features_df = gu.array_with_column_titles_to_df( features, feature_names )

    specimen_mask = gu.produce_mask( sample_array, samples_to_plot )

    features_df_copy = features_df.iloc[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array_copy = sample_array[specimen_mask]

    if specimens:

        gu.plot_scatterplot_of_two_features( directory, features_df_copy["Rhe_Crossover"].apply( lambda x: 10 ** x ), features_df_copy["Rhe_SMCrossover"].apply( lambda x: 10 ** x ), sample_array_copy, [f[2] for f in file_data_mask], line_of_best_fit = False, xlog = True, ylog = True, xlabel = "Angular Frequency [rad/s]", ylabel = "Storage/Loss Modulus [Pa]", savefig = savefig, filename = output_directory + "Rheology/Plots/Crossover_Point_Specimen.pdf" )

    if mean:

        mean_features = gu.extract_mean_features( features_df.to_numpy(), sample_array, samples_to_plot )

        mean_features_df = gu.array_with_column_titles_to_df( mean_features, features_df_copy.columns )

        gu.plot_scatterplot_of_two_features( directory, mean_features_df["Rhe_Crossover"].apply( lambda x: 10 ** x ), mean_features_df["Rhe_SMCrossover"].apply( lambda x: 10 ** x ), sample_array_copy, [resin_data.loc[i]["Label"] for i in samples_to_plot], line_of_best_fit = False, xlog = True, ylog = True, xlabel = "Angular Frequency [rad/s]", ylabel = "Storage/Loss Modulus [Pa]", savefig = savefig, filename = output_directory + "Rheology/Plots/Crossover_Point_Mean.pdf" )

def plot_van_Gurp_Palmen_plot( ip, resin_data, file_data, data, splits, sample_array, samples_present_array, samples_to_plot, specimens, mean, colours, data_extraction_bool, savefig ):

    shiny_de = []

    data_extraction = []

    lower_bound, upper_bound = splits[0], splits[1]

    if specimens:

        for i in samples_to_plot:

            mask = np.where( sample_array == i )[0]

            for ind, j in enumerate( mask ):

                xaxis_mask = np.where( (data[3][j] * data[0] <= upper_bound) & (data[3][j] * data[0] >= lower_bound) )[0]

                # deriv = gu.derivative( np.log( data[3][j] * data[0] ), np.arctan( data[4][j] ) )

                plt.scatter( data[3][j] * data[0], data[4][j], label = file_data[j][2], color = colours[i] )

                shiny_de.append( (data[3][j][xaxis_mask] * data[0][xaxis_mask]).tolist() )
                shiny_de.append( data[4][j][xaxis_mask].tolist() )

                # data_extraction.append( data[3][j] * data[0] )
                # data_extraction.append( data[4][j] )

                # plt.scatter( data[3][j][1:-1] * data[0][1:-1], deriv, label = file_data[j][2], color = colours[i] )

        ax = plt.gca()
        ax.set_xscale( 'log' )
        plt.xlabel( "Complex Modulus [Pa]" )
        plt.ylabel( "Phase Angle [°]" )
        # plt.legend( ncol = 3, loc = 'lower right', borderaxespad = 0 )
        plt.tight_layout()

        if savefig:

            plt.savefig( ip.output_directory + "Rheology/Plots/vGP_Specimens.pdf" )

        else:

            plt.show()

        plt.close()

    if mean:

        for i in samples_to_plot:

            index = np.where( samples_present_array == i )[0][0]

            xaxis_mask = np.where( (data[7][index] * data[0] <= upper_bound) & (data[7][index] * data[0] >= lower_bound) )[0]

            plt.scatter( data[7][index][xaxis_mask] * data[0][xaxis_mask], np.arctan( data[8][index][xaxis_mask] ) * 180 / np.pi, label = resin_data.loc[i]["Label"], color = colours[i] )

            shiny_de.append( (data[7][index][xaxis_mask] * data[0][xaxis_mask]).tolist() )
            shiny_de.append( (np.arctan( data[8][index][xaxis_mask] ) * 180 / np.pi).tolist() )

            data_extraction.append( data[7][index][xaxis_mask] * data[0][xaxis_mask] )
            data_extraction.append( np.arctan( data[8][index][xaxis_mask] ) * 180 / np.pi )

        ax = plt.gca()
        ax.set_xscale( 'log' )
        plt.xlabel( "Complex Modulus [Pa]" )
        plt.ylabel( "Phase Angle [°]" )
        plt.legend( ncol = 3, bbox_to_anchor = ( 0.880, 0 ), loc = 'lower center', borderaxespad = 0 )
        plt.tight_layout()

        if savefig:

            plt.savefig( ip.output_directory + "Rheology/Plots/vGP_Means.pdf" )

        else:

            plt.show()

        plt.close()

        if ip.shiny:

            return shiny_de

        if data_extraction_bool:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

def plot_data( ip, file_data, data, first_derivative_data, second_derivative_data, savefig = False ):

    perform_plot_crossover_points = False

    perform_van_Gurp_Palmen_plot = True

    perform_custom_plot = False

    resin_data = gu.get_list_of_resins_data( ip.directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    samples_to_plot = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]
    samples_to_plot = [16, 17, 19, 24, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 20, 21, 22, 23]
    samples_to_plot = [16, 17, 4, 8, 9, 23]

    specimens = False
    all_specimens = True
    specimen_mask_by_index = [0]
    specimen_mask = []

    mean = True

    deriv0 = True
    deriv1 = False
    deriv2 = False

    split = False
    num_splits = 2
    split_length = 120
    splits = [split_length * (i + 30 / 120) for i in range( num_splits )]
    splits = [0.1, 0.5]

    log_graph = True

    radial_graph = False

    x, y = 0, 3 # 0:af, 1:sm, 2:lm, 3:cv, 4:lf, 5-8 same but means.

    if not split:

        if perform_van_Gurp_Palmen_plot:

            splits = [0, 500000]

        else:

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
        perform_plot_crossover_points = False

        if ip.shiny_vgp == True:

            perform_van_Gurp_Palmen_plot = True
            perform_custom_plot = False

        else:

            perform_van_Gurp_Palmen_plot = False
            perform_custom_plot = True

            if ip.shiny_cv_vs_af == True:

                if specimens:

                    x, y = 0, 3

                else:

                    x, y = 0, 7

            elif ip.shiny_pa_vs_cv == True:

                if specimens:

                    x, y = 3, 4

                else:

                    x, y = 7, 8

        radial_graph = False
        log_graph = False

    colours = gu.read_list_of_colours( ip.directory )

    shiny_de = []

    data_extraction_bool = True

    if perform_plot_crossover_points:

        plot_crossover_points( ip.directory, ip.output_directory, resin_data, file_data, sample_array, samples_to_plot, specimens, mean, data_extraction_bool, savefig )

    if perform_van_Gurp_Palmen_plot:

        return plot_van_Gurp_Palmen_plot( ip, resin_data, file_data, data, splits, sample_array, samples_present_array, samples_to_plot, specimens, mean, colours, data_extraction_bool, savefig )

    if perform_custom_plot:

        for s in range( len( splits ) - 1 ):

            data_extraction = []

            lower_bound, upper_bound = splits[s], splits[s + 1]

            if radial_graph:

                ax = plt.subplots( 1, 1, subplot_kw = dict( polar = True ) )[1]

                for i in samples_to_plot:

                    index = np.where( samples_present_array == i )[0][0]

                    freq_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                    alpha_scale = np.linspace( 0.3, 1, len( data[8][index][freq_mask] ) )

                    ax.scatter( np.arctan( data[8][index][freq_mask] ), data[7][index][freq_mask], label = resin_data.loc[i]["Label"], color = colours[i], alpha = alpha_scale, s = 25 )

                ax.set_rlim( 3, 170000 )
                ax.set_thetamin( 30 )
                ax.set_thetamax( 75 )
                ax.set_rscale( 'symlog' )

                r = np.arange( 0, 170000, 10 )
                theta = [np.pi / 4 for i in r]
                ax.plot( theta, r, "k--" )

            else:

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

                                    if x == 0:

                                        if y == 4:

                                            data[y][j] = np.arctan( data[y][j] ) * 180 / np.pi

                                        xaxis_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                                        plt.plot( data[0][xaxis_mask], data[y][j][xaxis_mask], label = file_data[j][2], color = colours[i], linestyle = "None", marker = "o" )

                                        # plt.plot( data[0][xaxis_mask], data[1][j][xaxis_mask], label = "Storage Modulus", color = colours[i] )
                                        # plt.plot( data[0][xaxis_mask], data[2][j][xaxis_mask], label = "Loss Modulus", color = colours[i] )

                                        # plt.plot( data[0][freq_mask], data[0][freq_mask] ** m * np.exp( b ), "--", color = colours[i], linewidth = 2.5 )

                                        shiny_de.append( data[0][xaxis_mask].tolist() )
                                        shiny_de.append( data[y][j][xaxis_mask].tolist() )

                                        # m = (np.log( data[3][j][3] ) - np.log( data[3][j][1] )) / (np.log( data[0][3] ) - np.log( data[0][1] ))
                                        # b = np.log( data[3][j][2] / data[0][2] ** m )
                                        #
                                        data_extraction.append( data[0][xaxis_mask] )
                                        data_extraction.append( data[y][j][xaxis_mask] )
                                        # data_extraction.append( data[2][j][xaxis_mask] )

                                    else:

                                        if x == 4:

                                            data[x][j] = np.arctan( data[x][j] ) * 180 / np.pi

                                        if y == 4:

                                            data[y][j] = np.arctan( data[y][j] ) * 180 / np.pi

                                        xaxis_mask = np.where( (data[x][j] <= upper_bound) & (data[x][j] >= lower_bound) )[0]

                                        plt.plot( data[x][j][xaxis_mask], data[y][j][xaxis_mask], label = file_data[j][2], color = colours[i], linestyle = "None", marker = "o" )

                                        shiny_de.append( data[x][j][xaxis_mask].tolist() )
                                        shiny_de.append( data[y][j][xaxis_mask].tolist() )

                                if deriv1:

                                    freq_mask = np.where( (first_derivative_data[0] <= upper_bound) & (first_derivative_data[0] >= lower_bound) )[0]

                                    # Minus sign for log graph!

                                    plt.plot( first_derivative_data[0][freq_mask], -first_derivative_data[3][j][freq_mask], label = file_data[j][2], color = colours[i] )

                                if deriv2:

                                    freq_mask = np.where( (second_derivative_data[0] <= upper_bound) & (second_derivative_data[0] >= lower_bound) )[0]

                                    plt.plot( second_derivative_data[0][freq_mask], second_derivative_data[3][j][freq_mask], label = file_data[j][2], color = colours[i] )

                    if mean:

                        index = np.where( samples_present_array == i )[0][0]

                        if deriv0:

                            if x == 0:

                                if y == 8:

                                    data[y][index] = np.arctan( data[y][index] ) * 180 / np.pi

                                xaxis_mask = np.where( (data[0] <= upper_bound) & (data[0] >= lower_bound) )[0]

                                plt.plot( data[0][xaxis_mask], data[y][index][xaxis_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                                shiny_de.append( data[0][xaxis_mask].tolist() )
                                shiny_de.append( data[y][index][xaxis_mask].tolist() )

                            else:

                                if x == 8:

                                    data[x][index] = np.arctan( data[x][index] ) * 180 / np.pi

                                if y == 8:

                                    data[y][index] = np.arctan( data[y][index] ) * 180 / np.pi

                                xaxis_mask = np.where( (data[x][index] <= upper_bound) & (data[x][index] >= lower_bound) )[0]

                                plt.plot( data[x][index][xaxis_mask], data[y][index][xaxis_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                                shiny_de.append( data[x][index][xaxis_mask].tolist() )
                                shiny_de.append( data[y][index][xaxis_mask].tolist() )

                        if deriv1:

                            freq_mask = np.where( (first_derivative_data[0] <= upper_bound) & (first_derivative_data[0] >= lower_bound) )[0]

                            plt.plot( first_derivative_data[0][freq_mask], first_derivative_data[5][index][freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                        if deriv2:

                            freq_mask = np.where( (second_derivative_data[0] <= upper_bound) & (second_derivative_data[0] >= lower_bound) )[0]

                            plt.plot( second_derivative_data[0][freq_mask], second_derivative_data[7][index][freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

            if ip.shiny:

                return shiny_de

            if log_graph:

                ax = plt.gca()
                ax.set_xscale( 'log' )
                ax.set_yscale( 'log' )

            # plt.legend( ncol = 3, bbox_to_anchor = ( 1.010, 0 ), loc = 'center', borderaxespad = 0 )
            leg = ax.get_legend()

            # for lh in leg.legendHandles:
            #
            #     lh.set_alpha(1)

            # plt.legend( ncol = 2, loc = 'upper right', borderaxespad = 0 )
            plt.legend()

            plt.xlabel( "Angular Frequency [rad/s]" )
            plt.ylabel( "Storage / Loss Modulus [Pa]" )

            plt.tight_layout()

            # For overall pipeline figure.

            # ax = plt.gca()
            # ax.get_legend().remove()
            # plt.xlabel( "" )
            # plt.ylabel( "" )
            # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
            # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

            if savefig:

                plt.savefig( ip.output_directory + "Rheology/Plots/Plot.pdf" )

            else:

                plt.show()

            plt.close()

            if data_extraction_bool:

                array = data_extraction[0][:, np.newaxis]

                for i in range( 1, len( data_extraction ) ):

                    array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

                np.savetxt( ip.output_directory + "Plot_Coords/Unnamed.txt", array )

    return shiny_de
