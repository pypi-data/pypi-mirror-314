# Imports.

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

        column_data = [[] for i in range( 6 )]

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 5:

                linenumber += 1
                continue

            if line.rstrip():

                a_list = line.replace( '"', '' ).rstrip().split( "," )

                column_data[0].append( float( a_list[0] ) )
                column_data[1].append( float( a_list[1] ) )
                column_data[2].append( float( a_list[2] ) )
                column_data[3].append( float( a_list[3] ) )
                column_data[4].append( float( a_list[4] ) )
                column_data[5].append( float( a_list[5] ) )

            else:

                break

    for i in range( 6 ):

        data[i].append( np.array( column_data[i] ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], [], [], [], [], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    pass

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    # Add e for potentially erroneous data.

    specimens = {24:[9]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "e"

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

    for i, f in enumerate( file_data ):

        array = np.array( data[0][i] )[:, np.newaxis]

        for j in range( 1, 6 ):

            array = np.hstack( (array, np.array( data[j][i] )[:, np.newaxis]) )

        np.savetxt( output_directory + "TLS/Condensed_Data/Resin{}_{}_" + name_appendage + ".csv".format( f[0], f[1] ), array, delimiter = ",", fmt = "%.5f" )

    array = np.array( file_data )

    np.savetxt( output_directory + "TLS/File_Data/file_data" + name_appendage + ".csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups, name_appendage = "" ):
    '''Read the preprocessed .csv files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data = []

    df = pd.read_csv( output_directory + "TLS/File_Data/file_data" + name_appendage + ".csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    data = [[], [], [], [], [], []]

    filenames = sorted( [os.path.basename( path ) for path in glob.glob( output_directory + "TLS/Condensed_Data/*" ) if ("_" + name_appendage + ".csv") in path], key = gu.sort_raw_files_3 )

    for f in filenames:

        df = pd.read_csv( output_directory + "TLS/Condensed_Data/" + f, sep = ",", header = None )

        for i in range( len( df.columns ) ):

            data[i].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

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

        for i in range( len( data ) ):

            data[i].pop( r )

    return file_data, data

def compute_mean( output_directory, file_data, data, name_appendage = "" ):
    '''Compute the mean data for each resin.'''

    pass

def read_mean( output_directory, data, name_appendage = "" ):
    '''Read the computed means for each resin from a file.'''

    pass
