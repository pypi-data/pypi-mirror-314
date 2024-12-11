from mmcif.api.DataCategory import DataCategory


def reorderCategoryAttr(cobjIn, attrList=None):
    """
    Returns a new category with the attribute list reordered.

    Args:
        cobjIn (DataCategory): The input category object.
        attrList (list, optional): The desired order of attribute names. Defaults to None.

    Returns:
        DataCategory: The new category with the reordered attributes.
    """
    if attrList is None:
        attrList = []

    name_in = cobjIn.getName()
    attl_in = cobjIn.getAttributeList()

    d_in = []
    for row in range(cobjIn.getRowCount()):
        d = cobjIn.getRowAttributeDict(row)
        d_in.append(d)

    # Create new attribute name list based on what is present.
    used = {}
    newlist = []

    for att in attrList:
        if att in attl_in:
            newlist.append(att)
            used[att] = 1

    # Get rest
    for att in attl_in:
        if att not in used:
            newlist.append(att)

    newcat = DataCategory(name_in, newlist, d_in, copyInputData=True)

    return newcat
