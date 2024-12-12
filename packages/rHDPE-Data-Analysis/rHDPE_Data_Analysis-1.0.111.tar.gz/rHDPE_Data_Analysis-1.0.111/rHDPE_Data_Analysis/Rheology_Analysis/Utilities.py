# Imports.

import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [data[0][width:-width], [], [], [], [], [], [], [], []]

    for i in range( len( data[3] ) ):

        derivative_data[3].append( np.array( gu.derivative( data[0], data[3][i], width ) ) )

    for i in range( len( data[7] ) ):

        derivative_data[7].append( np.array( gu.derivative( data[0], data[7][i], width ) ) )

    return derivative_data

def extract_rheology_features( output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    # Viscosities at all angular frequencies.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( np.log10( data[3][i][0] ) )

    features = np.array( feature_1 )[:, np.newaxis]

    feature_names = ["Rhe_{:.2f}".format( data[0][0] )]

    for j in range( 1, len( data[0] ) ):

        feature_1 = []

        for i in range( len( file_data ) ):

            feature_1.append( np.log10( data[3][i][j] ) )

        features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

        feature_names.append( "Rhe_{:.2f}".format( data[0][j] ) )

    # SM at all angular frequencies

    for j in range( len( data[1][1] ) ):

        feature_1 = []

        for i in range( len( file_data ) ):

            feature_1.append( np.log10( data[1][i][j] ) )

        features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

        feature_names.append( "Rhe_SM_{:.2f}".format( data[0][j] ) )

    # LM at all angular frequencies

    for j in range( len( data[2][1] ) ):

        feature_1 = []

        for i in range( len( file_data ) ):

            feature_1.append( np.log10( data[2][i][j] ) )

        features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

        feature_names.append( "Rhe_LM_{:.2f}".format( data[0][j] ) )

    # Loss factor at all angular frequencies

    for j in range( len( data[4][1] ) ):

        feature_1 = []

        for i in range( len( file_data ) ):

            feature_1.append( data[4][i][j] )

        features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

        feature_names.append( "Rhe_Loss_{:.2f}".format( data[0][j] ) )

    # Crossover point.

    feature_1, feature_2 = [], []

    for i in range( len( file_data ) ):

        index_1, index_2 = -2, -1

        for j in range( len( data[4][i] ) ):

            if data[4][i][j] > 1:

                index_1 = j - 1
                index_2 = j
                break

        log_change = (np.log10( 1 ) - np.log10( data[4][i][index_1] )) / (np.log10( data[4][i][index_2] ) - np.log10( data[4][i][index_1] ))

        crossover_point = 10 ** ((np.log10( data[0][index_2] ) - np.log10( data[0][index_1] )) * log_change + np.log10( data[0][index_1] ))

        storage_modulus_crossover_point = 10 ** ((np.log10( data[1][i][index_2] ) - np.log10( data[1][i][index_1] )) * log_change + np.log10( data[1][i][index_1] ))

        feature_1.append( np.log10( crossover_point ) )
        feature_2.append( np.log10( storage_modulus_crossover_point ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )
    features = np.hstack( (features, np.array( feature_2 )[:, np.newaxis]) )

    feature_names.append( "Rhe_Crossover" )
    feature_names.append( "Rhe_SMCrossover" )

    # Log difference between extrapolated line of zero shear and reality.

    feature_1 = []

    for i in range( len( file_data ) ):

        m = (np.log( data[3][i][3] ) - np.log( data[3][i][1] )) / (np.log( data[0][3] ) - np.log( data[0][1] ))
        b = np.log( data[3][i][2] / data[0][2] ** m )

        extrapolated_value = data[0][len( data[0] ) - 1] ** m * np.exp( b )
        real_value = data[3][i][len( data[3][i] ) - 1]

        feature_1.append( np.log( extrapolated_value ) - np.log( real_value ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "Rhe_Log" )

    # V_deg value.

    feature_1 = []

    for i in range( len( file_data ) ):

        deriv = gu.derivative( np.log( data[3][i] * data[0] ), np.arctan( data[4][i] ) )

        feature_1.append( (deriv[14] - deriv[len( deriv ) - 5]) / (data[3][i][len( data[3][i] ) - 1] * data[0][len( data[0] ) - 1]) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "Rhe_V_deg" )

    # Custom V_deg value.

    feature_1 = []

    for i in range( len( file_data ) ):

        deriv = gu.derivative( np.log( data[3][i] ), data[4][i] )

        feature_1.append( deriv[14] - deriv[len( deriv ) - 5] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "Rhe_V_deg_custom" )

    df = gu.array_with_column_titles_to_df( features, feature_names )

    df.to_csv( output_directory + "Rheology/Features/Features.csv" )

def read_and_analyse_features( ip, file_data ):

    add_Carreau_Yasuda = False

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "Rheology/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]
        # ip.sample_mask = [16, 17, 19, 24, 12, 15, 1, 2, 3, 5, 6, 7, 8, 9, 4, 10, 13, 11, 14, 18, 20, 21, 22, 23]

        if add_Carreau_Yasuda:

            ip.sample_mask.pop( 23 )
            ip.sample_mask.pop( 22 )
            ip.sample_mask.pop( 6 )

    sample_mask = ip.sample_mask

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    if not ip.feature_selection:

        # ip.feature_selection = [i for i in range( len( feature_names ) )]
        ip.feature_selection = [0, 15, 30, 31, 46, 61, 62, 77, 92, 93, 108, 123, 124, 126]
        # ip.feature_selection = [0, 15, 30, 124, 126]
        # ip.feature_selection = [127, 128]
        # ip.feature_selection = [0, 30, 93, 123, 124, 125, 126]
        # ip.feature_selection = [0, 93, 30, 123, 126, 124, 125]
        # ip.feature_selection = [i for i in range( 62 )]

    feature_selection = ip.feature_selection

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    mean_features_unnormalised = gu.extract_mean_features( features, sample_array, samples_present )
    mean_feature_names = feature_names.copy()

    mean_features_unnormalised_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], mean_features_unnormalised) )

    df = gu.array_with_column_titles_to_df( mean_features_unnormalised_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "Rheology/Features/Mean_Features_Unnormalised.csv" )

    std_of_features = gu.extract_std_of_features( features, sample_array, samples_present )

    std_of_features_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "Rheology/Features/Std_of_Features_Unnormalised.csv" )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features = features[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    feature_weights = [1 for i in range( len( feature_selection ) )]

    gu.normalise_features( features, feature_weights )

    # Combine similar features and add a weighting.

    feature_combinations = [[0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8, 11], [12], [13]]

    features, feature_names = gu.combine_features( features, feature_names, feature_combinations )

    feature_weights = [2/3, 2/3, 2/3, 1, 1]

    gu.normalise_features( features, feature_weights )

    #####

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    if add_Carreau_Yasuda:

        # Add Carreau-Yasuda Data (No V1 data).

        eta_zero = [1, 1.71, 1.26, 2.37, 0.127, 1.25, 1.15, 0.798, 15.4, 2.77, 0.753, 0.297, 9.36, 1.19, 0.289, 0.752, 0.133, 7.22, 1183000, 0.0885, 12.6, 5140, 21.3, 402, 1]
        eta_zero = [np.log10( i ) for i in eta_zero]

        mean_features, mean_feature_names = gu.add_mean_feature( mean_features, mean_feature_names, sample_mask, eta_zero, "Rhe_Eta_Zero", weight = 1 )

        eta_inf = [1, 87774, 98324, 115000, 106000, 105000, 76214, 98396, 80000, 54242, 94807, 147000, 97278, 111000, 166000, 116000, 239000, 82292, 37074, 276000, 68147, 12401, 32037, 40000, 80000] # PCR 8 and 23 artificial data.
        eta_inf = [np.log10( i ) for i in eta_inf]

        mean_features, mean_feature_names = gu.add_mean_feature( mean_features, mean_feature_names, sample_mask, eta_inf, "Rhe_Eta_Inf", weight = 1 )

        lambda_param = [0, 0.13594, 0.20048, 0.06788, 0.011394, 0.23778, 0.14816, 0.16169, 0.94035, 0.21901, 0.11131, 0.090291, 0.44758, 0.17766, 0.10097, 0.038893, 0.12605, 0.07489, 0.085517, 0.1136, 0.12143, 0.72155, 0.10464, 0.083242, 0.1]

        mean_features, mean_feature_names = gu.add_mean_feature( mean_features, mean_feature_names, sample_mask, lambda_param, "Rhe_Lambda", weight = 1 )

        a_param = [0, 0.12552, 0.13952, 0.10886, 0.15203, 0.13854, 0.14265, 0.1569, 0.12139, 0.12649, 0.14568, 0.1725, 0.10818, 0.14222, 0.17806, 0.12853, 0.26823, 0.09261, 0.039129, 0.29079, 0.090029, 0.055225, 0.084577, 0.06129, 0.1]

        mean_features, mean_feature_names = gu.add_mean_feature( mean_features, mean_feature_names, sample_mask, a_param, "Rhe_A", weight = 1 )

        feature_combinations = [[0], [1], [2], [3], [4, 6, 8], [5], [7]]

        mean_features, mean_feature_names = gu.combine_features( mean_features, mean_feature_names, feature_combinations )

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    if add_Carreau_Yasuda:

        std_of_features = np.hstack( (std_of_features, np.zeros( len( sample_mask ) )[:, np.newaxis]) )
        std_of_features = np.hstack( (std_of_features, np.zeros( len( sample_mask ) )[:, np.newaxis]) )
        std_of_features = np.hstack( (std_of_features, np.zeros( len( sample_mask ) )[:, np.newaxis]) )
        std_of_features = np.hstack( (std_of_features, np.zeros( len( sample_mask ) )[:, np.newaxis]) )

        std_of_features, _ = gu.combine_features( std_of_features, feature_combinations = feature_combinations )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "Rheology/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "Rheology/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "Rheology/Features/Distance_Matrix.csv" )

    # Perform PCA for rheology features.

    # gu.perform_pca( ip.directory, gu.array_with_column_titles_to_df( mean_features, ["Rhe_Feature_" + str( i + 1 ) for i in range( len( mean_feature_names ) )] ), sample_mask, std_error = True, std_of_features_df = pd.DataFrame( std_of_features ), num_components = 2, filename = ip.output_directory + "Rheology/Features/PCA.pdf" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "Rheology/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "Rheology/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "Rheology/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "Rheology/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "Rheology/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "Rheology/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "Rheology/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "Rheology/Features/", title = "Means_Dendrogram.pdf" )

def sandbox( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    pass
