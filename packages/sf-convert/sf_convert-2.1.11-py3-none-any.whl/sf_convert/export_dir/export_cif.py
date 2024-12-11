from sf_convert.sffile.sf_file import StructureFactorFile

# from sf_convert.utils.reformat_sfhead import reformat_sfhead, reorder_sf_file, update_exptl_crystal


class ExportCif:
    def __init__(self, legacy):
        """Output to cif

        Args:
        legacy: Boolean - to add some old attributes to refln categor
        """
        self.__legacy = legacy
        self.__sffile = None

    def load_input(self, pathIn):
        """
        Loads PDBx/mmCIF SF file

        Args:
        pathIn: String - path to input file

        Returns:
        Nothing
        """
        self.__sffile = StructureFactorFile()

        self.__sffile.read_file(pathIn)

    def set_sf(self, sfobj):
        """
        Loads PDBx/mmCIF SF file

        Args:
        sf: StructureFactorFile - object with data

        Returns:
        Nothing
        """
        self.__sffile = sfobj

    def write_file(self, pathOut):
        """Writes SF file to output"""

        # Legacy requires END and END OF DATA comments
        endc = True if self.__legacy else False

        # If no data - produce empty file
        if self.__sffile.get_number_of_blocks() == 0:
            endc = False

        self.__sffile.write_file(pathOut, endcomments=endc)
