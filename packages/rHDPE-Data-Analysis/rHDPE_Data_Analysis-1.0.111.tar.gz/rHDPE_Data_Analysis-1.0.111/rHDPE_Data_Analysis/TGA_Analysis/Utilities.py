# Imports.

import numpy as np

from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [[], data[1][width: -width], [], [], [], []]

    for i in range( len( data[3] ) ):

        derivative_data[3].append( np.array( gu.derivative( data[1], data[3][i], width ) ) )

    for i in range( len( data[5] ) ):

        derivative_data[5].append( np.array( gu.derivative( data[1], data[5][i], width ) ) )

    return derivative_data

def extract_TGA_features( output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    # Residue

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( data[3][i][len( data[3][i] ) - 1] )

    features = np.array( feature_1 )[:, np.newaxis]

    feature_names = ["TGA_Residue"]

    # Mean derivative at a selection of 20 degree ranges

    for j in range( 28 ):

        feature_1 = []

        lower_bound = 20 * (j + 2)
        upper_bound = 20 * (j + 3)

        mask = np.where( (first_derivative_data[1] >= lower_bound) & (first_derivative_data[1] <= upper_bound) )[0]

        for i in range( len( file_data ) ):

            feature_1.append( -np.mean( first_derivative_data[3][i][mask] ) )

        features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

        feature_names.append( "TGA_Temp_{}-{}".format( lower_bound, upper_bound ) )

    df = gu.array_with_column_titles_to_df( features, feature_names )

    df.to_csv( output_directory + "TGA/Features/Features.csv" )

def read_and_analyse_TGA_features( ip, file_data ):

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "TGA/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = ip.sample_mask

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    if not ip.feature_selection:

        # ip.feature_selection = [i for i in range( len( feature_names ) )]
        ip.feature_selection = [0, 7, 14, 18, 22, 23]

    feature_selection = ip.feature_selection

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )
    # feature_names = ["Residue", "Feature 5", "Feature 4", "Feature 3", "Feature 2", "Feature 1"]

    mean_features_unnormalised = gu.extract_mean_features( features, sample_array, samples_present )
    mean_feature_names = feature_names.copy()

    mean_features_unnormalised_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], mean_features_unnormalised) )

    df = gu.array_with_column_titles_to_df( mean_features_unnormalised_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TGA/Features/Mean_Features_Unnormalised.csv" )

    std_of_features = gu.extract_std_of_features( features, sample_array, samples_present )

    std_of_features_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TGA/Features/Std_of_Features_Unnormalised.csv" )

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

    df.to_csv( ip.output_directory + "TGA/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "TGA/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "TGA/Features/Distance_Matrix.csv" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "TGA/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "TGA/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "TGA/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "TGA/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "TGA/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "TGA/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "TGA/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "TGA/Features/", title = "Means_Dendrogram.pdf" )

def extract_TGA_features_and_analyse_features_2( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    feature_1 = []

    lower_bound = 400
    upper_bound = 420

    mask = np.where( (first_derivative_data[1] >= lower_bound) & (first_derivative_data[1] <= upper_bound) )[0]

    for i in range( len( file_data ) ):

        feature_1.append( np.mean( first_derivative_data[3][i][mask] ) )

    features = np.array( feature_1 )[:, np.newaxis]

    feature_names = ["TGA_Temp_{}-{}".format( lower_bound, upper_bound )]

    feature_1 = []

    lower_bound = 360
    upper_bound = 380

    mask = np.where( (first_derivative_data[1] >= lower_bound) & (first_derivative_data[1] <= upper_bound) )[0]

    for i in range( len( file_data ) ):

        feature_1.append( np.mean( first_derivative_data[3][i][mask] ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "TGA_Temp_{}-{}".format( lower_bound, upper_bound ) )

    feature_1 = []

    lower_bound = 250
    upper_bound = 270

    mask = np.where( (first_derivative_data[1] >= lower_bound) & (first_derivative_data[1] <= upper_bound) )[0]

    for i in range( len( file_data ) ):

        feature_1.append( np.mean( first_derivative_data[3][i][mask] ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "TGA_Temp_{}-{}".format( lower_bound, upper_bound ) )

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    feature_selection = [i for i in range( len( feature_names ) )]

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

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

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "TGA/Sandbox/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "TGA/Sandbox/Std_of_Features.csv" )

    for i in range( len( features[0] ) ):

        gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = output_directory + "TGA/Sandbox/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    for i in range( len( mean_features[0] ) ):

        gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = output_directory + "TGA/Sandbox/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

def sandbox( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data ):

    perform_extract_TGA_features_and_analyse_features_2 = True

    if perform_extract_TGA_features_and_analyse_features_2:

        extract_TGA_features_and_analyse_features_2( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data )
