# Imports

import pandas as pd

from . import Utilities as util

from .. import Global_Utilities as gu

# Function definitions.

def read_files_and_preprocess( ip, normalised = True, minimal_datasets = False, feature_1 = "", feature_2 = "" ):

    authorised = False

    dataset_names = ["FTIR", "DSC", "TGA", "Rheology", "TT", "Colour", "SHM", "TLS", "ESCR", "FTIR2", "FTIR3", "TGA_SB"]
    dataset_directories = ["FTIR/Features/", "DSC/Features/", "TGA/Features/", "Rheology/Features/", "TT/Features/", "Colour/Features/", "SHM/Features/", "TLS/Features/", "ESCR/Features/", "FTIR/Integral_Analysis/", "FTIR/Component_Analysis/Features/", "TGA/Sandbox/"]

    normalised_ext = ""

    if normalised == False:

        normalised_ext = "_Unnormalised"

    dataset, std_dataset = [], []

    for i in range( len( dataset_names ) ):

        if not minimal_datasets:

            if (i + 1) not in ip.datasets_to_read:

                continue

        n = dataset_names[i]

        if not normalised and (n == "FTIR2" or n == "FTIR3" or n == "TGA_SB"):

            continue

        df, authorised = gu.read_csv_pipeline( ip, dataset_directories[i], "Mean_Features" + normalised_ext + ".csv", authorised )
        df_std, authorised = gu.read_csv_pipeline( ip, dataset_directories[i], "Std_of_Features" + normalised_ext + ".csv", authorised )

        # try:
        #
        #     df = pd.read_csv( ip.output_directory + dataset_directories[i] + "Mean_Features" + normalised_ext + ".csv", index_col = 0 )
        #     df_std = pd.read_csv( ip.output_directory + dataset_directories[i] + "Std_of_Features" + normalised_ext + ".csv", index_col = 0 )
        #
        # except FileNotFoundError:
        #
        #     try:
        #
        #         df = pd.read_csv( "tmp/" + dataset_directories[i] + "Mean_Features" + normalised_ext + ".csv", index_col = 0 )
        #         df_std = pd.read_csv( "tmp/" + dataset_directories[i] + "Std_of_Features" + normalised_ext + ".csv", index_col = 0 )
        #
        #     except FileNotFoundError:
        #
        #         if not authorised:
        #
        #             source_R_functions( ip.directory )
        #
        #             authorise_googledrive( ip.directory )
        #
        #             authorised = True
        #
        #         print( "File not found on server, getting it from Google Drive." )
        #
        #         df = read_csv_from_gd_via_R( dataset_directories[i], "~/Output/" + dataset_directories[i] + "Mean_Features" + normalised_ext + ".csv" )
        #         df_std = read_csv_from_gd_via_R( dataset_directories[i], "~/Output/" + dataset_directories[i] + "Std_of_Features" + normalised_ext + ".csv" )

        if minimal_datasets:

            if feature_1 not in df.columns.tolist():

                if feature_2 not in df.columns.tolist():

                    continue

        dataset.append( df )
        std_dataset.append( df_std )

    sample_mask = ip.sample_mask.copy()

    for i in range( len( dataset ) ):

        samples_present = dataset[i].iloc[:, 0].tolist()
        sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    features, feature_names = util.produce_full_dataset_of_features( dataset, sample_mask )

    rank_features = util.rank_features( features )

    features_df = gu.array_with_column_titles_and_label_titles_to_df( features, feature_names, sample_mask )

    rank_features_df = gu.array_with_column_titles_and_label_titles_to_df( rank_features, feature_names, sample_mask )

    std_of_features, _ = util.produce_full_dataset_of_features( std_dataset, sample_mask )

    std_of_features_df = gu.array_with_column_titles_and_label_titles_to_df( std_of_features, feature_names, sample_mask )

    #===============

    # Extracting the whole dataset as a .csv.

    # resin_data = gu.get_list_of_resins_data( ip.directory )
    #
    # sample_mask_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    #
    # features_2, feature_names_2, sample_mask_2 = util.compile_full_dataset_of_features( dataset, sample_mask_2 )
    # std_of_features_2, std_of_feature_names_2, sample_mask_2 = util.compile_full_dataset_of_features( std_dataset, sample_mask_2 )
    #
    # features_2_df = gu.array_with_column_titles_and_label_titles_to_df( features_2, feature_names_2, sample_mask_2 )
    # std_of_features_2_df = gu.array_with_column_titles_and_label_titles_to_df( std_of_features_2, std_of_feature_names_2, sample_mask_2 )
    #
    # features_2_df = features_2_df.set_axis( [resin_data.loc[i]["Label"] for i in features_2_df.index], axis = "index" )
    # std_of_features_2_df = std_of_features_2_df.set_axis( [resin_data.loc[i]["Label"] for i in std_of_features_2_df.index], axis = "index" )
    #
    # features_2_df.astype( float ).to_csv( ip.output_directory + "Global/Dataset/Full_Dataset.csv", float_format = "%.5f" )
    # std_of_features_2_df.astype( float ).to_csv( ip.output_directory + "Global/Dataset/Full_Dataset_Std.csv", float_format = "%.5f" )

    #===============

    return features_df, std_of_features_df, rank_features_df
