def Plot_DSC_Curves( output_directory, Temperature, Heat_Flow, filenames ):
    '''Plot each DSC curve.'''

    os.chdir( output_directory + "Plots" )

    for i in range( len( filenames ) ):

        plt.plot( Temperature[2][i], Heat_Flow[2][i] )
        plt.plot( Temperature[4][i], Heat_Flow[4][i] )
        plt.title( filenames[i][:-4] )
        plt.savefig( filenames[i][:-4] + ".pdf" )
        plt.close()

# Code to compute whether two samples can be distinguished.

if distinguish_pairs and compute_max_var:

    distinguish_matrix = np.zeros( (num_samples, num_samples) )

    for s1 in range( len( samples_present ) ):

        for s2 in range( s1 + 1, len( samples_present ) ):

            mask_1 = np.where( sample == samples_present[s1] )[0]
            mask_2 = np.where( sample == samples_present[s2] )[0]

            if len( mask_1 ) < 3 or len( mask_2 ) < 3:

                continue

            distinguish = False
            i_val = 0

            for i in range( len( Heat_Flow[2][0] ) ):

                value_1 = np.zeros( len( mask_1 ) )
                value_2 = np.zeros( len( mask_2 ) )

                for j, k in enumerate( mask_1 ):

                    value_1[j] = Heat_Flow[2][k][i]

                for j, k in enumerate( mask_2 ):

                    value_2[j] = Heat_Flow[2][k][i]

                distinguish_at_point = True

                for j in value_1:

                    for k in value_2:

                        if abs( j - k ) < max_var_c[i]:

                            distinguish_at_point = False

                            break

                    if not distinguish_at_point:

                        break

                if distinguish_at_point:

                    distinguish = True
                    i_val = Temperature[2][0][i]
                    break

            if distinguish == True:

                print( "Samples " + str( samples_present[s1] ) + " and " + str( samples_present[s2] ) + " can be distinguished at temperature " + str( i_val ) )

                distinguish_matrix[s1][s2] = 1
                distinguish_matrix[s2][s1] = 1

            else:

                print( "Samples " + str( samples_present[s1] ) + " and " + str( samples_present[s2] ) + " cannot be distinguished." )

    os.chdir( output_directory + "Distinguish/" )

    distinguish_matrix = np.vstack( (samples_present_array[np.newaxis, :], distinguish_matrix) )

    nonzero_mask = np.nonzero( integral_c )[0]

    distinguish_matrix = distinguish_matrix[:, nonzero_mask]

    nonzero_mask = nonzero_mask + 1

    nonzero_mask = np.concatenate( [np.array( [0] ), nonzero_mask] )

    distinguish_matrix = distinguish_matrix[nonzero_mask, :]

    np.savetxt( "Distinguish.txt", distinguish_matrix )

def distinguish_distance( mask, list_1, list_2 ):

    match = 0

    for i in list_1:

        for j in list_2:

            if i == j:

                match = match + 1

                break

    for i in mask:

        if i not in list_1 and i not in list_2:

            match = match + 1

    return 1 - match / len( mask )

def read_and_analyse_distinguish_matrix( output_directory, filenames, plot_distinguish_dendrogram ):

    os.chdir( output_directory + "Distinguish/" )

    distinguish_matrix = np.loadtxt( "Distinguish.txt" )

    samples_present_array = distinguish_matrix[0, :]
    num_samples = len( samples_present_array )

    distinguish_matrix = distinguish_matrix[1:, :]

    differences_list = []

    for j, i in enumerate( distinguish_matrix ):

        a = (i != 0)
        b = list( samples_present_array[a] )

        differences_list.append( b )

    distance_matrix = np.zeros_like( distinguish_matrix )

    for i in range( len( differences_list ) - 1 ):

        for j in range( i + 1, len( differences_list ) ):

            distance_matrix[i][j] = distance_matrix[j][i] = distinguish_distance( samples_present_array, differences_list[i], differences_list[j] )

    if plot_distinguish_dendrogram:

        DSC_plotting.plot_distinguish_dendrogram( samples_present_array, distance_matrix )

def plot_distinguish_dendrogram( mask, distance_matrix ):

    condensed_distance_matrix = squareform( distance_matrix )
    linkage_matrix = linkage( condensed_distance_matrix, "single" )
    dendrogram( linkage_matrix, labels = mask )

    plt.ylim( [-0.02, 1] )
    plt.xlabel( "PCR Sample" )
    plt.title( "Differentiating samples given variation" )
    plt.savefig( "Distinguish.pdf" )

if read_distinguish_matrix:

    util.read_and_analyse_distinguish_matrix( output_directory, filenames, plot_distinguish_dendrogram )

bound_temperature = False
range_mask_c_u, range_mask_c_l = 155, 45 #155, 45. # Range of focus for crystallisation. For plot variance bar, used 130, 80. Else 195, 0.
range_mask_m_u, range_mask_m_l = 150, 100 # Range of focus for melt. For plot variance bar, used 180, 100. Else 205, 60.

if bound_temperature:

    Preprocessing.bound_temperature( Temperature, Heat_Flow, m, range_mask_c_u, range_mask_c_l, range_mask_m_u, range_mask_m_l )

def bound_range( temperature, upper_bound = 205, lower_bound = 0 ):
    '''Creates a mask with which to bound the data.'''

    mask = np.where( (temperature <= upper_bound) & (temperature >= lower_bound) )[0]

    return mask

def bound_temperature( Temperature, Heat_Flow, m, range_mask_c_u, range_mask_c_l, range_mask_m_u, range_mask_m_l ):
    '''Bound the data so that it lies within a specified temperature range.'''

    range_mask_c = bound_range( np.array( Temperature[2][0] ), range_mask_c_u, range_mask_c_l )
    range_mask_m = bound_range( np.array( Temperature[4][0] ), range_mask_m_u, range_mask_m_l )

    for i in range( len( Heat_Flow[2] ) ):

        Heat_Flow[2][i] = list( np.array( Heat_Flow[2][i] )[range_mask_c] )

    Temperature[2][0] = list( np.array( Temperature[2][0] )[range_mask_c] )

    for i in range( len( Heat_Flow[4] ) ):

        Heat_Flow[4][i] = list( np.array( Heat_Flow[4][i] )[range_mask_m] )

    Temperature[4][0] = list( np.array( Temperature[4][0] )[range_mask_m] )

    for i in range( len( m[0] ) ):

        m[0][i] = list( np.array( m[0][i] )[range_mask_c] )

    for i in range( len( m[1] ) ):

        m[1][i] = list( np.array( m[1][i] )[range_mask_m] )
