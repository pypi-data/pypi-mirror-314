from mmcif.api.DataCategory import DataCategory


def reformat_sfhead(sf_file, pdb_id, logger, DETAIL=None):
    """
    Reformat the structure factor file by performing various operations.

    Args:
        sf_file (StructureFactorFile): The structure factor file object.
        logger: The logger object for logging messages.
        DETAIL: The detail value to be used for modifying the "details" attribute.

    Returns:
        bool: True if any changes were made, False otherwise.
    """
    changes_made = False
    remove_list = ["citation"]

    refln = {
        "A_calc_au": "A_calc",
        "B_calc_au": "B_calc",
        "A_cal": "A_calc",
        "B_cal": "B_calc",
        "resolution": "d_spacing",
        "Fc_au": "F_calc_au",
        "F_sigma": "F_meas_sigma_au",
        "F_meas_au_sigma": "F_meas_sigma_au",
        "F_squared_meas_sigma": "F_squared_sigma",
        "I_meas_au": "intensity_meas",
        "intensity": "intensity_meas",
        "intensity_meas_au": "intensity_meas",
        "intensity_sigm": "intensity_sigma",
        "I_meas_sigma_au": "intensity_sigma",
        "intensity_sigma_au": "intensity_sigma",
        "intensity_meas_sigma": "intensity_sigma",
        "intensity_meas_sigma_au": "intensity_sigma",
        "dfano": "pdbx_anom_difference",
        "DF_anomalous": "pdbx_anom_difference",
        "ccp4_phase_anom": "pdbx_anom_difference",
        "pdbx_phase_anom": "pdbx_anom_difference",
        "ccp4_anomalous_diff": "pdbx_anom_difference",
        "ccp4_SAD_phase_anom": "pdbx_anom_difference",
        "pdbx_anomalous_diff": "pdbx_anom_difference",
        "pdbx_SAD_phase_anom": "pdbx_anom_difference",
        "pdbx_anomalous_meas_au": "pdbx_anom_difference",
        "I_ano_meas": "pdbx_anom_difference",
        "I_ano_sigma": "pdbx_anom_difference_sigma",
        "DF_anomalous_sigma": "pdbx_anom_difference_sigma",
        "ccp4_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "pdbx_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "ccp4_anomalous_diff_sigma": "pdbx_anom_difference_sigma",
        "ccp4_SAD_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "pdbx_SAD_phase_anom_sigma": "pdbx_anom_difference_sigma",
        "pdbx_anomalous_meas_sigma_au": "pdbx_anom_difference_sigma",
        "F-_meas_au": "pdbx_F_minus",
        "pdbx_F_meas_minus": "pdbx_F_minus",
        "ccp4_F_meas_minus_au": "pdbx_F_minus",
        "pdbx_F_meas_minus_au": "pdbx_F_minus",
        "ccp4_SAD_F_meas_minus_au": "pdbx_F_minus",
        "F-_meas_sigma_au": "pdbx_F_minus_sigma",
        "pdbx_F_meas_minus_sigma": "pdbx_F_minus_sigma",
        "ccp4_F_meas_minus_sigma_au": "pdbx_F_minus_sigma",
        "pdbx_F_meas_minus_sigma_au": "pdbx_F_minus_sigma",
        "ccp4_SAD_F_meas_minus_sigma_au": "pdbx_F_minus_sigma",
        "F+_meas_au": "pdbx_F_plus",
        "pdbx_F_meas_plus": "pdbx_F_plus",
        "ccp4_F_meas_plus_au": "pdbx_F_plus",
        "pdbx_F_meas_plus_au": "pdbx_F_plus",
        "ccp4_SAD_F_meas_plus_au": "pdbx_F_plus",
        "F+_meas_sigma_au": "pdbx_F_plus_sigma",
        "pdbx_F_meas_plus_sigma": "pdbx_F_plus_sigma",
        "ccp4_F_meas_plus_sigma_au": "pdbx_F_plus_sigma",
        "pdbx_F_meas_plus_sigma_au": "pdbx_F_plus_sigma",
        "ccp4_SAD_F_meas_plus_sigma_au": "pdbx_F_plus_sigma",
        "pdbx_HLA": "pdbx_HL_A_iso",
        "ccp4_HL_A_iso": "pdbx_HL_A_iso",
        "ccp4_SAD_HL_A_iso": "pdbx_HL_A_iso",
        "pdbx_SAD_HL_A_iso": "pdbx_HL_A_iso",
        "pdbx_HLB": "pdbx_HL_B_iso",
        "ccp4_HL_B_iso": "pdbx_HL_B_iso",
        "ccp4_SAD_HL_B_iso": "pdbx_HL_B_iso",
        "pdbx_SAD_HL_B_iso": "pdbx_HL_B_iso",
        "pdbx_HLC": "pdbx_HL_C_iso",
        "ccp4_HL_C_iso": "pdbx_HL_C_iso",
        "ccp4_SAD_HL_C_iso": "pdbx_HL_C_iso",
        "pdbx_SAD_HL_C_iso": "pdbx_HL_C_iso",
        "pdbx_HLD": "pdbx_HL_D_iso",
        "ccp4_HL_D_iso": "pdbx_HL_D_iso",
        "ccp4_SAD_HL_D_iso": "pdbx_HL_D_iso",
        "pdbx_SAD_HL_D_iso": "pdbx_HL_D_iso",
        "ccp4_I_minus": "pdbx_I_minus",
        "ccp4_I_minus_sigma": "pdbx_I_minus_sigma",
        "ccp4_I_plus": "pdbx_I_plus",
        "ccp4_I_plus_sigma": "pdbx_I_plus_sigma",
        "pahse_calc": "phase_calc",
        "F.phase_calc": "phase_calc",
        "phase_au": "phase_meas",
        "sgx_fmap": "pdbx_FWT",
        "pdbx_fom_weighted_fmap": "pdbx_FWT",
        "statu": "status",
        "F_status": "status",
        "status_au": "status",
        "R_free_flag": "status",
        "phenix_R_free_flags": "pdbx_r_free_flag",
        "observed_status": "status",
        "waveLEngth_id": "wavelength_id",
        "wavelength_di": "wavelength_id",
        "index_l>": "index_l",
        "fiber_coordinate": "pdbx_fiber_coordinate",
        "fiber_F_meas_au": "pdbx_fiber_F_meas_au",
        "fiber_layer": "pdbx_fiber_layer",
        "F_squared_meas": "intensity_meas",
        "F_squared_sigma": "intensity_sigma",
        "gsas_i100_meas": "pdbx_gsas_i100_meas",
        "gphl_signal_type": "pdbx_signal_type",
        "gphl_observed_signal_threshold": "pdbx_observed_signal_threshold",
    }

    audit = {"update_recor": "update_record"}

    cell = {"enrty_id": "entry_id", "enry_id": "entry_id", "entry": "entry_id", "ndb_unique_axis": "pdbx_unique_axis"}

    diffrn = {"detail": "details"}

    symmetry = {"int_tables_number": "Int_Tables_number", "ndb_full_space_group_name_H-M": "space_group_name_H-M", "space_group_name_h-m": "space_group_name_H-M"}

    mapping_dicts = {"refln": refln, "audit": audit, "cell": cell, "diffrn": diffrn, "symmetry": symmetry}

    attributes_to_append = {"_diffrn": {"ambient_temp": "?", "crystal_treatment": "?"}}

    changes_made |= rename_sfhead(sf_file, mapping_dicts, logger)
    changes_made |= remove_sfhead(sf_file, remove_list, logger)
    changes_made |= remove_sfhead(sf_file, ["audit"], logger, 1)  # Remove audit from second and subsequent blocks
    changes_made |= fix_entry_ids(sf_file, pdb_id)
    changes_made |= add_audit_if_needed(sf_file, logger)
    # changes_made |= remove_duplicate_reflections(sf_file)

    block_names = sf_file.get_all_block_names()

    # If diffrn category present, add missing attributes
    for i in range(len(block_names)):
        block_name = block_names[i]
        old_order = sf_file.get_category_names(block_name)
        old_order_copy = old_order[:]

        _, block = sf_file.get_block_by_name(block_name)
        cobj = block.getObj("diffrn")
        if cobj:
            attributes_to_append = ["ambient_temp", "crystal_treatment"]
            changes_made = append_attributes(sf_file, "diffrn", attributes_to_append, block_name)

            if DETAIL:
                changes_made = modify_attribute_value(sf_file, "diffrn", "details", DETAIL, block_name)
                changes_made = modify_attribute_value(sf_file, "diffrn", "crystal_id", 1, block_name)

            sf_file.reorder_category_attributes("diffrn", ["id", "crystal_id", "ambient_temp", "crystal_treatment", "details"], block_name)
            sf_file.reorder_categories_in_block(old_order_copy, block_name)

    # Reorder to ensure we have what we need.
    changes_made |= reorder_sf_file(sf_file)
    return changes_made


def rename_sfhead(sf_file, mapping_dicts, logger):
    """
    Rename attributes in the structure factor file based on the provided mapping dictionaries.

    Args:
        sf_file (StructureFactorFile): The structure factor file object.
        mapping_dicts (dict): A dictionary containing the mapping dictionaries for each category.
        logger: The logger object for logging messages.

    Returns:
        bool: True if any changes were made, False otherwise.
    """
    changes_made = False
    for dict_name, mapping_dict in mapping_dicts.items():
        for block_index in range(sf_file.get_number_of_blocks()):
            block = sf_file.get_block_by_index(block_index)
            category_object = sf_file.get_category_object(dict_name, block.getName())
            if category_object:
                attributeList = category_object.getAttributeList()
                renameDict = {}
                for attr in attributeList:
                    if attr in mapping_dict:
                        renameDict[attr] = mapping_dict[attr]
                if renameDict:
                    changes_made = True
                    for old_name, new_name in renameDict.items():
                        logger.pinfo(f"Renaming {old_name} to {new_name} in {dict_name} category of block {block.getName()}", 0)
                category_object.renameAttributes(renameDict)
    return changes_made


def remove_sfhead(sf_file, remove_list, logger, start=0):
    """
    Remove categories from the structure factor file based on the provided remove list.

    Args:
        sf_file (StructureFactorFile): The structure factor file object.
        remove_list (list): A list of category names to remove.
        logger: The logger object for logging messages.

    Returns:
        bool: True if any changes were made, False otherwise.
    """
    changes_made = False
    for catname in remove_list:
        for block_index in range(start, sf_file.get_number_of_blocks()):
            block = sf_file.get_block_by_index(block_index)
            removed_flag = sf_file.remove_category_by_name(catname, block.getName())
            if removed_flag:
                changes_made = True
                logger.pinfo(f"Removing {catname} category from block {block.getName()}", 0)
    return changes_made


# def remove_duplicate_reflections(sf_file):
#     """
#     Remove duplicate reflections from the structure factor file.

#     Args:
#         sf_file (StructureFactorFile): The structure factor file object.

#     Returns:
#         bool: True if any changes were made, False otherwise.
#     """
#     changes_made = False
#     total_blocks = sf_file.get_number_of_blocks()
#     for block_index in range(total_blocks):
#         block = sf_file.get_block_by_index(block_index)
#         changes_made |= sf_file.remove_duplicates_in_category('refln', block.getName())
#     return changes_made


def append_attributes(sf_file, category_name, attributes, block_name=None):
    """
    Append attributes to a category within a block.

    Args:
        sf_file (StructureFactorFile): The structure factor file object.
        category_name (str): The name of the category to append attributes to.
        attributes (list): A list of attribute names to append.
        block_name (str, optional): The name of the block to append attributes to.
                                    If not provided, the default block is used.

    Returns:
        bool: True if any changes were made, False otherwise.
    """
    changes_made = False

    # Get the block (use default block if block_name is None)
    if block_name:
        _, block = sf_file.get_block_by_name(block_name)
    else:
        block = sf_file.get_block_by_index(sf_file.get_default_block_index())

    if not block:
        return changes_made

    category = block.getObj(category_name)
    # If category doesn't exist, create it
    if not category:
        category = DataCategory(category_name)
        block.append(category)
        changes_made = True

    # Check each attribute and append if not present
    for attr_name in attributes:
        if not category.hasAttribute(attr_name):
            category.appendAttributeExtendRows(attr_name)
            changes_made = True

    return changes_made


def modify_attribute_value(sf_file, category_name, attribute_name, new_value, block_name=None):
    """
    Modify the value of a specified attribute in a given category within a block.

    Args:
        sf_file (StructureFactorFile): The structure factor file object.
        category_name (str): The name of the category containing the attribute.
        attribute_name (str): The name of the attribute to modify.
        new_value: The new value to set for the attribute.
        block_name (str, optional): The name of the block containing the category.
                                    If not provided, the default block is used.

    Returns:
        bool: True if the value was modified, False otherwise.
    """
    # Get the block (use default block if block_name is None)
    if block_name:
        _, block = sf_file.get_block_by_name(block_name)
    else:
        block = sf_file.get_block_by_index(sf_file.get_default_block_index())

    if not block:
        return False

    category = block.getObj(category_name)
    # If category doesn't exist, return False
    if not category:
        return False

    # Fetch the old value using getValueOrDefault
    old_value = category.getValueOrDefault(attribute_name, rowIndex=0, defaultValue=".")
    if old_value is not None:
        # Replace the old value with the new value
        num_replaced = category.replaceValue(old_value, new_value, attribute_name)
        return num_replaced > 0

    return False


def fix_entry_ids(sf_file, pdbid):
    """Corrects entry ids where needed:

        Args:
        sf_file (StructureFactorFile): The structure factor file object.
        pdbid (str): The pdb_id
        logger: The logger object for logging messages.

    Returns:
        bool: True if the value was modified, False otherwise.
    """

    updates = [
        ["entry", "id"],
        ["cell", "entry_id"],
        ["symmetry", "entry_id"],
        ["reflns", "entry_id"],
    ]

    changes = False
    for idx in range(sf_file.get_number_of_blocks()):
        blk = sf_file.get_block_by_index(idx)

        for upd in updates:
            cat = upd[0]
            attr = upd[1]
            cobj = blk.getObj(cat)
            if not cobj:
                continue
            if not cobj.hasAttribute(attr):
                continue

            # Should only be a single row for these categories - but let's be aggressive
            for row in range(cobj.getRowCount()):
                val = cobj.getValue(attr, row)
                if val != pdbid:
                    cobj.setValue(pdbid, attr, row)
                    changes = True

    return changes


def add_audit_if_needed(sf_file, logger):
    """Add audit record if missing from first block

        Args:
        sf_file (StructureFactorFile): The structure factor file object.
        logger: The logger object for logging messages.

    Returns:
        bool: True if the value was modified, False otherwise.
    """

    blk = sf_file.get_block_by_index(0)
    cobj = blk.getObj("audit")
    if cobj:
        return False

    aCat = DataCategory("audit")
    aCat.appendAttribute("revision_id")
    aCat.appendAttribute("creation_date")
    aCat.appendAttribute("update_record")
    aCat.append(["1_0", "?", "Initial release"])

    blk.append(aCat)

    logger.pinfo("Note: File has no _audit. (auto added)", 0)
    return True


def reorder_sf_file(sf_file):
    """Reorders sf_file with a few key items on top in specific order

    Args:
        sf_file (StructureFactorFile): The structure factor file object.

    """

    earlyorder = [
        "audit",
        "cell",
        "diffrn",
        "diffrn_radiation",
        "diffrn_radiation_wavelength",
        "diffrn_reflns",
        "diffrn_scale_group",
        "diffrn_standard_refln",
        "entry",
        "exptl_crystal",
        "reflns_scale",
        "symmetry",
    ]
    lateorder = ["refln", "diffrn_refln"]

    allbnames = sf_file.get_all_block_names()

    modified = False
    for bname in allbnames:
        catnames = sf_file.get_category_names(bname)

        ordered = []
        used = {}

        # First ones
        for cat in earlyorder:
            if cat in catnames:
                ordered.append(cat)
                used[cat] = True

        # Get middle
        for cat in catnames:
            if cat in lateorder:
                continue
            if cat in used:
                continue
            ordered.append(cat)
            used[cat] = True

        # Late
        for cat in lateorder:
            if cat in catnames and cat not in used:
                ordered.append(cat)
                used[cat] = True

        if catnames != ordered:
            # Reorder
            sf_file.reorder_categories_in_block(ordered, bname)
            modified = True

    return modified
