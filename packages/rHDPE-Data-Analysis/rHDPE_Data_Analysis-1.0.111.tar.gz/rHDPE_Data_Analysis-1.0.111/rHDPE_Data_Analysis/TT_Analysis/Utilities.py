# Imports.

import numpy as np

from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [[], [], [], [], [], [], [], []]

    for i in range( len( data[5] ) ):

        derivative_data[5].append( data[5][i][width:-width] )

        derivative_data[4].append( np.array( gu.derivative( data[5][i], data[4][i], width ) ) )

    return derivative_data

def extract_TT_features( output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    # Strain at break.

    feature_1 = []

    for i in range( len( file_data ) ):

        array = np.where( data[4][i] > 5 )[0]

        feature_1.append( data[5][i][array[-1]] ) # Changed definition of sab to be the largest strain at which the stress is greater than 5.

    features = np.array( feature_1 )[:, np.newaxis]

    cap_strain_at_break = True
    cap = 250

    if cap_strain_at_break:

        for i in range( len( features[:, 0] ) ):

            if features[i][0] > cap:

                features[i][0] = cap

    feature_names = ["TT_SAB"]

    # Ultimate tensile strength.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( data[4][i].max() )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "TT_UTS" )

    # Young's modulus.

    feature_1 = []

    for i in range( len( file_data ) ):

        young_index = 0

        for ind, str in enumerate( data[5][i] ):

            if str > 1:

                young_index = ind
                break

        feature_1.append( first_derivative_data[4][i][ind - 6] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "TT_YM" )

    df = gu.array_with_column_titles_to_df( features, feature_names )

    df.to_csv( output_directory + "TT/Features/Features.csv" )

def read_and_analyse_features( ip, file_data ):

    add_SHM = True

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "TT/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = ip.sample_mask

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    if not ip.feature_selection:

        ip.feature_selection = [i for i in range( len( feature_names ) )]

    feature_selection = ip.feature_selection

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    mean_features_unnormalised = gu.extract_mean_features( features, sample_array, samples_present )
    mean_feature_names = feature_names.copy()

    mean_features_unnormalised_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], mean_features_unnormalised) )

    df = gu.array_with_column_titles_to_df( mean_features_unnormalised_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TT/Features/Mean_Features_Unnormalised.csv" )

    std_of_features = gu.extract_std_of_features( features, sample_array, samples_present )

    std_of_features_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TT/Features/Std_of_Features_Unnormalised.csv" )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features = features[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    feature_weights = [1 for i in range( len( feature_selection ) )]

    gu.normalise_features( features )

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    if add_SHM:

        shm = [0, 10.05, 8.43, 5.04, 5.54, 10.27, 11.21, 9.1, 13.08, 10.28, 7.99, 7.34, 8.04, 8.13, 7.19, 5.61, 13.21, 9.76, 7.36, 10.27, 7.12, 6.77, 7.59, 7.6, 10.43]

        mean_features, mean_feature_names = gu.add_mean_feature( mean_features, mean_feature_names, sample_mask, shm, "TT_SHM", weight = 1 )

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    if add_SHM:

        std_of_features = np.hstack( (std_of_features, np.zeros( len( sample_mask ) )[:, np.newaxis]) )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TT/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TT/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "TT/Features/Distance_Matrix.csv" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "TT/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "TT/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "TT/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "TT/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "TT/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "TT/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "TT/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "TT/Features/", title = "Means_Dendrogram.pdf" )

def sandbox( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    pass
