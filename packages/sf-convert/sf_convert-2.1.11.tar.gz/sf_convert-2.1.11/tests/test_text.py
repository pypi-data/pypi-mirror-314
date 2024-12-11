from sf_convert.utils.TextUtils import is_cif
from sf_convert.utils.pinfo_file import PInfoLogger


class TestTextUtils:
    def test_iscif(self, cif_5pny_coordinate_pdb_path, cif_5pny_coordinate_path):
        """Tests functionality of is_cif for coordinate files"""
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")

        assert is_cif(cif_5pny_coordinate_pdb_path, logger) is False
        assert is_cif(cif_5pny_coordinate_path, logger) is True
