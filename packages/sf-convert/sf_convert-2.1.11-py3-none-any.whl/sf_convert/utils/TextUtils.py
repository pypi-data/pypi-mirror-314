import os
import re
import sys


def is_cif(fpath, pinfo):
    """Determine if the contents fpath looks like a cif file.  Quick and dirty.

    Returns True is if appears to be
    """

    # Search for lines that look like categories - limited number of lines in file.
    # If exceeds threshold, we are a cif...

    if not os.path.exists(fpath):
        pinfo.pinfo("%s does not exist" % fpath, 1)
        return False

    regexp = re.compile("^_[a-zA-Z0-9_]+\\.[a-zA-Z0-9_]+")

    found = 0
    threshold = 60
    with open(fpath, "r") as fin:
        for line in fin:
            sline = line.strip()
            if regexp.match(sline):
                found += 1
                if found > threshold:
                    break

    if found > threshold:
        return True

    return False


if __name__ == "__main__":
    print(is_cif(sys.argv[1], print))
