import os
import difflib
from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.utils.reformat_sfhead import reformat_sfhead
from sf_convert.utils.pinfo_file import PInfoLogger


class TestMmcifConversion:
    def test_mmcif_conversion(self, tmp_path, cif_5pny_data_path, cif_mmcif_5pny_detail_data_path, DETAIL="any text"):
        """
        Tests the conversion of a CIF file to mmCIF format.

        Args:
            tmp_path: The path to the temporary directory.
            cif_5pny_data_path: The path to the CIF file to be converted.
            cif_mmcif_5pny_detail_data_path: The path to the reference mmCIF file for comparison.
            DETAIL: Additional detail to be added to the mmCIF file (default is "any text").

        Returns:
            None
        """
        print("Starting the mmCIF conversion test...")

        # Define the path for the output file
        output_path = os.path.join(tmp_path, "output.mmcif")

        # Read and process the mmCIF file
        sffile = StructureFactorFile()
        sffile.read_file(cif_5pny_data_path)
        logger = PInfoLogger("path_to_log1.log", "path_to_log2.log")
        _ = reformat_sfhead(sffile, "5pny", logger, DETAIL)
        sffile.write_file(output_path)

        # Read the expected output file and filter out comment lines
        with open(cif_mmcif_5pny_detail_data_path, "r") as file:
            expected_lines = [line.strip() for line in file.readlines() if not line.strip().startswith("#")]

        # Read the generated output file and filter out comment lines
        with open(output_path, "r") as file:
            output_lines = [line.strip() for line in file.readlines() if not line.strip().startswith("#")]

        # Join split lines
        expected_lines = self.join_split_lines(expected_lines)
        output_lines = self.join_split_lines(output_lines)

        # Normalize whitespace in each line for accurate comparison
        expected_lines = [" ".join(line.split()) for line in expected_lines]
        output_lines = [" ".join(line.split()) for line in output_lines]

        # Compare the files
        differ = difflib.Differ()
        diffs = list(differ.compare(expected_lines, output_lines))

        # Check if there are differences
        differences = [diff for diff in diffs if diff[0] in ("-", "+")]

        if differences:
            print("\nDifferences found:")
            for line in differences:
                print(line)
            assert False, "Files are not the same"
        else:
            print("mmCIF conversion test completed.")

        # assert len(differences) == 0, "Files are not the same"

        print("mmCIF conversion test completed.")

    @staticmethod
    def join_split_lines(lines):
        """
        Join lines that are split into two.

        This function takes a list of strings and looks for lines that appear to be split over two entries.
        If the current line doesn't end with a quote and the next line starts with a quote,
        they are treated as split lines and are concatenated together.

        Args:
            lines (list of str): A list of strings representing lines from a file or data source.

        Returns:
            list of str: The modified list of strings where split lines have been joined.

        Example:
            Input: ["_diffrn.details", "'data for ligand evidence map'", "other data"]
            Output: ["_diffrn.details 'data for ligand evidence map'", "other data"]
        """
        i = 0
        while i < len(lines) - 1:
            if not lines[i].endswith("'") and lines[i + 1].startswith("'"):
                lines[i] += " '" + lines[i + 1][1:]
                del lines[i + 1]
            else:
                i += 1
        return lines
