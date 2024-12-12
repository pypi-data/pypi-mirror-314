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

    sheet = "Ramp 10.00 °Cmin to 600.00 °C"

    df = pd.read_excel( filename, sheet )

    for i in range( len( df.columns ) ):

        df.rename( columns = {df.columns[i]:df.loc[0][i]}, inplace = True )

    df.drop( [0, 1], inplace = True )

    for i in range( len( df.columns ) ):

        data[i].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

    if len( df.columns ) < 5:

        for i in range( 5 - len( df.columns ) ):

            data[4 - i].append( np.array( [] ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def read_raw_data_file_2( filename, f, resin_data, file_data, data ):

    pass

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], [], [], [], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            if resin == 40 or resin == 41:

                read_raw_data_file_2( data_directory + r + "/" + f, f, resin_data, file_data, data )

            else:

                read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    standard_temp_list = np.linspace( 30, 590, 5600 ).tolist()

    for i in range( len( data[0] ) ):

        mask = []

        array = data[1][i]

        for j in range( len( standard_temp_list ) ):

            interval_mask = np.where( array >= standard_temp_list[j] )[0]

            if interval_mask.any():

                mask.append( interval_mask[0] )

            else:

                mask.append( len( array ) - 1 )

        for j in range( len( data ) ):

            if j == 1:

                continue

            if data[j][i].any():

                data[j][i] = data[j][i][mask]

        print( i )

    data[1] = np.array( standard_temp_list )

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    # Add f for specimens whose main decomposition occurs much later, presumable an experimental error.
    # Add s for specimens whose experimental length is too short.

    specimens = {7:[1], 8:[1], 9:[1], 10:[1], 11:[1], 12:[1], 13:[1], 14:[1], 15:[1], 16:[1]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "f"

    specimens = {5:[1], 6:[1]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "s"

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

        for j in range( 1, 5 ):

            if j == 1:

                array = np.hstack( (array, np.array( data[j] )[:, np.newaxis]) )

            elif data[j][i].any():

                array = np.hstack( (array, np.array( data[j][i] )[:, np.newaxis]) )

        np.savetxt( output_directory + "TGA/Condensed_Data/Resin{}_{}_" + name_appendage + ".csv".format( f[0], f[1] ), array, delimiter = ",", fmt = "%.7f" )

    array = np.array( file_data )

    np.savetxt( output_directory + "TGA/File_Data/file_data" + name_appendage + ".csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups, name_appendage = "" ):
    '''Read the preprocessed .csv files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data = []

    df = pd.read_csv( output_directory + "TGA/File_Data/file_data" + name_appendage + ".csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    data = [[], [], [], [], []]

    filenames = sorted( [os.path.basename( path ) for path in glob.glob( output_directory + "TGA/Condensed_Data/*" ) if ("_" + name_appendage + ".csv") in path], key = gu.sort_raw_files_3 )

    for f in filenames:

        df = pd.read_csv( output_directory + "TGA/Condensed_Data/" + f, sep = ",", header = None )

        for i in range( len( df.columns ) ):

            data[i].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

        if len( df.columns ) < 5:

            for i in range( 5 - len( df.columns ) ):

                data[4 - i].append( np.array( [] ) )

    data[1] = data[1][0]

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
        data[0].pop( r )
        data[2].pop( r )
        data[3].pop( r )
        data[4].pop( r )

    return file_data, data

def compute_mean( output_directory, file_data, data, name_appendage = "" ):
    '''Compute the mean data for each resin.'''

    m = gu.sample_mean( file_data, data[3] )

    array = m[0][:, np.newaxis]

    for i in range( 1, len( m ) ):

        array = np.hstack( (array, m[i][:, np.newaxis]) )

    np.savetxt( output_directory + "TGA/Mean_Data/Means" + name_appendage + ".csv", array, delimiter = ",", fmt = "%.7f" )

def read_mean( output_directory, data, name_appendage = "" ):
    '''Read the computed means for each resin from a file.'''

    m = []

    df = pd.read_csv( output_directory + "TGA/Mean_Data/Means" + name_appendage + ".csv", sep = ",", header = None )

    for i in range( len( df.columns ) ):

        m.append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

    if len( data ) > 5: # A previous list of means is already appended.

            data[5] = m

    else:

        data.append( m )

    return data
