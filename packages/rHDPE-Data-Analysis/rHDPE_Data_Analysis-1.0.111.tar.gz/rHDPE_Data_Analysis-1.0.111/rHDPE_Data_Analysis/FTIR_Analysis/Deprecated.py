def argument_of_maximum_closest_to_wavenumber( x, y, wavenumber ):
    '''Finds the index of the maximum that is closest to a wavenumber.'''

    first_deriv = gu.derivative( x, y )

    local_max = []

    for j in range( 1, len( first_deriv ) ):

        if first_deriv[j] >= 0 and first_deriv[j - 1] <= 0:

            local_max.append( j + 1 )

    closest_dist = 1000
    index = 0

    for j in range( len( local_max ) ):

        if abs( x[local_max[j]] - wavenumber ) < closest_dist:

            closest_dist = abs( x[local_max[j]] - wavenumber )
            index = local_max[j]

    return index

def file_names( directory ):
    '''Outputs "filenames" object.'''

    os.chdir( directory )

    filenames = [] # Each element will have form ["PCR X", filename, X, Repetition of sample]

    dir_1 = sorted( glob.glob( "*" ), key = sort_files )

    for i in range( len( dir_1 ) ):

        dir = dir_1[i] + "/Data point table"

        os.chdir( directory + dir )

        pcr = int( dir_1[i][4:] )

        dir_2 = sorted( glob.glob( "*" ) )

        for j in range( len( dir_2 ) ):

            if pcr == 5 and j == 8:

                    filenames.append( [dir_1[i], dir_2[j], pcr, j] )
                    filenames.append( [dir_1[i], dir_2[j], pcr, j + 1] )
                    filenames.append( [dir_1[i], dir_2[j], pcr, j + 2] )

            elif pcr == 20 and j == 8:

                    filenames.append( [dir_1[i], dir_2[j], pcr, j] )
                    filenames.append( [dir_1[i], dir_2[j], pcr, j + 1] )
                    filenames.append( [dir_1[i], dir_2[j], pcr, j + 2] )

            else:

                filenames.append( [dir_1[i], dir_2[j], pcr, j] )

    filenames.append( ["Additives", "PCR-20 repeat", 26, 0] )
    filenames.append( ["Additives", "PCR-20 repeat", 26, 1] )
    filenames.append( ["Additives", "PCR-20 repeat", 26, 2] )

    additives = ["No additive", "IrgaCycle ", "Accelothene G5", "TegoCycle 310", "Irganox 1010", "Irganox 1010 + Irgafos 168", "Vistamaxx 6102"]

    for ind, a in enumerate( additives ):

        filenames.append( ["Additives", a, 27 + 3 * ind, 0] )
        filenames.append( ["Additives", a, 27 + 3 * ind, 1] )
        filenames.append( ["Additives", a, 27 + 3 * ind, 2] )
        filenames.append( ["Additives", a, 28 + 3 * ind, 0] )
        filenames.append( ["Additives", a, 28 + 3 * ind, 1] )
        filenames.append( ["Additives", a, 28 + 3 * ind, 2] )
        filenames.append( ["Additives", a, 29 + 3 * ind, 0] )
        filenames.append( ["Additives", a, 29 + 3 * ind, 1] )
        filenames.append( ["Additives", a, 29 + 3 * ind, 2] )

    return filenames

def extract_file_data_from_filenames( filenames ):
    """Returns file_data object of form [PCR Sample, PCR Specimen, PCR Label, Description]."""

    file_data = []

    for f in filenames:

        if f[2] == 0:

            file_data.append( [f[2], f[3], "V{}.{}".format( 1, f[3] ), ""] )

        elif f[2] == 16:

            file_data.append( [f[2], f[3], "V{}.{}".format( 6, f[3] ), ""] )

        elif f[2] == 17:

            file_data.append( [f[2], f[3], "V{}.{}".format( 7, f[3] ), ""] )

        elif f[2] == 19:

            file_data.append( [f[2], f[3], "V{}.{}".format( 8, f[3] ), ""] )

        else:

            file_data.append( [f[2], f[3], "PCR{}.{}".format( f[2], f[3] ), ""] )

    return file_data

def read_file( filename, x, y ):
    '''Read file, extracting x, y values where x varies from 599 to 3997.'''

    with open( filename, 'r' ) as file:

        lines = file.readlines()

        for line in lines:

            a_list = line.split()

            if a_list:

                map_object = map( float, a_list )
                list_of_floats = list( map_object )

                if list_of_floats[0] <= 3996.26214 and list_of_floats[0] >= 599.82506:

                    x.append( list_of_floats[0] )
                    y.append( list_of_floats[1] )

            else:

                break

def read_file_tf( filename, x1, y1, x2, y2, x3, y3 ):
    '''Read file, extracting x, y values where x varies from 599 to 3997.'''

    with open( filename, 'r' ) as file:

        lines = file.read().splitlines()

        counter = 0

        for line in lines:

            if counter < 2:

                counter += 1
                continue

            counter += 1

            a_list = line.split(",")

            a_list = [a_list[0], a_list[1], a_list[3], a_list[4], a_list[6], a_list[7]]

            if a_list:

                map_object = map( float, a_list )
                list_of_floats = list( map_object )

                if list_of_floats[0] <= 3996.26214 and list_of_floats[0] >= 599.82506:

                    x1.append( list_of_floats[0] )
                    y1.append( list_of_floats[1] )
                    x2.append( list_of_floats[2] )
                    y2.append( list_of_floats[3] )
                    x3.append( list_of_floats[4] )
                    y3.append( list_of_floats[5] )

            else:

                break

def read_files( directory, filenames ):
    '''Reads the files. y is a list of arrays, an array for each file, x is just a single array.'''

    x, y = [], []

    for i in range( len( filenames ) ):

        if filenames[i][2] < 26:

            if not ((filenames[i][2] == 5 and filenames[i][3] > 7) or (filenames[i][2] == 20 and filenames[i][3] > 7)):

                x1, y1 = [], []

                filename = directory + filenames[i][0] + "/Data point table/" + filenames[i][1]

                read_file( filename, x1, y1 )

                x.append( np.array( x1 ) )
                y.append( np.array( y1 ) )

            else:

                if filenames[i][3] > 8:

                    continue

                else:

                    x1, y1, x2, y2, x3, y3 = [], [], [], [], [], []

                    filename = directory + filenames[i][0] + "/Data point table/" + filenames[i][1]

                    read_file_tf( filename, x1, y1, x2, y2, x3, y3 )

                    x.append( np.array( x1 ) )
                    x.append( np.array( x2 ) )
                    x.append( np.array( x3 ) )

                    y.append( np.array( y1 ) )
                    y.append( np.array( y2 ) )
                    y.append( np.array( y3 ) )

        else:

            if (filenames[i][2] == 26 or filenames[i][2] % 3 == 0) and (filenames[i][3] == 0):

                df = pd.read_excel( directory[:-14] + "TF035_FT-IR_raw data.xlsx", filenames[i][1] )

                if filenames[i][2] == 26:

                    df = df.drop( df.columns[[2, 5]], axis = 1 )
                    df = df.drop( [0], axis = 0 )

                    x.append( df[df.columns[0]].to_numpy() )
                    x.append( df[df.columns[2]].to_numpy() )
                    x.append( df[df.columns[4]].to_numpy() )

                    y.append( df[df.columns[1]].to_numpy() )
                    y.append( df[df.columns[3]].to_numpy() )
                    y.append( df[df.columns[5]].to_numpy() )

                elif filenames[i][2] == 45:

                    df = df.drop( df.columns[[2, 5, 8, 11, 14, 17, 20, 23]], axis = 1 )
                    df = df.drop( [0], axis = 0 )

                    array = df[df.columns[6]].to_list()

                    array_1 = []
                    array_2 = []

                    for i in array:

                        split = i.split( ',' )

                        array_1.append( float( split[0] ) )
                        array_2.append( float( split[1] ) )

                    df[df.columns[6]] = array_1
                    df[df.columns[7]] = array_2

                    x.append( df[df.columns[0]].to_numpy() )
                    x.append( df[df.columns[2]].to_numpy() )
                    x.append( df[df.columns[4]].to_numpy() )
                    x.append( df[df.columns[6]].to_numpy() )
                    x.append( df[df.columns[8]].to_numpy() )
                    x.append( df[df.columns[10]].to_numpy() )
                    x.append( df[df.columns[12]].to_numpy() )
                    x.append( df[df.columns[14]].to_numpy() )
                    x.append( df[df.columns[16]].to_numpy() )

                    y.append( df[df.columns[1]].to_numpy() )
                    y.append( df[df.columns[3]].to_numpy() )
                    y.append( df[df.columns[5]].to_numpy() )
                    y.append( df[df.columns[7]].to_numpy() )
                    y.append( df[df.columns[9]].to_numpy() )
                    y.append( df[df.columns[11]].to_numpy() )
                    y.append( df[df.columns[13]].to_numpy() )
                    y.append( df[df.columns[15]].to_numpy() )
                    y.append( df[df.columns[17]].to_numpy() )

                elif filenames[i][2] > 26:

                    df = df.drop( df.columns[[2, 5, 8, 11, 14, 17, 20, 23]], axis = 1 )
                    df = df.drop( [0], axis = 0 )

                    x.append( df[df.columns[0]].to_numpy() )
                    x.append( df[df.columns[2]].to_numpy() )
                    x.append( df[df.columns[4]].to_numpy() )
                    x.append( df[df.columns[6]].to_numpy() )
                    x.append( df[df.columns[8]].to_numpy() )
                    x.append( df[df.columns[10]].to_numpy() )
                    x.append( df[df.columns[12]].to_numpy() )
                    x.append( df[df.columns[14]].to_numpy() )
                    x.append( df[df.columns[16]].to_numpy() )

                    y.append( df[df.columns[1]].to_numpy() )
                    y.append( df[df.columns[3]].to_numpy() )
                    y.append( df[df.columns[5]].to_numpy() )
                    y.append( df[df.columns[7]].to_numpy() )
                    y.append( df[df.columns[9]].to_numpy() )
                    y.append( df[df.columns[11]].to_numpy() )
                    y.append( df[df.columns[13]].to_numpy() )
                    y.append( df[df.columns[15]].to_numpy() )
                    y.append( df[df.columns[17]].to_numpy() )

    return x, y

def extract_raw_data( directory ):

    filenames = file_names( directory + "FTIR/FTIR of rHDPE/" )

    file_data = extract_file_data_from_filenames( filenames )

    unstandard_x, y = read_files( directory + "FTIR/FTIR of rHDPE/", filenames )

    data = [unstandard_x, y]

    return file_data, data

def scale_and_shift( file_data, data ):
    '''Apply a scale and then a shift to each specimen dependent on how it relates to the mean for that sample.'''

    splits = [int( data[0][len( data[0] ) - 1] ), 800, 1400, 1500, 2000, 2700, 3000, int( data[0][0] )]

    m = gu.sample_mean( file_data, data[1] )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    for s in range( len( splits ) - 1 ):

        range_mask = np.where( (data[0] >= splits[s]) & (data[0] < splits[s + 1]) )

        for ind, i in enumerate( samples_present ):

            mask = np.where( sample_array == i )[0]

            for j in mask:

                scale_mean = 0

                for k in range( len( data[1][j][range_mask] ) ):

                    scale_mean += data[1][j][range_mask][k] / m[ind][range_mask][k]

                scale_mean /= len( data[1][j][range_mask] )

                data[1][j][range_mask] = data[1][j][range_mask] / scale_mean

    m = gu.sample_mean( file_data, data[1] )

    for s in range( len( splits ) - 1 ):

        range_mask = np.where( (data[0] >= splits[s]) & (data[0] < splits[s + 1]) )

        for ind, i in enumerate( samples_present ):

            mask = np.where( sample_array == i )[0]

            for j in mask:

                shift_mean = 0

                for k in range( len( data[1][j][range_mask] ) ):

                    shift_mean += m[ind][range_mask][k] - data[1][j][range_mask][k]

                shift_mean /= len( data[1][j][range_mask] )

                data[1][j][range_mask] = data[1][j][range_mask] + shift_mean

def find_index( frequency, x ):
    '''Finds the index in the list x that corresponds with the given wavenumber. (Was used for single frequency analysis.)'''

    for idx in range( len( x ) ):

        if x[idx] < frequency:

            if abs( x[idx] - frequency ) > abs( x[idx - 1] - frequency ):

                return idx - 1

            else:

                return idx

def difference_vectors( y ):
    '''For two arrays of the same length, returns an array where each entry is the difference between the two input arrays at that index.'''

    diffs = []

    for i in range( len( y ) ):

        diffs1 = []

        for j in range( len( y ) - 1 - i ):

            diffs1.append( np.array( y[i] ) - np.array( y[i + j + 1] ) )

        diffs.append( diffs1 )

    return diffs

def compute_vector_distances( dist_type, x, diffs, distance_matrix, arg_of_max ):
    '''Turn the difference vectors into simpler results.'''

    for i in range( len( diffs ) ):

        for j in range( len( diffs ) - 1 - i ):

            if dist_type == "max":

                distance_matrix[i][j + 1 + i] = distance_matrix[j + 1 + i][i] = np.absolute( diffs[i][j] ).max()

                for idx, k in enumerate( np.absolute( diffs[i][j] ) ):

                    if k == distance_matrix[i][j + 1 + i]:

                        arg_of_max[i][j + 1 + i] = arg_of_max[j + 1 + i][i] = x[idx]
                        break

            if dist_type == "sum":

                distance_matrix[i][j + 1 + i] = distance_matrix[j + 1 + i][i] = np.absolute( diffs[i][j] ).sum()

def compute_difference_matrix( output_directory, file_data, dist_type, data ):
    '''Compute difference matrices for sum and max.'''

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]
    # sample_mask = samples_present

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    diffs = difference_vectors( data[1] )

    for dt in dist_type:

        max = False

        if dt == "max":

            max = True

        distance_matrix = np.zeros( (len( data[1] ), len( data[1] )) )
        arg_of_max = np.zeros( (len( data[1] ), len( data[1] )) )

        compute_vector_distances( dt, data[0], diffs, distance_matrix, arg_of_max )

        distance_matrix = distance_matrix[specimen_mask, :]
        distance_matrix = distance_matrix[:, specimen_mask]
        arg_of_max = arg_of_max[specimen_mask, :]
        arg_of_max = arg_of_max[:, specimen_mask]

        df = gu.array_with_column_titles_and_label_titles_to_df( distance_matrix, [f[2] for f in file_data_mask], [f[2] for f in file_data_mask] )

        df.to_csv( output_directory + "Matrices/" + dt + ".csv" )

        gu.plot_distance_matrix( output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "Matrices/", title = dt + ".pdf" )

        if max:

            df_arg = gu.array_with_column_titles_and_label_titles_to_df( arg_of_max, [f[2] for f in file_data_mask], [f[2] for f in file_data_mask] )

            df_arg.to_csv( output_directory + "Matrices/" + dt + "_arg.csv" )

            gu.plot_distance_matrix( output_directory, arg_of_max, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "Matrices/", title = dt + "_arg.pdf" )

def sigmoid_filter( magnitude, cutoff, threshold, shift, stretch ):
    '''Assigning a sigmoid filter to the magnitude of peaks.'''

    for i in range( len( magnitude ) ):

        for j in range( len( magnitude[i] ) ):

            if magnitude[i][j] < -cutoff:

                magnitude[i][j] = -1

            else:

                magnitude[i][j] = -1 / (1 + math.exp( -(stretch * ((2 * (-magnitude[i][j] - threshold) / (cutoff - threshold)) - 1) - shift) ))

# sigmoid_filter( mag_m_peaks, 0.00005, peak_threshold_1, 2, 5 )
# sigmoid_filter( mag_m_peaks, 0.00025, peak_threshold_1, 0, 3 )
