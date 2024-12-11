from sf_convert.sffile.sf_file import StructureFactorFile
from sf_convert.utils.version import get_version


class TestVersion:
    @staticmethod
    def test_get_version():
        """
        Tests if we can retrieve the version number.

        Returns:
            None
        """
        assert get_version() != ""

    @staticmethod
    def test_instantiate():
        """
        Tests if we can instantiate the StructureFactorFile class.

        Returns:
            None
        """
        s = StructureFactorFile()
        assert s
