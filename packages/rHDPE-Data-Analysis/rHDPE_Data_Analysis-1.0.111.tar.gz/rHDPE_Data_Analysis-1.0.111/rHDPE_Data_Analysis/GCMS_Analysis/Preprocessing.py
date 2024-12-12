# Imports.

import numpy as np
import pandas as pd
import math

from .. import Global_Utilities as gu

# Function definitions.

def read_raw_data_file_1( directory, file_data, data ):

    df = pd.read_excel( directory + "GCMS/Raw_Data/Malodour Controls.xlsx", "TICs", header = None )

    file_data.append( [0, 0, "Virgin 4 Aug", ""] )
    file_data.append( [1, 0, "KW 4 Aug", ""] )
    file_data.append( [1, 1, "KW 22 Aug", ""] )
    file_data.append( [1, 2, "KW 4 Aug (Normalised)", ""] )

    data[0].append( df[0].to_numpy( dtype = np.float64 )[6:] )
    data[0].append( df[3].to_numpy( dtype = np.float64 )[6:] )
    data[0].append( df[6].to_numpy( dtype = np.float64 )[6:] )
    data[1].append( df[1].to_numpy( dtype = np.float64 )[6:] )
    data[1].append( df[4].to_numpy( dtype = np.float64 )[6:] )
    data[1].append( df[7].to_numpy( dtype = np.float64 )[6:] )
    data[2].append( df[2].to_numpy( dtype = np.float64 )[6:] )
    data[2].append( df[5].to_numpy( dtype = np.float64 )[6:] )
    data[2].append( df[8].to_numpy( dtype = np.float64 )[6:] )

def read_raw_data_file_2( data_directory, i, file_data, data ):

    filename = data_directory + str( i ) + ".csv"

    labels = ["HOC 8/3/24", "HOC 19/3/24", "HOC 10/4/24", "HOC 20/6/24", "HOC 2/5/24", "HOC 16/5/24"]

    with open( filename, 'r' ) as file:

        x, y, z = [], [], []

        lines = file.read().splitlines()

        for line in lines:

            a_list = line.split( "," )

            if a_list:

                map_object = map( float, a_list )
                list_of_floats = list( map_object )

                x.append( list_of_floats[0] )
                y.append( list_of_floats[1] )
                z.append( list_of_floats[2] )

    data[0].append( np.array( x ) )
    data[1].append( np.array( y ) )

    file_data.append( [18, i - 1, labels[i - 1], ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    file_data, data = [], [[], []]

    # read_raw_data_file_1( directory, file_data, data )

    for i in range( 1, 7 ):

        read_raw_data_file_2( data_directory, i, file_data, data )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    data[0] = data[0][0]

    # Limonene normalisation

    maximum, minimum = [], []
    retention_time_shift = []

    rt_mask_limonene = np.where( (data[0] <= 4.3) & (data[0] >= 4) )[0]
    rt_mask_min = np.where( (data[0] <= 3.4) & (data[0] >= 2.4) )[0]

    for i in range( len( data[1] ) ):

        maximum.append( data[1][i][rt_mask_limonene].max() )
        minimum.append( data[1][i][rt_mask_min].min() )
        retention_time_shift.append( int( math.floor( (data[0][rt_mask_limonene][data[1][i][rt_mask_limonene].argmax()] - 4.18) * 1200 ) ) )

    maximum_array = np.array( maximum ).astype( np.float32 )
    minimum_array = np.array( minimum ).astype( np.float32 )

    normalised_headspaces = []

    for i in range( len( data[1] ) ):

        normalised_headspaces.append( 100 * (data[1][i] - minimum_array[i]) / (maximum_array[i] - minimum_array[i]) )

        if retention_time_shift[i] > 0:

            normalised_headspaces[i] = np.pad( normalised_headspaces[i][retention_time_shift[i]:], (0, retention_time_shift[i]) )

        if retention_time_shift[i] < 0:

            normalised_headspaces[i] = np.pad( normalised_headspaces[i][:retention_time_shift[i]], (-retention_time_shift[i], 0) )

    data[1].extend( normalised_headspaces )

    data[0] = data[0][120:-120]

    for i in range( len( data[1] ) ):

        data[1][i] = data[1][i][120:-120]

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    pass

def read_files_and_preprocess( directory, data_directory, merge_groups ):
    '''Read files and preprocess data.'''

    file_data, data = extract_raw_data( directory, data_directory )

    standardise_data( data )

    labels = ["HOC 8/3/24", "HOC 19/3/24", "HOC 10/4/24", "HOC 20/6/24", "HOC 2/5/24", "HOC 16/5/24"]

    for i in range( 6 ):

        file_data.append( [18, i + 6, "Normalised " + labels[i], ""] )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def write_csv( output_directory, file_data, data, name_appendage = "" ):
    '''Write read and preprocessed data to a .csv file.'''

    array = data[0][:, np.newaxis]

    for i in range( len( data[1] ) ):

        array = np.hstack( (array, data[1][i][:, np.newaxis]) )

    np.savetxt( output_directory + "GCMS/Condensed_Data/GCMS_data" + name_appendage + ".csv", array, delimiter = ",", fmt = "%.6f" )

    array = np.array( file_data )

    np.savetxt( output_directory + "GCMS/Condensed_Data/file_data" + name_appendage + ".csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups, name_appendage = "" ):
    '''Read the preprocessed .csv file.'''

    file_data = []

    labels = ["HOC 8/3/24", "HOC 19/3/24", "HOC 10/4/24", "HOC 20/6/24", "HOC 2/5/24", "HOC 16/5/24"]
    labels.extend( ["Normalised " + labels[i] for i in range( 6 )] )

    df = pd.read_csv( output_directory + "GCMS/Condensed_Data/file_data" + name_appendage + ".csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, labels[i], ""] )

    # file_data.append( [0, 0, "Virgin 4 Aug", ""] )
    # file_data.append( [1, 0, "KW 4 Aug", ""] )
    # file_data.append( [1, 1, "KW 22 Aug", ""] )
    # file_data.append( [1, 2, "KW 4 Aug (Normalised)", ""] )

    df = pd.read_csv( output_directory + "GCMS/Condensed_Data/GCMS_data" + name_appendage + ".csv", sep = ",", header = None )

    data = [df.iloc[:, 0].to_numpy( dtype = np.float64 ), []]

    for i in range( 1, len( df.columns ) ):

        data[1].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def remove_files( file_data, data, descriptors_to_remove = "" ):
    '''Remove files not needed/wanted for analysis by searching for letters in file descriptions.'''

    files_to_remove = []

    for i in range( len( file_data ) ):

        s = file_data[i][3]

        for l in descriptors_to_remove:

            if s.find( l ) > -0.5:

                files_to_remove.append( i )

                break

    files_to_remove.reverse()

    for r in files_to_remove:

        file_data.pop( r )
        data[1].pop( r )
        data[2].pop(r)

    return file_data, data

def compute_mean( output_directory, file_data, data, name_appendage = "" ):
    '''Compute the mean data for each resin.'''

    m = gu.sample_mean( file_data, data[1] )

    array = m[0][:, np.newaxis]

    for i in range( 1, len( m ) ):

        array = np.hstack( (array, m[i][:, np.newaxis]) )

    np.savetxt( output_directory + "GCMS/Condensed_Data/Means" + name_appendage + ".csv", array, delimiter = ",", fmt = "%.6f" )

def read_mean( output_directory, data, name_appendage = "" ):
    '''Read the computed means for each resin from a file.'''

    m = []

    df = pd.read_csv( output_directory + "GCMS/Condensed_Data/Means" + name_appendage + ".csv", sep = ",", header = None )

    for i in range( len( df.columns ) ):

        m.append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

    if len( data ) > 2: # A previous list of means is already appended.

            data[2] = m

    else:

        data.append( m )

    return data
