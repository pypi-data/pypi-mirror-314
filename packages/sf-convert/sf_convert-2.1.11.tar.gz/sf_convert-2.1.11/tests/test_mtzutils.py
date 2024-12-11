import os
from sf_convert.utils.MtzUtils import GetMtzInfo


class TestMtzUtils:
    def test_gen_mtzdump(self, tmp_path, mtz_Ras_NAD_data_path):
        """
        Tests generating a simple mtzdump file

        Returns:
            None
        """
        gmi = GetMtzInfo()
        gmi.readmtz(mtz_Ras_NAD_data_path)

        outfile = os.path.join(tmp_path, "mtzdump.log")
        gmi.write_fake_mtzdump(outfile)

        assert os.path.exists(outfile)

        with open(outfile, "r") as fin:
            lines = fin.readlines()

        assert len(lines) > 20
