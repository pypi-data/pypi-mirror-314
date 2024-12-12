# Imports.

from . import Preprocessing
from . import Utilities as util

from .. import Global_Utilities as gu

# Main function definition.

def Global_Analysis_Main( ip ):

    if type( ip.datasets_to_read ) == int:

        ip.datasets_to_read = [ip.datasets_to_read]

    if ip.datasets_to_read == False:

        print( "Please select a dataset(s)" )

        return 0

    resin_data = gu.get_list_of_resins_data( ip.directory ) # Obtain the spreadsheet of data for the resins.

    if ip.read_files:

        features_df, std_of_features_df, rank_features_df = Preprocessing.read_files_and_preprocess( ip )

    if ip.plot_global_features:

        gu.plot_global_features( ip.output_directory + "Global/", features_df.to_numpy(), features_df.columns, [resin_data.loc[i]["Label"] for i in features_df.index] )

    if ip.scatterplot:

        return util.scatterplots( ip )

    if ip.correlation_heatmaps:

        spearman_rank_df = util.correlation_heatmap( rank_features_df, spearman = True )
        pearson_df = util.correlation_heatmap( features_df )

        gu.plot_df_heatmap( spearman_rank_df, savefig = True, filename = ip.output_directory + "Global/Correlations/Spearman.pdf" )
        gu.plot_df_heatmap( pearson_df, savefig = True, filename = ip.output_directory + "Global/Correlations/Pearson.pdf" )

    if ip.pca:

        return util.pca( ip.directory, ip.output_directory, ip.shiny, features_df, std_of_features_df )

    if ip.distance_to_virgin_analysis_based_on_pcas:

        util.distance_to_virgin_analysis_based_on_pcas( ip.output_directory, features_df )

    if ip.manual_ml:

        util.manual_ml( ip.directory, ip, features_df )

    if ip.pca_ml:

        util.pca_ml( ip.directory, ip, features_df )

    if ip.sandbox:

        util.sandbox( ip.directory, features_df, std_of_features_df )
