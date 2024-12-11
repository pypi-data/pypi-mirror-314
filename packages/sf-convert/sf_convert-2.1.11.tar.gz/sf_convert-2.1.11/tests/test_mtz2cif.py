from sf_convert.import_dir.import_mtz import ImportMtz
from sf_convert.utils.pinfo_file import PInfoLogger
from TestHelper import comp_sfcif
from mmcif.io.IoAdapterCore import IoAdapterCore
import os


class TestMtzToCifConversion:
    def test_mtz2cif(self, tmp_path, mtz_Ras_NAD_data_path, cif_Ras_NAD_data_path):
        """
        Tests the conversion of an MTZ file to CIF format.

        Args:
            tmp_path: The path to the temporary directory.
            mtz_Ras_NAD_data_path: The path to the MTZ file to be converted.
            cif_Ras_NAD_data_path: The path to the reference CIF file for comparison.

        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "output.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")
        converter = ImportMtz(logger)

        # converter.process_labels()  # if labels are required
        converter.import_files([mtz_Ras_NAD_data_path])
        sffile = converter.get_sf()
        sffile.write_file(output_path)

        print("Comparing the outputs...")
        comp_sfcif(cif_Ras_NAD_data_path, output_path)

        print("Test completed.")

    def test_mtz2cif_multiple_label(self, tmp_path, mtz_Ras_NAD_data_path):
        """
        Tests the conversion of an MTZ file to CIF format - multiple labels

        Args:
            tmp_path: The path to the temporary directory.
            mtz_Ras_NAD_data_path: The path to the MTZ file to be converted.

        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "output_label2.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")
        converter = ImportMtz(logger)
        converter.set_labels("FP=F_XDSdataset ,  SIGFP=SIGF_XDSdataset  ")

        # converter.process_labels()  # if labels are required
        converter.import_files([mtz_Ras_NAD_data_path])
        sffile = converter.get_sf()
        sffile.write_file(output_path)

        print("Checking")
        io = IoAdapterCore()
        data = io.readFile(output_path, selectList=["refln"])

        assert data
        assert len(data) == 1

        b0 = data[0]
        cObj = b0.getObj("refln")
        assert cObj is not None
        alist = cObj.getAttributeList()

        should_have = ["index_h", "index_k", "index_l", "F_meas_au", "F_meas_sigma_au"]
        assert len(alist) == len(should_have)
        for a in alist:
            assert a in should_have

        print("Test completed.")

    def test_mtz2cif_label(self, tmp_path, mtz_Ras_NAD_data_path):
        """
        Tests the conversion of an MTZ file to CIF format.

        Args:
            tmp_path: The path to the temporary directory.
            mtz_Ras_NAD_data_path: The path to the MTZ file to be converted.

        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "output_label.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")
        converter = ImportMtz(logger)
        converter.set_labels("FP=F_XDSdataset ,  SIGFP=SIGF_XDSdataset : FP=F_XDSdataset ,  SIGFP=SIGF_XDSdataset, FREE=FreeR_flag")

        # converter.process_labels()  # if labels are required
        converter.import_files([mtz_Ras_NAD_data_path])
        sffile = converter.get_sf()
        sffile.write_file(output_path)

        print("Checking")
        io = IoAdapterCore()
        data = io.readFile(output_path, selectList=["refln"])

        assert data
        assert len(data) == 2

        def check(blkid, should_have):
            b0 = data[blkid]
            cObj = b0.getObj("refln")
            assert cObj is not None
            alist = cObj.getAttributeList()
            assert len(alist) == len(should_have)
            for a in alist:
                assert a in should_have

        check(0, ["index_h", "index_k", "index_l", "F_meas_au", "F_meas_sigma_au"])
        check(1, ["index_h", "index_k", "index_l", "F_meas_au", "F_meas_sigma_au", "status"])

        print("Test completed.")

    def test_mtz2cif_case_insensitive(self, tmp_path, mtz_7yra_data_path):
        """
        Tests the conversion of an MTZ file to CIF format in which FreeR column has unusual label.

        Args:
            tmp_path: The path to the temporary directory.
            mtz_7yra_data_path: The path to the MTZ file to be converted.
            cif_Ras_NAD_data_path: The path to the reference CIF file for comparison.

        Returns:
            None
        """
        print("Starting the test...")

        output_path = os.path.join(tmp_path, "7yra.mmcif")

        print("Loading and converting the file...")
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")
        converter = ImportMtz(logger)

        # converter.process_labels()  # if labels are required
        converter.import_files([mtz_7yra_data_path])
        sffile = converter.get_sf()
        sffile.write_file(output_path)

        print("Test labels...")
        io = IoAdapterCore()
        data = io.readFile(output_path, selectList=["refln"])

        assert data
        assert len(data) == 1

        b0 = data[0]
        cObj = b0.getObj("refln")
        assert cObj is not None
        alist = cObj.getAttributeList()

        should_have = [
            "index_h",
            "index_k",
            "index_l",
            "pdbx_r_free_flag",
            "intensity_meas",
            "intensity_sigma",
            "pdbx_I_plus",
            "pdbx_I_plus_sigma",
            "pdbx_I_minus",
            "pdbx_I_minus_sigma",
            "F_meas_au",
            "F_meas_sigma_au",
            "pdbx_F_plus",
            "pdbx_F_plus_sigma",
            "pdbx_F_minus",
            "pdbx_F_minus_sigma",
            "status",
        ]

        assert len(alist) == len(should_have)
        for a in alist:
            assert a in should_have

        print("Test completed.")
