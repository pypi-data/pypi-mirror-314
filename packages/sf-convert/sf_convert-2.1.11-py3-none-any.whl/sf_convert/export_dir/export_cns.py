class ExportCns:
    def __init__(self, logger, legacy=False):  # pylint: disable=unused-argument
        """
        Initializes the CifToCNSConverter object.

        """
        # self.__legacy = legacy
        # self.__logger = logger
        self.__sf_file = None
        self.__attr_existence = {}

        # Init here
        self.__status = None
        self.__Io = None
        self.__sIo = None
        self.__nref = 0
        self.__refln_data = None
        self.__sf_block = None

        # The following use setattr to init - but simplify for pylint - as we declare what we need
        self.__hla = self.__hlb = self.__hlc = self.__hld = self.__fom = None
        self.__F_plus = self.__F_minus = self.__sF_plus = self.__sF_minus = None
        self.__I_plus = self.__I_minus = self.__sI_plus = self.__sI_minus = None
        self.__Fo_au = self.__sFo_au = None
        self.__F2c = self.__Ic = self.__Fo = self.__sFo = None
        self.__Fc_au = self.__F2o = self.__Fc = None
        self.__H = self.__K = self.__L = None

        # Define attributes
        self.attributes = {
            "index_h": "H",
            "index_k": "K",
            "index_l": "L",
            "F_calc": "Fc",
            "F_calc_au": "Fc_au",
            "intensity_calc": "Ic",
            "F_squared_calc": "F2c",
            "F_meas_au": "Fo_au",
            "F_meas_sigma_au": "sFo_au",
            "F_meas_sigma": "sFo",
            "F_squared_sigma": "sF2o",
            "pdbx_I_plus_sigma": "sI_plus",
            "pdbx_I_minus_sigma": "sI_minus",
            "pdbx_F_plus_sigma": "sF_plus",
            "pdbx_F_minus_sigma": "sF_minus",
            "F_meas": "Fo",
            "F_squared_meas": "F2o",
            "pdbx_I_plus": "I_plus",
            "pdbx_I_minus": "I_minus",
            "pdbx_F_plus": "F_plus",
            "pdbx_F_minus": "F_minus",
            "fom": "fom",
            "pdbx_HL_A_iso": "hla",
            "pdbx_HL_B_iso": "hlb",
            "pdbx_HL_C_iso": "hlc",
            "pdbx_HL_D_iso": "hld",
        }

    def __initialize_data(self):
        """
        Initializes the data for the converter after SF set
        """
        self.__initialize_refln_data()
        self.__initialize_counts()
        self.__check_attributes_exist()

    def __initialize_refln_data(self):
        """
        Initializes the reflection data from the StructureFactorFile object.
        """
        self.__sf_block = self.__sf_file.get_block_by_index(0)
        self.__refln_data = self.__sf_block.getObj("refln")

    def __initialize_counts(self):
        """
        Initializes the number of reflections.
        """
        if self.__refln_data:
            self.__nref = self.__refln_data.getRowCount()

    def __check_attributes_exist(self):
        """
        Checks the existence of specific attributes in the reflection data.
        """
        for attr, value in self.attributes.items():
            self.__attr_existence[value] = self.__refln_data.hasAttribute(attr)

        # Check existence of specific attributes
        check_attributes = {
            "Io": ["intensity_meas", "intensity_meas_au", "intensity"],
            "sIo": ["intensity_sigma", "intensity_sigma_au", "intensity_sigm", "intensity_meas_sigma", "intensity_meas_sigma_au"],
            "status": ["status", "R_free_flag", "statu", "status_au"],
        }

        for attribute, alternatives in check_attributes.items():
            self.__attr_existence[attribute] = any(self.__refln_data.hasAttribute(alternative) for alternative in alternatives)

    def __initialize_columns_at_index(self, i):
        """
        Initializes the columns at a given index.

        Args:
            i (int): The index of the columns to initialize.
        """
        attL = self.__refln_data.getAttributeList()

        # First row - set attribute for columns that do not exist
        if i == 0:
            for attr, var in self.attributes.items():
                if attr not in attL:
                    setattr(self, "_ExportCns__" + var, None)

        for attr, var in self.attributes.items():
            if attr in attL:
                value = self.__refln_data.getValue(attr, i)
                setattr(self, "_ExportCns__" + var, value)

        self.__initialize_Io_at_index(i)
        self.__initialize_sIo_at_index(i)
        self.__initialize_status_at_index(i)

    def __initialize_Io_at_index(self, i):
        """
        Initializes the Io attribute at a given index.

        Args:
            i (int): The index of the Io attribute to initialize.
        """
        self.__Io = self.__get_first_refln_value(["intensity_meas", "intensity_meas_au", "intensity"], i)

    def __initialize_sIo_at_index(self, i):
        """
        Initializes the sIo attribute at a given index.

        Args:
            i (int): The index of the sIo attribute to initialize.
        """
        self.__sIo = self.__get_first_refln_value(["intensity_sigma", "intensity_sigma_au", "intensity_sigm", "intensity_meas_sigma", "intensity_meas_sigma_au"], i)

    def __initialize_status_at_index(self, i):
        """
        Initializes the status attribute at a given index.

        Args:
            i (int): The index of the status attribute to initialize.
        """
        self.__status = self.__get_first_refln_value(["status", "R_free_flag", "statu", "status_au"], i)

    def __get_first_refln_value(self, attrList, row):
        """
        Gets the first value from a list of attributes in the reflection data.

        Args:
            attrList (list): The list of attributes to check.
            row (int): The row index to check.

        Returns:
            The first value found in the attribute list, or None if no value is found.
        """
        attL = self.__refln_data.getAttributeList()

        ret = None
        for att in attrList:
            if att in attL:
                ret = self.__refln_data.getValue(att, row)
                break

        return ret

    def get_F_I(self, j):
        """
        Method to get H, K, L, F o& I from SF

        Args:
            j (int): The index of the reflection data.

        Returns:
            tuple: A tuple containing the values of H, K, L, F, sigma(F), I, sigma(I).
        """
        self.__initialize_columns_at_index(j)

        # Parse values to integers
        h = int(self.__H)
        k = int(self.__K)
        l = int(self.__L)  # noqa: E741

        # Initialize variables
        f, ssf, i, si, f1, sf1, f2, sf2 = 0, 0, 0, 0, 0, 0, 0, 0

        # sigma
        si = self.float_or_zero(self.__sIo) if self.__sIo else 0.0
        ssf = self.float_or_zero(self.__sFo_au) if self.__sFo_au else self.float_or_zero(self.__sFo) if self.__sFo else 0.0

        # for F
        f = (
            self.float_or_zero(self.__Fo_au)
            if self.__Fo_au
            else self.float_or_zero(self.__Fo) if self.__Fo else self.float_or_zero(self.__Fc_au) if self.__Fc_au else self.float_or_zero(self.__Fc) if self.__Fc else 0.0
        )

        if not self.__Io:
            i = f * f
            si = 2 * f * ssf

        # for I
        i = (
            self.float_or_zero(self.__Io)
            if self.__Io
            else self.float_or_zero(self.__F2o) if self.__F2o else self.float_or_zero(self.__Ic) if self.__Ic else self.float_or_zero(self.__F2c) if self.__F2c else 0.0
        )

        if not self.__Fo_au:
            if i > 0.0:
                f = i**0.5
                ssf = si / (2.0 * f)
            else:
                f = 0
                ssf = 0

        # F_plus exist
        if self.__F_plus and not (self.__Fo_au or self.__Io):
            f1 = self.float_or_zero(self.__F_plus)
            sf1 = self.float_or_zero(self.__sF_plus)

            f2 = self.float_or_zero(self.__F_minus)
            sf2 = self.float_or_zero(self.__sF_minus)

            if f1 > 0 and f2 < 0.0001:
                f = f1
                ssf = sf1
            elif f2 > 0 and f1 < 0.0001:
                f = f2
                ssf = sf2
            else:
                f = 0.5 * (f1 + f2)
                ssf = 0.5 * (sf1 + sf2)

            if not self.__I_plus:
                i = f * f
                si = 2.0 * f * ssf

        # I_plus exist
        if self.__I_plus and not (self.__Fo_au or self.__Io):
            f1 = self.float_or_zero(self.__I_plus)
            sf1 = self.float_or_zero(self.__sI_plus)

            f2 = self.float_or_zero(self.__I_minus)
            sf2 = self.float_or_zero(self.__sI_minus)

            if f1 > 0 and f2 < 0.0001:
                i = f1
                si = sf1
            elif f2 > 0 and f1 < 0.0001:
                i = f2
                si = sf2
            else:
                i = 0.5 * (f1 + f2)
                si = 0.5 * (sf1 + sf2)

            if not self.__F_plus:
                if i >= 0:
                    f = i**0.5
                    ssf = si / (2 * f) if f > 0.0001 else 0

        ff = f
        ii = i
        sii = si
        sff = ssf
        return h, k, l, ff, sff, ii, sii

    def float_or_zero(self, value):
        """
        Converts a value to float or returns 0 if it cannot be converted.

        Args:
            value (str): The value to convert.

        Returns:
            float: The converted value or 0 if it cannot be converted.
        """
        try:
            float(value)
            return float(value)
        except ValueError:
            return 0

    def write_cns_file(self, pathOut):
        """
        Writes the data to a CNS file.
        """
        with open(pathOut, "w") as output_file:
            output_file.write("NREFlection= {}\n".format(self.__nref))
            output_file.write("ANOMalous=FALSe { equiv. to HERMitian=TRUE}\n")
            output_file.write("DECLare NAME=FOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=SIGMA           DOMAin=RECIprocal   TYPE=REAL END\n")
            output_file.write("DECLare NAME=TEST            DOMAin=RECIprocal   TYPE=INTE END\n")

            # Assuming that all the variables here are boolean values
            if self.__attr_existence["Io"] or self.__attr_existence["F2o"]:
                output_file.write("DECLare NAME=IOBS            DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI            DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__attr_existence["F_plus"] and self.__attr_existence["F_minus"]:
                output_file.write("DECLare NAME=F+           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGF+        DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=F-           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGF-        DOMAin=RECIprocal   TYPE=REAL END\n")

            elif self.__attr_existence["I_plus"] and self.__attr_existence["I_minus"]:
                output_file.write("DECLare NAME=I+           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI+        DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=I-           DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=SIGI-        DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__attr_existence["fom"]:
                output_file.write("DECLare NAME=FOM   DOMAin=RECIprocal   TYPE=REAL END\n")

            if self.__attr_existence["hla"]:
                output_file.write("DECLare NAME=HLA   DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=HLB   DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=HLC   DOMAin=RECIprocal   TYPE=REAL END\n")
                output_file.write("DECLare NAME=HLD   DOMAin=RECIprocal   TYPE=REAL END\n")

            # Loop over all the data points
            for i in range(self.__nref):

                self.__initialize_columns_at_index(i)

                h, k, l, ff, sff, ii, sii = self.get_F_I(i)

                if self.__attr_existence["status"] and self.__status == "x":
                    continue

                if self.__status:
                    flag = 1 if (self.__status == "f" or self.__status == "1") else 0
                else:
                    flag = 0

                output_file.write("INDE  {} {} {} FOBS= {:.2f} SIGMA= {:.2f} TEST= {}\n".format(h, k, l, ff, sff, flag))

                if self.__attr_existence["Io"] or self.__attr_existence["F2o"]:
                    output_file.write("IOBS= {:.2f} SIGI= {:.2f}\n".format(ii, sii))

                if self.__attr_existence["F_plus"] and self.__attr_existence["F_minus"]:
                    output_file.write("F+= {:.2f} SIGF+= {:.2f}\n".format(self.float_or_zero(self.__F_plus), self.float_or_zero(self.__sF_plus)))
                    output_file.write("F-= {:.2f} SIGF-= {:.2f}\n".format(self.float_or_zero(self.__F_minus), self.float_or_zero(self.__sF_minus)))

                elif self.__attr_existence["I_plus"] and self.__attr_existence["I_minus"]:
                    output_file.write("I+= {:.2f} SIGI+= {:.2f}\n".format(self.float_or_zero(self.__I_plus), self.float_or_zero(self.__sI_plus)))
                    output_file.write("I-= {:.2f} SIGI-= {:.2f}\n".format(self.float_or_zero(self.__I_minus), self.float_or_zero(self.__sI_minus)))

                if self.__attr_existence["fom"]:
                    output_file.write("FOM= {:.2f}\n".format(self.float_or_zero(self.__fom)))

                if self.__attr_existence["hla"]:
                    output_file.write(
                        "HLA= {:.2f} HLB= {:.2f} HLC= {:.2f} HLD= {:.2f}\n".format(
                            self.float_or_zero(self.__hla), self.float_or_zero(self.__hlb), self.float_or_zero(self.__hlc), self.float_or_zero(self.__hld)
                        )
                    )

    def write_file(self, path_out):
        """
        Args:
            sffile (StructureFactorFile): The StructureFactorFile object containing the CIF data.
            fout_path (str): The path to the output CNS file.

        """
        self.__initialize_data()
        self.write_cns_file(path_out)

    def set_sf(self, sfobj):
        """
        Sets PDBx/mmCIF SF file

        Args:
        sf: StructureFactorFile - object with data

        Returns:
        Nothing
        """
        self.__sf_file = sfobj
