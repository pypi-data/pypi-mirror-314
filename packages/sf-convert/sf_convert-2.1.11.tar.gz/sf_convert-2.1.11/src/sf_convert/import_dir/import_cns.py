import os

from collections import defaultdict
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from sf_convert.sffile.sf_file import StructureFactorFile as SFFile


class ImportCns:

    def __init__(self, logger):
        """Class to import CNS files - multiple supported"""
        self.__logger = logger
        self.__sf = None
        self.__free = None

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

            cns2cif = CNSToCifConverter(fpath, "xxxx", self.__logger, self.__free)
            cns2cif.import_file()

            sf = cns2cif.get_sf()

            if self.__sf:
                self.__sf.merge_sf(sf)
            else:
                self.__sf = sf

    def get_sf(self):
        return self.__sf

    def set_free(self, free):
        """Sets free R set"""
        self.__free = free


class CNSToCifConverter:
    """
    A class for converting CNS files to CIF format.

    Args:
        file_path (str): The path to the CNS file.
        pdb_id (str): The PDB ID.
        logger (Logger): The logger object.
        FREERV (int, optional): The FREERV value. Defaults to None.
    """

    def __init__(self, file_path, pdb_id, logger, FREERV=None):

        if FREERV:
            self.__FREERV = int(FREERV)
        else:
            self.__FREERV = FREERV
        self.__pdb_id = pdb_id
        self.__file_path = file_path
        self.__h_values = []
        self.__k_values = []
        self.__l_values = []
        self.__values = defaultdict(list)
        self.__curContainer = DataContainer(self.__pdb_id)
        self.__pinfo_value = 0
        self.__logger = logger
        self.__sffile = None

    def import_file(self):
        self.process_file()
        self.rename_keys()
        self.create_data_categories()

        self.__sffile = SFFile()
        self.__sffile.add_block(self.__curContainer)
        self.__sffile.correct_block_names(self.__pdb_id)

    def __process_line(self, line):
        """
        Process a line from the CNS file.

        Args:
            line (str): The line to process.
        """
        words = line.split()
        if len(words) < 4:
            return
        try:
            h = int(words[1])
            k = int(words[2])
            l = int(words[3])  # noqa: E741
        except ValueError:
            return
        self.__h_values.append(h)
        self.__k_values.append(k)
        self.__l_values.append(l)
        current_key = None
        for word in words[4:]:
            if current_key is None and word.endswith("="):
                current_key = word[:-1]
            elif current_key is not None:
                try:
                    self.__values[current_key].append(float(word))
                except ValueError:
                    self.__values[current_key].append(word)
                current_key = None

    def __process_status_line(self, line):
        """
        Process a status line from the CNS file.

        Args:
            line (str): The status line to process.
        """
        if "INDE" in line:
            ffg = 0
            if "TEST" in line or "FREE" in line:
                if "TEST=" in line:
                    ffg = int(line.split("TEST=")[1].split()[0])
                elif "TEST" in line:
                    ffg = int(line.split("TEST")[1].split()[0])
                elif "FREE=" in line:
                    ffg = int(line.split("FREE=")[1].split()[0])
                elif "FREE " in line:
                    ffg = int(line.split("FREE ")[1].split()[0])
                if self.__FREERV:
                    self.__values["status"].append("f" if ffg == int(self.__FREERV) else "o")
                else:
                    self.__values["status"].append("f" if ffg == 1 else "o")

    def __rename_keys_complete(self):
        """
        Rename the keys in the values dictionary.

        Returns:
            dict: The renamed values dictionary.
        """
        rename_dict = {
            "FOBS": "F_meas_au",
            "FP": "F_meas_au",
            "SIGMA": "F_meas_sigma_au",
            "SIGFP": "F_meas_sigma_au",
            "TEST": "status",
            "FREE": "status",
            "IOBS": "intensity_meas",
            "I": "intensity_meas",
            "SIGI": "intensity_sigma",
            "PHIB": "phase_meas",
            "PHIC": "phase_calc",
            "FOM": "fom",
            "FC": "F_calc_au",
            "HLA": "pdbx_HLA",
            "HLB": "pdbx_HLB",
            "HLC": "pdbx_HLC",
            "HLD": "pdbx_HLD",
        }
        new_values = defaultdict(list)
        for key in self.__values:
            new_key = rename_dict.get(key, key)
            new_values[new_key] = self.__values[key]
        return new_values

    def process_file(self):
        """
        Process the CNS file.
        """
        with open(self.__file_path, "r") as file:
            for line in file:
                self.__process_line(line)
                self.__process_status_line(line)

    def rename_keys(self):
        """
        Rename the keys in the values dictionary.
        """
        self.__values = self.__rename_keys_complete()
        # Not needed here - as conversion already happened
        # self.__values['status'] = ['o' if v == 0 else 'f' for v in self.__values['status']]

    def create_data_categories(self):
        """
        Create the data categories for the CIF file.
        """
        aCat = DataCategory("audit")
        aCat.appendAttribute("revision_id")
        aCat.appendAttribute("creation_date")
        aCat.appendAttribute("update_record")
        aCat.append(["1_0", "?", "Initial release"])
        self.__curContainer.append(aCat)
        self.__logger.pinfo(f"Note: file {self.__file_path} has no _audit. (auto added)", self.__pinfo_value)

        bCat = DataCategory("diffrn_radiation_wavelength")
        bCat.appendAttribute("id")
        bCat.appendAttribute("wavelength")
        bCat.append(["1", "."])
        self.__curContainer.append(bCat)
        self.__logger.pinfo("Warning: No wavelength value was found in SF file", self.__pinfo_value)

        cCat = DataCategory("entry")
        cCat.appendAttribute("id")
        cCat.append(["xxxx"])
        self.__curContainer.append(cCat)

        dCat = DataCategory("exptl_crystal")
        dCat.appendAttribute("id")
        dCat.append(["1"])
        self.__curContainer.append(dCat)

        eCat = DataCategory("reflns_scale")
        eCat.appendAttribute("group_code")
        eCat.append(["1"])
        self.__curContainer.append(eCat)

        fCat = DataCategory("refln")
        fCat.appendAttribute("crystal_id")
        fCat.appendAttribute("wavelength_id")
        fCat.appendAttribute("scale_group_code")
        fCat.appendAttribute("index_h")
        fCat.appendAttribute("index_k")
        fCat.appendAttribute("index_l")

        # Preference order.... status F_meas_au F_meas_sigma_au, pdbx_HL_A, ....
        pref = [
            "status",
            "F_meas_au",
            "F_meas_sigma_au",
            "intensity_meas",
            "intensity_sigma",
            "phase_meas",
            "phase_calc",
            "fom",
            "F_calc_au",
            "pdbx_HLA",
            "pdbx_HLB",
            "pdbx_HLC",
            "pdbx_HLD",
        ]
        cur_key = {}
        for key in self.__values.keys():
            cur_key[key] = 1

        ordered_keys = []
        for p in pref:
            if p in cur_key:
                ordered_keys.append(p)
                del cur_key[p]

        for key in cur_key.keys():
            ordered_keys.append(key)

        for key in ordered_keys:
            fCat.appendAttribute(key)
        for i in range(len(self.__h_values)):
            values_to_append = (1, 1, 1, self.__h_values[i], self.__k_values[i], self.__l_values[i])
            for key in ordered_keys:
                values_to_append += (self.__values[key][i],)
            fCat.append(values_to_append)
        self.__curContainer.append(fCat)

    def get_sf(self):
        return self.__sffile
