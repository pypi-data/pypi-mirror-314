import os

from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.utils.CheckSfFile import CheckSfFile
from sf_convert.utils.pinfo_file import PInfoLogger
from TestHelper import comp_sfcif


class TestValid:
    def test_sf_file_validation(self, tmp_path, cif_5pny_data_path, cif_SF_4_validate_data_path):
        """
        Tests the validation of a structure factor file.

        Args:
            tmp_path: The path to the temporary directory.
            cif_5pny_data_path: The path to the CIF file containing the structure factor data.
            cif_SF_4_validate_data_path: The path to the reference output file for validation.

        Returns:
            None
        """
        print("Starting the test...")

        # Define the path for the output file
        output_path = os.path.join(tmp_path, "output.cif")

        print("Reading and validating the structure factor file...")
        sffile = StructureFactorFile()
        sffile.read_file(cif_5pny_data_path)
        n = sffile.get_number_of_blocks()
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")
        sf_stat = CheckSfFile(sffile, logger)
        sf_stat.check_sf_all_blocks(n)
        sf_stat.write_sf_4_validation(output_path)

        print("Comparing the outputs...")
        comp_sfcif(cif_SF_4_validate_data_path, output_path)

        print("Test completed.")
