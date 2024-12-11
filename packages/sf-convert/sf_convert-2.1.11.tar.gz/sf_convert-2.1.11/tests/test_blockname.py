from sf_convert.sffile.sf_file import StructureFactorFile


class TestBlockNanms:
    @staticmethod
    def test_datablock_simple():
        """
        Checks a few block ids that are expected
        """

        tests = [
            [0, "rabcdsf"],
            [1, "rabcdAsf"],
            [10, "rabcdJsf"],
            [26, "rabcdZsf"],
            [27, "rabcdAAsf"],
            [36, "rabcdJAsf"],
            [37, "rabcdKAsf"],
            [38, "rabcdLAsf"],
            [100, "rabcdVCsf"],
            [500, "rabcdFSsf"],
        ]

        sf = StructureFactorFile()

        pdbid = "abcd"
        for test in tests:
            blkidx = test[0]
            refblkname = test[1]

            blkname = sf.generate_expected_block_name(pdbid, blkidx)
            assert blkname == refblkname, f"{blkname} != {refblkname} for {blkidx}"

    @staticmethod
    def test_datablock_unique():
        """Tests that a case insensitive block name is unique"""

        pdbid = "1234"

        sf = StructureFactorFile()

        seen = {}
        for idx in range(5000):
            blkname = sf.generate_expected_block_name(pdbid, idx).lower()

            assert blkname not in seen
            seen[blkname] = 1
