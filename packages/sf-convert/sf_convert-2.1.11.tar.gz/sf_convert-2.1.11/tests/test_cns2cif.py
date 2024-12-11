from sf_convert.import_dir.import_cns import ImportCns
from sf_convert.export_dir.export_cif import ExportCif
from sf_convert.utils.pinfo_file import PInfoLogger
from TestHelper import comp_sfcif
import os


class TestCnsToCifConversion:
    def test_cns2cif(self, tmp_path, cns_5pny_data_path, cns_cif_5pny_data_path):
        """
        Tests the conversion of a CNS file to CIF format.

        Args:
            tmp_path: The path to the temporary directory.
            cns_5pny_data_path: The path to the CNS file to be converted.
            cif_5pny_data_path: The path to the reference CIF file for comparison.

        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "output_cns2cif.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")

        processor = ImportCns(logger)
        processor.set_free(1)
        processor.import_files([cns_5pny_data_path])

        sffile = processor.get_sf()
        ec = ExportCif(False)
        ec.set_sf(sffile)

        ec.write_file(output_path)

        print("Comparing the outputs...")
        comp_sfcif(cns_cif_5pny_data_path, output_path)

        print("Test completed.")
