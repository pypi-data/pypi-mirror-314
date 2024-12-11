import re

from mmcif.io.IoAdapterCore import IoAdapterCore


class ProteinDataBank:
    def extract_attributes_from_cif(self, sffile):
        """
        Extracts attributes from a CIF file and updates the ProteinDataBank object.

        Args:
            sffile (str): Path to PDBx/mmCIF file

        Returns:
            dict: A dictionary containing the extracted attributes.
        """
        io = IoAdapterCore()
        cl = io.readFile(sffile)
        if cl is None:
            return {}

        container = cl[0]
        attributes = self._get_cif_attributes(container)

        # Group cell parameters together
        attributes["CELL"] = [attributes.pop(key) for key in ["CELL_a", "CELL_b", "CELL_c", "CELL_alpha", "CELL_beta", "CELL_gamma"] if key in attributes]

        return attributes

    def _get_cif_attributes(self, container):
        """
        Extracts attributes from a CIF container.

        Args:
            container (DataContainer): The DataContainer object containing the CIF data.

        Returns:
            dict: A dictionary containing the extracted attributes.
        """
        cif_attributes = {
            # 'entry': [('id', 'pdb_id')],
            "reflns": [("d_resolution_high", "RESOH"), ("d_resolution_low", "RESOL"), ("free_R_factor", "FREERV")],
            "diffrn_radiation_wavelength": [("wavelength", "WAVE")],
            "pdbx_refine": [("free_R_val_test_set_ct_no_cutoff", "NFREE")],
            "cell": [
                ("length_a", "CELL_a"),
                ("length_b", "CELL_b"),
                ("length_c", "CELL_c"),
                ("angle_alpha", "CELL_alpha"),
                ("angle_beta", "CELL_beta"),
                ("angle_gamma", "CELL_gamma"),
            ],
            "symmetry": [("space_group_name_H-M", "SYMM")],
        }

        attributes = {}

        for obj_name, attrs in cif_attributes.items():
            obj = container.getObj(obj_name)
            if obj is not None:
                for attr, output_name in attrs:
                    store = None
                    if obj.hasAttribute(attr):
                        val = obj.getValue(attr)
                        if val not in [".", "?"]:
                            store = float(val) if val.replace(".", "", 1).isdigit() else val
                    attributes[output_name] = store
            else:
                for attr, output_name in attrs:
                    attributes[output_name] = None

        # Extract entry from database_2
        pdb_id = None

        cobj = container.getObj("database_2")
        if cobj is not None:
            for row in range(obj.getRowCount()):
                dbid = cobj.getValue("database_id", row)
                if dbid == "PDB":
                    pdb_id = cobj.getValue("database_code", row)
                    break  # Do not allow check in subsequent loops for NDB

                # Fallback for NDB
                if dbid == "NDB":
                    pdb_id = cobj.getValue("database_code", row)
                    # Do not break - if PDB comes after it will override

        attributes["pdb_id"] = pdb_id

        return attributes

    def extract_attributes_from_pdb(self, filename):
        """
        Extracts attributes from a PDB file and updates the ProteinDataBank object.

        Args:
            filename (str): The path to the PDB file.

        Returns:
            dict: A dictionary containing the extracted attributes.
        """
        attributes = self._get_pdb_attributes(filename)

        return attributes

    def _get_pdb_attributes(self, filename):
        """
        Extracts attributes from a PDB file.

        Args:
            filename (str): The path to the PDB file.

        Returns:
            dict: A dictionary containing the extracted attributes.
        """
        pdb_id = wave = nfree = resoh = resol = freerv = symm = None
        cell = [None] * 6

        with open(filename, "r") as file:
            for line in file:
                if line.startswith("HEADER"):
                    pdb_id = line[61:66].strip()

                elif "REMARK 200  WAVELENGTH OR RANGE        (A) :" in line:
                    wave = self._extract_float(line)

                elif "FREE R VALUE TEST SET COUNT   (NO CUTOFF)" in line:
                    nfree = self._extract_int(line)

                elif "RESOLUTION RANGE HIGH (ANGSTROMS)" in line:
                    resoh = self._extract_float(line)

                elif "RESOLUTION RANGE LOW  (ANGSTROMS)" in line:
                    resol = self._extract_float(line)

                elif "REMARK   test_flag_value:" in line and freerv is None:
                    freerv = line.split(":")[1].strip()

                elif line.startswith("CRYST1"):
                    cell = self._extract_cell_parameters(line)
                    symm = line[55:66].strip()

        return {"pdb_id": pdb_id, "RESOH": resoh, "RESOL": resol, "FREERV": freerv, "WAVE": wave, "NFREE": nfree, "SYMM": symm, "CELL": cell}

    def _extract_float(self, line):
        """
        Extracts a float value from a line of text.

        Args:
            line (str): The line of text.

        Returns:
            float: The extracted float value.
        """
        value = line.split(":")[1]
        search = re.search(r"[-+]?\d*\.\d+|\d+", value)

        ret = None
        if search:
            try:
                ret = float(search.group())
            except ValueError:
                pass

        return ret

    def _extract_int(self, line):
        """
        Extracts an integer value from a line of text.

        Args:
            line (str): The line of text.

        Returns:
            int: The extracted integer value.
        """
        value = line.split(":")[1]
        search = re.search(r"\d+", value)

        ret = None
        if search:
            try:
                ret = int(search.group())
            except ValueError:
                pass

        return ret

    def _extract_cell_parameters(self, line):
        """
        Extracts the cell parameters from a line of text.

        Args:
            line (str): The line of text.

        Returns:
            list: A list containing the extracted cell parameters.
        """
        cell_values = line[6:].split()[:6]
        return [float(val) for val in cell_values]

    # def update_FREERV(self, new_freerv):
    #     """
    #     Updates the FREERV attribute with a new value.

    #     Args:
    #         new_freerv: The new value for FREERV.
    #     """
    #     self.FREERV = new_freerv

    # def update_WAVE(self, new_wave):
    #     """
    #     Updates the WAVE attribute with a new value.

    #     Args:
    #         new_wave: The new value for WAVE.
    #     """
    #     self.WAVE = new_wave
