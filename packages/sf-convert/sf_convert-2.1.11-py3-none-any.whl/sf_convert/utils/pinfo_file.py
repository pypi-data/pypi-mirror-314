import io
import os

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.IoAdapterCore import IoAdapterCore


class PInfoBase:
    def __init__(self):
        self._lf1 = None
        self._lf2 = None

    def pinfo(self, info, pid):
        """
        Logs information and prints it to the console.

        Args:
            info (str): The information to log and print.
            pid (int): The ID of the logger to use.

        Notes:
            - If the information contains "Warning" or "Error", it is logged to the first log file and printed to the console.
            - If the ID is 0, the information is logged to the second log file and printed to the console.
            - If the ID is 1, the information is logged to the second log file.
            - If the ID is 2, the information is only printed to the console.
        """
        if "Warning" in info or "Error" in info:
            self._lf1.write(f"{info}\n")  # Log to FTMP1.log
            print(info)  # Also print to console
        else:
            if pid == 0:
                self._lf2.write(f"{info}\n")  # Log to FTMP2.log
                print(info)  # Also print to console
            elif pid == 1:
                self._lf2.write(f"{info}\n")  # Log to FTMP2.log
            elif pid == 2:
                print(info)  # Only print to console

    def output_reports(self, sfinfo="sf_information.cif", diag=None):
        """Output diagnostics file (if requested) and the sf_information.cif file"""

        if diag:
            self._lf1.seek(0)

            with open(diag, "w") as fout:
                num = 0
                for ln in self._lf1:
                    ln = ln.strip()
                    if len(ln):
                        num += 1
                        fout.write(f"{ln}\n")

                if num == 0:
                    fout.write("No Error/Warning messages were found.\n")

        self.__output_sf_info(sfinfo)

    def __output_sf_info(self, sfpath):
        """Outputs sf_info class"""

        self._lf1.seek(0)
        self._lf2.seek(0)

        err = ""
        for ln in self._lf1:
            # Leave new lines
            err += ln

        # We expect an 'empty' value returned - legacy code 'cheated'
        # by two lines with semi colon - but writer simplies to ?
        # Do not provide data with simply a newline

        info = ""
        for ln in self._lf2:
            # Leave new lines
            info += ln

        if info == "":
            info = "\n"

        b0 = DataContainer("info")
        aCat = DataCategory("sf_convert", ("error", "sf_information"))
        aCat.append((err, info))

        b0.append(aCat)

        cl = [b0]

        ioa = IoAdapterCore()
        ioa.writeFile(sfpath, cl)


class PInfoLogger(PInfoBase):
    def __init__(self, log_file1_path, log_file2_path):
        """
        Initializes a new instance of the PInfoLogger class.

        Args:
            log_file1_path (str): The path to the first log file.
            log_file2_path (str): The path to the second log file.
        """
        super().__init__()

        self.__log_file1 = log_file1_path
        self.__log_file2 = log_file2_path

        self.clear_logs()  # Clear the logs if they already exist

        self._lf1 = open(self.__log_file1, "w")
        self._lf2 = open(self.__log_file2, "w")

    def __del__(self):
        if self._lf1:
            self._lf1.close()
        if self._lf2:
            self._lf1.close()

    def clear_logs(self):
        """
        Clears the log files.
        """
        self.__remove_if_exists(self.__log_file1)
        self.__remove_if_exists(self.__log_file2)

    def __remove_if_exists(self, file_path):
        """
        Removes a file if it exists.

        Args:
            file_path (str): The path to the file.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"An error occurred while removing {file_path}: {e}")


class PStreamLogger(PInfoBase):
    """Logger but uses StringIO and not tempoary log files"""

    def __init__(self):
        super().__init__()
        self._lf1 = io.StringIO()
        self._lf2 = io.StringIO()
