from sf_convert.sffile.get_items_pdb import ProteinDataBank


class TestExtractCoordinate:
    def test_cif(self, cif_5pny_coordinate_path, cif_5pny_nodb2_coordinate_path):
        """
        Tests the extraction of data from PDBx/mmCIF file

        Args:
          cif_5pny_coordinate_path: The path to CIF to be extracted
          cif_5pny_nodb2_coordinate_path: The path to CIF w/o database_2 category

        Returns:
          None:
        """

        p = ProteinDataBank()
        db = p.extract_attributes_from_cif(cif_5pny_coordinate_path)

        assert db["pdb_id"] == "5PNY"
        assert db["RESOH"] == 1.48

        p = ProteinDataBank()
        db = p.extract_attributes_from_cif(cif_5pny_nodb2_coordinate_path)

        assert db["pdb_id"] is None
        assert db["RESOH"] == 1.48

    def test_pdb(self, cif_5pny_coordinate_pdb_path):
        """
        Tests the extraction of data from PDBx/mmCIF file

        Args:
          cif_5pny_coordinate_pdb_path: The path to PDB file to be extracted

        Returns:
          None:
        """

        p = ProteinDataBank()
        db = p.extract_attributes_from_pdb(cif_5pny_coordinate_pdb_path)

        assert db["pdb_id"] == "5PNY"
        assert db["RESOH"] == 1.48

    def test_pdb_null(self, pdb_100d_coordinate_pdb_path):
        """
        Tests the extraction of data from PDB file in which NULL is present
        for wavelength

        Args:
          pdb_100d_coordinate_pdb_path: The path to PDB file to be extracted

        Returns:
          None:
        """

        p = ProteinDataBank()
        db = p.extract_attributes_from_pdb(pdb_100d_coordinate_pdb_path)

        assert db["pdb_id"] == "100D"
        assert db["RESOH"] == 1.9
        assert db["WAVE"] is None

    def test_cif_null(self, cif_100d_coordinate_path):
        """
        Tests the extraction of data from PDB file in which NULL is present
        for wavelength

        Args:
          cif_100d_coordinate_cif_path: The path to PDBx/mmCIF file to be extracted

        Returns:
          None:
        """

        p = ProteinDataBank()
        db = p.extract_attributes_from_cif(cif_100d_coordinate_path)

        assert db["pdb_id"] == "100D"
        assert db["RESOH"] == 1.9
        assert db["WAVE"] is None
