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

    with open( filename, 'r', encoding = 'utf-16' ) as file:

        column_data = [[], [], [], [], []]

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 10:

                linenumber += 1
                continue

            a_list = line.split()

            column_data[0].append( float( a_list[1] ) )
            column_data[1].append( float( a_list[3] ) )
            column_data[2].append( float( a_list[4] ) )
            column_data[3].append( float( a_list[2] ) )
            column_data[4].append( float( a_list[5] ) )

    for i in range( 5 ):

        data[i].append( np.array( column_data[i] ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def read_raw_data_file_2( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r', encoding = "windows-1252" ) as file:

        column_data = [[], [], [], [], []]

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 2:

                linenumber += 1
                continue

            a_list = line.rstrip().split( "," )

            column_data[0].append( float( a_list[3] ) )
            column_data[1].append( float( a_list[0] ) * 10 ** 6 )
            column_data[2].append( float( a_list[1] ) * 10 ** 6 )
            column_data[3].append( float( a_list[9] ) )
            column_data[4].append( float( a_list[2] ) )

    for i in range( 5 ):

        column_data[i].reverse()
        data[i].append( np.array( column_data[i] ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

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

    standardised_angular_frequency = [10 ** (i / 10) for i in range( -10, 21 )]
    standardised_angular_frequency.reverse()

    for i in range( len ( data[0] ) ):

        sample_data = [[], [], [], [], []]

        for j in standardised_angular_frequency:

            index_1, index_2 = -2, -1

            for k, v in enumerate( data[0][i] ):

                if v < j:

                    index_1 = k - 1
                    index_2 = k
                    break

            log_change = (np.log10( j ) - np.log10( data[0][i][index_1] )) / (np.log10( data[0][i][index_2] ) - np.log10( data[0][i][index_1] ))

            for l in range( 1, 5 ):

                if data[l][i].any():

                    sample_data[l].append( 10 ** ((np.log10( data[l][i][index_2] ) - np.log10( data[l][i][index_1] )) * log_change + np.log10( data[l][i][index_1] )) )

        for l in range( 1, 5 ):

            data[l][i] = np.array( sample_data[l] )

    data[0] = np.array( standardised_angular_frequency )

def add_additional_variables( data ):

    complex_viscosity, loss_factor = [], []

    for i in range( len( data[1] ) ):

        cv, lf = [], []

        for j in range( len( data[1][i] ) ):

            cv.append( np.sqrt( data[1][i][j] ** 2 * data[2][i][j] ** 2 ) / data[0][j] )
            lf.append( data[2][i][j] / data[1][i][j] )

        complex_viscosity.append( cv )
        loss_factor.append( lf )

    data[3] = np.array( complex_viscosity )
    data[4] = np.array( loss_factor )

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    pass

def read_files_and_preprocess( directory, data_directory, merge_groups ):
    '''Read files and preprocess data.'''

    file_data, data = extract_raw_data( directory, data_directory )

    standardise_data( data )

    # add_additional_variables( data ) # Uncomment to compute additional variables from storage and loss modulii directly.

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def write_csv( output_directory, file_data, data, name_appendage = "" ):
    '''Write read and preprocessed data to a .csv file.'''

    array = data[0][:, np.newaxis]

    for i in range( len( data[1] ) ):

        array = np.hstack( (array, data[1][i][:, np.newaxis]) )
        array = np.hstack( (array, data[2][i][:, np.newaxis]) )
        array = np.hstack( (array, data[3][i][:, np.newaxis]) )
        array = np.hstack( (array, data[4][i][:, np.newaxis]) )

    np.savetxt( output_directory + "Rheology/Condensed_Data/Rheology_data" + name_appendage + ".csv", array, delimiter = ",", fmt = "%.5f" )

    array = np.array( file_data )

    np.savetxt( output_directory + "Rheology/Condensed_Data/file_data" + name_appendage + ".csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups, name_appendage = "" ):
    '''Read the preprocessed .csv files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data = []

    df = pd.read_csv( output_directory + "Rheology/Condensed_Data/file_data" + name_appendage + ".csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    data = [[], [], [], [], []]

    df = pd.read_csv( output_directory + "Rheology/Condensed_Data/Rheology_data" + name_appendage + ".csv", sep = ",", header = None )

    data[0] = df.iloc[:, 0].to_numpy( dtype = np.float64 )

    for i in range( 1, len( df.columns ) ):

        if i % 4 == 1:

            data[1].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

        elif i % 4 == 2:

            data[2].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

        elif i % 4 == 3:

            data[3].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

        elif i % 4 == 0:

            data[4].append( df.iloc[:, i].to_numpy( dtype = np.float64 ) )

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
        data[2].pop( r )
        data[3].pop( r )
        data[4].pop( r )

    return file_data, data

def compute_mean( output_directory, file_data, data, name_appendage = "" ):
    '''Compute the mean data for each resin.'''

    m = [gu.sample_mean( file_data, data[1] ), gu.sample_mean( file_data, data[2] ), gu.sample_mean( file_data, data[3] ), gu.sample_mean( file_data, data[4] )]

    labels = ["SM", "LM", "CV", "LF"]

    for i in range( len( m ) ):

        array = m[i][0][:, np.newaxis]

        for j in range( 1, len( m[i] ) ):

            array = np.hstack( (array, m[i][j][:, np.newaxis]) )

        np.savetxt( output_directory + "Rheology/Condensed_Data/" + labels[i] + "_Means" + name_appendage + ".csv", array, delimiter = ",", fmt = "%.5f" )

def read_mean( output_directory, data, name_appendage = "" ):
    '''Read the computed means for each resin from a file.'''

    labels = ["SM", "LM", "CV", "LF"]

    for i in range( len( labels ) ):

        m = []

        df = pd.read_csv( output_directory + "Rheology/Condensed_Data/" + labels[i] + "_Means" + name_appendage + ".csv", sep = ",", header = None )

        for j in range( len( df.columns ) ):

            m.append( df.iloc[:, j].to_numpy( dtype = np.float64 ) )

        if len( data ) > 5 + i: # A previous list of means is already appended.

            data[5 + i] = m

        else:

            data.append( m )

    return data
