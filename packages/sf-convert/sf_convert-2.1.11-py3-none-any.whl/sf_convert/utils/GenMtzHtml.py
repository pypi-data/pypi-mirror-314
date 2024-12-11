"""Code to generate an HTML template for manual selection of Mtz header"""

import os

from sf_convert.utils.MtzUtils import GetMtzInfo


class GenMtzHtml:
    def __init__(self, data):
        self.__data = data

    def genMtzInfor(self):
        """Generates an html fragment to support selection of columns

        Returns the output file
        """

        outdir = self.__data.get("outdir", ".")

        if "data_phs" in self.__data:
            outfile = "get_mtz_infor_phs.html"
        else:
            outfile = "get_mtz_infor.html"

        CGI_PATH = self.__data.get("cgi_bin", "")
        URL_USERS_DATA = self.__data.get("url_users_data", "")
        USERS_DATA = self.__data.get("users_data", "")
        path = self.__data.get("path", "")
        pdbid = self.__data.get("pdbid", "XXXX")
        numds = self.__data.get("mtz_man_html", 1)
        inpfile = self.__data["sf"]
        CCP4 = self.__data.get("CCP4", "")
        EXECUTE = self.__data.get("SF_EXEC", "")

        mtzdumpfile = os.path.join(outdir, "mtzdmp.log")

        gmi = GetMtzInfo()
        gmi.readmtz(inpfile)

        # Generate mtzdmp
        gmi.write_fake_mtzdump(mtzdumpfile)

        cdata = gmi.get_column_data()

        with open(outfile, "w") as fout:
            fout.write("<HTML> \n <Head>\n <TITLE> Semi-auto conversion of MTZ to mmCIF format</TITLE>\n </Head>\n")
            fout.write("<CENTER> <h3> Semi-auto conversion of MTZ to mmCIF format</h3></CENTER>\n")
            fout.write('<form ENCTYPE="multipart/form-data" Method="post" Action="%sconvert_man.py">\n' % CGI_PATH)
            fout.write('<p>INSTRUCTION: Select data item to match the appropriate <font color="blue"> SF PARAMETER </font> and click RUN to do conversion.\n')

            fout.write('<li> Data items in the uploaded MTZ can be seen <a href = "%s/%s/mtzdmp.log"  TARGET="other"> here </A>,\n' % (URL_USERS_DATA, path))
            fout.write('Details about the  MTZ format can be seen from  <a href = "https://www.ccp4.ac.uk/html/mtzformat.html" TARGET="other">CCP4</a>). </li>\n')

            fout.write("<li> Select FreeR value if it is not 0. </li>  \n")

            for idx in range(1, numds + 1):
                self.__write_mtz_data_4_html(fout, cdata, idx)

            fout.write('<INPUT TYPE=SUBMIT NAME="submit" VALUE="RUN"> \n')
            fout.write('<INPUT TYPE=RESET VALUE= "RESET">\n')
            fout.write("</center><p>\n")
            fout.write("\n")

            if inpfile.find("dir_") >= 0 and inpfile.find("/") >= 0:
                # rid of path
                start = inpfile.find("dir_") + 4
                file_new = inpfile[start:]
                pos = file_new.find("/")
                if pos >= 0:
                    start = pos + 1
                    file_new = file_new[start:]
            else:
                file_new = inpfile

            fout.write(f'<input type="hidden"  name="pdb_id" value="{pdbid}"> \n')
            fout.write(f'<input type="hidden"  name="infile" value="{file_new}"> \n')
            fout.write(f'<input type="hidden"  name="user_dir" value="{path}"> \n')

            fout.write(f'<input type="hidden"  name="url_users_data" value="{URL_USERS_DATA}"> \n')
            fout.write(f'<input type="hidden"  name="users_data" value="{USERS_DATA}"> \n')
            fout.write(f'<input type="hidden"  name="sf_convert" value="{EXECUTE}"> \n')
            fout.write(f'<input type="hidden"  name="ccp4" value="{CCP4}"> \n')
            fout.write(f'<input type="hidden"  name="data_set" value="{numds}"> \n')
            fout.write('<input type="hidden"  name="html_type" value="mtz"> \n')

            fout.write("\n</form>\n")

        return outfile

    def __write_mtz_data_4_html(self, fout, cdata, idx):
        """Write HTML fragment for dataset idx to fout based on cdata"""

        align = "center"

        fout.write('<center>\n <table align=center cellpadding=8 bgcolor="#CEF6F5">\n')
        fout.write(f"<b><p>Data Column Selector (Data Set {idx}) </b>\n")
        fout.write("<tr>\n")
        fout.write('<td align=center><b><font color="blue"> SF PARAMETER </font>  <b></td>\n')
        fout.write('<td align=center><b><font color="blue"> COLUMN USED IN<br> UPLOADED FILE  </font>  <b></td>\n')
        fout.write('<td align=center><b><font color="blue"> SF PARAMETER </font>  <b></td>\n')
        fout.write('<td align=center><b><font color="blue"> COLUMN USED IN<br> UPLOADED FILE  </font>  <b></td>\n')
        fout.write(" </tr>\n")

        # Fp and SigmaFP
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Native data amplitude (FP):", "fp", idx, cdata)
        self.__write_data_column(fout, align, "Sigma (SIGFP):", "sigfp", idx, cdata)
        fout.write(" </tr>\n")

        # Mean intensity sigma(IMEAN).
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Mean intensity (I):", "i", idx, cdata)
        self.__write_data_column(fout, align, "Sigma (SIGI): ", "sigi", idx, cdata)
        fout.write(" </tr>\n")

        # FreeR test
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Free R flag :", "free", idx, cdata)
        self.__write_data_column(fout, align, "FreeR value:", "freer", idx, cdata)
        fout.write(" </tr>\n")

        # I(+) and SigmaI(+)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Intensity (I(+))", "iplus", idx, cdata)
        self.__write_data_column(fout, align, "Sigma (SIGI(+))", "sigiplus", idx, cdata)
        fout.write(" </tr>\n")

        # I(-) and SigmaI(-)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Intensity (I(-))", "ineg", idx, cdata)
        self.__write_data_column(fout, align, "Sigma  (SIGI(-))", "sigineg", idx, cdata)
        fout.write(" </tr>\n")

        # F(+) and SigmaF(+)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Amplitude (F(+))", "fplus", idx, cdata)
        self.__write_data_column(fout, align, "Sigma (SIGF(+))", "sigfplus", idx, cdata)
        fout.write(" </tr>\n")

        # F(-) and SigmaF(-)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Amplitude (F(-))", "fneg", idx, cdata)
        self.__write_data_column(fout, align, "Sigma  (SIGF(-))", "sigfneg", idx, cdata)
        fout.write(" </tr>\n")

        # Calculated F (FC).Calculated Phase (PHIC)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Calculated F (FC):", "fc", idx, cdata)
        self.__write_data_column(fout, align, "Calculated Phase (PHIC):", "phic", idx, cdata)
        fout.write(" </tr>\n")

        # ABCD H/L coefficients (HLA,HLB,HLC,HLD)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "H/L coefficients (HLA):", "hla", idx, cdata)
        self.__write_data_column(fout, align, "H/L coefficients (HLB):", "hlb", idx, cdata)
        fout.write(" </tr>\n")

        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "H/L coefficients (HLC):", "hlc", idx, cdata)
        self.__write_data_column(fout, align, "H/L coefficients (HLD):", "hld", idx, cdata)
        fout.write(" </tr>\n")

        # DP and SigmaDP (Anomalous difference for native data)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Anomalous difference(DP)", "dp", idx, cdata)
        self.__write_data_column(fout, align, "Sigma  (SIGDP)", "sigdp", idx, cdata)
        fout.write(" </tr>\n")

        # figure of merit  (FOM) observed phase (PHIB)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Figure of merit  (FOM):", "fom", idx, cdata)
        self.__write_data_column(fout, align, "Observed phase (PHIB):", "phib", idx, cdata)
        fout.write(" </tr>\n")

        # MAP Coefficients and phases for 2Fo-Fc map (FWT, PHWT)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "2Fo-Fc map coeff. (FWT):", "fwt", idx, cdata)
        self.__write_data_column(fout, align, "2Fo-Fc map phases (PHWT):", "phwt", idx, cdata)
        fout.write(" </tr>\n")

        # MAP Coefficients and phases for Fo-Fc map (DELFWT, DELPHWT)
        fout.write("<tr>\n")
        self.__write_data_column(fout, align, "Fo-Fc map coeff. (DELFWT):", "delfwt", idx, cdata)
        self.__write_data_column(fout, align, "Fo-Fc map phases (DELPHWT):", "delphwt", idx, cdata)
        fout.write(" </tr>\n")

        #
        fout.write("</table>\n")

    def __write_data_column(self, fout, align, item_name, fname, ds_id, cdata):
        """Outputs columns"""

        filename = f"{fname}_{ds_id}"

        fout.write(f"<td align={align}%s><b>{item_name} &nbsp <b></td>\n")
        fout.write(f'<td><SELECT NAME="{filename}" WIDTH=10>\n')

        # get_labels(fout, k, sets, items, type, nitem, fname);
        rlabel = self.__get_labels(fout, ds_id, fname, cdata)

        fout.write('<OPTION VALUE=""> \n')

        if fname == "freer":
            for cnt in range(-1, 21):
                fout.write(f'<OPTION VALUE="{cnt}">{cnt}\n')
        else:
            for col in cdata[3:]:
                clabel = col["label"]
                if clabel in rlabel:
                    continue
                fout.write(f'<OPTION VALUE="{clabel}">{clabel}\n')

        fout.write("</SELECT> </td>\n")

    def __get_labels(self, fout, ds_id, fname, cdata):
        """Outputs label.  Returns list of labels added"""

        ret = []
        # Col 0,1,2 are always H/K/L
        for col in cdata[3:]:
            # If first dataset - list all pull downs.
            # If there is a single dataset - always
            # Otherwise only display column for the dataset
            if ds_id != 1 and cdata[-1]["dataset_id"] > 1 and col["dataset_id"] != ds_id:
                continue

            ctype = col["type"]
            clabel = col["label"]
            clabel_uc = clabel.upper()

            if ctype == "I" and fname == "free":
                if clabel_uc.find("FREE") >= 0 or clabel_uc.find("FLAG") >= 0 or clabel_uc.find("TEST") >= 0:
                    fout.write(f'<OPTION VALUE="{clabel}">{clabel}\n')
                    ret.append(clabel)

            elif (
                (ctype == "F" and clabel[0] == "F" and fname == "fp")
                or (ctype == "Q" and clabel_uc.find("SIGF") >= 0 and fname == "sigfp")
                or (ctype == "J" and clabel[0] == "I" and fname == "i")
                or (ctype == "Q" and clabel_uc.find("SIGI") >= 0 and fname == "sigi")
                or (ctype == "W" and clabel_uc.find("FOM") >= 0 and fname == "fom")
                or (ctype == "P" and clabel_uc.find("PHIB") >= 0 and fname == "phib")
                or (ctype == "F" and (clabel_uc.find("FC_ALL") >= 0 or (clabel_uc.find("F-MODEL"))) and fname == "fc")
                or (ctype == "P" and (clabel_uc.find("PHIC_ALL") >= 0 or (clabel_uc.find("PHIF-MODEL"))) and fname == "phic")
            ):
                fout.write(f'<OPTION VALUE="{clabel}">{clabel}\n')
                ret.append(clabel)

            elif (
                (ctype == "A" and clabel_uc.find("HLA") >= 0 and fname == "hla")
                or (ctype == "A" and clabel_uc.find("HLB") >= 0 and fname == "hlb")
                or (ctype == "A" and clabel_uc.find("HLC") >= 0 and fname == "hlc")
                or (ctype == "A" and clabel_uc.find("HLD") >= 0 and fname == "hld")
            ):
                fout.write(f'<OPTION VALUE="{clabel}">{clabel}\n')
                ret.append(clabel)

            elif (
                (ctype == "D" and clabel_uc[0] == "D" and fname == "dp")
                or (ctype == "Q" and clabel_uc.find("SIGD") >= 0 and fname == "sigdp")
                or (ctype == "G" and clabel_uc.find("(+)") >= 0 and clabel[0] == "F" and fname == "fplus")
                or (ctype == "L" and clabel_uc.find("(+)") >= 0 and clabel_uc[:4] == "SIGF" and fname == "sigfplus")
                or (ctype == "G" and clabel_uc.find("(-)") >= 0 and clabel[0] == "F" and fname == "fneg")
                or (ctype == "L" and clabel_uc.find("(-)") >= 0 and clabel_uc[:4] == "SIGF" and fname == "sigfneg")
                or (ctype == "K" and clabel_uc.find("(+)") >= 0 and clabel[0] == "I" and fname == "iplus")
                or (ctype == "M" and clabel_uc.find("(+)") >= 0 and clabel_uc[:4] == "SIGI" and fname == "sigiplus")
                or (ctype == "K" and clabel_uc.find("(-)") >= 0 and clabel[0] == "I" and fname == "ineg")
                or (ctype == "M" and clabel_uc.find("(-)") >= 0 and clabel_uc[:4] == "SIGI" and fname == "sigineg")
            ):
                fout.write(f'<OPTION VALUE="{clabel}">{clabel}\n')
                ret.append(clabel)
            elif (
                (ctype == "F" and clabel in ["2FOFCWT", "FWT"] and fname == "fwt")
                or (ctype == "P" and clabel in ["PH2FOFCWT", "PHWT"] and fname == "phwt")
                or (ctype == "F" and clabel in ["FOFCWT", "DELFWT"] and fname == "delfwt")
                or (ctype == "P" and clabel in ["PHFOFCWT", "PHDELWT"] and fname == "delphwt")
            ):
                fout.write(f'<OPTION VALUE="{clabel}">{clabel}\n')
                ret.append(clabel)

        return ret
