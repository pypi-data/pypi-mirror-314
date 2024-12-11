# Class to import cif files.

import os
from sf_convert.sffile.sf_file import StructureFactorFile


class ImportCif:

    def __init__(self, logger):
        """Class to import CIF files - multiple supported"""
        self.__logger = logger
        self.__sf = None

    def import_files(self, fileList):
        """Reads in possibly multiple SF files


        Args:
            fileList (list): List of file names

        Returns:
             StructureFile object
        """

        for fpath in fileList:
            if not os.path.exists(fpath):
                self.__logger.pinfo(f"File {fpath} does not exist", 0)
                self.__sf = None
                return None

            sf = StructureFactorFile()
            sf.read_file(fpath)

            if self.__sf:
                self.__sf.merge_sf(sf)
            else:
                self.__sf = sf

    def get_sf(self):
        return self.__sf
