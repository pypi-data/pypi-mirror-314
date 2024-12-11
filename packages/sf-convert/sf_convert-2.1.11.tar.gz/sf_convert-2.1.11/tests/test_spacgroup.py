from sf_convert.utils.SpaceGroup import SpaceGroup

from sf_convert.utils.pinfo_file import PStreamLogger


class TestSpaceGroup:
    def test_sg_normalization(self):
        """Tests normalization of spacegroup names"""

        log = PStreamLogger()
        sg = SpaceGroup(log)

        tests = [
            ["P21", "P 1 21 1"],
            ["P212121", "P 21 21 21"],
            ["UNKNOWN", "UNKNOWN"]
        ]

        for t in tests:
            assert sg.standardize_sg_name(t[0]) == t[1]
