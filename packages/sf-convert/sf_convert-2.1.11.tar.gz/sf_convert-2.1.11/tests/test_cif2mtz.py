import os
from sf_convert.export_dir.export_mtz import ExportMtz
from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.utils.pinfo_file import PInfoLogger


class TestCifToMtzConversion:
    def test_cif2mtz(self, tmp_path, cif_5pny_data_path):
        """
        Tests the conversion of a CIF file to MTZ format.

        Args:
            tmp_path: The path to the temporary directory.
            cif_5pny_data_path: The path to the CIF file to be converted.

        Returns:
            None
        """
        print("Starting the test...")

        # output_path = tmp_path / "output.mtz"
        output_path = os.path.join(tmp_path, "output.mtz")
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")

        print("Loading and converting the file...")
        sffile = StructureFactorFile()
        sffile.read_file(cif_5pny_data_path)

        converter = ExportMtz(logger)
        converter.set_sf(sffile)
        converter.write_file(output_path)

        print("Checking the output...")
        assert os.path.isfile(output_path)
        assert os.path.getsize(output_path) > 0

        print("Test completed.")
