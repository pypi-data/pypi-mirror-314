# Imports.

from numbers_parser import Document

# Class definitions.

class Input_Parameters():

    def __init__( self ):

        self.shiny = False

        self.directory = ""

        self.output_directory = ""

        self.datasets_to_read = []

        self.sample_mask = []

        self.read_files = False

        self.plot_global_features = False

        self.scatterplot = False

        self.correlation_heatmaps = False

        self.pca = False

        self.distance_to_virgin_analysis_based_on_pcas = False

        self.rank_resins_by_pp_content = False

        self.manual_ml = False

        self.pca_ml = False

        self.sandbox = False

        self.user = "philsmith"

        self.scatterplot_x = ""

        self.scatterplot_y = ""

# Function definitions.

def read_parameters_from_numbers_file( filename, ip ):

    doc = Document( filename )

    sheets = doc.sheets
    tables = sheets[0].tables
    rows = tables[0].rows()

    ip.shiny = bool( rows[0][1].value )

    ip.directory = str( rows[1][1].value or "" )

    ip.output_directory = str( rows[2][1].value or "" )

    ip.datasets_to_read = [int( i.value ) for i in rows[3][1:] if i.value != None]

    ip.sample_mask = [int( i.value ) for i in rows[4][1:] if i.value != None]

    ip.read_files = bool( rows[5][1].value )

    ip.plot_global_features = bool( rows[6][1].value )

    ip.scatterplot = bool( rows[7][1].value )

    ip.correlation_heatmaps = bool( rows[8][1].value )

    ip.pca = bool( rows[9][1].value )

    ip.distance_to_virgin_analysis_based_on_pcas = bool( rows[10][1].value )

    ip.rank_resins_by_pp_content = bool( rows[11][1].value )

    ip.manual_ml = bool( rows[12][1].value )

    ip.pca_ml = bool( rows[13][1].value )

    ip.sandbox = bool( rows[14][1].value )
