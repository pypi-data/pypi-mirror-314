# Imports

import os
import glob
import re
import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def read_raw_data_file_1( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r' ) as file:

        lines = file.readlines()

        a_list = lines[0].split( "," )

        data[0].append( float( a_list[0] ) )
        data[1].append( float( a_list[1] ) )
        data[2].append( float( a_list[2] ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], [], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    data[0] = np.array( data[0] )
    data[1] = np.array( data[1] )
    data[2] = np.array( data[2] )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    pass

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    pass

def read_files_and_preprocess( directory, data_directory, merge_groups ):
    '''Read files and preprocess data.'''

    file_data, data = extract_raw_data( directory, data_directory )

    standardise_data( data )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def write_csv( output_directory, file_data, data, name_appendage = "" ):
    '''Write read and preprocessed data to a .csv file.'''

    pass

def read_csv( directory, output_directory, merge_groups, name_appendage = "" ):
    '''Read the preprocessed .csv files.'''

    return [], []

def remove_files( file_data, data, descriptors_to_remove = "" ):
    '''Remove files not needed/wanted for analysis by searching for letters in file descriptions.'''

    # files_to_remove = []
    #
    # for i in range( len( file_data ) ):
    #
    #     s = file_data[i][3]
    #
    #     for l in descriptors_to_remove:
    #
    #         if s.find( l ) > -0.5:
    #
    #             files_to_remove.append( i )
    #
    #             break
    #
    # files_to_remove.reverse()
    #
    # for r in files_to_remove:
    #
    #     file_data.pop( r )

    return file_data, data

def compute_mean( output_directory, file_data, data, name_appendage = "" ):
    '''Compute the mean data for each resin.'''

    mL = [i[0] for i in gu.sample_mean( file_data, [[data[0][j]] for j in range( len( file_data ) )] )]
    ma = [i[0] for i in gu.sample_mean( file_data, [[data[1][j]] for j in range( len( file_data ) )] )]
    mb = [i[0] for i in gu.sample_mean( file_data, [[data[2][j]] for j in range( len( file_data ) )] )]

    m = [np.array( mL ), np.array( ma ), np.array( mb )]

    labels = ["L", "a", "b"]

    for i in range( len( m ) ):

        np.savetxt( output_directory + "Colour/Mean_Data/" + labels[i] + "_Means" + name_appendage + ".csv", m[i][np.newaxis, :], delimiter = ",", fmt = "%.3f" )

def read_mean( output_directory, data, name_appendage = "" ):
    '''Read the computed means for each resin from a file.'''

    labels = ["L", "a", "b"]

    for i in range( len( labels ) ):

        m = []

        df = pd.read_csv( output_directory + "Colour/Mean_Data/" + labels[i] + "_Means" + name_appendage + ".csv", sep = ",", header = None )

        for j in range( len( df.columns ) ):

            m.append( df.iloc[0, j] )

        if len( data ) > 3 + i: # A previous list of means is already appended.

            data[3 + i] = np.array( m )

        else:

            data.append( np.array( m ) )

    return data
