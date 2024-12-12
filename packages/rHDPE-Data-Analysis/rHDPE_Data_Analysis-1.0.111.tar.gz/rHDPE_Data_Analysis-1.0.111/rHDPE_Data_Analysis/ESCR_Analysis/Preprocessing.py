# Imports.

import os
import glob
import re
import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def read_raw_data_file_1( filename, resin_data, file_data, data ):

    with open( filename, 'r' ) as file:

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 1:

                resins = line.rstrip().split( "," )[1:]

                data[1] = [[] for i in resins]

                linenumber += 1
                continue

            if line.rstrip():

                a_list = line.rstrip().split( "," )

                data[0].append( float( a_list[0] ) )

                for ind, i in enumerate( a_list[1:] ):

                    data[1][ind].append( float( i ) )

            else:

                break

        for r in resins:

            file_data.append( [int( r ), 0, resin_data.loc[int( r )]["Label"] + ".{}".format( 0 ), ""] )

    data[0] = np.array( data[0] )

    for i in range( len( data[1] ) ):

        data[1][i] = np.array( data[1][i] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data, data = [], [[], [], np.array( [24, 48, 72, 96] )]

    read_raw_data_file_1( data_directory + "ESCR.csv", resin_data, file_data, data )

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
    '''Read the preprocessed .csv file.'''

    return [], []

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

    return file_data, data

def compute_mean( output_directory, file_data, data, name_appendage = "" ):
    '''Compute the mean data for each resin.'''

    pass

def read_mean( output_directory, data, name_appendage = "" ):
    '''Read the computed means for each resin from a file.'''

    pass
