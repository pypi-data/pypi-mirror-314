import gemmi
import os
from mmcif.api.DataCategory import DataCategory
import tempfile
from sf_convert.sffile.sf_file import StructureFactorFile as SFFile


class ImportMtz:
    def __init__(self, logger):
        """Class to import MTZ files - multiple supported"""
        self.__logger = logger
        self.__sf = None
        self.__free = None
        self.__label = None

    def import_files(self, fileList):
        """Reads in possibly multiple SF files


        Args:
            fileList (list): List of file names

        Returns:
             StructureFile object
        """

        # If multiple labels, handle separately
        if self.__have_multi_label():
            self.__import_files_multi_label(fileList)
            return

        for fpath in fileList:
            if not os.path.exists(fpath):
                self.__logger.pinfo(f"File {fpath} does not exist", 0)
                self.__sf = None
                return None

            mtz2cif = MtzToCifConverter(fpath, self.__logger)
            if self.__label:
                mtz2cif.process_labels(self.__label)

            if self.__free:
                mtz2cif.set_free(self.__free)

            mtz2cif.convert()
            sf = mtz2cif.get_sf()

            if self.__sf:
                self.__sf.merge_sf(sf)
            else:
                self.__sf = sf

    def __import_files_multi_label(self, fileList):
        """Process a single file with multiple label configuration

        Args:
            fileList (list): List of file names

        Returns:
             StructureFile object
        """

        if len(fileList) > 1:
            self.__logger.pinfo("Error: When using labels, only a single file can be used", 0)
            self.__sf = None
            return None

        fpath = fileList[0]
        if not os.path.exists(fpath):
            self.__logger.pinfo(f"File {fpath} does not exist", 0)
            self.__sf = None
            return None

        for idx, label in enumerate(self.__label.split(":")):
            self.__logger.pinfo(f"Processing datablock {idx + 1}", 0)

            mtz2cif = MtzToCifConverter(fpath, self.__logger)
            if label:
                mtz2cif.process_labels(label)

            if self.__free:
                mtz2cif.set_free(self.__free)

            mtz2cif.convert()
            sf = mtz2cif.get_sf()

            if self.__sf:
                self.__sf.merge_sf(sf)
            else:
                self.__sf = sf

    def get_sf(self):
        return self.__sf

    def set_free(self, free):
        """Sets free R set"""
        self.__free = free

    def set_labels(self, label):
        """Sets free R set"""
        self.__label = label

    def __have_multi_label(self):
        """Returns True if multiple datasets present in labels - i.e. with a ":" character"""
        if self.__label and ":" in self.__label:
            return True
        else:
            return False


class MtzToCifConverter:
    def __init__(self, mtz_file_path, logger):
        """
        Initializes the MtzToCifConverter object.

        Args:
            mtz_file_path (str): The path to the input MTZ file.
            output_file_path (str): The path to the output CIF file.
            pdb_id (str): The PDB ID.
            logger (Logger): The logger object for logging messages.
        """
        self.__pinfo_value = 0
        self.mtz_file_path = mtz_file_path
        self.mtz2cif = gemmi.MtzToCif()
        # Turn off comments in case ISO-8859 in history
        self.mtz2cif.with_comments = False
        self.mtz2cif.with_history = False

        self.sffile = SFFile()
        self.__logger = logger
        self.__assigned_labels = set()  # List of labels already assigned
        self.__categories = {
            "audit": {"revision_id": "1_0", "creation_date": "?", "update_record": "Initial release"},
            "exptl_crystal": {"id": "1"},
            "reflns_scale": {"group_code": "1"},
        }
        self.__logger.pinfo(f"Note: file {self.mtz_file_path} has no _audit. (auto added)", self.__pinfo_value)

        # This is used when depositor specifies labels
        self.__labels = [
            ("H", "H", "index_h"),
            ("K", "H", "index_k"),
            ("L", "H", "index_l"),
            ("?", "FREE", "I", "status", "S"),
            ("?", "RFREE", "I", "status", "S"),
            ("?", "FREER", "I", "status", "S"),
            ("?", "FreeR_flag", "I", "status", "S"),
            ("?", "R-free-flags", "I", "status", "S"),
            ("?", "FreeRflag", "I", "status", "S"),
            ("FreeR_flag", "I", "pdbx_r_free_flag"),
            ("F_XDSdataset", "F", "F_meas_au"),
            ("SIGF_XDSdataset", "Q", "F_meas_sigma_au"),
            ("?", "FC", "F", "F_calc_au"),
            ("?", "PHIC", "P", "phase_calc"),
            ("?", "PHIB", "P", "phase_meas"),
            ("?", "FWT", "F", "pdbx_FWT"),
            ("?", "2FOFCWT", "F", "pdbx_FWT"),
            ("&", "PHWT", "P", "pdbx_PHWT", ".3f"),
            ("&", "PH2FOFCWT", "P", "pdbx_PHWT", ".3f"),
            ("?", "DELFWT", "F", "pdbx_DELFWT"),
            ("?", "FOFCWT", "F", "pdbx_DELFWT"),
            ("&", "DELPHWT", "P", "pdbx_DELPHWT", ".3f"),
            ("&", "PHDELWT", "P", "pdbx_DELPHWT", ".3f"),
            ("&", "PHFOFCWT", "P", "pdbx_DELPHWT", ".3f"),
            ("?", "IMEAN", "J", "intensity_meas"),
            ("?", "I", "J", "intensity_meas"),
            ("?", "IOBS", "J", "intensity_meas"),
            ("?", "I-obs", "J", "intensity_meas"),
            ("&", "SIGIMEAN", "Q", "intensity_sigma"),
            ("&", "SIGI", "Q", "intensity_sigma"),
            ("&", "SIGIOBS", "Q", "intensity_sigma"),
            ("&", "SIGI-obs", "Q", "intensity_sigma"),
            ("?", "I(+)", "K", "pdbx_I_plus"),
            ("?", "IOBS(+)", "K", "pdbx_I_plus"),
            ("?", "I-obs(+)", "K", "pdbx_I_plus"),
            ("&", "SIGI(+)", "M", "pdbx_I_plus_sigma"),
            ("&", "SIGIOBS(+)", "M", "pdbx_I_plus_sigma"),
            ("&", "SIGI-obs(+)", "M", "pdbx_I_plus_sigma"),
            ("?", "I(-)", "K", "pdbx_I_minus"),
            ("?", "IOBS(-)", "K", "pdbx_I_minus"),
            ("?", "I-obs(-)", "K", "pdbx_I_minus"),
            ("&", "SIGI(-)", "M", "pdbx_I_minus_sigma"),
            ("&", "SIGIOBS(-)", "M", "pdbx_I_minus_sigma"),
            ("&", "SIGI-obs(-)", "M", "pdbx_I_minus_sigma"),
            ("?", "F", "F", "F_meas_au"),
            ("?", "FP", "F", "F_meas_au"),
            ("?", "FOBS", "F", "F_meas_au"),
            ("?", "F-obs", "F", "F_meas_au"),
            ("&", "SIGF", "Q", "F_meas_sigma_au"),
            ("&", "SIGFP", "Q", "F_meas_sigma_au"),
            ("&", "SIGFOBS", "Q", "F_meas_sigma_au"),
            ("&", "SIGF-obs", "Q", "F_meas_sigma_au"),
            ("?", "F(+)", "G", "pdbx_F_plus"),
            ("?", "FOBS(+)", "G", "pdbx_F_plus"),
            ("?", "F-obs(+)", "G", "pdbx_F_plus"),
            ("&", "SIGF(+)", "L", "pdbx_F_plus_sigma"),
            ("&", "SIGFOBS(+)", "L", "pdbx_F_plus_sigma"),
            ("&", "SIGF-obs(+)", "L", "pdbx_F_plus_sigma"),
            ("?", "F(-)", "G", "pdbx_F_minus"),
            ("?", "FOBS(-)", "G", "pdbx_F_minus"),
            ("?", "F-obs(-)", "G", "pdbx_F_minus"),
            ("&", "SIGF(-)", "L", "pdbx_F_minus_sigma"),
            ("&", "SIGFOBS(-)", "L", "pdbx_F_minus_sigma"),
            ("&", "SIGF-obs(-)", "L", "pdbx_F_minus_sigma"),
            ("?", "DP", "D", "pdbx_anom_difference"),
            ("&", "SIGDP", "Q", "pdbx_anom_difference_sigma"),
            ("?", "FOM", "W", "fom"),
            ("?", "HLA", "A", "pdbx_HL_A_iso"),
            ("&", "HLB", "A", "pdbx_HL_B_iso"),
            ("&", "HLC", "A", "pdbx_HL_C_iso"),
            ("&", "HLD", "A", "pdbx_HL_D_iso"),
        ]

        self.__CUSTOM_END = [("? FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag", "I", "status", "S")]

        self.__spec_file_content = []

    def set_spec(self):
        """
        Sets the spec lines for the MtzToCif object.
        """
        spec_lines = ["\t".join(line) for line in self.__spec_file_content]
        self.mtz2cif.spec_lines = spec_lines

    def set_free(self, free):
        """
        Sets the free R value for the MtzToCif object.
        """
        self.mtz2cif.free_flag_value = free

    def convert_mtz_to_cif(self):
        """
        Converts the MTZ file to CIF format.

        Returns:
            str: The CIF document.
        """
        mtz = gemmi.read_mtz_file(self.mtz_file_path)
        return self.mtz2cif.write_cif_to_string(mtz)

    def __read_cif_file(self, cif_file):
        """
        Reads the CIF file.

        Args:
            cif_file (str): The path to the CIF file.
        """
        self.sffile.read_file(cif_file)

    def __add_category(self, categories):
        """
        Adds the specified categories to the CIF file.

        Args:
            categories (dict): A dictionary containing the category names and their attributes.
        """
        for category_name, data_dict in categories.items():
            category = DataCategory(category_name)
            for key in data_dict.keys():
                category.appendAttribute(key)
            category.append(tuple(data_dict.values()))
            self.sffile.append_category_to_block(category)

    def __fix_attributes(self):
        """If gemmi decids unmerged data, we provide wrong attribute name due to template we provide"""
        for idx in range(self.sffile.get_number_of_blocks()):
            blk = self.sffile.get_block_by_index(idx)

            if "diffrn_refln" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("diffrn_refln")
            if "intensity_meas" in cObj.getAttributeList():
                cObj.renameAttributes({"intensity_meas": "intensity_net"})

    def process_labels(self, input_string):
        """
        Processes the labels based on the input string.

        Args:
            input_string (str): The input string containing the key-value pairs.

        Returns:
            None
        """
        # Remove commas
        lstr = input_string.replace(",", " ")
        # Get rid of multiple spaces
        lstr = " ".join(lstr.split())
        key_value_pairs = lstr.split(" ")
        key_value_dict = {pair.split("=")[0]: pair.split("=")[1] for pair in key_value_pairs}

        processed_labels = []

        for label in self.__labels:
            if label[0] in ["?", "&"] and label[1] in key_value_dict.keys():
                replaced_label = (label[0], key_value_dict[label[1]], label[2], label[3])
                if len(label) == 5:
                    processed_label = (f"{replaced_label[0]} {replaced_label[1]}", *replaced_label[2:], label[4]) if replaced_label[0] in ["?", "&"] else replaced_label
                else:
                    processed_label = (f"{replaced_label[0]} {replaced_label[1]}", *replaced_label[2:]) if replaced_label[0] in ["?", "&"] else replaced_label
                processed_labels.append(processed_label)
            elif label[0] in key_value_dict.keys():
                replaced_label = (key_value_dict[label[0]], label[1], *label[2:])
                processed_label = replaced_label
                processed_labels.append(processed_label)

        self.__spec_file_content = processed_labels

    def __assign_label(self, desired_label):
        """
        Assigns a label to a desired label.

        Args:
            desired_label (str): The desired label.

        Returns:
            str: The assigned label.
        """
        if desired_label not in self.__assigned_labels:
            self.__assigned_labels.add(desired_label)
            return desired_label
        return "Unknown Label"

    def __generate_full_label(self, i, labels_list):
        """
        Generates the full label based on the label type and content.

        Args:
            i (int): The index of the label in the labels list.
            labels_list (list): The list of labels.

        Returns:
            str: The generated full label.
        """
        label_type, label_content = labels_list[i]

        # Direct mappings
        if label_type == "H" and label_content in ["H", "K", "L"]:
            return self.__assign_label(f"index_{label_content.lower()}")
        elif label_type == "F" and label_content in ["2FOFCWT", "FWT", "F_ampl"]:
            return self.__assign_label("pdbx_FWT")
        elif label_type == "P" and label_content in ["PH2FOFCWT", "PHWT", "PHIF"]:
            return self.__assign_label("pdbx_PHWT")
        elif label_content in ["FOFCWT", "DELFWT"]:
            return self.__assign_label("pdbx_DELFWT")
        elif label_type == "P" and label_content in ["PHFOFCWT", "PHDELWT"]:
            return self.__assign_label("pdbx_DELPHWT")
        elif label_type == "I" and any(
            term.lower() in label_content.lower() for term in ["free", "R-free-flag", "flag", "TEST", "FREE", "RFREE", "FREER", "FreeR_flag", "FreeRflag"]
        ):  # FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag
            return self.__assign_label("pdbx_r_free_flag")

        # Unusual R flag for free R
        elif label_type == "R" and any(
            term.lower() in label_content.lower() for term in ["free", "R-free-flag", "flag", "TEST", "FREE", "RFREE", "FREER", "FreeR_flag", "FreeRflag"]
        ):  # FREE|RFREE|FREER|FreeR_flag|R-free-flags|FreeRflag
            return self.__assign_label("pdbx_r_free_flag")
        elif label_type == "D":
            return self.__assign_label("pdbx_anom_difference")
        elif label_type == "A":
            if "HLA" in label_content.upper():
                return self.__assign_label("pdbx_HL_A_iso")
            elif "HLB" in label_content.upper():
                return self.__assign_label("pdbx_HL_B_iso")
            elif "HLC" in label_content.upper():
                return self.__assign_label("pdbx_HL_C_iso")
            elif "HLD" in label_content.upper():
                return self.__assign_label("pdbx_HL_D_iso")
        elif label_type == "W" and "FOM" in label_content.upper():
            return self.__assign_label("fom")

        # Conditional checks based on label content and type of the previous or next label
        if label_type == "F":
            if label_content.upper() in ["FP", "F-OBS-FILTERED", "F-OBS"] or (i < len(labels_list) - 1 and labels_list[i + 1][0] == "Q"):
                return self.__assign_label("F_meas_au")
            elif label_content.upper() in ["FC", "FCAL"]:
                return self.__assign_label("F_calc_au")
        elif label_type == "Q":
            if i > 0:
                prev_label_type = labels_list[i - 1][0]
                if prev_label_type == "F":
                    return self.__assign_label("F_meas_sigma_au")
                elif prev_label_type == "J":
                    return self.__assign_label("intensity_sigma")
                elif prev_label_type == "D":
                    return self.__assign_label("pdbx_anom_difference_sigma")

        # Conditional checks for labels that depend on label content alone
        if label_type == "J":
            return self.__assign_label("intensity_meas")
        elif label_type == "G":
            if "(+)" in label_content:
                return self.__assign_label("pdbx_F_plus")
            elif "(-)" in label_content:
                return self.__assign_label("pdbx_F_minus")
        elif label_type == "L":
            if "(+)" in label_content:
                return self.__assign_label("pdbx_F_plus_sigma")
            elif "(-)" in label_content:
                return self.__assign_label("pdbx_F_minus_sigma")
        elif label_type == "K":
            if "(+)" in label_content:
                return self.__assign_label("pdbx_I_plus")
            elif "(-)" in label_content:
                return self.__assign_label("pdbx_I_minus")
        elif label_type == "M":
            if "(+)" in label_content:
                return self.__assign_label("pdbx_I_plus_sigma")
            elif "(-)" in label_content:
                return self.__assign_label("pdbx_I_minus_sigma")
        elif label_type == "P":
            if "PHIC" in label_content or "PHIC_ALL" in label_content or "AC" in label_content:
                return self.__assign_label("phase_calc")
            elif "PHIB" in label_content or "PHIM" in label_content:
                return self.__assign_label("phase_meas")

        return "Unknown Label"

    def __generate_full_labels_for_list(self, labels_list):
        """
        Generates the full labels for a list of labels.

        Args:
            labels_list (list): The list of labels.

        Returns:
            list: The list of generated full labels.
        """
        results = []

        # We pull out the "Standard" test flags first - before going through the list. Otherwise first come first server, and SA_flag is mistaken for free
        # set
        free_label = -1

        for i in range(len(labels_list)):
            label_type, label_content = labels_list[i]
            if label_type == "I" and label_content in ["free", "R-free-flag", "flag", "TEST", "FREE", "RFREE", "FREER", "FreeR_flag", "FreeRflag"]:
                free_label = i
                # Mark as used so will not be picked up by another
                self.__assign_label("pdbx_r_free_flag")
                break

        for i in range(len(labels_list)):
            if i != free_label:
                generated_label = self.__generate_full_label(i, labels_list)
            else:
                generated_label = "pdbx_r_free_flag"
            results.append((labels_list[i][0], labels_list[i][1], generated_label))
            if generated_label == "pdbx_r_free_flag":
                self.__CUSTOM_END = []
                self.__CUSTOM_END.append((labels_list[i][1], labels_list[i][0], "status", "S"))
        return results

    def __get_mtz_columns_with_custom_entries(self, mtz_file):
        """
        Gets the MTZ columns with custom entries.

        Args:
            mtz_file (str): The path to the MTZ file.

        Returns:
            list: The list of MTZ columns with custom entries.
        """
        mtz = gemmi.read_mtz_file(mtz_file)
        labels_list = [(column.type, column.label) for column in mtz.columns]
        results = self.__generate_full_labels_for_list(labels_list)
        filtered_results = [(type_, label, full_label) for label, type_, full_label in results if full_label != "Unknown Label"]
        return filtered_results + self.__CUSTOM_END

    def convert(self):
        """
        Converts the MTZ file to CIF format and writes it to the output file.
        """
        with tempfile.NamedTemporaryFile(prefix="sf_convert", delete=False) as tf:
            temp_file = tf.name

        # If -label option is given, the speci_file_content is set.
        if len(self.__spec_file_content) == 0:
            spec_lines_result = self.__get_mtz_columns_with_custom_entries(self.mtz_file_path)
            self.__spec_file_content = spec_lines_result

        self.set_spec()
        cif_doc = self.convert_mtz_to_cif()
        with open(temp_file, "w") as f:
            f.write(cif_doc)
        self.__read_cif_file(temp_file)
        os.remove(temp_file)
        self.__add_category(self.__categories)

        self.__fix_attributes()

        new_order = ["audit", "cell", "diffrn_radiation_wavelength", "entry", "exptl_crystal", "reflns_scale", "symmetry", "refln", "diffrn_refln"]
        self.sffile.reorder_categories_in_block(new_order)
        self.sffile.correct_block_names("xxxx")  # XXXX assumes entry.id = xxxx - need to be able to specify pdb id

    def get_sf(self):
        return self.sffile
