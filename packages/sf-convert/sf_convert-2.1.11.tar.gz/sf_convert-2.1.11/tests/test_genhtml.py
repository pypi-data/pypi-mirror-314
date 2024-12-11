import os
from sf_convert.utils.GenMtzHtml import GenMtzHtml


class TesGenHtml:
    def test_gen_mtz_html(self, tmp_path, mtz_Ras_NAD_data_path):
        """
        Tests generating an html form.

        Returns:
            None
        """

        d = {"mtz_man_html": 1, "sf": mtz_Ras_NAD_data_path, "outdir": tmp_path}

        gmh = GenMtzHtml(d)
        outfile = gmh.genMtzInfor()

        assert os.path.exists(outfile)

        with open(outfile, "r") as fin:
            lines = fin.readlines()

        assert len(lines) > 50
