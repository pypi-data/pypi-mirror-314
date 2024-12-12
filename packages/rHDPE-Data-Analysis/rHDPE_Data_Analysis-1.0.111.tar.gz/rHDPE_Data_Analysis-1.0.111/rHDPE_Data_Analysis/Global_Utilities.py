from distinctipy import distinctipy
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.spatial.distance import squareform
from sklearn.decomposition import PCA
import pandas as pd
import re
from scipy.optimize import curve_fit
from adjustText import adjust_text
import math
import itertools
import sys
from pathlib import Path

sys.path.append( Path( __file__ ).absolute().parents[0].as_posix() + "/Global/" )

from .Global_Analysis import Utilities as util

from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as robjects

def source_R_functions( directory ):

    r = robjects.r
    r['source']( directory + 'rHDPE_R_Functions.R' )

def authorise_googledrive( directory ):

    robjects.globalenv['authorise_googledrive']( directory )

def read_csv_from_gd_via_R( directory, filename ):

    read_csv_from_gd = robjects.globalenv['read_csv_from_gd']

    rdf = read_csv_from_gd( directory, filename )

    with localconverter( robjects.default_converter + pandas2ri.converter ):

        pydf = robjects.conversion.rpy2py( rdf )

    return pydf

def read_csv_pipeline( ip, directory, filename, authorised = False ):

    try:

        df = pd.read_csv( ip.output_directory + directory + filename, index_col = 0 )

    except FileNotFoundError:

        try:

            df = pd.read_csv( "tmp/" + directory + filename, index_col = 0 )

        except FileNotFoundError:

            if ip.user == "shiny" or ip.user == "philsmith":

                if not authorised:

                    source_R_functions( ip.directory )

                    authorise_googledrive( ip.directory )

                    authorised = True

                print( "File not found on server, getting it from Google Drive." )

                df = read_csv_from_gd_via_R( directory, "~/Output/" + directory + filename )

    return df, authorised

def print_files_read( files_read, target ):

    print( str( files_read ) + " files have been read." )

    if files_read != target:

        print( "Warning: " + str( target ) + " files have not been read." )

def test_for_duplicates( file_data, data ):

    for i in range( len( file_data ) ):

        for j in range( i + 1, len( file_data ) ):

            if (data[i] == data[j]).all():

                print( file_data[i], file_data[j], "are the same!" )

def sort_raw_files_1( elem ):
    '''Files will have form ResinX, sorting according to X.'''

    pattern = re.compile( r"^Resin(\d+)" )

    return int( pattern.search( elem ).groups()[0] )

def sort_raw_files_2( elem ):
    '''Files will have form ResinX_Y_, sorting according to Y.'''

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    return int( pattern.search( elem ).groups()[1] )

def sort_raw_files_3( elem ):
    '''Files will have form ResinX_Y_, sorting according to X, then Y.'''

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    return [int( pattern.search( elem ).groups()[0] ), int( pattern.search( elem ).groups()[1] )]

def get_list_of_resins_data( directory, name_appendage = "" ):

    return pd.read_excel( directory + "List_of_Resins" + name_appendage + ".xlsx", header = 0, index_col = 0 )

def get_features_metadata( directory ):

    df = pd.read_excel( directory + "Features_Metadata.xlsx", header = 0, index_col = 0 )

    return df

def merge( file_data ):
    '''Merge resins that are technically the same material.'''

    # Resin40 becomes Resin5
    # Resin41 becomes Resin20
    # Resin1XX becomes ResinXX
    # Resin324 becomes Resin24

    for i in range( len( file_data ) ):

        if file_data[i][0] == 40:

            file_data[i][0] = 5

        if file_data[i][0] == 41:

            file_data[i][0] = 20

        if file_data[i][0] >= 101 and file_data[i][0] <= 200:

            file_data[i][0] -= 100

        if file_data[i][0] == 324:

            file_data[i][0] = 24

def extract_file_data_from_filenames( filenames, pattern_string ):
    """Returns file_data object of form [PCR Sample, PCR Specimen, Plot Label, Description]."""

    file_data = []

    pattern = re.compile( pattern_string )

    for f in filenames:

        sample = int( pattern.search( f ).groups()[0] )
        specimen = int( pattern.search( f ).groups()[1] )

        if sample == 0:

            file_data.append( [sample, specimen, "V{}.{}".format( 1, specimen ), ""] )

        elif sample == 16:

            file_data.append( [sample, specimen, "V{}.{}".format( 6, specimen ), ""] )

        elif sample == 17:

            file_data.append( [sample, specimen, "V{}.{}".format( 7, specimen ), ""] )

        elif sample == 19:

            file_data.append( [sample, specimen, "V{}.{}".format( 8, specimen ), ""] )

        else:

            file_data.append( [sample, specimen, "PCR{}.{}".format( sample, specimen ), ""] )

    return file_data

def sample_data_from_file_data( file_data ):
    '''Extract sample data from file data.'''

    sample = []

    for f in file_data:

        sample.append( f[0] )

    sample_array = np.array( sample )
    samples_present = sorted( list( set( sample ) ) )
    samples_present_array = np.array( samples_present )

    return sample, sample_array, samples_present, samples_present_array

def sample_mean( file_data, data ):
    '''Compute the mean for each sample.'''

    m = []

    sample, sample_array, samples_present, samples_present_array = sample_data_from_file_data( file_data )

    for i in samples_present:

        mean_array = []

        mask = np.where( sample_array == i )[0]

        for j in range( len( data[mask[0]] ) ):

            mean = 0

            for k in mask:

                mean += data[k][j]

            mean /= len( mask )

            mean_array.append( mean )

        m.append( np.array( mean_array ) )

    return m

def derivative( x, y, width = 1 ):
    '''Computes the derivative of a set of xy points.'''

    deriv = []

    for i in range( width, len( x ) - width ):

        if x[i + width] == x[i - width]:

            if i != width:

                deriv_at_point = deriv[i - width - 1]

            else:

                x = 1 / 0 # To retrun divide by zero error.

        else:

            deriv_at_point = (y[i + width] - y[i - width]) / (x[i + width] - x[i - width])

        deriv.append( deriv_at_point )

    return deriv

def integral_1( x, y, start, end, min_val = 0 ):
    '''Compute the integral of an xy curve between bounds. This is a true integral, perhaps with a subtraction of a rectangle with height the minimum value.'''

    integral = 0

    for i in range( start, end ):

        integral += abs( x[i] - x[i + 1] ) * 0.5 * (y[i] + y[i + 1] - 2 * min_val)

    return integral

def integral_2( x, y, start, end, min_val = 0 ):
    '''Compute the integral of an xy curve between bounds. This is the integral if the baseline is the line from the startpoint to the endpoint.'''

    integral = 0

    for i in range( start, end ):

        integral += abs( x[i] - x[i + 1] ) * 0.5 * (y[i] + y[i + 1] - 2 * min_val)

    integral -= abs( y[start] - y[end] ) * abs( x[start] - x[end] ) * 0.5

    return integral

def integral_3( y, width ):
    '''Compute the integral of an xy curve where the data points are at regular intervals (width).'''

    return (y[1: -1].sum() + 0.5 * (y[0] + y[-1])) * width

def array_with_column_titles_to_df( array, titles ):

    df = pd.DataFrame( array )
    df.columns = titles

    return df

def csv_to_df_to_array_and_column_titles( filename ):

    df = pd.read_csv( filename )

    df.drop( columns = [df.columns[0]], inplace = True )

    column_titles = df.columns.tolist()

    array_columns = []

    for i in range( len( df.columns ) ):

        array_columns.append( df.iloc[:, i].to_numpy() )

    array = array_columns[0][:, np.newaxis]

    for i in range( 1, len( array_columns ) ):

        array = np.hstack( (array, array_columns[i][:, np.newaxis]) )

    return column_titles, array

def remove_redundant_samples( sample_mask, samples_present ):

    to_pop = []

    for ind, i in enumerate( sample_mask ):

        if i not in samples_present:

            to_pop.append( ind )

    to_pop.reverse()

    for p in to_pop:

        sample_mask.pop( p )

    return sample_mask

def produce_mask( array_to_mask, desired_mask ):
    '''Generate a mask to apply given an array to mask and a desired mask.'''

    applied_mask = np.where( array_to_mask == desired_mask[0] )[0]

    for idx, k in enumerate( desired_mask ):

        if idx == 0:

            continue

        applied_mask = np.concatenate( [applied_mask, np.where( array_to_mask == k )[0]] )

    return applied_mask

def normalise_features( features, feature_weights = [] ):

    for i in range( features.shape[1] ):

        min = features[:, i].min()
        max = features[:, i].max()
        feature_range = max - min

        feature_weight = 1

        if feature_weights:

            feature_weight = feature_weights[i]

        features[:, i] = feature_weight * (features[:, i] - min) / feature_range

def combine_features( features, feature_names = [], feature_combinations = [] ):

    new_features = np.zeros( len( features ) )[:, np.newaxis]
    new_feature_names = []

    for i in feature_combinations:

        feature = np.zeros( len( features ) )

        feature_name = ""

        for j in i:

            feature += features[:, j]

            if not feature_name and feature_names:

                feature_name += feature_names[j]

        feature /= len( i )

        new_features = np.hstack( (new_features, np.array( feature )[:, np.newaxis]) )

        new_feature_names.append( feature_name )

    new_features = new_features[:, 1:]

    if not feature_combinations:

        return features, feature_names

    else:

        return new_features, new_feature_names

def extract_mean_features( features, sample_array, sample_mask ):

    mean_features = np.zeros( (len( sample_mask ), features.shape[1] ) )

    for ind, i in enumerate( sample_mask ):

        mask = np.where( np.array( sample_array ) == i )[0]

        for m in mask:

            for j in range( features.shape[1] ):

                mean_features[ind][j] += features[m][j]

        mean_features[ind] = mean_features[ind] / len( mask )

    return mean_features

def extract_mean_features_2( features, sample_array, sample_mask ):

    mean_features = np.zeros( (len( sample_mask ), features.shape[1] ) )

    for ind, i in enumerate( sample_mask ):

        mask = np.where( np.array( sample_array ) == i )[0]

        for m in mask:

            for j in range( features.shape[1] ):

                mean_features[ind][j] += features[m][j]

        if len( mask ) == 2:

            mean_features[ind] = mean_features[ind] / len( mask )

        else:

            for j in range( features.shape[1] ):

                mean_features[ind][j] -= features[mask, j].max()
                mean_features[ind][j] -= features[mask, j].min()

            mean_features[ind] = mean_features[ind] / (len( mask ) - 2)

    return mean_features

def extract_std_of_features( features, sample_array, sample_mask ):

    std_of_features = np.zeros( (len( sample_mask ), features.shape[1] ) )

    for ind, i in enumerate( sample_mask ):

        mask = np.where( np.array( sample_array ) == i )[0]

        if len( mask ) <= 1:

            for j in range( features.shape[1] ):

                std_of_features[ind][j] = 0

        else:

            for j in range( features.shape[1] ):

                std_of_features[ind][j] = np.std( features[mask, j], ddof = 1 ) / np.sqrt( len( mask ) )

    return std_of_features

def extract_range_of_features( features, sample_array, sample_mask ):

    range_of_features = np.zeros( (len( sample_mask ), features.shape[1] ) )

    for ind, i in enumerate( sample_mask ):

        mask = np.where( np.array( sample_array ) == i )[0]

        if len( mask ) <= 1:

            for j in range( features.shape[1] ):

                range_of_features[ind][j] = 0

        else:

            for j in range( features.shape[1] ):

                range_of_features[ind][j] = np.ptp( features[mask, j] )

    return range_of_features

def add_mean_feature( features, feature_names, sample_mask, new_feature, feature_name, weight = 1 ):

    feature = np.array( new_feature )[sample_mask]

    normalised_feature = (feature - feature.min()) / (feature.max() - feature.min()) * weight

    features = np.hstack( (features, np.array( normalised_feature )[:, np.newaxis]) )
    # features = np.hstack( (features, feature[:, np.newaxis]) )

    feature_names.append( feature_name )

    return features, feature_names

def compute_range_mean_std( data, mask ):
    '''Computes the range, median, mean and standard deviation of a set of curves.'''

    range_list = []
    high_point = []
    low_point = []
    median = []
    mean = []
    std = []

    for i in range( len( data[0] ) ):

        value = np.zeros( len( mask ) )

        for j, k in enumerate( mask ):

            value[j] = data[k][i]

        value = np.sort( value )

        range_list.append( value.max() - value.min() )
        high_point.append( value.max() )
        low_point.append( value.min() )

        if len( mask ) % 2 == 0:

            median.append( (value[int( len( mask ) / 2 )] + value[int( len( mask ) / 2 - 1 )]) / 2 )

        else:

            median.append( value[int( (len( mask ) - 1) / 2 )] )

        m = value.sum() / len( mask )
        mean.append( m )

        dev = 0

        for j in range( len( mask ) ):

            dev += (value[j] - m) * (value[j] - m)

        dev /= len( mask )

        dev = math.sqrt( dev )

        std.append( dev )

    return range_list, high_point, low_point, median, mean, std

def index_to_label( i ):

    if i == 24:

        return "V1"

    elif i < 0:

        return "V{}".format( 1 - i)

    elif i == 16:

        return "V1"

    elif i == 17:

        return "V2"

    elif i == 19:

        return "V3"

    else:

        return "PCR {}".format( i )

def plot_global_features( output_directory, features, feature_names, labels, subdirectory = "Features/", title = "Unnamed.pdf" ):

    features = np.transpose( features )

    fig, ax = plt.subplots()

    fig.set_size_inches( 5, 12 )

    im = ax.imshow( features, cmap = cm.plasma )
    plt.xticks( np.arange( 0, len( labels ), 1 ) )
    plt.yticks( np.arange( 0, len( feature_names ), 1 ) )
    plt.tick_params( left = False )

    ax.set_yticklabels( [n for n in feature_names], fontsize = 10 )
    # ax.set_yticklabels( labels = "" )
    ax.set_xticklabels( labels, rotation = 270, fontsize = 13 )

    linewidth = 6

    x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [-0.5, -0.5, 32.5, 32.5, -0.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [32.5, 32.5, 37.5, 37.5, 32.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [37.5, 37.5, 43.5, 43.5, 37.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [43.5, 43.5, 48.5, 48.5, 43.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [48.5, 48.5, 52.5, 52.5, 48.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [52.5, 52.5, 55.5, 55.5, 52.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    # x, y = ([-0.5, 22.5, 22.5, -0.5, -0.5], [57.5, 57.5, 59.5, 59.5, 57.5])
    # line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    # ax.add_line( line )

    cbar = fig.colorbar( im, orientation = 'horizontal', location = 'top', shrink = 0.8, pad = 0.02 )
    cbar.ax.tick_params( labelsize = 13 )

    plt.tight_layout()

    plt.savefig( output_directory + subdirectory + title )

    plt.close()

def plot_global_features_transpose( output_directory, features, feature_names, labels, subdirectory = "Features/", title = "Unnamed.pdf" ):

    fig, ax = plt.subplots()

    fig.set_size_inches( 12, 6 )

    im = ax.imshow( features, cmap = cm.plasma )
    plt.xticks( np.arange( 0, len( feature_names ), 1 ) )
    plt.yticks( np.arange( 0, len( labels ), 1 ) )

    ax.set_xticklabels( [n for n in feature_names], rotation = 270, fontsize = 10 )
    ax.set_yticklabels( labels, fontsize = 10 )

    linewidth = 6

    y, x = ([-0.5, 22.5, 22.5, -0.5, -0.5], [-0.5, -0.5, 32.5, 32.5, -0.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    y, x = ([-0.5, 22.5, 22.5, -0.5, -0.5], [32.5, 32.5, 37.5, 37.5, 32.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    y, x = ([-0.5, 22.5, 22.5, -0.5, -0.5], [37.5, 37.5, 43.5, 43.5, 37.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    y, x = ([-0.5, 22.5, 22.5, -0.5, -0.5], [43.5, 43.5, 48.5, 48.5, 43.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    y, x = ([-0.5, 22.5, 22.5, -0.5, -0.5], [48.5, 48.5, 52.5, 52.5, 48.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    y, x = ([-0.5, 22.5, 22.5, -0.5, -0.5], [52.5, 52.5, 55.5, 55.5, 52.5])
    line = mlines.Line2D( x, y, lw = linewidth, c = 'lime' )
    ax.add_line( line )

    fig.colorbar( im, orientation = 'vertical', location = 'right', shrink = 0.75, pad = 0.02 )

    plt.tight_layout()

    plt.savefig( output_directory + subdirectory + title )

    plt.close()

def plot_boxplot( directory, features, feature_names, file_data, sample_mask, feature_name, xlabel = "", ylabel = "", filename = "", savefig = False ):

    resin_data = get_list_of_resins_data( directory )

    sample, sample_array, samples_present, samples_present_array = sample_data_from_file_data( file_data )

    sample_mask = remove_redundant_samples( sample_mask, samples_present )

    boxplot_list = []

    for i in sample_mask:

        specimen_mask = produce_mask( sample_array, [i] )

        features_2 = features[specimen_mask, feature_names.index( feature_name )]

        boxplot_list.append( features_2.tolist() )

    plt.boxplot( boxplot_list, whis = 10 )

    ax = plt.gca()

    ax.set_xticks( [y + 1 for y in range( len( boxplot_list ) )], labels = [resin_data.loc[i]["Label"] for i in sample_mask] )

    ax.set_xlabel( xlabel )
    ax.set_ylabel( ylabel )

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()

def plot_features( output_directory, features, feature_names, labels, specimen = False, subdirectory = "Features/", title = "Unnamed.pdf" ):

    fig, ax = plt.subplots()

    if specimen:

        fig.set_size_inches( 13, 18 )

    else:

        fig.set_size_inches( 8, 4 )

    im = ax.imshow( features, vmin = 0, vmax = 1, cmap = cm.plasma )
    plt.xticks( np.arange( 0, len( feature_names ), 1 ) )
    plt.yticks( np.arange( 0, len( labels ), 1 ) )

    if specimen:

        ax.set_xticklabels( [n for n in feature_names], rotation = 270, fontsize = 7 )
        ax.set_yticklabels( labels, fontsize = 7 )

    else:

        ax.set_xticklabels( [n for n in feature_names], rotation = 270, fontsize = 8 )
        ax.set_yticklabels( labels, fontsize = 7 )

    # [l.set_visible(False) for (i, l) in enumerate( ax.xaxis.get_ticklabels() ) if i % 2 != 0]

    cbar = fig.colorbar( im, orientation = 'vertical' )
    # cbar.ax.tick_params( labelsize = 9 )

    plt.tight_layout()
    ax.invert_yaxis()
    ax.invert_xaxis()

    plt.savefig( output_directory + subdirectory + title )

    plt.close()

def list_of_colours():
    '''Returns an object of 28 colours.'''

    colours = [(0, 0, 0)]

    colours.extend( distinctipy.get_colors( 130, pastel_factor = 0.2, rng = 2 ) )

    colours.extend( colours )
    colours.extend( colours )
    colours.extend( colours )

    return colours

def read_list_of_colours( directory ):

    df = pd.read_csv( directory + "List_of_Colours.csv" )

    return [(df.at[i, "r"], df.at[i, "g"], df.at[i, "b"]) for i in range( len( df.index ) )]

def write_list_of_colours_to_file( output_directory ):

    colours = list_of_colours()

    df = pd.DataFrame( colours )

    df.columns = ["r", "g", "b"]

    df.to_csv( output_directory + "List_of_Colours.csv" )

def plot_barchart_of_feature( features, labels, errorbars = False, std = [], colour = False, colour_mask = [], xlabel = "", ylabel = "", title = "", filename = "", savefig = False ):

    y_pos = np.arange( len( features ) )

    colours = list_of_colours()
    colours = [colours[i] for i in colour_mask]

    if colour:

        plt.bar( y_pos, features, align = 'center', alpha = 0.5, color = colours )

    else:

        plt.bar( y_pos, features, align = 'center', alpha = 0.5 )

    if errorbars:

        ax = plt.gca()

        for x, y, e, colour in zip( y_pos, features, std, colours ):

            ax.errorbar( x, y, e, capsize = 4, color = colour )

    plt.xticks( y_pos, labels, rotation = 90 )

    plt.xlabel( xlabel )
    plt.ylabel( ylabel )
    plt.title( title )

    plt.ylim( [55, 75] )

    plt.tight_layout()

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()

def distance_matrix_from_features( features ):

    distance_matrix = np.zeros( (features.shape[0], features.shape[0]) )

    for i in range( features.shape[0] ):

        for j in range( i + 1, features.shape[0] ):

            distance_matrix[i][j] = distance_matrix[j][i] = np.absolute( features[i] - features[j] ).sum()

    return distance_matrix

def array_with_column_titles_and_label_titles_to_df( array, column_titles, label_titles ):

    df = pd.DataFrame( array )
    df.columns = column_titles
    df = df.set_axis( label_titles, axis = "index" )

    return df

def subset_combinations_for_all_sizes_of_subsets( set_size ):

    set = range( set_size )

    combinations = []

    for L in range( set_size ):

        for subset in itertools.combinations( set, set_size - L ):

            combinations.append( list( subset ) )

    return combinations

def plot_boxes( ax, width, height, origin_x, origin_y ):
    '''Add boxes to a distance matrix around specimens of the same sample.'''

    x, y = ([origin_x, width + origin_x, width + origin_x, origin_x, origin_x], [origin_y, origin_y, height + origin_y, height + origin_y, origin_y])
    line = mlines.Line2D( x, y, lw = 1, c = 'w' )
    ax.add_line( line )

def plot_distance_matrix( output_directory, distance_matrix, labels, specimen = False, file_data = [], sample_mask = [], subdirectory = "Features/", title = "Unnamed.pdf" ):

    fig, ax = plt.subplots()

    if specimen:

        fig.set_size_inches( 20, 20 )

    else:

        fig.set_size_inches( 9, 9 )

    im = ax.imshow( distance_matrix, cmap = cm.plasma )

    # fig.colorbar( im, orientation = 'vertical' )

    plt.xticks( np.arange( 0, len( labels ), 1 ) )
    plt.yticks( np.arange( 0, len( labels ), 1 ) )

    if specimen:

        ax.set_xticklabels( labels, rotation = 270, fontsize = 6 )
        ax.set_yticklabels( labels, fontsize = 6 )

    else:

        ax.set_xticklabels( labels, rotation = 270, fontsize = 8 )
        ax.set_yticklabels( labels, fontsize = 8 )

    if not specimen:

        for i in range( len( labels ) ):

            for j in range( len( labels ) ):

                ax.text( j, i, "{:.0f}".format( distance_matrix[i][j] ), ha = "center", va = "center", color = "w" )

    if specimen:

        sample, sample_array, samples_present, samples_present_array = sample_data_from_file_data( file_data )

        num_specimens_of_each_sample = np.zeros( len( samples_present ) )

        for f in file_data:

            num_specimens_of_each_sample[np.argwhere( samples_present_array == f[0] )[0]] += 1

        cumulative_specimens_x = 0

        for i in range( len( sample_mask ) ):

            cumulative_specimens_y = 0

            for j in range( len( sample_mask ) ):

                plot_boxes( ax, num_specimens_of_each_sample[samples_present.index( sample_mask[i] )], num_specimens_of_each_sample[samples_present.index( sample_mask[j] )], -0.5 + cumulative_specimens_x, -0.5 + cumulative_specimens_y )

                cumulative_specimens_y += num_specimens_of_each_sample[samples_present.index( sample_mask[j] )]

            cumulative_specimens_x += num_specimens_of_each_sample[samples_present.index( sample_mask[i] )]

    plt.tight_layout()
    ax.invert_yaxis()

    plt.savefig( output_directory + subdirectory + title )

    plt.close()

def plot_dendrogram( output_directory, distance_matrix, labels, specimen = False, subdirectory = "Features/", title = "Unnamed.pdf" ):

    fig, ax = plt.subplots()

    if specimen:

        fig.set_size_inches( 18, 14 )

    else:

        fig.set_size_inches( 10, 8 )

    condensed_distance_matrix = squareform( distance_matrix )
    linkage_matrix = linkage( condensed_distance_matrix, "ward" )
    dendrogram( linkage_matrix, labels = labels, color_threshold = 0.65 * max( linkage_matrix[:,2] ), count_sort = True, leaf_rotation = 90 )

    plt.tight_layout()

    plt.savefig( output_directory + subdirectory + title )

    plt.close()

def csv_to_df_to_array_and_column_titles_and_label_titles( filename ):

    df = pd.read_csv( filename )

    label_titles = df[df.columns[0]].tolist()

    df.drop( columns = [df.columns[0]], inplace = True )

    column_titles = df.columns.tolist()

    array_columns = []

    for i in range( len( df.columns ) ):

        array_columns.append( df.iloc[:, i].to_numpy() )

    array = array_columns[0][:, np.newaxis]

    for i in range( 1, len( array_columns ) ):

        array = np.hstack( (array, array_columns[i][:, np.newaxis]) )

    return array, column_titles, label_titles

def func( x, a, b, c ):

    return a * np.exp( b * x ) + c

def exponential_curve_fit( feature_1, feature_2 ):

    feature_1 = np.array( feature_1 )
    feature_2 = np.array( feature_2 )

    xdata_max = feature_1.max()
    ydata_max = feature_2.max()

    xdata = feature_1 / xdata_max
    ydata = feature_2 / ydata_max

    temp = xdata.argsort()

    xdata = xdata[temp]
    ydata = ydata[temp]

    popt, pcov = curve_fit( func, xdata, ydata, maxfev = 800 )

    popt[0] = popt[0] * feature_2.max()
    popt[1] = popt[1] / feature_1.max()
    popt[2] = popt[2] * feature_2.max()

    return popt

def plot_scatterplot_of_two_features( directory, feature_1, feature_2, sample, labels, errorbars = False, std = [], line_of_best_fit = True, exponential_fit = False, xlog = False, ylog = False, title = "", xlabel = "", ylabel = "", annotate_style = 1, savefig = False, filename = "" ):

    colours = read_list_of_colours( directory )
    scatter_colours = [colours[sample[i]] for i in range( len( feature_1 ) )]
    # scatter_colours = sample

    if errorbars:

        ax = plt.gca()

        for x, y, xe, ye, colour in zip( feature_1, feature_2, std[0], std[1], scatter_colours ):

            ax.errorbar( x, y, xerr = xe, yerr = ye, fmt = "none", capsize = 4, ecolor = colour, zorder = 0 )

    sc = plt.scatter( feature_1, feature_2, color = scatter_colours, s = 100 )
    # sc = plt.scatter( feature_1, feature_2, edgecolor = "red", linewidths = 1, s = 120, c = scatter_colours )

    fig = plt.gcf()
    ax = plt.gca()

    # ax.plot( [np.min( [ax.get_xlim(), ax.get_ylim()] ), np.max( [ax.get_xlim(), ax.get_ylim()] )], [np.min( [ax.get_xlim(), ax.get_ylim()] ), np.max( [ax.get_xlim(), ax.get_ylim()] )], 'k-', alpha = 0.75, zorder = 0 )

    if line_of_best_fit:

        m, b = np.polyfit( feature_1, feature_2, 1 )

        plt.plot( feature_1, feature_1 * m + b )

    if exponential_fit:

        popt = exponential_curve_fit( feature_1, feature_2 )

        # funcx = np.linspace( 0.007, 1, 1000 )
        # funcx = np.linspace( -0.07, feature_1.max(), 1000 )
        funcx = np.linspace( feature_1.min(), feature_1.max(), 1000 )

        plt.plot( funcx, func( funcx, *popt ), 'r-', label = 'fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple( popt ) )

    plt.title( title )
    plt.xlabel( xlabel, fontsize = 13 )
    plt.ylabel( ylabel, fontsize = 13 )

    if annotate_style == 1:

        for i in range( len( feature_1 ) ):

            ax.annotate( labels[i], (feature_1[i] + 0.001, feature_2[i] + 0.001), fontsize = 13 )

    elif annotate_style == 2:

        TEXTS = []

        for i in range( len( feature_1 ) ):

            x = feature_1[i]
            y = feature_2[i]
            text = labels[i]

            TEXTS.append( ax.text( x, y, text, color = scatter_colours[i], fontsize = 14 ) )

        # 'expand_points' is a tuple with two multipliers by which to expand the bounding box of texts when repelling them from points.
        # 'arrowprops' receives a dictionary with all the properties we want for the arrows.

        # adjust_text( TEXTS, arrowprops = dict( arrowstyle = "->", lw = 2 ), expand_points = (3, 3), expand_text = (1, 1) )
        adjust_text( TEXTS, arrowprops = dict( arrowstyle = "->", lw = 2 ) )

    ax = plt.gca()

    if xlog == True:

        ax.set_xscale( 'log' )

    if ylog == True:

        ax.set_yscale( 'log' )

    # plt.xlim( [0, 1] )
    # plt.ylim( [0, 1] )

    plt.tight_layout()

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()

    # array = feature_1[:, np.newaxis]
    #
    # array = np.hstack( (array, feature_2[:, np.newaxis], np.array( std[0] )[:, np.newaxis], np.array( std[1] )[:, np.newaxis]) )
    #
    # np.savetxt( "/Users/philsmith/Documents/Postdoc/rHDPE_Data_Analysis/Output/Plot_Coords/Unnamed.txt", array )

    # array = 10 ** np.array( feature_1 )[:, np.newaxis]

    # array = np.hstack( (array, np.array( feature_2 )[:, np.newaxis]) )

    # array = np.hstack( (array, np.array( feature_2 )[:, np.newaxis], np.array( std[0] )[:, np.newaxis], np.array( std[1] )[:, np.newaxis]) )

    # array = np.pad( array, ((0, 976), (0, 0)) )

    # m, b = np.polyfit( feature_1, feature_2, 1 )
    #
    # array = np.hstack( (array, (np.array( feature_1 ) * m + b)[:, np.newaxis]) )

    # popt = exponential_curve_fit( feature_1, feature_2 )
    #
    # funcx = np.linspace( feature_1.min(), feature_1.max(), 1000 )
    #
    # array = np.hstack( (array, np.array( funcx )[:, np.newaxis], np.array( func( funcx, *popt ) )[:, np.newaxis]) )

    # np.savetxt( "/Users/philsmith/Documents/Postdoc/rHDPE_Data_Analysis/Output/Plot_Coords/Unnamed.txt", array )

def plot_scatterplot_of_two_features_pca( directory, feature_1, feature_2, coeff, coeff_names, sample, labels, errorbars = False, std = [], line_of_best_fit = True, exponential_fit = False, xlog = False, ylog = False, title = "", xlabel = "", ylabel = "", annotate_style = 1, savefig = False, filename = "" ):

    colours = read_list_of_colours( directory )
    scatter_colours = [colours[sample[i]] for i in range( len( feature_1 ) )]
    # scatter_colours = sample

    if errorbars:

        ax = plt.gca()

        for x, y, xe, ye, colour in zip( feature_1, feature_2, std[0], std[1], scatter_colours ):

            ax.errorbar( x, y, xerr = xe, yerr = ye, fmt = "none", capsize = 4, ecolor = colour, zorder = 0 )

    sc = plt.scatter( feature_1, feature_2, color = scatter_colours, s = 100 )

    fig = plt.gcf()
    ax = plt.gca()

    # ax.plot( [np.min( [ax.get_xlim(), ax.get_ylim()] ), np.max( [ax.get_xlim(), ax.get_ylim()] )], [np.min( [ax.get_xlim(), ax.get_ylim()] ), np.max( [ax.get_xlim(), ax.get_ylim()] )], 'k-', alpha = 0.75, zorder = 0 )

    if line_of_best_fit:

        m, b = np.polyfit( feature_1, feature_2, 1 )

        plt.plot( feature_1, feature_1 * m + b )

    if exponential_fit:

        xdata = feature_1
        ydata = feature_2

        temp = xdata.argsort()

        xdata = xdata[temp]
        ydata = ydata[temp]

        popt, pcov = curve_fit( func, xdata, ydata )

        funcx = np.linspace( 0.007, 1, 1000 )

        plt.plot( funcx, func( funcx, *popt ), 'r-', label = 'fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple( popt ) )

    n = coeff.shape[0]

    for i in range( n ):

        plt.arrow( 0, 0, coeff[i, 0], coeff[i, 1], color = 'r', alpha = 0.5 )

        plt.text( coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, coeff_names[i], color = 'b', ha = 'center', va = 'center' )

    plt.title( title )
    plt.xlabel( xlabel, fontsize = 13 )
    plt.ylabel( ylabel, fontsize = 13 )

    if annotate_style == 1:

        for i in range( len( feature_1 ) ):

            ax.annotate( labels[i], (feature_1[i] + 0.001, feature_2[i] + 0.001), fontsize = 13 )

    elif annotate_style == 2:

        TEXTS = []

        for i in range( len( feature_1 ) ):

            x = feature_1[i]
            y = feature_2[i]
            text = labels[i]

            TEXTS.append( ax.text( x, y, text, color = scatter_colours[i], fontsize = 14 ) )

        # 'expand_points' is a tuple with two multipliers by which to expand the bounding box of texts when repelling them from points.
        # 'arrowprops' receives a dictionary with all the properties we want for the arrows.

        # adjust_text( TEXTS, arrowprops = dict( arrowstyle = "->", lw = 2 ), expand_points = (3, 3), expand_text = (1, 1) )
        adjust_text( TEXTS, arrowprops = dict( arrowstyle = "->", lw = 2 ) )

    ax = plt.gca()

    if xlog == True:

        ax.set_xscale( 'log' )

    if ylog == True:

        ax.set_yscale( 'log' )

    # plt.xlim( [0, 1] )
    # plt.ylim( [0, 1] )

    plt.tight_layout()

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()

    # array = feature_1[:, np.newaxis]
    #
    # array = np.hstack( (array, feature_2[:, np.newaxis], np.array( std[0] )[:, np.newaxis], np.array( std[1] )[:, np.newaxis]) )
    #
    # np.savetxt( "/Users/philsmith/Documents/Postdoc/rHDPE_Data_Analysis/Output/Plot_Coords/Unnamed.txt", array )

    # array = np.array( feature_1 )[:, np.newaxis]
    #
    # array = np.hstack( (array, feature_2[:, np.newaxis], np.array( std[0] )[:, np.newaxis], np.array( std[1] )[:, np.newaxis]) )
    #
    # for i in range( 2 ):
    #
    #     array_2 = np.pad( coeff[:, i], (0, len( array[:, 0] ) - len( coeff[:, i] )) )
    #
    #     array = np.hstack( (array, array_2[:, np.newaxis]) )
    #
    # np.savetxt( "/Users/philsmith/Documents/Postdoc/rHDPE_Data_Analysis/Output/Plot_Coords/Unnamed.txt", array )

def plot_scatterplot_of_three_features( directory, feature_1, feature_2, feature_3, samples_present, labels, title = "", xlabel = "", ylabel = "", zlabel = "", savefig = False, filename = "" ):

    colours = read_list_of_colours( directory )
    scatter_colours = [colours[samples_present[i]] for i in range( len( samples_present ) )]
    # scatter_colours = samples_present # Current method of plotting the actual resin colours.

    fig = plt.figure()
    ax = fig.add_subplot( projection = '3d' )

    ax.scatter3D( feature_1, feature_2, feature_3, s = 120, color = scatter_colours )
    # ax.scatter3D( feature_1, feature_2, feature_3, edgecolor = "red", linewidths = 1, s = 120, c = scatter_colours )

    for i in range( len( feature_1 ) ):

        ax.text( feature_1[i], feature_2[i], feature_3[i], labels[i], size = 8, zorder = 1,  color = 'k' )

    ax.set_title( title )
    ax.set_xlabel( xlabel )
    ax.set_ylabel( ylabel )
    ax.set_zlabel( zlabel )

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()

    array = np.array( feature_1 )[:, np.newaxis]

    array = np.hstack( (array, np.array( feature_2 )[:, np.newaxis]) )

    array = np.hstack( (array, np.array( feature_3 )[:, np.newaxis]) )

    np.savetxt( "/Users/philsmith/Documents/Postdoc/rHDPE_Data_Analysis/Output/Plot_Coords/Unnamed.txt", array )

def plot_scatterplot_of_two_features_with_hover_annotation( feature_1, feature_2, sample_mask, labels, xlabel = "", ylabel = "", title = "", savefig = False, filename = "" ):

    colours = list_of_colours()
    scatter_colours = [colours[sample_mask[i]] for i in range( len( feature_1 ) )]

    sc = plt.scatter( feature_1, feature_2, color = scatter_colours )

    lp = lambda i: plt.plot( [], color = colours[sample_mask[i]], label = labels[i], marker = "o" )[0]
    handles = [lp( i ) for i in range( len( sample_mask ) )]
    plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )

    fig, ax = plt.gcf(), plt.gca()

    annot = ax.annotate( "", xy = ( 0, 0 ), xytext = ( 20, 20 ), textcoords = "offset points", bbox = dict( boxstyle = "round", fc = "w" ), arrowprops = dict( arrowstyle = "->" ) )
    annot.set_visible( False )

    def update_annot( ind ):
        '''Update the annotation of a dot in the plot.'''

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos

        text = ""

        for i in range( len( ind["ind"] ) ):

            if i >= 1:

                text += ", "

            text += labels[ind["ind"][i]]

        annot.set_text( text )
        annot.get_bbox_patch().set_alpha( 0.4 )

    def hover( event ):
        '''Determine what happens when the mouse hovers over a point in the plot.'''

        vis = annot.get_visible()

        if event.inaxes == ax:

            cont, ind = sc.contains( event )

            if cont:

                update_annot( ind )
                annot.set_visible( True )
                fig.canvas.draw_idle()

            else:

                if vis:

                    annot.set_visible( False )
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect( "motion_notify_event", hover )

    plt.xlabel( xlabel )
    plt.ylabel( ylabel )
    plt.title( title )

    plt.tight_layout()

    if savefig:

        plt.savefig( filename )

    plt.show()

    plt.close()

def plot_scatterplot_of_two_specimen_features_with_hover_annotation( feature_1, feature_2, file_data, xlabel = "", ylabel = "", title = "", savefig = False, filename = "" ):

    sample, sample_array, samples_present, samples_present_array = sample_data_from_file_data( file_data )

    colours = list_of_colours()
    scatter_colours = [colours[file_data[i][0]] for i in range( len( feature_1 ) )]

    sc = plt.scatter( feature_1, feature_2, color = scatter_colours )

    lp = lambda i: plt.plot( [], color = colours[samples_present[i]], label = index_to_label( samples_present[i] ), marker = "o" )[0]
    handles = [lp( i ) for i in range( len( samples_present ) )]
    plt.legend( handles = handles )
    plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'upper left', borderaxespad = 0 )

    fig, ax = plt.gcf(), plt.gca()

    annot = ax.annotate( "", xy = ( 0, 0 ), xytext = ( 20, 20 ), textcoords = "offset points", bbox = dict( boxstyle = "round", fc = "w" ), arrowprops = dict( arrowstyle = "->" ) )
    annot.set_visible( False )

    def update_annot( ind ):
        '''Update the annotation of a dot in the plot.'''

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos

        text = ""

        for i in range( len( ind["ind"] ) ):

            if i >= 1:

                text += ", "

            text += file_data[ind["ind"][i]][2]

        annot.set_text( text )
        annot.get_bbox_patch().set_alpha( 0.4 )

    def hover( event ):
        '''Determine what happens when the mouse hovers over a point in the plot.'''

        vis = annot.get_visible()

        if event.inaxes == ax:

            cont, ind = sc.contains( event )

            if cont:

                update_annot( ind )
                annot.set_visible( True )
                fig.canvas.draw_idle()

            else:

                if vis:

                    annot.set_visible( False )
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect( "motion_notify_event", hover )

    plt.xlabel( xlabel )
    plt.ylabel( ylabel )
    plt.title( title )

    plt.tight_layout()

    if savefig:

        plt.savefig( filename )

    plt.show()

    plt.close()

def plot_df_heatmap( df, savefig = False, filename = "" ):

    fig, ax = plt.subplots()

    fig.set_size_inches( 20, 20 )

    im = ax.imshow( df, cmap = cm.plasma )

    plt.xticks( np.arange( 0, len( df.columns ), 1 ) )
    plt.yticks( np.arange( 0, len( df.index ), 1 ) )

    ax.set_xticklabels( df.columns, rotation = 270, fontsize = 6 )
    ax.set_yticklabels( df.index, fontsize = 6 )

    plt.tight_layout()
    ax.invert_yaxis()

    # for i in range( len( df.columns ) ):
    #
    #         for j in range( len( df.index ) ):
    #
    #             ax.text( i, j, "{:.1f}".format( df.iloc[j, i] ), ha = "center", va = "center", color = "w" )

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()

def pca_analysis( pca, features_df, plot_pc_heatmaps = False ):

    print( "Full explained ratio: ", pca.explained_variance_ratio_, "\n" )

    components_to_keep = [i for i in range( len( pca.explained_variance_ratio_ ) ) if pca.explained_variance_ratio_[i] > 0.1]

    num_components = len( components_to_keep )

    most_important_features = []

    for i in range( num_components ):

        most_important_features.append( np.argsort( -np.abs( pca.components_[i] ) ) )

        most_important_features[i] = [j for j in most_important_features[i] if abs( pca.components_[i][j] ) > 0.05] # 0.05

        print( "Key features for PC ", i + 1, ":\n" )

        for j in range( len( most_important_features[i] ) ):

            print( pca.feature_names_in_[most_important_features[i][j]], pca.components_[i][most_important_features[i][j]] )

        print( "\n" )

        if plot_pc_heatmaps:

            pc_df = features_df[pca.feature_names_in_[most_important_features[i]]]

            plot_df_heatmap( pc_df )

    nums = np.arange( len( pca.explained_variance_ratio_ ) + 1 )
    var_ratio = [np.sum( pca.explained_variance_ratio_[:i] ) for i in range( len( pca.explained_variance_ratio_ ) + 1 )]

    # plt.figure( figsize = ( 4, 2 ), dpi = 150 )
    # plt.grid()
    # plt.plot( nums, var_ratio, marker = 'o' )
    # plt.xlabel( 'n_components' )
    # plt.ylabel( 'Explained variance ratio' )
    # plt.title( 'n_components vs. Explained Variance Ratio' )
    # plt.show()
    # plt.close()

    # print( var_ratio )

def perform_pca( directory, features_df, sample_mask, std_error = False, std_of_features_df = [], num_components = 3, filename = "Unnamed.pdf", analysis_of_pca = True ):

    resin_data = get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    pca = PCA( n_components = num_components )
    pca_ft = pca.fit_transform( features_df )

    if analysis_of_pca:

        pca_analysis( pca, features_df )

    pca_ft_df = array_with_column_titles_and_label_titles_to_df( pca_ft, ["PC{}".format( i ) for i in range( num_components )], sample_mask )

    if std_error:

        std = [[] for i in range( num_components )]

        for k in range( num_components ):

            for i in range( len( std_of_features_df.iloc[:, 0] ) ):

                s = 0

                for j in range( len( pca.components_[k] ) ):

                    s += abs( pca.components_[k][j] ) * std_of_features_df.iloc[i, j]

                std[k].append( s )

        if num_components == 2:

            plot_scatterplot_of_two_features_pca( directory, pca_ft_df[pca_ft_df.columns[0]].to_numpy(), pca_ft_df[pca_ft_df.columns[1]].to_numpy(), np.transpose( pca.components_[0:2, :] ), pca.feature_names_in_, pca_ft_df.index, [resin_data.loc[i]["Label"] for i in pca_ft_df.index], errorbars = True, std = [std[0], std[1]], line_of_best_fit = False, xlabel = "First Principal Component", ylabel = "Second Principal Component", annotate_style = 2, savefig = True, filename = filename )

        elif num_components == 3:

            plot_scatterplot_of_three_features( directory, pca_ft_df[pca_ft_df.columns[0]].to_numpy(), pca_ft_df[pca_ft_df.columns[1]].to_numpy(), pca_ft_df[pca_ft_df.columns[2]].to_numpy(), pca_ft_df.index, [resin_data.loc[i]["Label"] for i in pca_ft_df.index], xlabel = "First Principal Component", ylabel = "Second Principal Component", zlabel = "Third Principal Component" )

    else:

        if num_components == 2:

            plot_scatterplot_of_two_features_pca( directory, pca_ft_df[pca_ft_df.columns[0]].to_numpy(), pca_ft_df[pca_ft_df.columns[1]].to_numpy(), np.transpose( pca.components_[0:2, :] ), pca.feature_names_in_, pca_ft_df.index, [resin_data.loc[i]["Label"] for i in pca_ft_df.index], line_of_best_fit = False, xlabel = "First Principal Component", ylabel = "Second Principal Component", annotate_style = 2, savefig = True, filename = filename )

        elif num_components == 3:

            plot_scatterplot_of_three_features( directory, pca_ft_df[pca_ft_df.columns[0]].to_numpy(), pca_ft_df[pca_ft_df.columns[1]].to_numpy(), pca_ft_df[pca_ft_df.columns[2]].to_numpy(), pca_ft_df.index, [resin_data.loc[i]["Label"] for i in pca_ft_df.index], xlabel = "First Principal Component", ylabel = "Second Principal Component", zlabel = "Third Principal Component" )

    if std_error:

        return pca_ft_df, [std[0], std[1]], np.transpose( pca.components_[0:2, :] ), pca.feature_names_in_

    else:

        return pca_ft_df, [], np.transpose( pca.components_[0:2, :] ), pca.feature_names_in_

def relabel_index_and_delete_first_column( df ):

    indices = df[df.columns[0]].tolist()
    df.set_axis( indices, axis = 0, inplace = True )
    df.drop( columns = df.columns[0], inplace = True )

    return indices

def plot_kmeans_plus_pca( features, kmeans, sample_mask, labels, title = "", xlabel = "", ylabel = "", savefig = False, filename = "" ):

    # Step size of the mesh. Decrease to increase the quality of the VQ.

    h = 0.005  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each

    x_min, x_max = features[:, 0].min() - 0.1, features[:, 0].max() + 0.1
    y_min, y_max = features[:, 1].min() - 0.1, features[:, 1].max() + 0.1
    xx, yy = np.meshgrid( np.arange( x_min, x_max, h ), np.arange( y_min, y_max, h ) )

    # Obtain labels for each point in mesh. Use last trained model.

    Z = kmeans.predict( np.c_[xx.ravel(), yy.ravel()] )

    # Put the result into a color plot

    Z = Z.reshape( xx.shape )
    plt.figure()
    plt.gcf().set_size_inches( 15, 15 )
    plt.clf()
    plt.imshow( Z, interpolation = "nearest", extent = ( xx.min(), xx.max(), yy.min(), yy.max() ), cmap = plt.cm.Paired, aspect = "auto", origin = "lower" )

    colours = list_of_colours()
    scatter_colours = [colours[sample_mask[i]] for i in range( len( sample_mask ) )]

    sc = plt.scatter( features[:, 0], features[:, 1], color = scatter_colours, s = 300 )

    fig = plt.gcf()
    ax = plt.gca()

    for i in range( len( sample_mask ) ):

        ax.annotate( labels[i], (features[:, 0][i] + 0.01, features[:, 1][i] + 0.01), fontsize = 30 )

    # Plot the centroids as a white X

    centroids = kmeans.cluster_centers_
    # plt.scatter( centroids[:, 0], centroids[:, 1], marker = "o", color = "w", zorder = 10 )

    plt.title( title )
    plt.xlabel( xlabel, fontsize = 30 )
    plt.ylabel( ylabel, fontsize = 30 )

    if savefig:

        plt.savefig( filename )

    else:

        plt.show()

    plt.close()
