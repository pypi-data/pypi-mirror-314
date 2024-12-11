"""Script to provide HTML form for use in manually editing labels

Invoked:
        options = (
            " -mtz_man_html "
            + self.__mtzDataSet
            + " -url_users_data "
            + os.path.join("/sessions", self.__sessionId)
            + " -users_data "
            + self.__topSessionPath
            + " -cgi_bin  /cgi-bin/ -sf "
            + self.__mtzFileName
            + " > "
            + logPath
            + " 2>&1 ; "

"""

import argparse
import os
import sys

from sf_convert.utils.GenMtzHtml import GenMtzHtml


def main():
    parser = argparse.ArgumentParser(description="Generates HTML forms for use in manually providing input for SF conversion")
    # Currently required argument. Could add CNS manual operation
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-mtz_man_html", type=int, action="store", const=1, nargs="?", metavar="num_datasets", help="The number of datasets to consider")

    parser.add_argument("-url_users_data", type=str, default="", help="URL path for where to store data")
    parser.add_argument("-users_data", type=str, default="", help="Session path")
    parser.add_argument("-cgi_bin", type=str, default="", help="where to find cgi scripts on server")
    parser.add_argument("-sf", type=str, required=True, help="Structure factor file")
    parser.add_argument("-pdb_id", type=str, default="xxxx", help="PDB ID to use")
    parser.add_argument("-path", type=str, default=".", help="additional path to cgi data")

    args = parser.parse_args()

    if not os.path.exists(args.sf):
        print(f"File not found '{args.sf}'")
        sys.exit(1)

    # Package up

    if os.getenv("PROG_VARI"):
        sf_convert_exec = os.path.join(os.getenv("PROG_VARI"), "bin", "sf_convert")
    else:
        sf_convert_exec = "sf_convert"

    d = {
        "mtz_man_html": args.mtz_man_html,
        "users_data": args.users_data,
        "url_users_data": args.url_users_data,
        "cgi_bin": args.cgi_bin,
        "sf": args.sf,
        "pdbid": args.pdb_id,
        "path": args.path,
        "CCP4": os.getenv("CCP4"),
        "SF_EXEC": sf_convert_exec,
    }

    if args.mtz_man_html:
        gmh = GenMtzHtml(d)
        gmh.genMtzInfor()

    return 0


if __name__ == "__main__":
    main()
