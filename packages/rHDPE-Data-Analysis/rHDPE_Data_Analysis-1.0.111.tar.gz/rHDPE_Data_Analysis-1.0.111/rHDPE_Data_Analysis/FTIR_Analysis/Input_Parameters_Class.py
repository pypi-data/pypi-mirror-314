# Imports.

from numbers_parser import Document

# Class definitions.

class Input_Parameters():

    def __init__( self ):

        self.shiny = False

        self.directory = ""

        self.data_directory = ""

        self.output_directory = ""

        self.read_files = False

        self.merge_groups = False

        self.write_csv = False

        self.read_csv = False

        self.remove_files = False

        self.compute_mean = False

        self.read_mean = False

        self.derivative = False

        self.extract_features = False

        self.peak_threshold_1 = 0

        self.peak_threshold_2 = 0

        self.peak_spacing = 0

        self.peak_limit = 0

        self.read_and_analyse_features = False

        self.plot_data = False

        self.sandbox = False

        self.sample_mask = []

        self.feature_selection = []

        self.shiny_samples_to_plot = []

        self.shiny_specimens_to_plot = []

        self.shiny_split = []

        self.shiny_mean = False

        self.shiny_specimen = False

        self.name_appendage = ""

# Function definitions.

def read_parameters_from_numbers_file( filename, ip ):

    doc = Document( filename )

    sheets = doc.sheets
    tables = sheets[0].tables
    rows = tables[0].rows()

    ip.shiny = bool( rows[0][1].value )

    ip.directory = str( rows[1][1].value or "" )

    ip.data_directory = str( rows[2][1].value or "" )

    ip.output_directory = str( rows[3][1].value or "" )

    ip.read_files = bool( rows[4][1].value )

    ip.merge_groups = bool( rows[5][1].value )

    ip.write_csv = bool( rows[6][1].value )

    ip.read_csv = bool( rows[7][1].value )

    ip.remove_files = bool( rows[8][1].value )

    ip.compute_mean = bool( rows[9][1].value )

    ip.read_mean = bool( rows[10][1].value )

    ip.derivative = bool( rows[11][1].value )

    ip.extract_features = bool( rows[12][1].value )

    ip.peak_threshold_1 = float( rows[13][1].value )

    ip.peak_threshold_2 = float( rows[14][1].value )

    ip.peak_spacing = float( rows[15][1].value )

    ip.peak_limit = float( rows[16][1].value )

    ip.read_and_analyse_features = bool( rows[17][1].value )

    ip.plot_data = bool( rows[18][1].value )

    ip.sandbox = bool( rows[19][1].value )

    ip.sample_mask = [int( i.value ) for i in rows[20][1:] if i.value != None]

    ip.feature_selection = [int( i.value ) for i in rows[21][1:] if i.value != None]
