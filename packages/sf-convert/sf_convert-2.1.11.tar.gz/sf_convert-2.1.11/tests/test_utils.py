from mmcif.api.DataCategory import DataCategory
from sf_convert.utils.CifUtils import reorderCategoryAttr


class TestUtils:
    @staticmethod
    def test_attribute_reorder():
        """
        Tests the reordering of attributes in a category.

        Returns:
            None
        """
        attrList = ["a", "b", "c", "d", "e"]
        row_temp = ["something", "there", "maybe", "I"]
        rowlist = []
        for i in range(1, 10):
            tr = [i] + row_temp
            rowlist.append(tr)

        dc = DataCategory("something", attrList, rowlist)

        assert dc.getRowCount() == 9

        dout = reorderCategoryAttr(dc)
        assert dout == dc

        # Now test reordering

        dout = reorderCategoryAttr(dc, ["b", "fred", "a"])
        assert dout != dc

        assert dout.getAttributeList() == ["b", "a", "c", "d", "e"]

        assert dout.getValue("a", 2) == 3
