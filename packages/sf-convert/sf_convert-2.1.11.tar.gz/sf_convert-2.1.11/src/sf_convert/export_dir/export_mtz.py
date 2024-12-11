import tempfile
import os

from sf_convert.sffile.sf_file import StructureFactorFile
import gemmi


class ExportMtz:
    def __init__(self, logger):  # pylint: disable=unused-argument
        """
        Initializes a CifToMTZConverter object.

        Args:
            cif_path (str): The path to the CIF file.
        """
        # self.__logger = logger
        self.__mappings = {
            "h_index_mapping": [["index_h", "H", "H", 0]],
            "k_index_mapping": [["index_k", "K", "H", 0]],
            "l_index_mapping": [["index_l", "L", "H", 0]],
            "status_mapping": [["status", "FREE", "I", 0, "o=1,f=0"], ["pdbx_r_free_flag", "FREE", "I", 0]],  # add more tags if needed
            "F_meas_mapping": [["F_meas_au", "FP", "F", 1], ["F_meas", "FP", "F", 1]],
            "F_sigma_mapping": [["F_meas_sigma_au", "SIGFP", "Q", 1], ["F_meas_sigma", "SIGFP", "Q", 1]],
            "F_calc_mapping": [["F_calc_au", "FC", "F", 1], ["F_calc", "FC", "F", 1]],
            "phase_calc_mapping": [["phase_calc", "PHIC", "P", 1]],
            "phase_meas_mapping": [["phase_meas", "PHIB", "P", 1]],
            "fom_mapping": [["fom", "FOM", "W", 1], ["weight", "FOM", "W", 1]],
            "intensity_meas_mapping": [["intensity_meas", "I", "J", 1], ["F_squared_meas", "I", "J", 1]],
            "intensity_sigma_mapping": [["intensity_sigma", "SIGI", "Q", 1], ["F_squared_sigma", "SIGI", "Q", 1]],
            "F_part_mapping": [["F_part_au", "FPART", "F", 1]],
            "phase_part_mapping": [["phase_part", "PHIP", "P", 1]],
            "pdbx_F_plus_mapping": [["pdbx_F_plus", "F(+)", "G", 1]],
            "pdbx_F_plus_sigma_mapping": [["pdbx_F_plus_sigma", "SIGF(+)", "L", 1]],
            "pdbx_F_minus_mapping": [["pdbx_F_minus", "F(-)", "G", 1]],
            "pdbx_F_minus_sigma_mapping": [["pdbx_F_minus_sigma", "SIGF(-)", "L", 1]],
            "pdbx_anom_difference_mapping": [["pdbx_anom_difference", "DP", "D", 1]],
            "pdbx_anom_difference_sigma_mapping": [["pdbx_anom_difference_sigma", "SIGDP", "Q", 1]],
            "pdbx_I_plus_mapping": [["pdbx_I_plus", "I(+)", "K", 1]],
            "pdbx_I_plus_sigma_mapping": [["pdbx_I_plus_sigma", "SIGI(+)", "M", 1]],
            "pdbx_I_minus_mapping": [["pdbx_I_minus", "I(-)", "K", 1]],
            "pdbx_I_minus_sigma_mapping": [["pdbx_I_minus_sigma", "SIGI(-)", "M", 1]],
            "pdbx_HL_A_iso_mapping": [["pdbx_HL_A_iso", "HLA", "A", 1]],
            "pdbx_HL_B_iso_mapping": [["pdbx_HL_B_iso", "HLB", "A", 1]],
            "pdbx_HL_C_iso_mapping": [["pdbx_HL_C_iso", "HLC", "A", 1]],
            "pdbx_HL_D_iso_mapping": [["pdbx_HL_D_iso", "HLD", "A", 1]],
            "pdbx_DELFWT_mapping": [["pdbx_DELFWT", "DELFWT", "F", 1]],
            "pdbx_DELPHWT_mapping": [["pdbx_DELPHWT", "PHDELWT", "P", 1]],
            "pdbx_FWT_mapping": [["pdbx_FWT", "FWT", "F", 1]],
            "pdbx_PHWT_mapping": [["pdbx_PHWT", "PHWT", "P", 1]],
        }
        self.__rblock = None
        self.__cv = gemmi.CifToMtz()
        self.__sf_file = None

    def __load_cif(self):
        """
        Loads the CIF file and returns the column labels.

        Returns:
            list: The column labels of the CIF file.
        """

        # write out a temporary file with first block
        blk = self.__sf_file.get_block_by_index(0)
        sftemp = StructureFactorFile()
        sftemp.add_block(blk)
        with tempfile.NamedTemporaryFile(prefix="sf_convert", delete=False) as tf:
            temp_file = tf.name

        sftemp.write_file(temp_file)

        cif_doc = gemmi.cif.read(temp_file)  # pylint: disable=no-member
        self.__rblock = gemmi.as_refln_blocks(cif_doc)[0]  # pylint: disable=unsubscriptable-object

        os.remove(temp_file)

        return self.__rblock.column_labels()

    def __determine_mappings(self):
        """
        Determines the mappings between column labels and MTZ specifications.

        Returns:
            list: The MTZ specification lines.
        """
        spec_lines = []
        column_labels = self.__rblock.column_labels()
        for _key, alternatives in self.__mappings.items():
            for alternative in alternatives:
                if alternative[0] in column_labels:
                    spec_line = " ".join([alternative[0]] + list(map(str, alternative[1:])))
                    spec_lines.append(spec_line)
                    break
        self.__cv.spec_lines = spec_lines
        return spec_lines

    def __convert_to_mtz(self, output_path):
        """
        Converts the CIF file to MTZ format and writes it to the specified output path.

        Args:
            output_path (str): The path to write the MTZ file.

        Returns:
            list: The column labels of the MTZ file.
        """
        mtz = self.__cv.convert_block_to_mtz(self.__rblock)
        mtz.write_to_file(output_path)
        return [col.label for col in mtz.columns]

    def set_sf(self, sfobj):
        """
        Sets PDBx/mmCIF SF file

        Args:
        sf: StructureFactorFile - object with data

        Returns:
        Nothing
        """
        self.__sf_file = sfobj

    def write_file(self, path_out):
        """
        Writes the output MTZ
        """
        self.__load_cif()
        self.__determine_mappings()
        self.__convert_to_mtz(path_out)
