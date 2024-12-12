# Imports.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( ip, file_data, data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "Colour/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    samples_to_plot = samples_present
    samples_to_plot = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]
    samples_to_plot = [16, 17, 19, 24, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 20, 21, 22, 23]

    specimens = False
    all_specimens = True
    specimen_mask = []

    mean = True

    if ip.shiny:

        samples_to_plot = ip.shiny_samples_to_plot

        if type( samples_to_plot ) == int:

            samples_to_plot = [samples_to_plot]

        specimen_mask = ip.shiny_specimens_to_plot

        if type( specimen_mask ) == int:

            specimen_mask = [specimen_mask]

        mean = ip.shiny_mean
        specimens = ip.shiny_specimen
        all_specimens = False

    if specimens:

        if ip.shiny:

            specimen_mask_2 = []

            for i in range( len( file_data ) ):

                if file_data[i][2] in specimen_mask:

                    specimen_mask_2.append( True )

                else:

                    specimen_mask_2.append( False )

            features = features[specimen_mask_2, :]

            return features[:, 0].tolist(), features[:, 1].tolist(), features[:, 2].tolist()

        specimen_mask = gu.produce_mask( sample_array, samples_to_plot )

        features = features[specimen_mask, :]
        file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
        file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
        sample_array = sample_array[specimen_mask]

        ab_euclidean = np.sqrt( features[:, 1] * features[:, 1] + features[:, 2] * features[:, 2] )

        gu.plot_scatterplot_of_two_features( ip.directory, ab_euclidean, features[:, 0], sample_array, [f[2] for f in file_data], line_of_best_fit = False, xlabel = "sqrt(a*^2 + b*^2)", ylabel = "L*", savefig = savefig, filename = ip.output_directory + "Colour/Plots/L_vs_Colour.pdf" )

        gu.plot_scatterplot_of_three_features( ip.directory, features[:, 1], features[:, 2], features[:, 0], sample_array, [f[2] for f in file_data], title = "", xlabel = "a*", ylabel = "b*", zlabel = "L*", savefig = savefig, filename = ip.output_directory + "Colour/Plots/3D.pdf" )

    if mean:

        # resin_colours = pd.read_csv( ip.output_directory + "Colour/Sandbox/rgb_colours.csv", header = None )
        #
        # resin_colours[0] = resin_colours[0].astype( int )
        #
        # resin_colours.index = resin_colours[0]
        #
        # resin_colours.drop( columns = [0], inplace = True )
        #
        # resin_colours_list = [[resin_colours.loc[s, 1] / 255, resin_colours.loc[s, 2] / 255, resin_colours.loc[s, 3] / 255] for s in samples_to_plot]

        mean_features = gu.extract_mean_features( features, sample_array, samples_to_plot )

        if ip.shiny:

            return mean_features[:, 0], mean_features[:, 1], mean_features[:, 2]

        std_of_features = gu.extract_std_of_features( features, sample_array, samples_to_plot )

        ab_euclidean = np.sqrt( features[:, 1] * features[:, 1] + features[:, 2] * features[:, 2] )

        ab_euclidean_mean = gu.extract_mean_features( ab_euclidean[:, np.newaxis], sample_array, samples_to_plot )

        ab_euclidean_std = gu.extract_std_of_features( ab_euclidean[:, np.newaxis], sample_array, samples_to_plot )

        # gu.plot_scatterplot_of_two_features( ip.directory, ab_euclidean_mean[:, 0], mean_features[:, 0], samples_to_plot, [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = [ab_euclidean_std[:, 0], std_of_features[:, 0]], line_of_best_fit = False, xlabel = "sqrt(a*^2 + b*^2)", ylabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/L_vs_Colour.pdf" )

        # gu.plot_scatterplot_of_two_features( ip.directory, mean_features[:, 1], mean_features[:, 0], resin_colours_list, [resin_data.loc[i]["Label"] for i in samples_to_plot], line_of_best_fit = False, xlabel = "a*", ylabel = "L*", savefig = savefig, filename = ip.output_directory + "Colour/Plots/L_vs_a.pdf" )

        # gu.plot_scatterplot_of_two_features( ip.directory, mean_features[:, 2], mean_features[:, 0], resin_colours_list, [resin_data.loc[i]["Label"] for i in samples_to_plot], line_of_best_fit = False, xlabel = "b*", ylabel = "L*", savefig = savefig, filename = ip.output_directory + "Colour/Plots/L_vs_b.pdf" )

        gu.plot_scatterplot_of_three_features( ip.directory, mean_features[:, 1], mean_features[:, 2], mean_features[:, 0], samples_to_plot, [resin_data.loc[i]["Label"] for i in samples_to_plot], title = "", xlabel = "a*", ylabel = "b*", zlabel = "L*", savefig = savefig, filename = ip.output_directory + "Colour/Plots/3D.pdf" )

    return [], [], []