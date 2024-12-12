if bound_temperature:

    Preprocessing.bound_temperature( data, m, lower_bound, upper_bound )

def bound_range( temperature, lower_bound, upper_bound ):
    '''Creates a mask with which to bound the data.'''

    mask = np.where( (temperature <= upper_bound) & (temperature >= lower_bound) )[0]

    return mask

def bound_temperature( data, m, lower_bound, upper_bound ):
    '''Bound the data so that it lies within a specified temperature range.'''

    range_mask = bound_range( np.array( data[1][0] ), lower_bound, upper_bound )

    for i in range( len( data[3] ) ):

        data[3][i] = list( np.array( data[3][i] )[range_mask] )

    data[1][0] = list( np.array( data[1][0] )[range_mask] )

    for i in range( len( m ) ):

        m[i] = list( np.array( m[i] )[range_mask] )

def deriv_simplification( y, width ):

    deriv_simp = []

    for i in range( width, len( y ) - width ):

        list = y[i - width:i + width]
        array = np.array( list )
        min = array.min()
        max = array.max()
        deriv_simp.append( 0.5 * (min + max) )

    return deriv_simp

# Mean derivative at a selection of 20 degree ranges using deriv_simplification.

for j in range( 28 ):

    feature_1 = []

    # if j not in [6, 9, 13, 15, 17, 19, 21]:
    #
    #     continue

    lower_bound = 20 * (j + 2)
    upper_bound = 20 * (j + 3)

    mask = np.where( (np.array( data[1][0] ) >= lower_bound) & (np.array( data[1][0] ) <= upper_bound) )

    for i in range( len( file_data ) ):

        x = list( np.array( data[1][i] )[mask] )
        y = list( np.array( data[3][i] )[mask] )

        width = 7
        simp = 12
        step = 1

        y = gu.derivative( x, y, width )
        y = deriv_simplification( y, simp )

        feature_1.append( np.mean( np.array( y ) ) )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "TGA_Temp_{}-{}".format( lower_bound, upper_bound ) )
