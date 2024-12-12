# Imports.

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from . import Preprocessing
from ..Global_Analysis import Utilities as util2
from .. import Global_Utilities as gu

# Function definitions.

def compute_derivatives( data, width = 1 ):
    '''Compute the derivatives.'''

    derivative_data = [data[0][width: -width], [], []]

    for i in range( len( data[1] ) ):

        derivative_data[1].append( np.array( gu.derivative( data[0], data[1][i], width ) ) )

    for i in range( len( data[2] ) ):

        derivative_data[2].append( np.array( gu.derivative( data[0], data[2][i], width ) ) )

    return derivative_data

def identify_peaks( data, first_derivative_data, second_derivative_data, third_derivative_data, peak_threshold_1, peak_threshold_2 ):
    '''Identify peaks in the spectrums by considering where the curve of the third derivative
    crosses the x-axis with positive gradient as wavenumbers increase,
    using the magnitude of the second derivative at this point to determine the significance.'''

    y_peaks, m_peaks, mag_y_peaks, mag_m_peaks = [], [], [], []

    structure = [(third_derivative_data[0], data[1], first_derivative_data[1], second_derivative_data[1], third_derivative_data[1], y_peaks, mag_y_peaks), (third_derivative_data[0], data[2], first_derivative_data[2], second_derivative_data[2], third_derivative_data[2], m_peaks, mag_m_peaks)]

    for s in structure:

        xd3, d0, d1, d2, d3, _, _ = s

        for i in range( len( d3 ) ):

            local_min, local_mag = [], []

            for j in range( 1, len( d3[i] ) ):

                if d3[i][j] <= 0 and d3[i][j - 1] > 0:

                    if d2[i][j + 1] < peak_threshold_1 or d2[i][j] < peak_threshold_1:

                        if d2[i][j + 1] < d2[i][j]:

                            if not (d2[i][j] > 0 or d2[i][j + 2] > 0): # Ensure peak not due to noise/more precise FTIR spectra.

                                local_min.append( xd3[j] )
                                local_mag.append( d2[i][j + 1] )

                        else:

                            if not (d2[i][j - 1] > 0 or d2[i][j + 1] > 0): # Ensure peak not due to noise/more precise FTIR spectra.

                                local_min.append( xd3[j - 1] )
                                local_mag.append( d2[i][j] )

                # The following clause was used to find minima in the spectra. Was particularly useful for CO2 where there were minima, I think due to background spectra being subtracted. There was a strong correlation
                # between 667, 2343, and 2381.

                # elif d3[i][j] >= 0 and d3[i][j - 1] < 0:
                #
                #     if d2[i][j + 1] > -peak_threshold_1 or d2[i][j] > -peak_threshold_1:
                #
                #         if d2[i][j + 1] > d2[i][j]:
                #
                #             local_min.append( xd3[j] )
                #             local_mag.append( -d2[i][j + 1] )
                #
                #         else:
                #
                #             local_min.append( xd3[j - 1] )
                #             local_mag.append( -d2[i][j] )

            s[5].append( local_min )
            s[6].append( local_mag )

    return y_peaks, m_peaks, mag_y_peaks, mag_m_peaks

def linear_filter( magnitude, cutoff, threshold ):
    '''Assigning a sigmoid filter to the magnitude of peaks.'''

    for i in range( len( magnitude ) ):

        for j in range( len( magnitude[i] ) ):

            if magnitude[i][j] < -cutoff:

                magnitude[i][j] = -1

            else:

                magnitude[i][j] = -(-magnitude[i][j] + threshold) / (cutoff + threshold)

def merge_close_peaks( peaks_array, peak_spacing ):
    '''Peaks whose wavenumbers are within a threshold are merged.'''

    iterations = 2

    spacings = [3, peak_spacing] # Was [3, peak_spacing].

    unique, counts = np.unique( peaks_array, return_counts = True )

    dict_peaks = dict( zip( unique, counts ) )

    popped_dict = {}

    for r in range( iterations ):

        skip = 0

        for ind, u in enumerate( unique ):

            if skip > 0:

                skip -= 1
                continue

            if ind >= len( unique ) - 1:

                continue

            if unique[ind + 1] - unique[ind] > spacings[r]:

                continue

            else:

                indices = [ind, ind + 1]

                for i in range( ind + 2, len( unique ) ):

                    if unique[i] - unique[i - 1] < spacings[r]:

                        indices.append( i )

                    else:

                        break

                skip = len( indices ) - 1
                index_of_max_count = indices[0]

                for i in range( 1, len( indices ) ):

                    if counts[indices[i]] > counts[index_of_max_count]:

                        index_of_max_count = indices[i]

                for i in indices:

                    if i == index_of_max_count:

                        continue

                    else:

                        dict_peaks[unique[index_of_max_count]] += counts[i]
                        dict_peaks.pop( unique[i] )
                        popped_dict[unique[i]] = unique[index_of_max_count]

        unique = np.array( list( dict_peaks.keys() ) )
        counts = np.array( list( dict_peaks.values() ) )

    return dict_peaks, popped_dict

def populate_peaks_array( list_of_peaks, magnitude_of_peaks, peak_spacing, peak_limit ):
    '''Produce a peaks array: where each row is a heat map of where peaks are for a corresponding specturm.'''

    peaks = []

    for i in range( len( list_of_peaks ) ):

        for j in list_of_peaks[i]:

            peaks.append( j )

    peaks_array = np.array( peaks )

    dict_peaks, popped_dict = merge_close_peaks( peaks_array, peak_spacing )

    peaks = list( dict_peaks.keys() )

    peaks_array = np.zeros( (len( list_of_peaks ), len( peaks )) )

    for i in range( len( list_of_peaks ) ):

        for ind, j in enumerate( list_of_peaks[i] ):

            if j in peaks:

                if -magnitude_of_peaks[i][ind] > peaks_array[i][peaks.index( j )]:

                    peaks_array[i][peaks.index( j )] = -magnitude_of_peaks[i][ind]

            elif popped_dict[j] in peaks:

                if -magnitude_of_peaks[i][ind] > peaks_array[i][peaks.index( popped_dict[j] )]:

                    peaks_array[i][peaks.index( popped_dict[j] )] = -magnitude_of_peaks[i][ind]

            else:

                if -magnitude_of_peaks[i][ind] > peaks_array[i][peaks.index( popped_dict[popped_dict[j]] )]:

                    peaks_array[i][peaks.index( popped_dict[popped_dict[j]] )] = -magnitude_of_peaks[i][ind]

    peaks = list( np.array( peaks )[np.where( np.array( peaks ) < peak_limit )[0]] )
    peaks_array = peaks_array[:, :len( peaks )]

    return peaks, peaks_array

def remove_identical_columns( peaks_array, peaks ):
    '''Remove identical columns in a peaks array.'''

    trans_arr = peaks_array.T
    not_uniform_column = []

    for i in range( trans_arr.shape[0] ):

        if not np.all( trans_arr[i] == trans_arr[i][0] ):

            not_uniform_column.append( i )

    peaks = list( np.array( peaks )[not_uniform_column] )
    peaks_array = peaks_array[:, not_uniform_column]

    return peaks, peaks_array

def remove_wavenumbers( peaks, peaks_array ):

    # Remove wavenumbers corresponding to CO2.

    peaks_to_remove = []

    for i, p in enumerate( peaks ):

        if p < 675 and p > 660:

            peaks_to_remove.append( i )

        elif p < 2400 and p > 2300:

            peaks_to_remove.append( i )

    peaks_to_remove.reverse()

    for p in peaks_to_remove:

        peaks.pop( p )
        peaks_array = np.delete( peaks_array, p, 1 )

    return peaks_array

def extract_FTIR_features( output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data, peak_threshold_1, peak_threshold_2, peak_spacing, peak_limit ):

    m_peak_analysis = True
    y_peak_analysis = True

    y_peaks, m_peaks, mag_y_peaks, mag_m_peaks = identify_peaks( data, first_derivative_data, second_derivative_data, third_derivative_data, peak_threshold_1, peak_threshold_2 )

    m_peaks_array, y_peaks_array = [], []

    if m_peak_analysis:

        linear_filter( mag_m_peaks, peak_threshold_2, peak_threshold_1 )
        m_peaks, m_peaks_array = populate_peaks_array( m_peaks, mag_m_peaks, peak_spacing, peak_limit )
        m_peaks, m_peaks_array = remove_identical_columns( m_peaks_array, m_peaks )
        m_peaks_array = remove_wavenumbers( m_peaks, m_peaks_array )

        feature_names = ["FTIR_{}".format( int( i ) ) for i in m_peaks]

        df = gu.array_with_column_titles_to_df( m_peaks_array, feature_names )

        df.to_csv( output_directory + "FTIR/Features/Features.csv" )

    if y_peak_analysis:

        peaks_specified_by_m_peak_analysis = True

        linear_filter( mag_y_peaks, peak_threshold_2, peak_threshold_1 )

        if peaks_specified_by_m_peak_analysis:

            peaks = m_peaks # Current m_peaks are [777.4173764906302, 808.2725724020441, 825.6286201022145, 841.0562180579215, 854.5553662691651, 875.7683134582622, 908.5519591141395, 972.190800681431, 997.2606473594548, 1018.473594548552, 1066.6848381601362, 1082.1124361158431, 1166.9642248722316, 1195.8909710391822, 1213.2470187393524, 1261.4582623509368, 1367.5229982964224, 1377.1652470187391, 1398.3781942078365, 1409.9488926746167, 1435.0187393526403, 1490.9437819420782, 1541.083475298126, 1577.72402044293, 1631.7206132879044, 1645.2197614991483, 1658.7189097103917, 1739.7137989778535, 1978.841567291312, 2162.044293015332, 2952.708688245315, 2960.4224872231684, 3297.9011925042582].

            peaks_array = np.zeros( (len( y_peaks ), len( peaks )) )

            for i in range( len( y_peaks ) ):

                for j in range( len( peaks ) ):

                    argmin = min( range( len( y_peaks[i] ) ), key = lambda x: abs( y_peaks[i][x] - peaks[j] ) )

                    if abs( y_peaks[i][argmin] - peaks[j] ) < 6:

                        peaks_array[i][peaks.index( peaks[j] )] = -mag_y_peaks[i][argmin]

            y_peaks = peaks
            y_peaks_array = peaks_array

        else:

            y_peaks, y_peaks_array = populate_peaks_array( y_peaks, mag_y_peaks, peak_spacing, peak_limit )
            y_peaks, y_peaks_array = remove_identical_columns( y_peaks_array, y_peaks )
            y_peaks_array = remove_wavenumbers( y_peaks, y_peaks_array )

        feature_names = ["FTIR_{}".format( int( i ) ) for i in y_peaks]

        df = gu.array_with_column_titles_to_df( y_peaks_array, feature_names )

        df.to_csv( output_directory + "FTIR/Features/Specimen_Features.csv" )

    return m_peaks, m_peaks_array, y_peaks, y_peaks_array

def read_and_analyse_FTIR_features( ip, file_data ):

    precomputed_means = False

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "FTIR/Features/Specimen_Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        # ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]
        # ip.sample_mask = [301, 303, 306, 308, 309, 312, 313, 315, 318, 320, 324, 325]
        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24, 500, 502, 504, 506, 508, 510, 512, 514, 516, 518]

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

    df.to_csv( ip.output_directory + "FTIR/Features/Mean_Features_Unnormalised.csv" )

    std_of_features = gu.extract_std_of_features( features, sample_array, samples_present )

    std_of_features_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "FTIR/Features/Std_of_Features_Unnormalised.csv" )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features = features[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    feature_weights = [1 for i in range( len( feature_selection ) )]

    # gu.normalise_features( features, feature_weights )

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "FTIR/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "FTIR/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "FTIR/Features/Distance_Matrix.csv" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "FTIR/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "FTIR/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, [f[5:] for f in feature_names], [f[2] for f in file_data_mask], specimen = True, subdirectory = "FTIR/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, [f[5:] for f in mean_feature_names], [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "FTIR/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "FTIR/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Dendrogram.pdf" )

    if precomputed_means:

        feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "FTIR/Features/Features.csv" )

        feature_selection = [i for i in range( len( feature_names ) )]

        features = features[:, feature_selection]
        feature_names = list( np.array( feature_names )[feature_selection] )

        samples_present_mask = gu.produce_mask( samples_present_array, sample_mask )

        features = features[samples_present_mask, :]

        feature_weights = [1 for i in range( len( feature_selection ) )]

        # gu.normalise_features( features, feature_weights )

        distance_matrix = gu.distance_matrix_from_features( features )

        mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], features) )

        df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + feature_names )

        df.to_csv( ip.output_directory + "FTIR/Features/Mean_Features.csv" )

        df = gu.array_with_column_titles_and_label_titles_to_df( distance_matrix, sample_mask, sample_mask )

        df.to_csv( ip.output_directory + "FTIR/Features/Distance_Matrix.csv" )

        if plot_mean_bars:

            for i in range( len( features[0] ) ):

                gu.plot_barchart_of_feature( features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "FTIR/Feature_Bars/Mean/" + feature_names[i] + ".pdf", savefig = True )

        if plot_mean_features:

            gu.plot_features( ip.output_directory, features, [f[5:] for f in feature_names], [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Features.pdf" )

        if plot_mean_distance_matrix:

            gu.plot_distance_matrix( ip.output_directory, distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Distance_Matrix.pdf" )

        if plot_mean_dendrogram:

            gu.plot_dendrogram( ip.output_directory, distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Dendrogram.pdf" )

def integral_analysis( directory, output_directory, file_data, data ):
    '''Perform an analysis on the data that focuses on integrals.'''

    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    # splits = [660, 680, 765, 785, 890, 910, 1340, 1390, 1425, 1445, 1480, 1500, 1625, 1675, 1730, 1750, 2300, 2370, 2950, 2970, 3100, 3500]
    splits = [868, 885, 965, 980]

    feature = []

    range_mask = np.where( (data[0] >= splits[0]) & (data[0] < splits[1]) )

    for i in range( len( data[1] ) ):

        feature.append( gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() ) )

    features = np.array( feature )[:, np.newaxis]

    feature_names = ["FTIR_{}-{}".format( splits[0], splits[1] )]

    for s in range( 2, len( splits ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= splits[s]) & (data[0] < splits[s + 1]) )

        for i in range( len( data[1] ) ):

            feature.append( gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() ) )

        features = np.hstack( (features, np.array( feature )[:, np.newaxis]) )

        feature_names.append( "FTIR_{}-{}".format( splits[s], splits[s + 1] ) )

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

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Integral_Analysis/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Integral_Analysis/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( output_directory + "FTIR/Integral_Analysis/Distance_Matrix.csv" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "FTIR/Integral_Analysis/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Integral_Analysis/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "FTIR/Integral_Analysis/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Integral_Analysis/", title = "Means_Dendrogram.pdf" )

def component_analysis( directory, output_directory, file_data, data ):

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]
    # sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416]
    # sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 500, 502, 504, 506, 508, 510, 512, 514, 516]
    # sample_mask = [500, 502, 504, 506, 508, 510, 512, 514, 516]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    pp_integrals = [835, 845, 993, 1005, 2950, 2970]

    features = []

    for s in range( 0, len( pp_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= pp_integrals[s]) & (data[0] < pp_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.mean( features_array, 1 )[:, np.newaxis]
    feature_names = ["PP Content"]

    irgafos_integrals = [770, 785, 820, 830, 850, 860, 1075, 1090, 1485, 1495]

    features = []

    for s in range( 0, len( irgafos_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= irgafos_integrals[s]) & (data[0] < irgafos_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.hstack( (mean_integral, np.mean( features_array, 1 )[:, np.newaxis]) )
    feature_names.append( "Irgafos Content" )

    CaCO3_integrals = [868, 885]

    features = []

    for s in range( 0, len( CaCO3_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= CaCO3_integrals[s]) & (data[0] < CaCO3_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.hstack( (mean_integral, np.mean( features_array, 1 )[:, np.newaxis]) )
    feature_names.append( "CaCO3 Content" )

    vinyl_integrals = [906, 912]

    features = []

    for s in range( 0, len( vinyl_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= vinyl_integrals[s]) & (data[0] < vinyl_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.hstack( (mean_integral, np.mean( features_array, 1 )[:, np.newaxis]) )
    feature_names.append( "Vinyl Content" )

    pet_integrals = [1015, 1025, 1095, 1105, 1110, 1125, 1405, 1415, 1715, 1730]

    features = []

    for s in range( 0, len( pet_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= pet_integrals[s]) & (data[0] < pet_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.hstack( (mean_integral, np.mean( features_array, 1 )[:, np.newaxis]) )
    feature_names.append( "PET Content" )

    pa_integrals = [1635, 1650, 3280, 3320]

    features = []

    for s in range( 0, len( pa_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= pa_integrals[s]) & (data[0] < pa_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.hstack( (mean_integral, np.mean( features_array, 1 )[:, np.newaxis]) )
    feature_names.append( "PA Content" )

    cast_integrals = [1570, 1585]

    features = []

    for s in range( 0, len( cast_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= cast_integrals[s]) & (data[0] < cast_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    gu.normalise_features( features_array )

    mean_integral = np.hstack( (mean_integral, np.mean( features_array, 1 )[:, np.newaxis]) )
    feature_names.append( "CaSt Content" )

    feature_selection = [i for i in range( len( feature_names ) )]

    mean_integral = mean_integral[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    mean_features_unnormalised = gu.extract_mean_features( mean_integral, sample_array, samples_present )
    mean_feature_names = feature_names.copy()

    mean_features_unnormalised_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], mean_features_unnormalised) )

    df = gu.array_with_column_titles_to_df( mean_features_unnormalised_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Component_Analysis/Features/Mean_Features_Unnormalised.csv" )

    std_of_features = gu.extract_std_of_features( mean_integral, sample_array, samples_present )

    std_of_features_plus_sample_mask = np.hstack( (samples_present_array[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Component_Analysis/Features/Std_of_Features_Unnormalised.csv" )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    mean_integral = mean_integral[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    mean_features = gu.extract_mean_features( mean_integral, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( mean_integral, sample_array, sample_mask )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Component_Analysis/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Component_Analysis/Features/Std_of_Features.csv" )

    if plot_specimen_bars:

        for i in range( len( mean_integral[0] ) ):

            gu.plot_barchart_of_feature( mean_integral[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = output_directory + "FTIR/Component_Analysis/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = output_directory + "FTIR/Component_Analysis/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( output_directory, mean_integral, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "FTIR/Component_Analysis/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Component_Analysis/Features/", title = "Means_Features.pdf" )

    import matplotlib.pyplot as plt

    # plt.plot( [0, 2, 4, 6, 8, 10, 12, 14, 16], mean_features, 'o' )

    # model = np.poly1d( np.polyfit( [0, 2, 4, 6, 8, 10, 12, 14, 16], mean_features[23:, 0], 2) )
    #
    # polyline = np.linspace( 0, 16, 100 )
    #
    # plt.scatter( [0, 2, 4, 6, 8, 10, 12, 14, 16], mean_features[23:, 0] )
    #
    # colours = gu.read_list_of_colours( directory )
    # scatter_colours = [colours[sample_mask[i]] for i in range( 23 )]
    #
    # plt.scatter( [(model - mean_features[i, 0]).roots[1] for i in range( 23 )], mean_features[:23, 0], color = scatter_colours, s = 100 )
    #
    # plt.plot(polyline, model( polyline ) )
    #
    # plt.xlabel( "Known concentration of PP (%)", fontsize = 13 )
    # plt.ylabel( "Model value", fontsize = 13 )
    #
    # plt.show()
    #
    # plt.close()

def specimen_feature_correlation( directory, output_directory, file_data ):

    df = pd.read_csv( output_directory + "FTIR/Features/Specimen_Features.csv" )

    df.drop( columns = df.columns[0], inplace = True )

    # feature_1 = "FTIR_667"
    # feature_2 = "FTIR_2349"
    #
    # pearson, _ = pearsonr( df[feature_1].to_list(), df[feature_2].to_list() )
    #
    # print( pearson )
    #
    # gu.plot_scatterplot_of_two_specimen_features_with_hover_annotation( df[feature_1].to_list(), df[feature_2].to_list(), file_data )

    # for i in range( len( df.columns ) ):
    #
    #     feature_1 = df.columns[i]
    #
    #     for j in range( i + 1, len( df.columns ) ):
    #
    #         feature_2 = df.columns[j]
    #
    #         pearson, _ = pearsonr( df[feature_1].to_list(), df[feature_2].to_list() )
    #
    #         if abs( pearson ) > 0.75:
    #
    #             print( pearson, feature_1, feature_2 )
    #
    #             gu.plot_scatterplot_of_two_specimen_features_with_hover_annotation( df[feature_1].to_list(), df[feature_2].to_list(), file_data )

    feature_1 = "FTIR_663"

    for j in range( len( df.columns ) ):

        feature_2 = df.columns[j]

        pearson, _ = pearsonr( df[feature_1].to_list(), df[feature_2].to_list() )

        if abs( pearson ) > 0.75:

            print( pearson, feature_1, feature_2 )

            gu.plot_scatterplot_of_two_specimen_features_with_hover_annotation( df[feature_1].to_list(), df[feature_2].to_list(), file_data )

def correlation_with_external_data( directory, output_directory, file_data, data ):
    '''Find correlations with external data.'''

    resin_data = gu.get_list_of_resins_data( directory )

    external_data = pd.read_csv( output_directory + "DSC/Output/Features/Mean_Features.csv" )

    external_data.drop( columns = [external_data.columns[0]], inplace = True )

    samples_present_external_data = external_data.iloc[:, 0].tolist()

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = samples_present

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present_external_data )

    feature_list = []

    for s in sample_mask:

        feature_list.append( external_data.iloc[samples_present_external_data.index( s ), 1] )

    feature = np.array( feature_list )

    max_covalence = 0
    max_pearson = 0
    index_covalence = -1
    index_pearson = -1

    for i in range( len( data[0] ) ): # Loop over wavenumbers.

        wavenumber_values = []

        for j in range( len( data[2] ) ):

            wavenumber_values.append( data[2][j][i] )

        wavenumber_values_array = np.array( wavenumber_values )

        covalence = np.cov( feature, wavenumber_values_array )[0][1]
        pearson, _ = pearsonr( feature, wavenumber_values_array )

        if max_pearson < pearson:

            max_pearson = pearson
            index_pearson = i

        if max_covalence < covalence:

            max_covalence = covalence
            index_covalence = i

    print( max_pearson, index_pearson )
    print( max_covalence, index_covalence )

    wavenumber_values = []

    for j in range( len( data[2] ) ):

        wavenumber_values.append( data[2][j][index_pearson] )

    wavenumber_values_array = np.array( wavenumber_values )

    gu.plot_scatterplot_of_two_features( feature, wavenumber_values_array, sample_mask, [resin_data.loc[i]["Label"] for i in sample_mask] )

def normalisation_experimentation( directory, output_directory, file_data, data ):
    '''Experimenting to find best preprocessing for PCA.'''

    for i in range( len( data[1] ) ):

        # data[1][i] = (data[1][i] / data[1][i].max())
        data[1][i] = ((data[1][i] - data[1][i].min()) / (data[1][i].max() - data[1][i].min()))

    Preprocessing.compute_mean( output_directory, file_data, data )

    Preprocessing.read_mean( output_directory, data )

    first_derivative_data = compute_derivatives( data )
    second_derivative_data = compute_derivatives( first_derivative_data )
    third_derivative_data = compute_derivatives( second_derivative_data )

    m_peaks, m_peaks_array, y_peaks, y_peaks_array = extract_FTIR_features( output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data, -0.00008, 0.0002, 6, 3400 )

    resin_data = gu.get_list_of_resins_data( directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( output_directory + "FTIR/Features/Specimen_Features.csv" )

    ###

    features = first_derivative_data[1]
    feature_names = [str( i ) for i in first_derivative_data[0]]

    ###

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

    # gu.normalise_features( features, feature_weights )

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( output_directory + "FTIR/Features/Distance_Matrix.csv" )

    # gu.plot_features( output_directory, mean_features, [f[5:] for f in mean_feature_names], [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Features/", title = "Means_Features.pdf" )

    features_df = gu.array_with_column_titles_and_label_titles_to_df( mean_features, [str( i ) for i in mean_feature_names], sample_mask )

    # features_df = StandardScaler().fit_transform( features_df )

    features_df = gu.array_with_column_titles_and_label_titles_to_df( features_df, [str( i ) for i in mean_feature_names], sample_mask )

    std_of_features_df = gu.array_with_column_titles_and_label_titles_to_df( std_of_features, [str( i ) for i in mean_feature_names], sample_mask )

    util2.pca( directory, features_df, std_of_features_df )

    # Default:
    # [0.0, 0.35883070579474546, 0.58859988292701, 0.7390626819327278, 0.8210366863949823, 0.8693373369051673, 0.904292376728703, 0.9304661729563468, 0.9513682016298718, 0.9652131579541247, 0.975691795171862]

    # No normalisation:
    # [0.0, 0.3524054219641353, 0.604358407390208, 0.7488330420945205, 0.8358651978695985, 0.8823789020545217, 0.9102495323025178, 0.9342043003316911, 0.954834274196833, 0.9690753972011436, 0.9790872682977163]

    # Max-min normalisation:
    # [0.0, 0.35975369836811844, 0.5878277260239937, 0.738444752490623, 0.8204529185163695, 0.8686913461725618, 0.9041059160564926, 0.9303498261009217, 0.9514856417411043, 0.9652947741566771, 0.9756082339872473]

    # Max-min normalisation, all in:
    # [0.0, 0.519424198453715, 0.7109133621521699, 0.8403923836430574, 0.9029294068088906, 0.9354452996364587, 0.9563529416662541, 0.9693791609314283, 0.9812628941776536, 0.987887135278509, 0.9918010241419203]

    # Max-min normalisation, all in, first derivative:
    # [0.0, 0.43051277477178207, 0.8298189845995849, 0.9090705223769208, 0.9442834667082102, 0.959899984490423, 0.9692436649075102, 0.9761112933461358, 0.9817540207900024, 0.9857847801988655, 0.9894756652385638]

def pp_percentage_model( directory, output_directory, file_data, data, name_appendage = "" ):

    blend_samples = [500, 502, 504, 506, 508, 510, 512, 514, 516] # Samples with known ratios of HDPE/PP.

    resin_data = gu.get_list_of_resins_data( directory, name_appendage )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 601, 602, 603, 604, 605, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 500, 502, 504, 506, 508, 510, 512, 514, 516, 518]
    sample_mask = samples_present

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    # Applying minmax normalisation.

    range_mask = np.where( (data[0] >= 3050) & (data[0] < 3100) )

    for i in range( len( data[1] ) ):

        mini = data[1][i][range_mask].min()

        data[1][i] = ((data[1][i] - mini) / (data[1][i].max() - mini))

    ######
    # Scaling data so that all spectra have a peak magnitude of 0.1 or less at 720.

    range_mask = np.where( (data[0] >= 712) & (data[0] < 726) )

    for i in range( len( data[1] ) ):

        value = data[1][i][range_mask].max()

        if value > 0.1:

            data[1][i] = data[1][i] * 0.1 / value

    # Integrating PP peaks.

    pp_integrals = [801, 815, 834, 848, 966, 980, 990, 1004, 1160, 1174, 1365, 1385] # [803, 813, 836, 846, 968, 978, 992, 1002, 1162, 1172, 1375, 1382] # Previous intervals used, now use slightly broader ones.
    feature_names = ["808", "841", "973", "997", "1167", "1377"]

    features = []

    for s in range( 0, len( pp_integrals ) - 1, 2 ):

        feature = []

        range_mask = np.where( (data[0] >= pp_integrals[s]) & (data[0] < pp_integrals[s + 1]) )

        for i in range( len( data[1] ) ):

            integral = gu.integral_2( data[0][range_mask], data[1][i][range_mask], 0, len( data[0][range_mask] ) - 1, data[1][i][range_mask].min() )

            if integral < 0:

                integral = 0

            feature.append( integral )

        features.append( feature )

    features_array = np.array( features[0] )[:, np.newaxis]

    for i in range( 1, len( features ) ):

        features_array = np.hstack( (features_array, np.array( features[i] )[:, np.newaxis]) )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features_array = features_array[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    mean_features_without_extremities_pre_adjust = gu.extract_mean_features_2( features_array, sample_array, sample_mask )
    mean_features_without_extremities = mean_features_without_extremities_pre_adjust - mean_features_without_extremities_pre_adjust[sample_mask.index( 500 ), :]

    # mean_features = gu.extract_mean_features( features_array, sample_array, sample_mask )
    # mean_feature_names = feature_names.copy()
    #
    # std_of_features = gu.extract_std_of_features( features_array, sample_array, sample_mask )
    #
    # mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )
    #
    # df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )
    #
    # df.to_csv( output_directory + "FTIR/Sandbox/PP_Percentage_Analysis/Features/Mean_Features.csv" )
    #
    # std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )
    #
    # df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )
    #
    # df.to_csv( output_directory + "FTIR/Sandbox/PP_Percentage_Analysis/Features/Std_of_Features.csv" )
    #
    # for i in range( len( features_array[0] ) ):
    #
    #     gu.plot_barchart_of_feature( features_array[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = output_directory + "FTIR/Sandbox/PP_Percentage_Analysis/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )
    #
    # for i in range( len( mean_features[0] ) ):
    #
    #     gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = output_directory + "FTIR/Sandbox/PP_Percentage_Analysis/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )
    #
    # gu.plot_features( output_directory, features_array, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "FTIR/Sandbox/PP_Percentage_Analysis/Features/", title = "Specimen_Features.pdf" )
    #
    # gu.plot_features( output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Sandbox/PP_Percentage_Analysis/Features/", title = "Means_Features.pdf" )

    def func( x, a ):

        return a * x

    def positive_definite_and_ton_limit( x ):

        if x < 0:

            return 0.0

        elif x > 100:

            return 100.0

        else:

            return x

    vfunc = np.vectorize( positive_definite_and_ton_limit )

    popts = []

    for i in range( len( features_array[0] ) ):

        popt, _ = curve_fit( func, [0, 2, 4, 6, 8, 10, 12, 14, 16], mean_features_without_extremities[[sample_mask.index( j ) for j in blend_samples], i] )

        popts.append( popt )

        mean_features_without_extremities[:, i] = mean_features_without_extremities[:, i] / popt[0]

        features_array[:, i] = vfunc( (features_array[:, i] - mean_features_without_extremities_pre_adjust[sample_mask.index( 500 ), i]) / popt[0] )

    df = gu.array_with_column_titles_and_label_titles_to_df( features_array, feature_names, [file_data_mask[i][0] for i in range( len( file_data_mask ) )] )

    df.to_csv( output_directory + "FTIR/Sandbox/PP_Percentage_Analysis/Features/PP_Predictions" + name_appendage + ".csv", float_format = "%.3f" )

    final_pp_prediction = []

    for i in sample_mask:

        specimen_mask = gu.produce_mask( sample_array, [i] )

        features_array_copy = features_array[specimen_mask, :]

        specimen_predictions = []

        for j in range( len( features_array_copy ) ):

            specimen_predictions.append( (features_array_copy[j].sum() - features_array_copy[j].max() - features_array_copy[j].min()) / (len( features_array_copy[j] ) - 2) )

        if len( specimen_predictions ) >= 5:

            array = np.array( specimen_predictions )

            final_pp_prediction.append( (array.sum() - array.max() - array.min()) / (len( array ) - 2) )

        else:

            array = np.array( specimen_predictions )

            final_pp_prediction.append( array.mean() )

        # print( i, final_pp_prediction[-1] )

    pearson, _ = pearsonr( [0, 2, 4, 6, 8, 10, 12, 14, 16], np.array( final_pp_prediction )[[sample_mask.index( j ) for j in blend_samples]] )

    # print( "R squared value of PP prediction is ", pearson * pearson )

    # y_pos = np.arange( 6 ) * 9
    #
    # for i in range( 9 ):
    #
    #     plt.bar( y_pos + i, mean_features_without_extremities[sample_mask.index( blend_samples[i] ), :], align = 'center', alpha = 0.5 )
    #
    # plt.tight_layout()
    #
    # plt.show()
    #
    # plt.close()

    ###### Miles's approach

    feature = []

    range_mask_1 = np.where( (data[0] >= 3090) & (data[0] < 3110) )
    range_mask_2 = np.where( (data[0] >= 1374) & (data[0] < 1379) )
    range_mask_3 = np.where( (data[0] >= 717) & (data[0] < 722) )

    for i in range( len( data[1] ) ):

        value_1 = data[1][i][range_mask_1].min()
        value_2 = data[1][i][range_mask_2].max()
        value_3 = data[1][i][range_mask_3].max()

        feature.append( (value_2 - value_1) / (value_3 + value_2 - value_1 - value_1) )

    features_array = np.array( feature )[:, np.newaxis]

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features_array = features_array[specimen_mask, :]
    sample_array = sample_array[specimen_mask]

    mean_features_without_extremities_pre_adjust = gu.extract_mean_features_2( features_array, sample_array, sample_mask )
    mean_features_without_extremities = mean_features_without_extremities_pre_adjust - mean_features_without_extremities_pre_adjust[sample_mask.index( 500 ), :]

    popt, _ = curve_fit( func, [0, 2, 4, 6, 8, 10, 12, 14, 16], mean_features_without_extremities[[sample_mask.index( j ) for j in blend_samples], 0] )

    mean_features_without_extremities[:, 0] = mean_features_without_extremities[:, 0] / popt[0]

    features_array[:, 0] = vfunc( (features_array[:, 0] - mean_features_without_extremities_pre_adjust[sample_mask.index( 500 ), 0]) / popt[0] )

    final_pp_prediction_2 = []

    for i in sample_mask:

        specimen_mask = gu.produce_mask( sample_array, [i] )

        features_array_copy = features_array[specimen_mask, :]

        if len( features_array_copy[:, 0] ) >= 5:

            array = features_array_copy[:, 0]

            final_pp_prediction_2.append( (array.sum() - array.max() - array.min()) / (len( array ) - 2) )

        else:

            array = features_array_copy[:, 0]

            final_pp_prediction_2.append( array.mean() )

        # print( i, final_pp_prediction_2[-1] )

    pearson, _ = pearsonr( [0, 2, 4, 6, 8, 10, 12, 14, 16], np.array( final_pp_prediction_2 )[[sample_mask.index( j ) for j in blend_samples]] )

    # print( "R squared value of PP prediction is ", pearson * pearson )

def crystallinity_determination( directory, output_directory, file_data, data ):

    resin_data = gu.get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    features = []

    feature = []

    range_mask_1 = np.where( (data[0] >= 755) & (data[0] < 765) )
    range_mask_2 = np.where( (data[0] >= 715) & (data[0] < 725) )
    range_mask_3 = np.where( (data[0] >= 725) & (data[0] < 735) )

    for i in range( len( data[1] ) ):

        i_a = data[1][i][range_mask_3].max() - data[1][i][range_mask_1].min()
        i_b = data[1][i][range_mask_2].max() - data[1][i][range_mask_1].min()

        cryst = (1 - (i_a / i_b) / 1.233) / (1 + i_a / i_b) * 100

        feature.append( cryst )

    features.append( feature )

    feature = []

    for i in range( len( data[1] ) ):

        i_a = data[1][i][range_mask_2].max() - data[1][i][range_mask_3].max()

        feature.append( i_a )

    features.append( feature )

    feature = []

    range_mask_1 = np.where( (data[0] >= 1500) & (data[0] < 1525) )
    range_mask_2 = np.where( (data[0] >= 1460) & (data[0] < 1468) )
    range_mask_3 = np.where( (data[0] >= 1470) & (data[0] < 1480) )

    for i in range( len( data[1] ) ):

        i_a = data[1][i][range_mask_3].max() - data[1][i][range_mask_1].min()
        i_b = data[1][i][range_mask_2].max() - data[1][i][range_mask_1].min()

        cryst = (1 - (i_a / i_b) / 1.233) / (1 + i_a / i_b) * 100

        feature.append( cryst )

    features.append( feature )

    feature_names = ["FTIR_Cryst1", "FTIR_Cryst2", "FTIR_Cryst3"]

    features_array = np.array( features[0] )[:, np.newaxis]

    features_array = np.hstack( (features_array, np.array( features[1] )[:, np.newaxis]) )
    features_array = np.hstack( (features_array, np.array( features[2] )[:, np.newaxis]) )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features_array = features_array[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    gu.normalise_features( features_array )

    features = features_array

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Sandbox/Crystallinity/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( output_directory + "FTIR/Sandbox/Crystallinity/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( output_directory + "FTIR/Sandbox/Crystallinity/Distance_Matrix.csv" )

    gu.plot_features( output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "FTIR/Sandbox/Crystallinity/", title = "Specimen_Features.pdf" )

    gu.plot_features( output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "FTIR/Sandbox/Crystallinity/", title = "Means_Features.pdf" )

def sandbox( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data, third_derivative_data ):

    perform_integral_analysis = False # Perform a second kind of analysis on the spectrums focusing on integrals.

    perform_component_analysis = False

    perform_specimen_feature_correlation = False

    perform_correlation_with_external_data = False # Try to find correlations between external data and FTIR data.

    perform_normalisation_experimentation = False

    perform_pp_percentage_model = True

    perform_crystallinity_determination = False

    if perform_integral_analysis:

        integral_analysis( directory, output_directory, file_data, data )

    if perform_component_analysis:

        component_analysis( directory, output_directory, file_data, data )

    if perform_specimen_feature_correlation:

        specimen_feature_correlation( directory, output_directory, file_data )

    if perform_correlation_with_external_data:

        correlation_with_external_data( directory, output_directory, file_data, data )

    if perform_normalisation_experimentation:

        normalisation_experimentation( directory, output_directory, file_data, data )

    if perform_pp_percentage_model:

        pp_percentage_model( directory, output_directory, file_data, data )

    if perform_crystallinity_determination:

        crystallinity_determination( directory, output_directory, file_data, data )
