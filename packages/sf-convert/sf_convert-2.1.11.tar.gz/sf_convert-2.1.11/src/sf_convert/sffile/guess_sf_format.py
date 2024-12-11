def guess_sf_format(inpfile: str) -> str:
    """
    Guesses the format of a structure factor file based on its content.

    Args:
        inpfile (str): The path to the input file.

    Returns:
        str: The guessed format of the structure factor file, or None if the format is not recognized.
    """
    try:
        with open(inpfile, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Check CIF
        for line in lines:
            if line.strip().startswith("_reflns."):
                return "CIF"

        # Check mmCIF
        for line in lines:
            if line.strip().startswith("_refln."):
                return "mmCIF"

        # Check CNS
        n3 = m1 = m2 = mm1 = 0
        for line in lines:
            line = line.strip()
            if line.startswith("INDE") or (line.startswith("DECLare") and "RECIproca" in line[20:]):
                if "FOBS=" in line or "FO=" in line or " F_" in line or "F=" in line:
                    m1 += 1
                if "IOBS=" in line or "IO=" in line or "I=" in line:
                    m2 += 1
                if " FOBS " in line:
                    mm1 += 1
                n3 += 1
                if n3 > 300:
                    break
            elif "FOBS=" in line or "FO=" in line or "F=" in line:
                n3 += 1
                m1 += 1
                if m1 > 300:
                    break
            elif "IOBS=" in line or " IO=" in line or " I=" in line:
                n3 += 1
                m2 += 1
                if m2 > 300:
                    break

        if n3 >= 50 and mm1 < 10:
            return "CNS"

        # Check TNT
        n4 = 0
        for line in lines:
            if line.strip().startswith("HKL"):
                n4 += 1
                if n4 > 200:
                    break
        if n4 >= 100:
            return "TNT"

        # Check XSCALE
        n5 = 0
        for line in lines:
            if line.strip().startswith(("!SPACE_GROUP_NUMBER=", "!UNIT_CELL_CONSTANTS=", "!ITEM_H=", "!ITEM_K=", "!ITEM_L=")):
                n5 += 1
                if n5 > 4:
                    return "XSCALE"

        # Check DTREK
        n6 = 0
        for line in lines:
            line = line.strip()
            if (
                line.startswith("CRYSTAL_MOSAICITY=")
                or line.startswith("CRYSTAL_SPACEGROUP=")
                or line.startswith("CRYSTAL_UNIT_CELL=")
                or line.startswith("nH")
                or line.startswith("nK")
                or line.startswith("nL")
            ):
                n6 += 1
                if n6 > 5:
                    return "DTREK"

        # Check SCALEPACK
        n7 = 0
        for i, line in enumerate(lines):
            strs = line.split()
            if (
                (i == 0 and strs[0] == "1" and len(strs) == 1)
                or (i == 1 and (strs[0] == "-985" or strs[0] == "-987") and len(strs) == 1)
                or (i == 2 and "." in strs[0] and len(line) > 60)
                and len(strs) == 6
            ):
                n7 += 1
                if n7 >= 3:
                    return "SCALEPACK"

        # Check SHELX
        n8 = 0
        for line in lines:
            if len(line) > 50 and len(line.strip()) == 32:
                n8 += 1
            if n8 >= 200:
                return "SHELX"

        # Check SAINT
        n9 = 0
        for i, line in enumerate(lines):
            if i > 50 and len(line.strip()) > 150:
                n9 += 1
                if n9 >= 200:
                    return "SAINT"

    except UnicodeDecodeError:
        try:
            with open(inpfile, "rb") as file:
                first_three_bytes = file.read(3)

            if first_three_bytes == b"MTZ":
                return "MTZ"
        except Exception as _e:  # noqa: F841
            return None

    return "Format not recognized"
