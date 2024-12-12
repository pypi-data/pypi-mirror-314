import pandas as pd
import numpy as np
import re
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.metrics import r2_score
import math
from sklearn import datasets, linear_model

from . import Preprocessing
from .. import Global_Utilities as gu

def compile_full_dataset_of_features( dataset, sample_mask = [] ):

    samples_present = []

    for i in dataset:

        s_p = [int( j ) for j in i.iloc[:, 0].tolist()]
        
        samples_present = samples_present + list( set( s_p) - set( samples_present ) )

    samples_present = sorted( samples_present )

    features = np.zeros( len( samples_present ) )[:, np.newaxis]

    feature_names = []

    for i in dataset:

        feature_names.extend( i.columns[1:] )

        s_p = [int( j ) for j in i.iloc[:, 0].tolist()]

        for j in range( 1, len( i.columns ) ):

            feature = []

            for k in samples_present:

                if k in s_p:

                    feature.append( i.iloc[s_p.index( k ), j] )

                else:

                    feature.append( None )

            features = np.hstack( (features, np.array( feature )[:, np.newaxis]) )

    features = features[:, 1:]

    if sample_mask:

        array_index = [samples_present.index( s ) for s in sample_mask]

        features = features[array_index, :]

        samples_present = sample_mask

    return features, feature_names, samples_present

def produce_full_dataset_of_features( dataset, sample_mask ):

    features = np.zeros( len( sample_mask ) )[:, np.newaxis]

    feature_names = []

    for i in dataset:

        feature_names.extend( i.columns[1:] )

        samples_present = i.iloc[:, 0].tolist()

        for j in range( 1, len( i.columns ) ):

            feature = []

            for k in sample_mask:

                feature.append( i.iloc[samples_present.index( k ), j] )

            features = np.hstack( (features, np.array( feature )[:, np.newaxis]) )

    features = features[:, 1:]

    return features, feature_names

def rank_features( features ):

    rank_features = np.zeros( len( features ) )[:, np.newaxis]

    for i in range( len( features[0] ) ):

        array = features[:, i]

        temp = array.argsort()

        ranks = np.empty_like( temp )

        ranks[temp] = np.arange( len( array ) )

        rank_features = np.hstack( (rank_features, ranks[:, np.newaxis]) )

    rank_features = rank_features[:, 1:]

    return rank_features

# Historic suggestions of things to correlate.

# feature_1_labels = ["FTIR_965-980"]
# feature_2_labels = ["TT_SAB"]
# feature_1_labels = ["PA Content"]
# feature_2_labels = ["TGA_Temp_400-420"]
# feature_1_labels = ["PET Content"]
# feature_2_labels = ["TGA_Temp_360-380"]
# feature_1_labels = ["Irgafos Content"]
# feature_2_labels = ["TGA_Temp_250-270"]
# feature_1_labels = ["DSC_M_Onset"]
# feature_2_labels = ["TT_YM"]
# feature_1_labels = ["TT_SAB"]
# feature_2_labels = ["TT_SHM"]
# feature_1_labels = ["Rhe_Loss_0.10"]
# feature_2_labels = ["FTIR_908"]

def scatterplots( ip ):

    features_df, std_of_features_df, _ = Preprocessing.read_files_and_preprocess( ip, normalised = False, minimal_datasets = True, feature_1 = ip.scatterplot_x, feature_2 = ip.scatterplot_y )

    ip.sample_mask = features_df.index.tolist()

    feature_1 = features_df[ip.scatterplot_x].to_numpy()
    feature_2 = features_df[ip.scatterplot_y].to_numpy()
    std = [std_of_features_df[ip.scatterplot_x].to_numpy(), std_of_features_df[ip.scatterplot_y].to_numpy()]

    if not ip.shiny:

        resin_data = gu.get_list_of_resins_data( ip.directory ) # Obtain the spreadsheet of data for the resins.
        features_metadata = gu.get_features_metadata( ip.directory ) # Obtain the spreadsheet of metadata for the features.

        corr, _ = pearsonr( feature_1, feature_2 )

        print( "The Pearson correlation coefficient is:", corr )

        gu.plot_scatterplot_of_two_features( ip.directory, feature_1, feature_2, features_df.index, [resin_data.loc[i]["Label"] for i in features_df.index], errorbars = True, std = std, line_of_best_fit = False, exponential_fit = False, xlabel = features_metadata.loc[ip.scatterplot_x]["Axis_Label"], ylabel = features_metadata.loc[ip.scatterplot_y]["Axis_Label"], savefig = False, filename = ip.output_directory + "Global/Scatterplots/New_Figure.pdf" )

    return feature_1.tolist(), feature_2.tolist(), std[0].tolist(), std[1].tolist()

def correlation_heatmap( df, spearman = False ):

    correlation_heatmap = np.zeros( (len( df.columns ), len( df.columns )) )

    for i in range( len( df.columns ) ):

        for j in range( i, len( df.columns ) ):

            if spearman:

                correlation, _ = spearmanr( df.iloc[:, i], df.iloc[:, j] )

            else:

                correlation, _ = pearsonr( df.iloc[:, i], df.iloc[:, j] )

            correlation = abs( correlation )

            correlation_heatmap[i][j] = correlation_heatmap[j][i] = correlation

    correlation_df = gu.array_with_column_titles_and_label_titles_to_df( correlation_heatmap, df.columns, df.columns )

    return correlation_df

def pop_columns_from_dataframe( df, features ):

    popped_column = df.pop( features[0] )

    popped_dataframe = popped_column.to_frame()

    for i in range( 1, len( features ) ):

        popped_column = df.pop( features[i] )

        popped_dataframe = popped_dataframe.merge( popped_column.to_frame(), left_index = True, right_index = True )

    return popped_dataframe

def pop_features_from_dataframe( df, features ):

    popped_column = df.pop( features[0] )

    popped_dataframe = popped_column.to_frame()

    for i in range( 1, len( features ) ):

        popped_column = df.pop( features[i] )

        popped_dataframe = popped_dataframe.merge( popped_column.to_frame(), left_index = True, right_index = True )

    df = df.T

    popped_column = df.pop( features[0] )

    for i in range( 1, len( features ) ):

        popped_column = df.pop( features[i] )

    df = df.T

    return df, popped_dataframe

def euclidean_distance_to_virgin( features, sample_mask, virgin_samples, weighting = False ):

    dist = [[] for i in range( len( virgin_samples ) )]

    if weighting:

        features[:, 0] = features[:, 0] * 0.41
        features[:, 1] = features[:, 1] * 0.25
        features[:, 2] = features[:, 2] * 0.12

    for i in range( len( features ) ):

        for j in range( len( virgin_samples ) ):

            dist[j].append( np.linalg.norm( features[i] - features[sample_mask.index( virgin_samples[j] )] ) )

    dist = [np.array( i ) for i in dist]

    return dist

def distance_to_virgin_rank( resin_data, distance_to_virgin, virgin_samples, sample_mask ):

    sample_mask_array = np.array( sample_mask )

    ranks = []

    for i in range( len( virgin_samples ) ):

        temp = distance_to_virgin[i].argsort()

        print( "Virgin " + resin_data.loc[virgin_samples[i]]["Label"] + ":", [resin_data.loc[i]["Label"] for i in sample_mask_array[temp]] )

        rank = np.zeros_like( temp )
        rank[temp] = np.arange( len( sample_mask ) )

        ranks.append( rank )

    sum_ranks = np.zeros_like( temp )

    for i in range( len( virgin_samples ) ):

        sum_ranks += ranks[i]

    temp = sum_ranks.argsort()

    print( "Mean:", [resin_data.loc[i]["Label"] for i in sample_mask_array[temp]] )

def pca( directory, output_directory, shiny, features_df, std_of_features_df ):

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    pca_of_whole_dataset = False
    pca_of_pca_of_individual_datasets = True

    if pca_of_whole_dataset:

        gu.perform_pca( directory, features_df, [int( i ) for i in features_df.index], std_error = True, std_of_features_df = std_of_features_df, num_components = 2, filename = output_directory + "Global/PCA/Overall.pdf" )

    if pca_of_pca_of_individual_datasets:

        compute_distance_to_virgin = False

        perform_k_means = False

        dataset_names = ["FTIR", "DSC", "TGA", "Rhe", "TT", "Colour", "SHM", "TLS", "ESCR"]

        sample_mask = features_df.index.to_list()

        features_split_by_dataset_df, std_split_by_dataset_df = [], []

        for i, n in enumerate( dataset_names ):

            df = features_df.filter( regex = r"^" + n )

            features_split_by_dataset_df.append( df )

            df = std_of_features_df.filter( regex = r"^" + n )

            std_split_by_dataset_df.append( df )

        pcas, stds = [], []

        for i in range( len( features_split_by_dataset_df ) ):

            if not (features_split_by_dataset_df[i].empty or len( features_split_by_dataset_df[i].columns ) == 1):

                num_components = 2

                pca = PCA( n_components = num_components )
                pca_ft = pca.fit_transform( features_split_by_dataset_df[i] )

                gu.pca_analysis( pca, features_split_by_dataset_df[i] )

                std = [[] for n in range( num_components )]

                for k in range( num_components ):

                    for l in range( len( std_split_by_dataset_df[i].iloc[:, 0] ) ):

                        s = 0

                        for j in range( len( pca.components_[k] ) ):

                            s += abs( pca.components_[k][j] ) * std_split_by_dataset_df[i].iloc[l, j]

                        std[k].append( s )

                std_array = np.array( std ).transpose()

                pcas.append( gu.array_with_column_titles_and_label_titles_to_df( pca_ft, [dataset_names[i] + "_PC1", dataset_names[i] + "_PC2"], sample_mask ) )
                stds.append( gu.array_with_column_titles_and_label_titles_to_df( std_array, [dataset_names[i] + "_PC1", dataset_names[i] + "_PC2"], sample_mask ) )

            elif len( features_split_by_dataset_df[i].columns ) == 1:

                pcas.append( features_split_by_dataset_df[i] )
                stds.append( std_split_by_dataset_df[i] )

            else:

                pcas.append( pd.DataFrame() )
                stds.append( pd.DataFrame() )

        pcas_to_include, stds_to_include = [], []

        for i in range( len( dataset_names ) ):

            if not pcas[i].empty:

                pcas_to_include.append( pcas[i] )
                stds_to_include.append( stds[i] )

        overall_pca = np.zeros( len( sample_mask ) )[:, np.newaxis]
        overall_stds = np.zeros( len( sample_mask ) )[:, np.newaxis]

        feature_names = []

        for i in range( len( pcas_to_include ) ):

            for j in range( len( pcas_to_include[i].columns ) ):

                overall_pca = np.hstack( (overall_pca, pcas_to_include[i].iloc[:, j].to_numpy()[:, np.newaxis]) )
                overall_stds = np.hstack( (overall_stds, stds_to_include[i].iloc[:, j].to_numpy()[:, np.newaxis]) )

                feature_names.append( pcas_to_include[i].columns[j] )

        overall_pca = overall_pca[:, 1:]
        overall_stds = overall_stds[:, 1:]

        num_components = len( overall_pca[0] )

        if len( pcas_to_include ) != 1:

            for i in range( num_components ):

                overall_pca[:, i] =  (overall_pca[:, i] - overall_pca[:, i].min()) / (overall_pca[:, i].max() - overall_pca[:, i].min())
                overall_stds[:, i] =  overall_stds[:, i] / (overall_pca[:, i].max() - overall_pca[:, i].min())

        overall_pca_df = gu.array_with_column_titles_and_label_titles_to_df( overall_pca, feature_names, sample_mask )
        overall_stds_df = gu.array_with_column_titles_and_label_titles_to_df( overall_stds, feature_names, sample_mask )

        if shiny:

            pca_ft_df, pca_std, components, pca_feature_names = gu.perform_pca( directory, overall_pca_df, [int( i ) for i in overall_pca_df.index], std_error = True, std_of_features_df = overall_stds_df, num_components = 2, filename = output_directory + "Global/PCA/Overall.png" )

        else:

            pca_ft_df, pca_std, components, pca_feature_names = gu.perform_pca( directory, overall_pca_df, [int( i ) for i in overall_pca_df.index], std_error = True, std_of_features_df = overall_stds_df, num_components = 2, filename = output_directory + "Global/PCA/Overall.pdf" )

        pca_ft = pca_ft_df.to_numpy()

        if compute_distance_to_virgin:

            virgin_samples = [16, 17, 19]

            virgin_samples = [i for i in virgin_samples if i in sample_mask]

            distance_to_virgin = euclidean_distance_to_virgin( pca_ft, sample_mask, virgin_samples )

            distance_to_virgin_rank( resin_data, distance_to_virgin, virgin_samples, sample_mask )

            # Virgin V6: ['V6', 'V8', 'PCR 6', 'PCR 1', 'PCR 12', 'PCR 5', 'PCR 15', 'PCR 7', 'V7', 'PCR 9', 'PCR 2', 'PCR 8', 'PCR 3', 'PCR 13', 'PCR 14', 'PCR 11', 'PCR 10', 'PCR 21', 'PCR 20', 'PCR 4', 'PCR 18', 'PCR 22', 'PCR 23']
            # Virgin V7: ['V7', 'PCR 15', 'PCR 3', 'V8', 'PCR 1', 'PCR 12', 'V6', 'PCR 5', 'PCR 2', 'PCR 6', 'PCR 14', 'PCR 9', 'PCR 7', 'PCR 4', 'PCR 11', 'PCR 13', 'PCR 10', 'PCR 21', 'PCR 18', 'PCR 20', 'PCR 22', 'PCR 8', 'PCR 23']
            # Virgin V8: ['V8', 'V6', 'V7', 'PCR 15', 'PCR 1', 'PCR 12', 'PCR 3', 'PCR 5', 'PCR 6', 'PCR 2', 'PCR 7', 'PCR 9', 'PCR 14', 'PCR 11', 'PCR 13', 'PCR 8', 'PCR 10', 'PCR 4', 'PCR 21', 'PCR 20', 'PCR 18', 'PCR 22', 'PCR 23']
            # Mean: ['V8', 'V6', 'PCR 15', 'V7', 'PCR 1', 'PCR 12', 'PCR 5', 'PCR 6', 'PCR 3', 'PCR 2', 'PCR 7', 'PCR 9', 'PCR 14', 'PCR 11', 'PCR 13', 'PCR 8', 'PCR 10', 'PCR 4', 'PCR 21', 'PCR 20', 'PCR 18', 'PCR 22', 'PCR 23']

        if perform_k_means:

            kmeans = KMeans( n_clusters = 3, random_state = 0 ).fit( pca_ft[:, [0, 1]] )

            gu.plot_kmeans_plus_pca( pca_ft, kmeans, sample_mask, [resin_data.loc[i]["Label"] for i in sample_mask], savefig = True, xlabel = "First Principal Component", ylabel = "Second Principal Component", filename = output_directory + "Global/Kmeans/Kmeans.png" )

            label_and_cluster_label = zip( [resin_data.loc[i]["Label"] for i in sample_mask], kmeans.labels_ )

            print( "KMeans cluster labels:", list( label_and_cluster_label ) )

        return pca_ft_df.index.tolist(), pca_ft_df[pca_ft_df.columns[0]].tolist(), pca_ft_df[pca_ft_df.columns[1]].tolist(), np.array( pca_std[0] ).tolist(), np.array( pca_std[1] ).tolist(), components[:, 0].tolist(), components[:, 1].tolist(), pca_feature_names

def distance_to_virgin_analysis_based_on_pcas( output_directory, features_df ):

    dataset_names = ["FTIR", "DSC", "TGA", "Rhe", "TT", "Colour"]
    dataset_labels = ["FTIR", "DSC", "TGA", "Rheo", "Mech", "Colour"]

    iter = gu.subset_combinations_for_all_sizes_of_subsets( len( dataset_names ) )

    virgin_samples = [16, 17, 19]

    num_components = 3

    sample_mask = features_df.index.to_list()

    virgin_samples = [i for i in virgin_samples if i in sample_mask]

    features_split_by_dataset_df = []

    for i, n in enumerate( dataset_names ):

        df = features_df.filter( regex = r"^" + n )

        features_split_by_dataset_df.append( df )

    pcas = []

    for i in range( len( features_split_by_dataset_df ) ):

        if not features_split_by_dataset_df[i].empty:

            pca = PCA( n_components = num_components )
            pca_ft = pca.fit_transform( features_split_by_dataset_df[i].to_numpy() )

            pcas.append( gu.array_with_column_titles_and_label_titles_to_df( pca_ft, [dataset_names[i] + "_PC" + str( j ) for j in range( 1, num_components + 1 )], sample_mask ) )

        else:

            pcas.append( pd.DataFrame() )

    iter_dist_to_virgin = []
    iter_names = []

    for it in iter:

        iter_name = ""

        for i in range( len( dataset_names ) ):

            if i in it:

                if iter_name != "":

                    iter_name += "+"

                iter_name += dataset_labels[i]

        iter_names.append( iter_name )

        pcas_to_include = []

        for i in range( len( dataset_names ) ):

            if i in it and not pcas[i].empty:

                pcas_to_include.append( pcas[i] )

        overall_pca = np.zeros( len( sample_mask ) )[:, np.newaxis]

        feature_names = []

        for i in range( len( pcas_to_include ) ):

            for j in range( len( pcas_to_include[i].columns ) ):

                overall_pca = np.hstack( (overall_pca, pcas_to_include[i].iloc[:, j].to_numpy()[:, np.newaxis]) )

                feature_names.append( pcas_to_include[i].columns[j] )

        overall_pca = overall_pca[:, 1:]

        num_components = len( overall_pca[0] )

        for i in range( num_components ):

            overall_pca[:, i] =  (overall_pca[:, i] - overall_pca[:, i].min()) / (overall_pca[:, i].max() - overall_pca[:, i].min())

        overall_pca_df = gu.array_with_column_titles_and_label_titles_to_df( overall_pca, feature_names, sample_mask )

        pca = PCA( n_components = 2 )
        pca_ft = pca.fit_transform( overall_pca_df )

        iter_dist_to_virgin.append( euclidean_distance_to_virgin( pca_ft, sample_mask, virgin_samples ) )

    iter_mean_resin_dist_to_virgin = []

    for i in range( len( iter ) ):

        array = np.array( iter_dist_to_virgin[i] )

        if i == 0 or iter_names[i] == "FTIR+TGA+Mech":

            iter_mean_resin_dist_to_virgin.append( [(array[0][j] + array[1][j] + array[2][j]) / 3 for j in range( len( array[0] ) )] )

    fig, ax = plt.subplots()

    x = np.arange( len( sample_mask ) )
    width = 0.25
    multiplier = 0

    for i in range( 2 ):

        offset = width * multiplier
        rects = ax.bar( x + offset, np.array( iter_mean_resin_dist_to_virgin )[i], width, label = i )
        multiplier += 1

    ax.set_ylabel( "Mean Distance to Virgin" )
    ax.set_xticks( x, sample_mask )
    ax.set_ylim( 0, 2.2 )

    # plt.show()

    plt.close()

    sum_iter_dist_to_virgin = []

    for i in range( len( iter ) ):

        array_1 = np.array( iter_dist_to_virgin[0] )
        array_2 = np.array( iter_dist_to_virgin[i] )

        sum_iter_dist_to_virgin.append( abs( array_1 - array_2 ).sum() / (len( virgin_samples ) * len( sample_mask )) )

    result_dict = {iter_names[i]: sum_iter_dist_to_virgin[i] for i in range( len ( iter_names ) )}

    max_dist = max( result_dict.values() )
    min_dist = min( result_dict.values() )

    dicts, dfs = [], []

    if False:

        # Triplets, horizontal.

        dicts3 = {key: result_dict[key] for key in result_dict if key.count( "+" ) == 2}

        max_dist = max( dicts3.values() )
        min_dist = min( dicts3.values() )

        dicts3 = dict( sorted( dicts3.items(), key = lambda x:x[1] ) )

        df3 = pd.DataFrame.from_dict( dicts3, orient = "index" )

        df3.index = df3.reset_index( drop = True ).index // 10

        df3 = df3.groupby( level = 0 ).apply( lambda x: x[0].reset_index( drop = True ) ).T

        fig, ax = plt.subplots( 2, 1 )

        fig.set_size_inches( 30, 20 )

        im = ax[0].imshow( df3[df3.columns[0]].to_frame().T, vmin = min_dist, vmax = max_dist + 0.07, cmap = cm.plasma )
        im = ax[1].imshow( df3[df3.columns[1]].to_frame().T, vmin = min_dist, vmax = max_dist + 0.07, cmap = cm.plasma )

        for j in range( 10 ):

            pattern = re.compile( r"^(\w+)\+(\w+)\+(\w+)$" )

            ax[0].text( j, 0, pattern.search( list( dicts3.keys() )[j] ).groups()[0] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[1] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[2], ha = "center", va = "center", color = "w", fontsize = 25 )

        for j in range( 10, 20 ):

            pattern = re.compile( r"^(\w+)\+(\w+)\+(\w+)$" )

            ax[1].text( j - 10, 0, pattern.search( list( dicts3.keys() )[j] ).groups()[0] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[1] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[2], ha = "center", va = "center", color = "w", fontsize = 25 )

        ax[0].tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        ax[0].tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )
        ax[1].tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        ax[1].tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        # fig.colorbar( im, orientation = 'vertical' )
        # fig.subplots_adjust( right = 0.6 )

        # plt.tight_layout()

        cbar_ax = fig.add_axes( [0.8, 0.4, 0.04, 0.2] )
        cbar = fig.colorbar( im, cax = cbar_ax, shrink = 0.2 )
        cbar.ax.tick_params( labelsize = 25 )

        plt.subplots_adjust( left = 0.1, bottom = 0.4, right = 0.9, top = 0.6, wspace = 0.4, hspace = 0.4 )

        plt.savefig( output_directory + "Global/Distance_to_Virgin_Analysis/" + "Horizontal.pdf" )

        plt.close()

    if True:

        # Triplets, vertical.

        dicts3 = {key: result_dict[key] for key in result_dict if key.count( "+" ) == 2}

        max_dist = max( dicts3.values() )
        min_dist = min( dicts3.values() )

        dicts3 = dict( sorted( dicts3.items(), key = lambda x:x[1] ) )

        df3 = pd.DataFrame.from_dict( dicts3, orient = "index" )

        df3.index = df3.reset_index( drop = True ).index // 10

        df3 = df3.groupby( level = 0 ).apply( lambda x: x[0].reset_index( drop = True ) ).T

        fig, ax = plt.subplots( 1, 2 )

        fig.set_size_inches( 20, 30 )

        im = ax[0].imshow( df3[df3.columns[0]].to_frame(), vmin = min_dist, vmax = max_dist + 0.07, cmap = cm.plasma )
        im = ax[1].imshow( df3[df3.columns[1]].to_frame(), vmin = min_dist, vmax = max_dist + 0.07, cmap = cm.plasma )

        for j in range( 10 ):

            pattern = re.compile( r"^(\w+)\+(\w+)\+(\w+)$" )

            ax[0].text( 0, j, pattern.search( list( dicts3.keys() )[j] ).groups()[0] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[1] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[2], ha = "center", va = "center", color = "w", fontsize = 25 )

        for j in range( 10, 20 ):

            pattern = re.compile( r"^(\w+)\+(\w+)\+(\w+)$" )

            ax[1].text( 0, j - 10, pattern.search( list( dicts3.keys() )[j] ).groups()[0] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[1] + "\n" + pattern.search( list( dicts3.keys() )[j] ).groups()[2], ha = "center", va = "center", color = "w", fontsize = 25 )

        ax[0].tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        ax[0].tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )
        ax[1].tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        ax[1].tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        # fig.colorbar( im, orientation = 'vertical' )
        # fig.subplots_adjust( right = 0.6 )

        # plt.tight_layout()

        cbar_ax = fig.add_axes( [0.66, 0.22, 0.06, 0.56] )
        cbar = fig.colorbar( im, cax = cbar_ax, shrink = 1 )
        cbar.ax.tick_params( labelsize = 25 )

        plt.subplots_adjust( left = 0.4, bottom = 0.1, right = 0.6, top = 0.9, wspace = 0.4, hspace = 0.4 )

        plt.savefig( output_directory + "Global/Distance_to_Virgin_Analysis/" + "Vertical.pdf" )

        plt.close()

    if False:

        searches = ["FTIR", "DSC", "TGA", "Rheo", "Mech", "Colour"]

        for i, s in enumerate( searches ):

            pattern = re.compile( s )

            dicts.append( {key: result_dict[key] for key in result_dict if pattern.search( key ) != None} )

            dfs.append( pd.DataFrame.from_dict( dicts[i], orient = "index" ) )

            dfs[i].rename( columns = {dfs[i].columns[0]:s}, inplace = True )

        fig, ax = plt.subplots( 1, 6 )

        fig.set_size_inches( 20, 20 )

        for i in range( len( searches ) ):

            im = ax[i].imshow( dfs[i], vmin = 0, vmax = max_dist, cmap = cm.plasma )

            ax[i].set_xticks( np.arange( 0, len( dfs[i].columns ), 1 ) )
            ax[i].set_yticks( np.arange( 0, len( dfs[i].index ), 1 ) )

            ax[i].set_xticklabels( dfs[i].columns, rotation = 270, fontsize = 20 )
            ax[i].set_yticklabels( dfs[i].index, fontsize = 10 )

            # for j in range( len( dfs[i].index ) ):
            #
            #     pattern = re.compile( r"^(\w+)\+(\w+)\+(\w+)$" )
            #
            #     ax[i].text( 0, j, pattern.search( dfs[i].index[j] ).groups()[0] + "\n" + pattern.search( dfs[i].index[j] ).groups()[1] + "\n" + pattern.search( dfs[i].index[j] ).groups()[2], ha = "center", va = "center", color = "w" )

            ax[i].invert_yaxis()

        plt.tight_layout()

        plt.savefig( output_directory + "Global/Distance_to_Virgin_Analysis/" + "Plot.pdf" )

        plt.close()

def manual_ml( directory, ip, features_df ):

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    ml_features = pd.DataFrame( features_df["FTIR_777"] )
    ml_features = ml_features.merge( features_df["DSC_HFM_160"], left_index = True, right_index = True )
    ml_features = ml_features.merge( features_df["TGA_Temp_380-400"], left_index = True, right_index = True )
    ml_features = ml_features.merge( features_df["Rhe_Crossover"], left_index = True, right_index = True )

    scalars = [-1, -0.7, -0.3, 0, 0.3, 0.7, 1]

    a, b, c, d = 0, 0, 0, 0

    max_pearson = 0

    for i in scalars:

        for j in scalars:

            for k in scalars:

                for l in scalars:

                    if i == 0 and j == 0 and k == 0 and l == 0:

                        continue

                    ml_copy = ml_features.copy()

                    ml_copy[ml_copy.columns[0]] = ml_copy[ml_copy.columns[0]].apply( lambda x: x * i )
                    ml_copy[ml_copy.columns[1]] = ml_copy[ml_copy.columns[1]].apply( lambda x: x * j )
                    ml_copy[ml_copy.columns[2]] = ml_copy[ml_copy.columns[2]].apply( lambda x: x * k )
                    ml_copy[ml_copy.columns[3]] = ml_copy[ml_copy.columns[3]].apply( lambda x: x * l )

                    sum_ml = ml_copy.sum( axis = 1 )

                    pearson, _ = pearsonr( sum_ml, features_df["TT_SAB"].tolist() )

                    if abs( pearson ) > max_pearson:

                        max_pearson = abs( pearson )
                        a, b, c, d = i, j, k, l

    print( a, b, c, d, max_pearson )

    ml_copy = ml_features.copy()

    ml_copy[ml_copy.columns[0]] = ml_copy[ml_copy.columns[0]].apply( lambda x: x * a )
    ml_copy[ml_copy.columns[1]] = ml_copy[ml_copy.columns[1]].apply( lambda x: x * b )
    ml_copy[ml_copy.columns[2]] = ml_copy[ml_copy.columns[2]].apply( lambda x: x * c )
    ml_copy[ml_copy.columns[3]] = ml_copy[ml_copy.columns[3]].apply( lambda x: x * d )

    sum_ml = ml_copy.sum( axis = 1 )

    feature_1 = sum_ml.to_numpy()
    feature_2 = features_df["TT_SAB"].to_numpy()

    # gu.plot_scatterplot_of_two_features( feature_1, feature_2, ip.sample_mask, [resin_data.loc[i]["Label"] for i in features_df.index] )

    X = ml_features.to_numpy()
    y = features_df["TT_SAB"].to_numpy()

    training_resins = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23]
    test_resins = [7, 9, 11, 13, 15, 17, 19, 21]

    split_train = [ml_features.index.to_list().index( i ) for i in training_resins]
    split_test = [ml_features.index.to_list().index( i ) for i in test_resins]

    X_train = X[split_train]
    X_test = X[split_test]
    y_train = y[split_train]
    y_test = y[split_test]

    regr = linear_model.LinearRegression()

    regr.fit( X_train, y_train )

    y_pred = regr.predict( X_test )

    print( "Coefficients: ", regr.coef_ ) # The coefficients.
    print( "Mean squared error: %.2f" % mean_squared_error( y_test, y_pred ) ) # The mean squared error.
    print( "Coefficient of determination: %.2f" % r2_score( y_test, y_pred ) ) # The coefficient of determination: 1 is perfect prediction.

    gu.plot_scatterplot_of_two_features( y_test, y_pred, test_resins, [resin_data.loc[i]["Label"] for i in test_resins] )

def pca_ml( directory, ip, features_df ):

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    num_components = 5

    X, _, _, _ = gu.perform_pca( directory, features_df, ip.sample_mask, num_components = num_components, analysis_of_pca = False )

    # gu.plot_df_heatmap( X )

    X, y = X.to_numpy(), features_df["TT_SAB"].to_numpy()

    number_repeats = 1

    coefficients = []
    mse = []
    cod = []

    for r in range( number_repeats ):

        training_resins = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23]
        test_resins = [7, 9, 11, 13, 15, 17, 19, 21]

        split_train = [features_df.index.to_list().index( i ) for i in training_resins]
        split_test = [features_df.index.to_list().index( i ) for i in test_resins]

        # X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 7 )

        X_train = X[split_train]
        X_test = X[split_test]
        y_train = y[split_train]
        y_test = y[split_test]

        regr = linear_model.LinearRegression()

        regr.fit( X_train, y_train )

        y_pred = regr.predict( X_test )

        coefficients.append( regr.coef_ )
        mse.append( mean_squared_error( y_test, y_pred ) )
        cod.append( r2_score( y_test, y_pred ) )

        print( "Coefficients: ", regr.coef_ ) # The coefficients.
        print( "Mean squared error: %.2f" % mean_squared_error( y_test, y_pred ) ) # The mean squared error.
        print( "Coefficient of determination: %.2f" % r2_score( y_test, y_pred ) ) # The coefficient of determination: 1 is perfect prediction.

        gu.plot_scatterplot_of_two_features( y_test, y_pred, test_resins, [resin_data.loc[i]["Label"] for i in test_resins] )

    mean_mse = np.array( mse ).mean()
    mean_cod = np.array( cod ).mean()
    c_coefficients = []

    for j in range( num_components ):

        c_coefficients.append( [coefficients[i][j] for i in range( number_repeats )] )

    mean_coefficients = [np.array( c_coefficients[i] ).mean() for i in range( num_components )]

    print( "Mean MSE: ", mean_mse )
    print( "Mean cod: ", mean_cod )
    print( "Mean coefficients: ", mean_coefficients )

    # Output: Mean MSE:  0.07447263900017585
    # Mean cod:  0.3498298501594448
    # Mean coefficients:  [-0.15599656149109054, -0.25995542978716757, 0.10756368212119027, -0.08592974744840264, 0.21583468703827902]

def common_value( list_1, list_2, i ):

    if type( list_1[i] ) == str or type( list_2[i] ) == str:

        return False

    elif math.isnan( list_1[i] ) or math.isnan( list_2[i] ):

        return False

    else:

        return True

def plot_two_columns_of_df( output_directory, df, c1, c2 ):

    list_1 = df[df.columns[c1]].tolist()
    list_2 = df[df.columns[c2]].tolist()

    list_3 = [list_1[x] for x in range( len( list_1 ) ) if common_value( list_1, list_2, x )]
    list_4 = [list_2[x] for x in range( len( list_2 ) ) if common_value( list_2, list_1, x )]

    fig, ax = plt.subplots()

    ax.plot( list_4, list_3, 'rx' )

    ax.set_xscale( 'log' )
    ax.set_yscale( 'log' )
    ax.set_title( "Zero-shear Viscosity")
    ax.set_xlabel( "Zero-Shear Viscosity " )
    ax.set_ylabel( "MFI (190°, 2.16kg)" )
    plt.tight_layout()

    array_3 = np.array( list_3 )
    array_4 = np.array( list_4 )

    m, b = np.polyfit( np.log( array_4 ), np.log( array_3 ), 1 )

    array_4 = np.sort( array_4 )

    plt.plot( array_4, array_4 ** m * np.exp( b ) )

    for i in range( len( df.index.values ) ):

        if df.iat[i, 4] == 1:

            ax.errorbar( df.iat[i, 8], df.iat[i, 3], 0.5 * (df.iat[i, 6] - df.iat[i, 5]), capsize = 5 )

    output_file = df.columns[c1][:3] + df.columns[c2][:3] + ".png"

    plt.savefig( output_directory + output_file )

def mfi_vs_zero_shear( directory ):

    df = pd.read_csv( directory + "rhdpe_dataset.csv" )

    df.drop( df.columns[0], axis = 1, inplace = True )

    # df.drop( [18, 21, 23], inplace = True )

    plot_two_columns_of_df( directory + "Global/Output/Sandbox/MFI/", df, 3, 8 )

def mlpregressor( features_df ):

    target_column = ['TT_SAB']
    predictors = list( set( list( features_df.columns ) ) - set( target_column ) )

    predictors = ["FTIR_997", "Rhe_Crossover", "TT_SHM"]
    features_df[predictors] = features_df[predictors]/features_df[predictors].max()

    X = features_df[predictors].values
    y = features_df[target_column].values

    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 0.20, random_state = 40 )

    mlp = MLPRegressor( hidden_layer_sizes=( 8, 8, 8 ), activation = 'relu', solver = 'adam', max_iter = 500 )
    mlp.fit( X_train, y_train.ravel() )

    predict_train = mlp.predict( X_train )
    predict_test = mlp.predict( X_test )

    pred = mlp.predict(X_test)

    # Calculate accuracy and error metrics

    test_set_rsquared = mlp.score( X_test, y_test )
    test_set_rmse = np.sqrt( mean_squared_error( y_test, pred ) )

    # Print R_squared and RMSE value

    print( 'R_squared value: ', test_set_rsquared )
    print( 'RMSE: ', test_set_rmse )

    plt.plot( predict_train, y_train, 'o' )
    plt.plot( pred, y_test, 'o' )
    plt.show()

from sklearn.cross_decomposition import PLSRegression

def pls( features_df ):
    '''https://towardsdatascience.com/partial-least-squares-f4e6714452a'''

    X_colnames = features_df.columns[:-7].to_list() + features_df.columns[-3:].to_list()
    Y_colnames = features_df.columns[-7:-3].to_list()

    X = features_df[X_colnames].values
    Y = features_df[Y_colnames].values

    sab_plot = []
    uts_plot = []
    ym_plot = []
    shm_plot = []

    for n_comp in range( 1, 21 ):

      my_plsr = PLSRegression( n_components = n_comp, scale = True )
      my_plsr.fit( X, Y )
      preds = my_plsr.predict( X )

      sab_rmse = sqrt( mean_squared_error( Y[:,0] , preds[:,0] ) )
      uts_rmse = sqrt( mean_squared_error( Y[:,1] , preds[:,1] ) )
      ym_rmse = sqrt( mean_squared_error( Y[:,2] , preds[:,2] ) )
      shm_rmse = sqrt( mean_squared_error( Y[:,3] , preds[:,3] ) )

      sab_plot.append( sab_rmse )
      uts_plot.append( uts_rmse )
      ym_plot.append( ym_rmse )
      shm_plot.append( shm_rmse )

    # Create the three plots using matplotlib
    fig, axs = plt.subplots(1,4)

    axs[0].plot( range( 1, 21 ), sab_plot )
    axs[1].plot( range( 1, 21 ), uts_plot )
    axs[2].plot( range( 1, 21 ), ym_plot )
    axs[3].plot( range( 1, 21 ), shm_plot )

    # plt.show()


    best_model = PLSRegression( n_components = 10, scale = True )
    best_model.fit( X, Y )
    test_preds = best_model.predict( X )
    print( r2_score( Y, test_preds ) )

import itertools
from sklearn.linear_model import LinearRegression

def escr_predictor( directory, features_df, std_of_features_df ):

    # [1.12733926] -0.1283258558485133

    resin_data = gu.get_list_of_resins_data( directory )

    # target_escr = features_df["ESCR_50%Failure"]
    #
    # X_escr = pd.DataFrame( features_df["SHM"] )
    #
    # reg = LinearRegression().fit( X_escr, target_escr )
    #
    # score = reg.score( X_escr, target_escr )
    #
    # print( score )
    # print( reg.coef_, reg.intercept_)
    #
    # prediction = reg.predict( X_escr )
    #
    # gu.plot_scatterplot_of_two_features( directory, prediction, target_escr.to_numpy(), features_df.index, [resin_data.loc[i]["Label"] for i in features_df.index], errorbars = False, std = "", line_of_best_fit = False, exponential_fit = False, xlabel = "Prediction", ylabel = "Target", savefig = False, filename = "" )
    #
    # plt.show()
    #
    # plt.close()

    target = features_df["SHM"]

    X = features_df.drop( ["SHM", "TT_SHM"], axis = 1 )
    # X = features_df.drop( ["SHM"], axis = 1 )

    print( X.shape )

    combinations = itertools.combinations( [i for i in range( 23 )], 3 )

    i = 0
    score = 0
    best_c = None

    # for c in combinations:
    #
    #     i += 1
    #
    #     if (i > 100):
    #
    #         pass
    #         # break
    #
    #     X1 = X.iloc[:, list( c )]
    #
    #     reg = LinearRegression().fit( X1, target )
    #
    #     score_1 = reg.score( X1, target )
    #
    #     if score_1 > score:
    #
    #         score = score_1
    #         best_c = c

    best_c = (2, 11, 14)

    print( score, best_c, X.iloc[:, list( best_c )].columns )

    X1 = X.iloc[:, list( best_c )]

    reg = LinearRegression().fit( X1, target )

    prediction = reg.predict( X1 )

    prediction_escr = prediction * 1.12 - 0.13

    unnormalised_shm = prediction * 9 + 5
    unnormalised_escr = prediction_escr * 80 + 16

    array = np.hstack( (unnormalised_shm[:, np.newaxis], unnormalised_escr[:, np.newaxis]) )

    np.savetxt( "/Users/philsmith/Documents/Postdoc/rHDPE_Data_Analysis/Output/Global/Sandbox/ESCR_Prediction/ESCR_Prediction.csv", array, delimiter = ",", fmt = "%.5f" )

    gu.plot_scatterplot_of_two_features( directory, prediction, target.to_numpy(), features_df.index, [resin_data.loc[i]["Label"] for i in features_df.index], errorbars = False, std = "", line_of_best_fit = False, exponential_fit = False, xlabel = "Prediction", ylabel = "Target", savefig = False, filename = "" )

def feature_regression( directory, features_df ):

    # PP and CaCO3 vs SAB.

    # feature_1_labels = ["FTIR_868-885", "FTIR_965-980"]
    # feature_2_labels = ["TT_SAB"]

    resin_data = gu.get_list_of_resins_data( directory )

    target_feature = "ESCR_50%Failure"
    regression_features = ["SHM", "TT_SAB"]

    target = features_df[target_feature]
    features_df = features_df.drop( target_feature, axis = 1 )

    X = features_df[regression_features]

    reg = LinearRegression().fit( X, target )

    prediction = reg.predict( X )

    for i in range( len( regression_features ) ):

        print( regression_features[i], "has coefficient", reg.coef_[i] )

    print( "Intercept:", reg.intercept_ )

    gu.plot_scatterplot_of_two_features( directory, prediction, target.to_numpy(), features_df.index, [resin_data.loc[i]["Label"] for i in features_df.index], errorbars = False, std = "", line_of_best_fit = False, exponential_fit = False, xlabel = "Prediction", ylabel = "Target", savefig = False, filename = "" )

def sandbox( directory, features_df, std_of_features_df ):

    perform_mfi_vs_zero_shear = False
    perform_mlpregressor = False
    perform_pls = False
    perform_escr_predictor = False
    perform_feature_regression = True

    if perform_mfi_vs_zero_shear:

        mfi_vs_zero_shear( directory )

    if perform_mlpregressor:

        mlpregressor( features_df )

    if perform_pls:

        pls( features_df )

    if perform_escr_predictor:

        escr_predictor( directory, features_df, std_of_features_df )

    if perform_feature_regression:

        feature_regression( directory, features_df )