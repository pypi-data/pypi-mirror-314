class SpaceGroup:
    def __init__(self, logger):

        self.__logger = logger

        self.__symmetry95 = [
            "A 1",
            "A 1 2 1",
            "B 1 1 2",
            "B 2",
            "B 2 21 2",
            "C 1 2 1",
            "C 1 21 1",
            "C 2(A 112)",
            "C 2 2 2",
            "C 2 2 21",
            "C 4 21 2",
            "F 2 2 2",
            "F 2 3",
            "F 4 2 2",
            "F 4 3 2",
            "F 41 3 2",
            "I 1 2 1",
            "I 1 21 1",
            "I 2 2 2",
            "I 2 3",
            "I 21 3",
            "I 4",
            "I 21 21 21",
            "I 4 2 2",
            "I 4 3 2",
            "I 41",
            "I 41 2 2",
            "I 41 3 2",
            "P 1",
            "P -1",
            "P 1 2 1",
            "P 1 1 2",
            "P 2 2 2",
            "P 2 3",
            "P 2 2 21",
            "P 2 21 21",
            "P 1 21 1",
            "P 1 1 21",
            "P 21(C)",
            "P 21 2 21",
            "P 21 3",
            "P 21 21 2",
            "P 21 21 2 A",
            "P 21 21 21",
            "P 3",
            "P 3 1 2",
            "P 3 2 1",
            "P 31",
            "P 31 1 2",
            "P 31 2 1",
            "P 32",
            "P 32 1 2",
            "P 32 2 1",
            "P 4",
            "P 4 2 2",
            "P 4 3 2",
            "P 4 21 2",
            "P 41",
            "P 41 2 2",
            "P 41 3 2",
            "P 41 21 2",
            "P 42",
            "P 42 2 2",
            "P 42 3 2",
            "P 42 21 2",
            "P 43",
            "P 43 2 2",
            "P 43 3 2",
            "P 43 21 2",
            "P 6",
            "P 6 2 2",
            "P 61",
            "P 61 2 2",
            "P 62",
            "P 62 2 2",
            "P 63",
            "P 63 2 2",
            "P 64",
            "P 64 2 2",
            "P 65",
            "P 65 2 2",
            "H 3",
            "R 3",
            "H 3 2",
            "R 3 2",
            "I 41/a",
            "P 1 21/c 1",
            "C 1 2/c 1",
            "P 1 21/n 1",
            "I -4 c 2",
            "I -4 2 d",
            "I -3",
            "P b c n ",
        ]

    def standardize_sg_name(self, symm):
        """Standardize spacegroup name"""

        if symm is None:
            return None

        symm2 = symm.replace(" ", "")

        # Fix up some standard
        if symm2 == "R3:H":
            return "H3"
        if symm2 == "R33:H":
            return "H32"

        if symm2 == "P2":
            return "P 1 2 1"
        if symm2 == "P21":
            return "P 1 21 1"

        if symm2 == "C2":
            return "C 1 2 1"
        if symm2 == "C21":
            return "C 1 21 1"

        if symm2 == "I2":
            return "I 1 2 1"
        if symm2 == "I21":
            return "I 1 21 1"

        if symm2 == "A2":
            return "A 1 2 1"

        for s95 in self.__symmetry95:
            s95trim = s95.replace(" ", "")
            if s95trim == symm2:
                return s95

        self.__logger.pinfo("Warning: the space group (%s) can not be converted to the standard", symm)
        return symm
