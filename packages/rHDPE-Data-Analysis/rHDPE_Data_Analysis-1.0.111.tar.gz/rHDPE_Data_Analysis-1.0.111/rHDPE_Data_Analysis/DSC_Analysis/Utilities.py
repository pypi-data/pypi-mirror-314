# Imports.

import numpy as np
import pandas as pd

from . import DSC_plotting

from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [data[0][width: -width], [], data[2][width: -width], [], [], []]

    for i in range( len( data[1] ) ):

        derivative_data[1].append( np.array( gu.derivative( data[0], data[1][i], width ) ) )
        derivative_data[3].append( np.array( gu.derivative( data[2], data[3][i], width ) ) )

    for i in range( len( data[4] ) ):

        derivative_data[4].append( np.array( gu.derivative( data[0], data[4][i], width ) ) )
        derivative_data[5].append( np.array( gu.derivative( data[2], data[5][i], width ) ) )

    return derivative_data

def half_peak_width( temp, heat_flow, melt = False ):

    if not melt:

        peak = heat_flow.max()

    else:

        peak = heat_flow.min()

    half_peak = peak / 2

    if not melt:

        mask = np.where( heat_flow >= half_peak )[0]

    else:

        mask = np.where( heat_flow <= half_peak )[0]

    new_temp = temp[mask]

    temp_max = new_temp.max()
    temp_min = new_temp.min()

    return temp_max - temp_min

def extract_DSC_features( output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    # Temp and Heat Flow of maximum of cryst second derivative between 120-130.

    feature_1, feature_2 = [], []

    temp_mask = np.where( (second_derivative_data[0] <= 130) & (second_derivative_data[0] >= 120) )[0]

    for i in range( len( file_data ) ):

        array = second_derivative_data[1][i][temp_mask]

        feature_1.append( array.max() )
        feature_2.append( second_derivative_data[0][temp_mask][np.argmax( array )] )

    features = np.array( feature_1 )[:, np.newaxis]

    features = np.hstack( (features, np.array( feature_2 )[:, np.newaxis]) )

    feature_names = ["DSC_HFC_120", "DSC_TC_120"]

    # Minimum of cryst first derivative between 80 and 90.

    feature_1 = []

    temp_mask = np.where( (first_derivative_data[0] <= 90) & (first_derivative_data[0] >= 80) )[0]

    for i in range( len( file_data ) ):

        array = first_derivative_data[1][i][temp_mask]

        feature_1.append( array.min() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_HFC_80" )

    # Temp and Heat Flow at maximum cryst heat flow and maximum melt heat flow.

    feature_1, feature_2, feature_3, feature_4 = [], [], [], []

    for i in range( len( file_data ) ):

        feature_1.append( data[0][np.argmax( data[1][i] )] )
        feature_2.append( data[1][i].max() )
        feature_3.append( data[2][np.argmin( data[3][i] )] )
        feature_4.append( data[3][i].min() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis], np.array( feature_2 )[:, np.newaxis], np.array( feature_3 )[:, np.newaxis], np.array( feature_4 )[:, np.newaxis]) )

    feature_names.append( "DSC_TC_Max" )
    feature_names.append( "DSC_HFC_Max" )
    feature_names.append( "DSC_TM_Max" )
    feature_names.append( "DSC_HFM_Max" )

    # Max second derivative between 160 and 170.

    feature_1 = []

    temp_mask = np.where( (second_derivative_data[2] <= 170) & (second_derivative_data[2] >= 160) )[0]

    for i in range( len( file_data ) ):

        array = second_derivative_data[3][i][temp_mask]

        feature_1.append( array.max() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_HFM_160" )

    # Cryst and melt half-peak widths.

    feature_1, feature_2 = [], []

    for i in range( len( file_data ) ):

        feature_1.append( half_peak_width( data[0], data[1][i] ) )
        feature_2.append( half_peak_width( data[2], data[3][i], melt = True ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis], np.array( feature_2 )[:, np.newaxis]) )

    feature_names.append( "DSC_C_HalfPeak" )
    feature_names.append( "DSC_M_HalfPeak" )

    # Minimum of cryst second derivative between 102 and 106.

    feature_1 = []

    temp_mask = np.where( (second_derivative_data[0] <= 106) & (second_derivative_data[0] >= 102) )[0]

    for i in range( len( file_data ) ):

        array = second_derivative_data[1][i][temp_mask]

        feature_1.append( array.min() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_HFC_102" )

    # Cryst onset temperature.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( first_derivative_data[0][np.where( (first_derivative_data[1][i] < -0.2) )[0][0]] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_C_Onset" )

    # Melt onset temperature.

    feature_1 = []

    temp_mask = np.where( (first_derivative_data[2] <= 145) )[0]

    for i in range( len( file_data ) ):

        array = np.where( (first_derivative_data[3][i][temp_mask] > 0.1) )[0]

        feature_1.append( first_derivative_data[2][temp_mask][array[len( array ) - 1]] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_M_Onset" )

    # Crystallinity and PP content.

    feature_1, feature_2 = [], []

    temp_mask_1 = np.where( (data[2] <= 145) & (data[2] >= 65) )[0]
    temp_mask_2 = np.where( (data[2] <= 170) & (data[2] >= 143) )[0]

    for i in range( len( file_data ) ):

        integral_1 = gu.integral_2( data[2][temp_mask_1], -data[3][i][temp_mask_1], 0, len( data[2][temp_mask_1] ) - 1, min( -data[3][i][temp_mask_1][0], -data[3][i][temp_mask_1][len( data[3][i][temp_mask_1] ) - 1] ) ) / 293 * 6
        integral_2 = gu.integral_2( data[2][temp_mask_2], -data[3][i][temp_mask_2], 0, len( data[2][temp_mask_2] ) - 1, min( -data[3][i][temp_mask_2][0], -data[3][i][temp_mask_2][len( data[3][i][temp_mask_2] ) - 1] ) ) / 208 * 6 / 0.5

        if integral_2 < 0:

            integral_2 = 0

        # fpp = integral_2 / (integral_1 + integral_2)

        integral_1 = integral_1 / (1 - integral_2)

        integral_1 = integral_1 * 100
        integral_2 = integral_2 * 100

        feature_1.append( integral_1 )
        feature_2.append( integral_2 )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis], np.array( feature_2 )[:, np.newaxis]) )

    feature_names.append( "DSC_Crystallinity" )
    feature_names.append( "DSC_fPP" )

    # Modified melt temperature.

    feature_1 = []

    for i in range( len( file_data ) ):

        temp_mask_1 = np.where( (data[2] >= data[2][data[3][i].argmin()]) & (data[3][i] >= -2) )[0]

        feature_1.append( data[2][temp_mask_1[0]] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "DSC_Melt_Temp" )

    df = gu.array_with_column_titles_to_df( features, feature_names )

    df.to_csv( output_directory + "DSC/Features/Features.csv" )

# Crystallinity values from Andy.
#
# crystallinity = [0, 65.5, 64.3, 66, 64.1, 61.3, 61.8, 62.6, 58.5, 61.7, 60.7, 60, 68.2, 60.5, 65.2, 74.1, 66.3, 69, 59.4, 73, 62.4, 62.5, 61.2, 51.1, 66.7]

def read_and_analyse_features( ip, file_data ):

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "DSC/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]
        # ip.sample_mask = [17, 16, 19, 24, 1, 12, 15, 6, 7, 2, 3, 5, 9, 8, 13, 11, 14, 20, 21, 10, 18, 4, 22, 23]
        # ip.sample_mask = [16, 17, 19, 24, 12, 15, 1, 2, 3, 5, 6, 7, 8, 9, 4, 10, 13, 11, 14, 18, 20, 21, 22, 23]

    sample_mask = ip.sample_mask

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    if not ip.feature_selection:

        # ip.feature_selection = [i for i in range( len( feature_names ) )]
        ip.feature_selection = [7, 8, 9, 10, 13]
        # ip.feature_selection = [8, 9, 11, 12, 13, 14]
        # ip.feature_selection = [14, 13, 12, 11, 9, 8]

    feature_selection = ip.feature_selection

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    mean_features_unnormalised = gu.extract_mean_features( features, sample_array, samples_present )
    mean_feature_names = feature_names.copy()

    mean_features_unnormalised_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], mean_features_unnormalised) )

    df = gu.array_with_column_titles_to_df( mean_features_unnormalised_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "DSC/Features/Mean_Features_Unnormalised.csv" )

    std_of_features = gu.extract_std_of_features( features, sample_array, samples_present )

    std_of_features_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "DSC/Features/Std_of_Features_Unnormalised.csv" )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features = features[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    feature_weights = [1 for i in range( len( feature_selection ) )]

    gu.normalise_features( features, feature_weights )

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "DSC/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "DSC/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "DSC/Features/Distance_Matrix.csv" )

    # Perform PCA for DSC features.

    # gu.perform_pca( ip.directory, gu.array_with_column_titles_to_df( mean_features, [str( i ) for i in mean_feature_names] ), sample_mask, std_error = True, std_of_features_df = pd.DataFrame( std_of_features ), num_components = 2, filename = ip.output_directory + "DSC/Features/PCA.pdf" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "DSC/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "DSC/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "DSC/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "DSC/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "DSC/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "DSC/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "DSC/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "DSC/Features/", title = "Means_Dendrogram.pdf" )

def variance_analysis( directory, output_directory, file_data, data ):

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    integral_c, integral_m = np.zeros( len( sample_mask ) ), np.zeros( len( sample_mask ) )

    for i, s in enumerate( sample_mask ):

        mask = np.where( sample_array == s )[0]

        range_c, high_point_c, low_point_c, median_c, mean_c, std_c = gu.compute_range_mean_std( data[1], mask )
        range_m, high_point_m, low_point_m, median_c, mean_m, std_m = gu.compute_range_mean_std( data[3], mask )

        DSC_plotting.plot_variance( directory, output_directory + "DSC/Sandbox/Variance/", data, mask, s, std_c, std_m )

        if len( mask ) >= 3:

            integral_c[i] = gu.integral_3( np.array( std_c ), 0.1 )
            integral_m[i] = gu.integral_3( np.array( std_m ), 0.1 )

    nonzero_mask = np.nonzero( integral_c )[0]
    integral_c = integral_c[nonzero_mask]
    integral_m = integral_m[nonzero_mask]
    sample_mask = np.array( sample_mask )[nonzero_mask]

    gu.plot_barchart_of_feature( integral_c, [resin_data.loc[i]["Label"] for i in sample_mask], colour = True, colour_mask = sample_mask, xlabel = "PCR Sample", ylabel = "Integral of Standard Deviation", title = "Variance of Samples during Crystallisation", filename = output_directory + "DSC/Sandbox/Variance/BarCryst.pdf", savefig = True )

    gu.plot_barchart_of_feature( integral_m, [resin_data.loc[i]["Label"] for i in sample_mask], colour = True, colour_mask = sample_mask, xlabel = "PCR Sample", ylabel = "Integral of Standard Deviation", title = "Variance of Samples during Melt", filename = output_directory + "DSC/Sandbox/Variance/BarMelt.pdf", savefig = True )

def identify_anomalies( file_data, data ):

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    for s in sample_mask:

        mask = np.where( sample_array == s )[0]

        if len( mask ) < 3:

            print( "Less than three specimens of sample {} so no specimens removed".format( s ) )

            continue

        for i in mask:

            anomalous_cryst, anomalous_melt = False, False

            other_specimens = [j for j in mask if j != i]

            range_s, high_point, low_point, median, mean, std = gu.compute_range_mean_std( data[1], other_specimens )

            for j in range( len( data[1][0] ) ):

                value = data[1][i][j]

                error = 0.6 + 3 * std[j]

                if value < mean[j] - error or value > mean[j] + error:

                    anomalous_cryst = True

                    print( file_data[i][2], "should be removed due to value {} during crystallisation at {}".format( value, data[0][j] ) )

                    for l in mask:

                        print( data[1][l][j] )

                    print( mean[j], error )

                    break

            range_s, high_point, low_point, median, mean, std = gu.compute_range_mean_std( data[3], other_specimens )

            for j in range( len( data[3][0] ) ):

                value = data[3][i][j]

                error = 0.6 + 3 * std[j]

                if value < mean[j] - error or value > mean[j] + error:

                    anomalous_melt = True

                    print( file_data[i][2], "should be removed due to value {} during melt at {}".format( value, data[2][j] ) )

                    for l in mask:

                        print( data[3][l][j] )

                    print( mean[j], error )

                    break

            if anomalous_melt and anomalous_cryst:

                print( file_data[i], "should be removed." )

def boxplot_variance( directory, output_directory, file_data, data ):

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( output_directory + "DSC/Features/Features.csv" )
    # _, std_of_features = gu.csv_to_df_to_array_and_column_titles( output_directory + "DSC/Features/Std_of_Features.csv" )

    feature_selection = [8, 9, 11, 12, 13, 14]

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    range_of_features = gu.extract_range_of_features( features, sample_array, sample_mask )

    print( feature_names )
    print( np.ptp(features, axis = 0))
    print( np.mean( range_of_features, axis = 0))
    print(np.mean( range_of_features, axis = 0) / np.ptp(features, axis = 0))

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    gu.plot_boxplot( directory, features, feature_names, file_data, sample_mask, "DSC_C_Onset", xlabel = "Samples", ylabel = "Secondary Peak at 160°C" )

def comparison_of_different_machines( directory, output_directory, file_data ):

    resin_data = gu.get_list_of_resins_data( directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( output_directory + "DSC/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    feature_weights = [1 for i in range( len( features[0] ) )]

    # gu.normalise_features( features, feature_weights )

    mean_features = gu.extract_mean_features( features, sample_array, samples_present )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( features, sample_array, samples_present )

    samples_to_compare = [1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    feature_name = "DSC_M_Onset"

    x_values = [mean_features[samples_present.index( i )][feature_names.index( feature_name )] for i in samples_to_compare]
    y_values = [mean_features[samples_present.index( i + 100 )][feature_names.index( feature_name )] for i in samples_to_compare]

    gu.plot_scatterplot_of_two_features( x_values, y_values, samples_to_compare, [resin_data.loc[i]["Label"] for i in samples_to_compare], line_of_best_fit = False, xlabel = "PP Content from Machine 1", ylabel = "PP Content from Machine 2" )

def sandbox( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    perform_variance_analysis = False # Perform computations relating to variance.

    perform_identify_anomalies = False # Identifies anomalies based on standard deviations.

    perform_boxplot_variance = True # Plot boxplots of variance of features for specimens.

    perform_comparison_of_different_machines = False # Compare curves obtained from different machines.

    if perform_variance_analysis:

        variance_analysis( directory, output_directory, file_data, data )

    if perform_identify_anomalies:

        identify_anomalies( file_data, data )

    if perform_boxplot_variance:

        boxplot_variance( directory, output_directory, file_data, data )

    if perform_comparison_of_different_machines:

        comparison_of_different_machines( directory, output_directory, file_data )
