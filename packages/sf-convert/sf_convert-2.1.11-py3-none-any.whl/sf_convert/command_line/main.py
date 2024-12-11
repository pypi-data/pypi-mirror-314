import argparse
import traceback
import os
import re
import sys

from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.sffile.get_items_pdb import ProteinDataBank
from sf_convert.import_dir.import_mtz import ImportMtz
from sf_convert.import_dir.import_cif import ImportCif
from sf_convert.import_dir.import_cns import ImportCns
from sf_convert.export_dir.export_cns import ExportCns
from sf_convert.export_dir.export_mtz import ExportMtz
from sf_convert.export_dir.export_cif import ExportCif
from sf_convert.sffile.guess_sf_format import guess_sf_format
from sf_convert.utils.reformat_sfhead import reformat_sfhead, fix_entry_ids
from sf_convert.utils.sf_correct import SfCorrect
from sf_convert.utils.pinfo_file import PStreamLogger
from sf_convert.utils.CheckSfFile import CheckSfFile
from sf_convert.utils.version import get_version
from sf_convert.utils.TextUtils import is_cif

VALID_FORMATS = ["CNS", "MTZ", "MMCIF", "CIF"]


class ImportSf:
    """Class to import and possibly make corrections"""

    def __init__(self, logger):
        self.__logger = logger
        self.__legacy = True  # old sf_convert behaviour

    def import_sf(self, pdict):
        """Imports structures as needed.
        Returns StructureeFile class object"""

        format_in = pdict["inp_format"].lower()

        sf = None
        if format_in in ["mmcif", "cif"]:
            sf = self.__import_mmcif(pdict)
        elif format_in == "cns":
            sf = self.__import_cns(pdict)
        elif format_in == "mtz":
            sf = self.__import_mtz(pdict)
        else:
            print("Internal error type unknown")
            sys.exit(1)

        return sf

    def __import_mmcif(self, pdict):
        sfin = pdict["sfin"]
        format_out = pdict["out_format"]
        pdb_data = pdict.get("pdb_data", {})
        pdb_wave = pdb_data.get("WAVE", None)
        pdb_symm = pdb_data.get("SYMM", None)
        wave_arg = pdict.get("wave_cmdline", None)
        free_arg = pdict.get("free", None)
        pdb_cell = pdb_data.get("CELL", None)
        pdb_id_cmd = pdict.get("pdb_id", None)

        ic = ImportCif(self.__logger)
        ic.import_files(sfin)
        sffile = ic.get_sf()

        # We apply corrections if cif -> cif conversion, otherwise bring in
        sfc = SfCorrect(self.__logger, self.__legacy)
        if format_out == "MMCIF":

            # Warn about bad names
            sfc.check_unwanted_cif_items(sffile)

            # Remove blocks with too few reflections.
            sfc.remove_empty_blocks(sffile)

            # PDB id comes from
            #  sffile block name - unless coordinate file used - and then use that
            pdbid = pdb_data.get("pdb_id", None)

            if not pdbid:
                pdbid = sfc.get_pdbid(sffile)  # XXX should be a utility function somewhere else

            # Command line trumps
            if pdb_id_cmd:
                pdbid = pdb_id_cmd

            if pdbid:
                pdbid = pdbid.lower()

            # Logic:
            #  If command line - then use
            #  If SF file has and model file - use model file and warn
            #  If SF has - leave alone
            #  Else write empty

            setwlarg = None
            if wave_arg:
                setwlarg = wave_arg
            elif pdb_wave not in [".", "?", None]:
                setwlarg = pdb_wave

            if pdb_cell:
                sfc.set_cell_if_missing(sffile, pdbid, pdb_cell)

            # We take symmetry from model if not set
            if pdb_symm:
                sfc.set_space_group_if_missing(sffile, pdbid, pdb_symm)

            sfc.annotate_wavelength(sffile, pdbid, setwlarg)

            sfc.handle_standard(sffile, pdbid)

        # If set free...
        if free_arg is not None:
            sfc.reassign_free(sffile, free_arg)

        return sffile

    def __import_mtz(self, pdict):
        sfin = pdict["sfin"]
        pdb_data = pdict.get("pdb_data", {})
        pdb_id_cmd = pdict.get("pdb_id", None)
        sfc = SfCorrect(self.__logger, self.__legacy)

        # pdb_wave = pdb_data.get("WAVE", None)
        # wave_arg = pdict.get("wave_cmdline", None)

        converter = ImportMtz(self.__logger)

        if pdict.get("label", None):
            converter.set_labels(pdict["label"])

        free = pdict.get("free", None)
        if free:
            converter.set_free(free)

        converter.import_files(sfin)

        sffile = converter.get_sf()

        # PDB id comes from
        #  sffile block name - unless coordinate file used - and then use that

        # Command line trumps
        if pdb_id_cmd:
            pdbid = pdb_id_cmd
        else:
            pdbid = pdb_data.get("pdb_id", None)

            if not pdbid:
                pdbid = sfc.get_pdbid(sffile)  # XXX should be a utility function somewhere else

        if pdbid:
            pdbid = pdbid.lower()

        sfc.correct_cell_precision(sffile)
        sfc.handle_standard(sffile, pdbid)

        return sffile

    def __import_cns(self, pdict):
        sfin = pdict["sfin"]
        pdb_data = pdict.get("pdb_data", {})
        # pdb_wave = pdb_data.get("WAVE", None)
        pdb_symm = pdb_data.get("SYMM", None)
        pdb_cell = pdb_data.get("CELL", None)
        # wave_arg = pdict.get("wave_cmdline", None)
        pdb_id_cmd = pdict.get("pdb_id", None)
        free = pdict.get("free", None)

        ic = ImportCns(self.__logger)
        ic.set_free(free)
        ic.import_files(sfin)
        sffile = ic.get_sf()

        if pdb_id_cmd:
            pdbid = pdb_id_cmd
        else:
            pdbid = "xxxx"

        sfc = SfCorrect(self.__logger, self.__legacy)
        if pdb_cell:
            sfc.set_cell(sffile, pdb_cell)

        if pdb_symm:
            sfc.set_space_group_if_missing(sffile, pdbid, pdb_symm)

        sfc.ensure_catkeys(sffile, pdbid)
        sfc.reorder_sf_file(sffile)

        # Remove duplicate audits for multiple imports
        sfc.cleanup_extra_audit(sffile)

        # PDB id comes from
        #  sffile block name - unless coordinate file used - and then use that
        pdbid = pdb_data.get("pdb_id", None)

        if pdbid:
            pdbid = pdbid.lower()
            fix_entry_ids(sffile, pdbid)
            sffile.correct_block_names(pdbid)

        return sffile


class ExportSf:
    """Class to import and possibly make corrections"""

    def __init__(self, logger):
        self.__logger = logger
        self.__legacy = True  # old sf_convert behaviour

    def export_sf(self, sffile, pdict):
        """Exports structures as needed."""

        format_out = pdict["out_format"].lower()

        if format_out in ["mmcif", "cif"]:
            self.__export_mmcif(sffile, pdict)
        elif format_out == "cns":
            self.__export_cns(sffile, pdict)
        elif format_out == "mtz":
            self.__export_mtz(sffile, pdict)
        else:
            print("Internal error type unknown", format_out)
            sys.exit(1)

    def __export_mmcif(self, sffile, pdict):
        output = pdict["output"]

        ec = ExportCif(self.__legacy)
        ec.set_sf(sffile)
        ec.write_file(output)

    def __export_cns(self, sffile, pdict):
        output = pdict["output"]

        CNSexport = ExportCns(self.__logger)
        CNSexport.set_sf(sffile)
        CNSexport.write_file(output)

    def __export_mtz(self, sffile, pdict):
        output = pdict["output"]

        MTZexport = ExportMtz(self.__logger)
        MTZexport.set_sf(sffile)
        MTZexport.write_file(output)


class SFConvertMain:
    """Main class to perform conversion steps."""

    def __init__(self, logger):
        self.__logger = logger

    def convert(self, pdict):
        """Handles the conversion as needed"""
        impsf = ImportSf(self.__logger)
        sffile = impsf.import_sf(pdict)

        # Any transformations that are necessary
        # None right now

        esf = ExportSf(self.__logger)
        esf.export_sf(sffile, pdict)

        # Generate statistics
        output = pdict["output"]
        pdb_data = pdict.get("pdb_data", {})
        pdb_cell = pdb_data.get("CELL", None)
        pdb_symm = pdb_data.get("SYMM", None)

        checksf = CheckSfFile(sffile, self.__logger)
        if pdb_cell:
            checksf.set_pdb_cell(pdb_cell)
        if pdb_symm:
            checksf.set_pdb_symm(pdb_symm)
        checksf.sf_stat(output, "SF_4_validate.cif")

        # checksffile code


class CustomHelpParser(argparse.ArgumentParser):
    def print_help(self, file=None):  # pylint: disable=unused-argument
        """
        Prints the custom help message for the sf_convert script.
        """
        custom_help_message = (
            """
    =======================================================================
                """
            + get_version()
            + """
    =======================================================================

    Usage: 'sf_convert  -i input_format -o output_format -sf data_file'
    or  'sf_convert  -o output_format -sf data_file'
    =======================================================================
    -i <input_format> :  optional,  support one of the format below.
            (If '-i' is not given, sf_convert will guess the input format.)

            MTZ, mmCIF, CNS.

    -o  <output_format> : support one of output format (below)

            mmCIF, MTZ, CNS.

    -sf  <datafile> : Give the Input Structure Factor File Name.
    -sf  <datafile> <datafile>: Provide multiple input files. Types will be based on first

    -out <output_file> :  Give output file name (if not given, default by program).

        Other options (below) can be added to the argument:
    -label   followed by label name for CNS & MTZ (see examples below).
    -freer   followed by a free test number (-freer 1) in the reflection (SF) file.
    -pdb     followed by a PDB file (add items to the converted SF file if missing).
    -detail  followed by a text (-detail " text " ), give a note to the data set.
    -wave    followed by a wavelength (-wave 0.998). It overwrites the existing one.
    -diags   followed by a log file (-diags file) containing warning/error message.

        Other not often used options (below) can be added to the argument:
    -valid   check various SF errors, and correct!(sf_convert -valid sffile)

    ==============================================================================
    Note:
    1. CIF is for small molecule. The mmCIF is for macro-molecule format.

        mmCIF token                    type     data label

    _refln.F_meas_au                  F           FP
    _refln.F_meas_sigma_au            Q           SIGFP
    _refln.intensity_meas             J           I
    _refln.intensity_sigma            Q           SIGI

    _refln.F_calc_au                  F           FC
    _refln.phase_calc                 P           PHIC
    _refln.phase_meas                 P           PHIB
    _refln.fom                        W           FOM

    _refln.pdbx_FWT                   F           FWT
    _refln.pdbx_PHWT                  P           PHWT
    _refln.pdbx_DELFWT                F           DELFWT
    _refln.pdbx_DELPHWT               P           DELPHWT

    _refln.pdbx_HL_A_iso              A           HLA
    _refln.pdbx_HL_B_iso              A           HLB
    _refln.pdbx_HL_C_iso              A           HLC
    _refln.pdbx_HL_D_iso              A           HLD

    _refln.pdbx_F_plus                G           F(+)
    _refln.pdbx_F_plus_sigma          L           SIGF(+)
    _refln.pdbx_F_minus               G           F(-)
    _refln.pdbx_F_minus_sigma         L           SIGF(-)
    _refln.pdbx_anom_difference       D           DP
    _refln.pdbx_anom_difference_sigma Q           SIGDP
    _refln.pdbx_I_plus                K           I(+)
    _refln.pdbx_I_plus_sigma          M           SIGI(+)
    _refln.pdbx_I_minus               K           I(-)
    _refln.pdbx_I_minus_sigma         M           SIGI(-)

    _refln.status                     I           FREE
    _refln.pdbx_r_free_flag           I           FLAG
    ==============================================================================

    Example_1: convert any supported format to any output format:
        sf_convert  -o any_output_format -sf sf_file -out output_file

    Example_2: convert mtz to mmcif (automatic):
        sf_convert  -o mmcif -sf mtzfile -out output_file

    Example_3: convert mtz to mmcif (give the free set):
        sf_convert  -o mmcif -sf mtzfile -freer 1 -out output_file

    Example_4: convert mtz to mmcif (use labels in mtz, one data set):
            (The labels on the left must be one of mmcif tokens)
        sf_convert -o mmcif -sf mtzfile -label FP=?, SIGFP=?, FREE=?, \\
                I=?, SIGI=?  -freer 1 -out output_file

    Example_5: convert MTZ to mmcif (one data set with anomalous)
            (If label has '(' or ')', the pair must be quoted by ' ')
        sf_convert  -o mmcif -sf mtz_file -freer 1 -label FP=? ,SIGFP=? , \\
                FREE=? , 'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?'

    Example_6: convert MTZ to mmcif (two or more data set using labels)
            (Each data set must be separated by ':' !)
        sf_convert  -o mmcif -sf mtz_file -freer 1 -label \\
                    FP=? ,SIGFP=? , FREE=? , I=?, SIGI=?, \\
                    'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?', \\
                    'I(+)=?' ,'SIGI(+)=?','I(-)=?' ,'SIGI(-)=?'  \\
                    :  \\
                    FP=? ,SIGFP=? , FREE=? , I=?, SIGI=?, \\
                    'F(+)=?' ,'SIGF(+)=?','F(-)=?' ,'SIGF(-)=?',  \\
                    'I(+)=?' ,'SIGI(+)=?','I(-)=?' ,'SIGI(-)=?' \\
                    -out output_file

    Example_7: Multiple file auto-conversion. (files separated by ',' or space)
        sf_convert  -o mmcif -sf sffile1 sffile2 sffile3 -out outfile_name

    Example_8: Make the converted mmcif be complete (using coordinate).
        sf_convert  -o mmcif -sf sf_file -pdb xyzfile

    Example_9: Give a remark to the converted data set.
        sf_convert  -o mmcif -sf sf_file -detail "any text"

    Note: The question marks '?' correspond to the labels in the SF file.
    """
        )
        print(custom_help_message)

    def error(self, message):
        """
        Prints an error message and exits the program.

        Args:
            message: The error message to be printed.
        """
        sys.stderr.write("Error: %s\n" % message)
        sys.exit(2)


def validate_file_exists(filepath: str):
    """
    Validates if a given file exists.

    Args:
        filepath: The path to the file to be validated.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")


def validate_format(file_format: str):
    """
    Validates if the given format is one of the VALID_FORMATS.

    Args:
        file_format: The format to be validated.

    Raises:
        ValueError: If the format is not valid.
    """
    if file_format.upper() not in VALID_FORMATS:
        raise ValueError(f"Invalid format: {file_format}. Please use one of the following formats: {VALID_FORMATS}")


def get_input_format(args: argparse.Namespace) -> str:
    """
    Determines the input format either from the provided argument or by guessing.

    Args:
        args: The command line arguments.

    Returns:
        The determined input format.

    Raises:
        ValueError: If the source file is not provided.
    """
    if args.i:
        validate_format(args.i)
        return args.i
    if args.sf is None:
        raise ValueError("Source file (-sf) must be provided.")
    return guess_sf_format(args.sf[0])


def handle_pdb_argument(args, pdb, logger):
    """
    Handles operations related to the -pdb argument.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.

    Returns:
        The extracted attributes from the PDB file.

    Raises:
        ValueError: If the file format for -pdb argument is invalid.
        FileNotFoundError: If the PDB file does not exist.
    """
    validate_file_exists(args.pdb)
    if is_cif(args.pdb, logger):
        return pdb.extract_attributes_from_cif(args.pdb)
    else:
        return pdb.extract_attributes_from_pdb(args.pdb)


def handle_label_argument(args):
    """
    Validates the -label argument format.

    Args:
        args: The command line arguments.

    Raises:
        ValueError: If the format for -label argument is invalid.
    """

    # Consolidate labels into space separated list
    labels = " ".join(args.label)
    pattern = re.compile(r"^([^=]+=[^=]+)(,\s*[^=]+=[^=]+)*$")
    if not pattern.match(labels):
        raise ValueError("Invalid format for -label argument. Please use the format 'key1=value1, key2=value2, ...'")


def handle_freer_argument(args, logger):
    """
    Handles operations related to the -freer argument.

    Args:
        args: The command line arguments.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.

    Raises:
        ValueError: If the -freer argument is not a positive integer.
    """
    if args.freer < 0:
        print("-freer argument must be a positive integer.")
        sys.exit(1)

    logger.pinfo(f"Note: {args.freer} is used for free data set.", 0)


def handle_wave_argument(args):
    """
    Handles operations related to the -wave argument.

    Args:
        args: The command line arguments.

    Raises:
        ValueError: If the -wave argument is not a positive float.
    """
    if args.wave <= 0.0:
        raise ValueError("-wave argument must be a positive float.")


def handle_valid_argument(args, logger):
    """
    Handles operations related to the -valid argument.

    Args:
        args: The command line arguments.
        logger: The PInfoLogger object.
    """
    sffile = StructureFactorFile()
    sffile.read_file(args.sf)
    n = sffile.get_number_of_blocks()
    sf_stat = CheckSfFile(sffile, logger)
    sf_stat.check_sf_all_blocks(n)
    sf_stat.write_sf_4_validation(args.out + "_SF_4_validate.cif")


def reformat_sf_header(sffile, pdbid, logger, detail=None):
    """
    Reformats the SF header.

    Args:
        sffile: The StructureFactorFile object.
        pdbid: the pdb id to set
        logger: The PInfoLogger object.
        detail: Any details
    """
    _ = reformat_sfhead(sffile, pdbid, logger, detail)


def validate_block_name(block_name):
    """
    Validates the block name length.

    Args:
        block_name: The block name to be validated.

    Raises:
        ValueError: If the block name is not 4 characters long.
    """
    if len(block_name) != 4:
        raise ValueError(f"Block name must be 4 characters long. {block_name} is not valid.")


def convert_files(args, input_format, pdb_data, logger):
    """
    Converts files based on input and output formats.

    Args:
        args: The command line arguments.
        input_format: The determined input format.
        pdb: The ProteinDataBank object.
        logger: The PInfoLogger object.

    Raises:
        ValueError: If the conversion from input to output format is not supported.
    """
    output_format = args.o
    input_format = input_format.upper()

    if output_format is None:
        raise ValueError(f"Conversion from {input_format} to {output_format} is not supported.")

    output_format = output_format.upper()

    # Setup dictionary of what we would like done
    pdict = {}
    pdict["sfin"] = args.sf
    pdict["inp_format"] = input_format
    pdict["out_format"] = output_format

    if args.out is not None:
        output = args.out
    else:
        output = f"{args.sf[0]}.{args.o}"

    pdict["output"] = output
    pdict["pdb_data"] = pdb_data

    if args.wave is not None:
        pdict["wave_cmdline"] = float(args.wave)  # Type checked in argument parser

    if args.label is not None:
        pdict["label"] = " ".join(args.label)

    if args.freer is not None:
        pdict["free"] = args.freer

    if args.pdb_id is not None:
        pdict["pdb_id"] = args.pdb_id

    sfc = SFConvertMain(logger)

    if output_format in ["MMCIF", "CNS", "MTZ"]:
        sfc.convert(pdict)
    elif args.valid is False:
        raise ValueError(f"Conversion from {input_format} to {output_format} is not supported.")

    rdict = {"output": output, "out_format": output_format}
    return rdict


def main():
    """
    The main function that handles the execution of the sf_convert script.
    """
    try:
        args = parse_arguments()

        version = get_version()

        print("=======================================================================")
        print(f"              {version}")
        print("=======================================================================")

        pdb = ProteinDataBank()
        logger = PStreamLogger()

        input_format = get_input_format(args)

        if args.pdb:
            pdb_data = handle_pdb_argument(args, pdb, logger)
        else:
            pdb_data = {}

        # Wavelength, etc - not pdb_data - need to know where comes from

        if args.label:
            handle_label_argument(args)

        if args.freer is not None:
            handle_freer_argument(args, logger)

        if args.wave:
            handle_wave_argument(args)

        if args.valid:
            handle_valid_argument(args, logger)

        rdict = convert_files(args, input_format, pdb_data, logger)

    except ValueError as e:
        print(f"Error: {e}")
        traceback.print_exc()
        sys.exit(2)

    # Write out final files

    outpath = rdict["output"]
    outformat = rdict["out_format"].lower()
    print(f"Output File Name = {outpath} : ({outformat} format)")

    diags = args.diags if args.diags else None

    logger.output_reports("sf_information.cif", diags)


def parse_arguments() -> argparse.Namespace:
    """
    Parses and returns the command line arguments.

    Returns:
        The parsed command line arguments.
    """
    parser = CustomHelpParser(description="This script allows various operations on files. Refer to the help document for more details.")

    parser.add_argument("-i", type=str, help="Input format")
    parser.add_argument("-o", type=str, help="Output format. Accepted values are mmCIF, CNS, MTZ")
    parser.add_argument("-sf", type=str, nargs="+", help="Source file")
    parser.add_argument("-out", type=str, default=None, help="Output file name (if not given, default by program)")
    parser.add_argument("-label", type=str, nargs="*", help="Label name for CNS & MTZ")
    parser.add_argument("-pdb", type=str, help="PDB file (add items to the converted SF file if missing)")
    parser.add_argument("-pdb_id", type=str, help="PDB id to set)")
    parser.add_argument("-freer", type=int, help="Free test number in the reflection (SF) file")
    parser.add_argument("-wave", type=float, help="Wavelength setting. It overwrites the existing one")
    parser.add_argument("-diags", type=str, help="Log file containing warning/error message")
    parser.add_argument("-detail", type=str, help="Give a note to the data set")
    parser.add_argument("-valid", action="store_true", help="Check various SF errors, and correct!")

    return parser.parse_args()


if __name__ == "__main__":
    main()
