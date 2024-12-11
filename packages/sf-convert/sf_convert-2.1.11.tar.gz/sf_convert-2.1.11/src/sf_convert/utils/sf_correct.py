# Utilities to correct imported CIF files

import math

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import CifName

from sf_convert.utils.reformat_sfhead import reformat_sfhead, reorder_sf_file
from sf_convert.utils.dict_filter import DictFilter


class SfCorrect:
    def __init__(self, logger, legacy=True):
        self.__legacy = legacy
        self.__logger = logger
        self.__stdorder = [
            "crystal_id",
            "wavelength_id",
            "scale_group_code",
            "index_h",
            "index_k",
            "index_l",
            "status",
            "pdbx_r_free_flag",
            "F_meas_au",
            "F_meas_sigma_au",
            "intensity_calc",
            "intensity_meas",
            "intensity_sigma",
            "F_calc",
            "F_calc_au",
            "F_squared_meas",
            "F_squared_calc",
            "F_squared_sigma",
            "phase_calc",
            "phase_meas",
            "pdbx_I_plus",
            "pdbx_I_plus_sigma",
            "pdbx_I_minus",
            "pdbx_I_minus_sigma",
            "pdbx_F_plus",
            "pdbx_F_plus_sigma",
            "pdbx_F_minus",
            "pdbx_F_minus_sigma",
            "pdbx_HL_A_iso",
            "pdbx_HL_B_iso",
            "pdbx_HL_C_iso",
            "pdbx_HL_D_iso",
            "pdbx_anom_difference",
            "pdbx_anom_difference_sigma",
            "d_spacing",
            "A_calc",
            "B_calc",
            "F_meas_sigma_uncorrected",
            "F_meas_uncorrected",
            "pdbx_gsas_i100_meas",
            "intensity_meas_unknown",
            "intensity_sigma_unknown",
            "pdbx_phase_calc_part_solvent",
            "pdbx_F_calc_part_solvent",
            "pdbx_F_calc_with_solvent",
            "pdbx_phase_calc_with_solvent",
            "pdbx_FWT",
            "pdbx_PHWT",
            "pdbx_DELFWT",
            "pdbx_DELPHWT",
            "fom",
            "pdbx_fiber_coordinate",
            "pdbx_fiber_F_meas_au",
            "pdbx_fiber_layer",
            "weight",
        ]

        self.__unmergedorder = [
            "diffrn_id",
            "crystal_id",
            "wavelength_id",
            "id",
            "standard_code",
            "scale_group_code",
            "index_h",
            "index_k",
            "index_l",
            "intensity_meas",
            "intensity_sigma",
        ]

    def get_pdbid(self, sffile):
        """Returns the PDB id from datablock name of sf"""
        return sffile.extract_pdbid_from_block()

    def annotate_wavelength(self, sffile, pdb_id, setwlarg):
        """
        Handles addition of wavelength to the SF file if needed

        Args:
        sffile: SFFile object
        setlwarg: Wavelength to set
        """

        cat = "diffrn_radiation_wavelength"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                if "wavelength" not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows("wavelength")
                curwave = cObj.getValue("wavelength", 0)
            else:
                curwave = None

            setwl = "."
            setwlf = 0.0

            try:
                if setwlarg:
                    setwl = setwlarg
                    setwlf = float(setwlarg)
            except ValueError:
                self.__logger.pinfo("Error: trying to set wavelength to non float", 0)

            if curwave is not None:
                # Category present, attribute available - could bt "."
                if curwave not in ["?", "."]:
                    try:
                        wave = float(curwave)
                        if wave > 2.0 or wave < 0.6:
                            self.__logger.pinfo(f"Warning: ({pdb_id} nblock={idx} wavelength value {curwave} is abnormal (double check)!", 0)
                    except ValueError:
                        # Wavelnegth might be a range
                        self.__logger.pinfo(f"Wavelength not a float {curwave}", 0)
                        wave = None

                    if setwl != ".":
                        if setwlf > 0.8 and setwlf < 1.8 and setwlf != 1.0 and wave:
                            if abs(setwlf - wave) > 0.0001 and idx == 0:
                                self.__logger.pinfo(f"Warning: ({pdb_id} nblock={idx}) wavelength mismatch (pdb= {setwlf} : sf= {curwave})!", 0)
                            elif setwlf > 0 and abs(setwlf - wave) > 0.0001 and idx == 0:
                                self.__logger.pinfo("Warning: ({pdb_id} nblock={idx}) wavelength mismatch (pdb= {setwlf} : sf= {curwave}). (double check!)", 0)

                # Set the values....
                for row in range(cObj.getRowCount()):
                    cObj.setValue(setwl, "wavelength", row)

            else:
                # Create category - for dictionary compliance purposes. Might not be needed depending on data.
                # Decision to instantiate always for backwards compatibility - for potential outsider use.

                # Ensure proper values produced if existing data present
                cObj = blk.getObj("refln")
                wl = setwlarg if setwlarg else "."

                if cObj and "wavelength_id" in cObj.getAttributeList():
                    values = cObj.getAttributeUniqueValueList("wavelength_id")
                    data = []
                    for val in values:
                        data.append([val, wl])
                else:
                    data = [["1", wl]]

                newObj = DataCategory(cat, ["id", "wavelength"], data)
                blk.append(newObj)
                self.__logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def __instantiate_diffrn_rad_wavelength(self, sffile):
        """Instantiate diffrn_radiation_wavelength if needed.  In case wavelength is not set, but needed for dictionary purposes"""

        cat = "diffrn_radiation_wavelength"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                continue

            # Instantiate if needed
            cObj = blk.getObj("refln")
            if not cObj:
                continue
            if "wavelength_id" not in cObj.getAttributeList():
                continue

            values = cObj.getAttributeUniqueValueList("wavelength_id")

            data = []
            for val in values:
                data.append([val, "."])

            newObj = DataCategory(cat, ["id", "wavelength"], data)
            blk.append(newObj)
            self.__logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def __instantiate_diffrn_scale_group(self, sffile):
        """Instantiate diffrn_scale_group needed if dirrn_refln.scale_group_code present."""

        cat = "diffrn_scale_group"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                continue

            # Instantiate if needed
            cObj = blk.getObj("diffrn_refln")
            if not cObj:
                continue
            if "scale_group_code" not in cObj.getAttributeList():
                continue

            values = cObj.getAttributeUniqueValueList("scale_group_code")

            data = []
            for val in values:
                data.append([val])

            newObj = DataCategory(cat, ["code"], data)
            blk.append(newObj)
            self.__logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def __instantiate_diffrn_standard_refln(self, sffile):
        """Instantiate diffrn_standard_refln if diffrrn_refln.standard_code present."""

        cat = "diffrn_standard_refln"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                continue

            # Instantiate if needed
            cObj = blk.getObj("diffrn_refln")
            if not cObj:
                continue

            if "standard_code" not in cObj.getAttributeList():
                continue

            # We "assume" diffrn_id is in file.  So far good assumption.

            values = self.__getUniqueTuples(cObj, ["standard_code", "diffrn_id"])
            if not values:
                # Error already given
                continue

            # Assemble data needed - we need Miller index for code
            data = []
            for v in values:
                sc = v[0]
                di = v[1]

                for row in range(cObj.getRowCount()):
                    if cObj.getValue("standard_code", row) == sc and cObj.getValue("diffrn_id", row) == di:
                        ah = cObj.getValue("index_h", row)
                        ak = cObj.getValue("index_k", row)
                        al = cObj.getValue("index_l", row)
                        data.append([sc, di, ah, ak, al])
                        break

            newObj = DataCategory(cat, ["code", "diffrn_id", "index_h", "index_k", "index_l"], data)
            blk.append(newObj)
            self.__logger.pinfo(f"Creating {cat} in nblock={idx}", 0)

    def handle_standard(self, sffile, pdbid):
        """Handles standard operations"""

        detail = None

        # for idx in range(sffile.get_number_of_blocks()):
        #     blk = sffile.get_block_by_index(idx)
        #     print(blk.printIt())

        self.__update_exptl_crystal(sffile)

        if self.__legacy:
            self.__remove_similar_refln_attr(sffile)

        if self.__legacy:
            # pdbx_audit_conform used here
            self.__handle_legacy_attributes(sffile)

        self.__update_reflns_scale(sffile)

        if self.__legacy:
            self.__update_pdbx_r_free_flag(sffile)

        self.__update_status(sffile)

        if self.__legacy:
            self.__remove_categories(sffile)

        if self.__legacy:
            self.__cleanup_symmetry(sffile)

        self.__ensure_catkeys(sffile, pdbid)

        self.__instantiate_exptl_crystal(sffile)

        self.__instantiate_entry(sffile, pdbid)

        self._cleanup_audit(sffile)

        # pdbx_audit_conform will be removed here
        self.__remove_pdbx_audit_conform(sffile)

        if sffile.get_number_of_blocks() == 0:
            return

        # This reorders categories as well
        reformat_sfhead(sffile, pdbid, self.__logger, detail)

        # Remap category names if duplicates from refln to diffrn_refln.
        self.remap_unmerged(sffile)

        # See if diffrn_scale_group is needed if diffrn_refln.scale_group_code present
        self.__instantiate_diffrn_scale_group(sffile)

        # See if diffrn_standard_refln is needed if diffrrn_refln.standard_code present
        self.__instantiate_diffrn_standard_refln(sffile)

        # Might have removed all data if model file uploaded
        if sffile.get_number_of_blocks() == 0:
            return

        # Reflns names might have been modified
        self.__handle_reflns(sffile)

        # Creates diffrn category if need be....
        self.__handle_diffrn(sffile, pdbid, details=detail)

        # Renames diffrn_radiation to diffrn_radiation__wavelength if needed
        self.__rename_diffrn_radiation(sffile)

        self.__instantiate_diffrn_rad_wavelength(sffile)

        sffile.correct_block_names(pdbid)

        # Add status column if missing
        self.__instantiate_refln_status(sffile)

        # In case some blocks need updating
        self.__reorder_refln_all(sffile)

        self.__reorder_symmetry(sffile)

        self.__ensure_pdbx_r_free_flag_int(sffile)

        # Remove improper attributes
        self.__filter_attributes(sffile)

        self.__reorder_sf_file(sffile)

    def __handle_legacy_attributes(self, sffile):
        """Adds in _refln.crystal_id, refln.wavelength_id and refln.scale_group_code if need be"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            # For new data coming from staraniso, these attributes are not added
            if "pdbx_audit_conform" in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            for attr in ["crystal_id", "wavelength_id", "scale_group_code"]:
                if attr not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows(attr, "1")

    def __remove_similar_refln_attr(self, sffile):
        """Remove common "similar" columns"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            pairs = [
                [["F_meas_au", "F_meas_sigma_au"], ["F_meas", "F_meas_sigma"]],
            ]

            attrlist = cObj.getAttributeList()
            for p in pairs:
                r1 = p[0]
                r2 = p[1]

                if r1[0] in attrlist and r1[1] in attrlist and r2[0] in attrlist and r2[1] in attrlist:
                    cObj.removeAttribute(r2[0])
                    cObj.removeAttribute(r2[1])

    def __update_reflns_scale(self, sffile):
        """If reflns_scale missing in datablock add if needed"""

        cat = "reflns_scale"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if cat in blk.getObjNameList():
                continue

            if "refln" not in blk.getObjNameList():
                continue

            # See if need to instantiate
            cObj = blk.getObj("refln")
            if cObj and "scale_group_code" in cObj.getAttributeList():
                values = cObj.getAttributeUniqueValueList("scale_group_code")
                data = []
                for val in values:
                    data.append([val])
                newObj = DataCategory(cat, ["group_code"], data)
                blk.append(newObj)

    def __update_pdbx_r_free_flag(self, sffile):
        """Old sf_convert used to use atoi(value) -- for "?" this converts to 0.  Luckily appears only for map coefficients"""
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "refln" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if cObj is None:
                continue  # should never happen

            if "pdbx_r_free_flag" in cObj.getAttributeList():
                cObj.replaceValue("?", "0", "pdbx_r_free_flag")

    def __update_status(self, sffile):
        """Old sf_convert used to use assume empty data is x."""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "refln" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("refln")
            if cObj is None:
                continue  # should never happen

            if "status" in cObj.getAttributeList():
                cObj.replaceValue("?", "x", "status")
                cObj.replaceValue(".", "x", "status")

    def __remove_categories(self, sffile):
        """Backwards compatibility - remove some categories"""

        cats = ["space_group", "space_group_symop"]
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            for cat in cats:
                if cat in blk.getObjNameList():
                    blk.remove(cat)

    def ensure_catkeys(self, sffile, pdbid):
        """Fix entry_id in categories - public"""
        self.__ensure_catkeys(sffile, pdbid)

    def __ensure_catkeys(self, sffile, pdbid):
        """Sometimes categories come in without the entry_id.  Add"""

        cats = ["cell", "symmetry"]

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            for cat in cats:
                if cat in blk.getObjNameList():
                    cObj = blk.getObj(cat)
                    if "entry_id" not in cObj.getAttributeList():
                        cObj.appendAttributeExtendRows("entry_id", pdbid)
                        # entry_id first in category
                        sffile.reorder_category_attributes(cat, ["entry_id"], blk.getName())

    def __instantiate_exptl_crystal(self, sffile):
        """If refln.crystal_id is present, exptl_crystal must be present"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "refln" in blk.getObjNameList():
                cObj = blk.getObj("refln")
                if "crystal_id" not in cObj.getAttributeList():
                    continue

                if "exptl_crystal" not in blk.getObjNameList():
                    values = cObj.getAttributeUniqueValueList("crystal_id")
                    data = []
                    for val in values:
                        data.append([val])

                    newObj = DataCategory("exptl_crystal", ["id"], data)
                    blk.append(newObj)

    def __instantiate_entry(self, sffile, pdb_id):
        """If entry category is not present, create"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "entry" not in blk.getObjNameList():
                newObj = DataCategory("entry", ["id"], [[pdb_id]])
                blk.append(newObj)

    def __cleanup_symmetry(self, sffile):
        """If symmetry is present, we only allow entry_id and space_group_name_H-M"""

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            if "symmetry" not in blk.getObjNameList():
                continue

            cObj = blk.getObj("symmetry")

            attrlist = list(cObj.getAttributeList())  # ensure not an iterator that might get changed

            for attr in attrlist:
                if attr not in ["entry_id", "space_group_name_H-M", "Int_Tables_number"]:
                    cObj.removeAttribute(attr)

            # Remove "empty" category
            attrlist = cObj.getAttributeList()
            if len(attrlist) == 0 or attrlist == ["entry_id"]:
                blk.remove("symmetry")

    def __handle_diffrn(self, sffile, pdbid, details=None):  # pylint: disable=unused-argument
        """Instantiate diffrn category if needed, seet diffrn.id if needed.
        Enforces integer diffrn_ids
        """

        cats = ["diffrn_refln", "diffrn_radiation", "diffrn_reflns"]

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            # Assemble list of possible diffrn_ids needed

            # Get diffrn ids if present...
            difids = set()

            needdiffrn = False
            for cat in cats:
                if cat in blk.getObjNameList():
                    cObj2 = blk.getObj(cat)
                    if "diffrn_id" in cObj2.getAttributeList():
                        values = cObj2.getAttributeUniqueValueList("diffrn_id")
                        difids.update(values)
                        needdiffrn = True

            if len(difids) == 0:
                difids.add("1")

            # Remap if non-integral....
            remap = {}
            cur = 1
            for d in difids:
                try:
                    int(d)
                except:  # noqa: E722 pylint: disable=bare-except
                    while str(cur) in difids:
                        cur += 1
                    remap[d] = str(cur)
                    cur += 1  # For next item....

            if len(remap) > 0:
                # Remap as needed
                for cat in cats:
                    if cat in blk.getObjNameList():
                        cObj2 = blk.getObj(cat)
                        if "diffrn_id" in cObj2.getAttributeList():
                            for row in range(cObj2.getRowCount()):
                                val = cObj2.getValue("diffrn_id", row)
                                if val in remap:
                                    cObj2.setValue(remap[val], "diffrn_id", row)
                for k, v in remap.items():
                    difids.discard(k)
                    difids.add(v)

            # Create a mapping if need be???? Should be numeric
            diffidsl = sorted([int(x) for x in list(difids)])

            # Crystal id
            if "refln" in blk.getObjNameList():
                cObj2 = blk.getObj("refln")
                if "crystal_id" not in cObj2.getAttributeList():
                    crystids = ["1"]
                else:
                    crystids = cObj2.getAttributeUniqueValueList("crystal_id")
            else:
                crystids = ["1"]

            # If we need to instantiate do it
            if "diffrn" not in blk.getObjNameList() and needdiffrn is False and details is None:
                continue

            cObj = blk.getObj("diffrn")
            if cObj is None:
                # Instantiate category
                rows = []
                if details is None:
                    details = "?"
                for d in diffidsl:
                    for c in crystids:
                        rows.append([d, c, details])
                newObj = DataCategory("diffrn", ["id", "crystal_id", "details"], rows)
                blk.append(newObj)
                continue

            # Update existing copy
            if "id" not in cObj.getAttributeList():
                cObj.appendAttributeExtendRows("id", diffidsl[0])
            if "crystal_id" not in cObj.getAttributeList():
                cObj.appendAttributeExtendRows("crystal_id", crystids[0])
            if details and "details" not in cObj.getAttributeList():
                cObj.appendAttributeExtendRows("details", details)

            sffile.reorder_category_attributes("diffrn", ["id", "crystal_id", "ambient_temp", "crystal_treatment", "details"], blk.getName())

    def _cleanup_audit(self, sffile):
        """Cleanup audit records that should not be present

        Args:
            sffile (StructureFactorFile): The structure factor file object.

        Returns:
            None: True if the value was modified, False otherwise.
        """
        if sffile.get_number_of_blocks() == 0:
            return False

        blk = sffile.get_block_by_index(0)

        cat = "audit"
        cObj = blk.getObj(cat)
        if cObj is None:
            return False

        curlist = cObj.getAttributeList()

        allowed = ["revision_id", "creation_date", "update_record"]

        upd = False
        for attr in curlist:
            if attr not in allowed:
                cObj.removeAttribute(attr)
                self.__logger.pinfo(f"Warning: block has unwanted CIF item _{cat}.{attr} and is removed", 0)
                upd = True

        return upd

    def __remove_pdbx_audit_conform(self, sffile):
        """Remove pdbx_audit_conform from final file

        Args:
            sffile (StructureFactorFile): The structure factor file object.

        Returns:
            None
        """
        if sffile.get_number_of_blocks() == 0:
            return

        cat = "pdbx_audit_conform"
        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            if cat in blk.getObjNameList():
                blk.remove(cat)
                self.__logger.pinfo(f"Removing {cat} category from block {blk.getName()}", 0)

                blk = sffile.get_block_by_index(0)

    def __handle_reflns(self, sffile):
        """Handles reflns and diffrn_reflns data

        Assumption: diffrn_id is 1 if not provided

        diffrn_reflns and reflns are merged to diffrn_reflns
        """

        def get_val(attr_ref, attr_dif):
            val = None
            if cObjref and attr_ref in cObjref.getAttributeList():
                val = cObjref.getValue(attr_ref, 0)
            if val is None and cObjdif and attr_dif in cObjdif.getAttributeList():
                val = cObjdif.getValue(attr_dif, 0)

            return val

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObjdif = blk.getObj("diffrn_reflns")
            cObjref = blk.getObj("reflns")

            if cObjdif is None and cObjref is None:
                continue

            props = [
                ["resh", "d_resolution_high", "pdbx_d_res_high"],
                ["resl", "d_resolution_low", "pdbx_d_res_low"],
                ["hmax", "limit_h_max", "limit_h_max"],
                ["hmin", "limit_h_min", "limit_h_min"],
                ["kmax", "limit_k_max", "limit_k_max"],
                ["kmin", "limit_k_min", "limit_k_min"],
                ["lmax", "limit_l_max", "limit_l_max"],
                ["lmin", "limit_l_min", "limit_l_min"],
                ["nall", "number_all", "number"],
                ["nobs", "number_obs", "pdbx_number_obs"],
            ]

            data = {}
            for p in props:
                k = p[0]
                rk = p[1]
                rd = p[2]
                val = get_val(rk, rd)
                if val:
                    data[k] = val

            if not data.get("resh", None) and not data.get("nall", None) and not data.get("nobs", None):
                continue

            if cObjref:
                blk.remove("reflns")

            create = False
            if cObjdif is None:
                cObjdif = DataCategory("diffrn_reflns")
                create = True

            if "diffrn_id" not in cObjdif.getAttributeList():
                # appendAttributeExtendRows must have data to use or will not set - until some data present
                cObjdif.appendAttributeExtendRows("diffrn_id")
                cObjdif.setValue("1", "diffrn_id", 0)

            for p in props:
                k = p[0]
                rd = p[2]
                if k in data:
                    val = data[k]
                    if rd in cObjdif.getAttributeList():
                        cObjdif.setValue(val, rd, 0)
                    else:
                        cObjdif.appendAttributeExtendRows(rd, val)

            if create:
                blk.append(cObjdif)

    def __reorder_sf_file(self, sffile):
        """Reorders sf_file"""
        reorder_sf_file(sffile)

    def reorder_sf_file(self, sffile):
        """Reorders sf_file"""
        self.__reorder_sf_file(sffile)

    def __update_exptl_crystal(self, sf_file):
        """If exptl_crystal present, remove everything but id

        Args:
           sf_file (StructureFactorFile): The structure factor file object.

        Returns:
           bool: True if the value was modified, False otherwise.
        """
        modified = False
        for idx in range(sf_file.get_number_of_blocks()):
            blk = sf_file.get_block_by_index(idx)

            cObj = blk.getObj("exptl_crystal")
            if not cObj:
                continue

            attrNames = cObj.getAttributeList()
            # We do not want to to be updating while removing
            for attr in attrNames:
                if attr not in ["id"]:
                    modified = True
                    cObj.removeAttribute(attr)

            if len(cObj.getAttributeList()) == 0:
                blk.remove("exptl_crystal")
                modified = True

        return modified

    def __reorder_refln_all(self, sffile):
        """Reorders refln category for all blocks"""
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            sffile.reorder_category_attributes("refln", self.__stdorder, blk.getName())

    def __reorder_symmetry(self, sffile):
        """Reorders symmetry category for all blocks"""
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("symmetry")
            if not cObj:
                continue

            sffile.reorder_category_attributes("symmetry", ["entry_id", "space_group_name_H-M", "Int_Tables_number"], blk.getName())

    def correct_cell_precision(self, sffile):
        """We limit cell to 3 significant digits

        Used with non cif2cif
        """

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("cell")
            if not cObj:
                continue

            alist = ["length_a", "length_b", "length_c", "angle_alpha", "angle_beta", "angle_gamma"]

            attrlist = cObj.getAttributeList()

            for attr in alist:
                if attr in attrlist:
                    try:
                        val = float(cObj.getValue(attr, 0))
                        val = f"{val:.3f}"
                        cObj.setValue(str(val), attr, 0)
                    except ValueError:
                        # Ignore
                        pass

    def set_cell(self, sffile, cell):
        """Sets the unit cell -- assumption all blocks"""

        assert len(cell) == 6

        alist = ["length_a", "length_b", "length_c", "angle_alpha", "angle_beta", "angle_gamma"]

        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj("cell")

            create = False
            if not cObj:
                cObj = DataCategory("cell", alist)
                create = True

            # Delete unknown
            attrlist = cObj.getAttributeList()

            for attr in alist:
                if attr not in attrlist:
                    cObj.removeAttribute(attr)

            # Now set
            attrlist = cObj.getAttributeList()
            for idx, attr in enumerate(alist):
                if attr not in attrlist:
                    cObj.appendAttributeExtendRows(attr, cell[idx])
                else:
                    cObj.setValue(cell[idx], attr, 0)

            if create:
                blk.append(cObj)

    def cleanup_extra_audit(self, sffile):
        """Removes extra audit records from second and more blocks"""

        cat = "audit"
        for block_index in range(1, sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            if cat in blk.getObjNameList():
                blk.remove(cat)
                self.__logger.pinfo(f"Removing {cat} category from block {blk.getName()}", 0)

    def remove_empty_blocks(self, sffile):
        """Removes blocks with too little real data"""
        cats = ["refln", "diffrn_refln"]

        remove = []
        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)

            total = 0
            for cat in cats:
                if cat in blk.getObjNameList():
                    cObj = blk.getObj(cat)
                    total += cObj.getRowCount()

            if total < 30:
                bname = blk.getName()
                self.__logger.pinfo(f"Error: block {bname} has no data in this block -- removing", 0)
                remove.append(block_index)

        if remove:
            # Reverse list - so do not need to adjust numbers as removed
            remove.reverse()

            for rem in remove:
                sffile.remove_block(rem)

    def __check_hkl_duplcate(self, blk, blkname):
        """Provides a count of duplicate HKL.  Report first four, return count"""

        # Note for those who wonder.  Using a dictionary is a little faster than set() and must faster than using a list()
        ndup = 0

        cObj = blk.getObj("refln")
        if not cObj:
            return ndup

        alist = cObj.getAttributeList()
        for attr in ("index_h", "index_k", "index_l"):
            if attr not in alist:
                return ndup

        ref = {}
        for idx in range(cObj.getRowCount()):
            ah = cObj.getValue("index_h", idx)
            ak = cObj.getValue("index_k", idx)
            al = cObj.getValue("index_l", idx)

            key = (ah, ak, al)
            if key in ref:
                if ndup <= 4:
                    self.__logger.pinfo(f"Warning: Duplicated H,K,L ({ah}, {ak}, {al}) (data block={blkname}).", 0)
                ndup += 1
            else:
                ref[key] = True

        return ndup

    def remap_unmerged(self, sffile):
        """Map refln to diffrn_refln"""

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            ndup = self.__check_hkl_duplcate(blk, blkname)

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            alist = cObj.getAttributeList()
            have_Io = "intensity_meas" in alist
            have_I_plus = "pdbx_I_plus" in alist

            have_unmerge_i = False
            have_diffrn_refln = False
            cObj = blk.getObj("diffrn_refln")
            if cObj:
                have_diffrn_refln = True
                if "intensity_net" in cObj.getAttributeList():
                    have_unmerge_i = True

            # Legacy logic...
            if (ndup > 1 and (have_Io or have_I_plus)) or have_unmerge_i:
                if block_index == 0:
                    self.__logger.pinfo(f"Warning: Unmerged data in block 1 (blockId={blkname})!", 0)
                else:
                    self.__logger.pinfo(f"Note: Unmerged data in (blockId={blkname})!", 0)

                if block_index == 0:
                    # do not change token for 1st block even it is unmerged.
                    continue

                if have_diffrn_refln:
                    self.__logger.pinfo(f"Error: Block {blkname} has both _reflns and _diffrn_reflns and both unmerged", 0)
                    continue

                # Rename block.
                blk.rename("refln", "diffrn_refln")

                cObj = blk.getObj("diffrn_refln")

                # Cleanup attributes that are not used...
                for attr in ("crystal_id", "status"):  # Want a list and not truncated
                    if attr in cObj.getAttributeList():
                        cObj.removeAttribute(attr)

                # Instantiate diffrn_id if not present
                attr = "diffrn_id"
                if attr not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows(attr, "1")

                attr = "wavelength_id"
                if attr not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows(attr, "1")

                # attr = "standard_code"
                # if attr not in cObj.getAttributeList():
                #     cObj.appendAttributeExtendRows(attr, "1")

                # attr = "scale_group_code"
                # if attr not in cObj.getAttributeList():
                #     cObj.appendAttributeExtendRows(attr, "1")

                attr = "id"
                if attr not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows(attr)

                    for idx in range(cObj.getRowCount()):
                        cObj.setValue(str(idx + 1), attr, idx)

                # relabel attributes
                if "intensity_meas" in cObj.getAttributeList() and "intensity_net" not in cObj.getAttributeList():
                    cObj.renameAttributes({"intensity_meas": "intensity_net"})

                # Reassign data if need be.....
                if "intensity_net" not in cObj.getAttributeList():
                    # We fake it...
                    for attrl in (["F_squared_meas", "F_squared_sigma"], ["pdbx_I_plus", "pdbx_I_plus_sigma"], ["pdbx_I_minus", "pdbx_I_minus_sigma"]):
                        if attrl[0] in cObj.getAttributeList():
                            cObj.renameAttributes({attrl[0]: "intensity_net"})
                            self.__logger.pinfo(f"Warning: Copying {attrl[0]} to intensity_net in block {blkname}", 0)
                            if attrl[1] in cObj.getAttributeList():
                                cObj.renameAttributes({attrl[1]: "intensity_sigma"})
                                self.__logger.pinfo(f"Warning: Copying {attrl[1]} to intensity_sigma in block {blkname}", 0)
                            break

                # Delete columns cannot deal with
                for attr in ("pdbx_I_plus", "pdbx_I_plus_sigma", "pdbx_I_minus", "pdbx_I_minus_sigma"):
                    if attr in cObj.getAttributeList():
                        self.__logger.pinfo(f"Warning: Removing attribute {attr} in block {blkname}", 0)
                        cObj.removeAttribute(attr)

                sffile.reorder_category_attributes("diffrn_refln", self.__unmergedorder, blk.getName())
                blk = sffile.get_block_by_index(block_index)

    def check_unwanted_cif_items(self, sffile):
        """Checks and logs unwated item"""

        check_list = [
            "atom_sites.entry_id",
            "audit_author.name",
            "audit.creation_method",
            "audit.update_recor",
            "cell.CCP4_crystal_id",
            "cell.CCP4_wavelength_id",
            "cell.enry_id",
            "cell.entry",
            "cell_entry.id",
            "cell.enrty_id",
            "cell.entry.id",
            "cell.ndb_unique_axis",
            "cell.Z_PDB",
            "database_2.database_code",
            "database_2.database_id",
            "database.entry_id",
            "database.ndb_code_NDB",
            "database.ndb_code_PDB",
            "diffrn.detail",
            "diffrn.pdbx_crystal_id",
            "diffrn_radiation.id",
            "diffrn_radiation.pdbx_wavelength_list",
            "diffrn_radiation.type",
            "diffrn_radiation_wavelength.CCP4_crystal_id",
            "diffrn_radiation_wavelength.wt",
            "pdbx_powder_refln.d_spacing",
            "pdbx_powder_refln.F_squared_calc",
            "pdbx_powder_refln.F_squared_meas",
            "pdbx_powder_refln.gsas_i100_meas",
            "pdbx_powder_refln.index_h",
            "pdbx_powder_refln.index_k",
            "pdbx_powder_refln.index_l",
            "pdbx_powder_refln.observed_status",
            "pdbx_powder_refln.phase_calc",
            "pdbx_reflns_twin.crystal_id",
            "pdbx_reflns_twin.diffrn_id",
            "pdbx_reflns_twin.fraction",
            "pdbx_reflns_twin.mean_F_square_over_mean_F2",
            "pdbx_reflns_twin.mean_I2_over_mean_I_square",
            "pdbx_reflns_twin.operator",
            "pdbx_reflns_twin.type",
            "phasing_set_refln.crystal_id",
            "phasing_set_refln.F_meas_au",
            "phasing_set_refln.fom",
            "phasing_set_refln.index_h",
            "phasing_set_refln.index_k",
            "phasing_set_refln.index_l",
            "phasing_set_refln.phase_meas",
            "phasing_set_refln.scale_group_code",
            "phasing_set_refln.status",
            "phasing_set_refln.wavelength_id",
            "radiation.id",
            "refine.entry_id",
            "refine.ls_d_res_high",
            "refine.ls_d_res_low",
            "refln.fiber_coordinate",
            "refln.fiber_F_meas_au",
            "refln.fiber_layer",
            "refln.F_meas_sigma_uncorrected",
            "refln.F_meas_uncorrected",
            "refln.F_part_au",
            "refln.gsas_i100_meas",
            "refln.intensity_calc",
            "refln.intensity_meas_au",
            "refln.intensity_meas_sigma_au",
            "refln.intensity_meas_unknown",
            "refln.intensity_sigma_unknown",
            "refln.mean_path_length_tbar",
            "refln.observed_status",
            "refln.pdbx_cos_phase_calc",
            "refln.pdbx_F_backtransform_au",
            "refln.pdbx_fom_weighted_fmap",
            "refln.pdbx_gsas_i100_meas",
            "refln.pdbx_HLA",
            "refln.pdbx_HLB",
            "refln.pdbx_HLC",
            "refln.pdbx_HLD",
            "refln.pdbx_phase_backtransform",
            "refln.pdbx_phase_cycle",
            "refln.pdbx_sin_phase_calc",
            "refln.phase_meas_sigma",
            "refln.phase_part",
            "refln.sgx_fmap",
            "refln.sint_over_lambda",
            "refln.symmetry_multiplicity",
            "refln.wavelength",
            "refln.waveLEngth_id",
            "refln.weight",
            "reflns.CCP4_crystal_id",
            "reflns.CCP4_wavelength_id",
            "reflns.observed_criterion_sigma_I",
            "struct_keywords.entry_id",
            "struct_keywords.ndb_keywords",
            "struct_keywords.text",
            "symmetry.cell_setting",
            "symmetry.int_tables_number",
            "symmetry.ndb_full_space_group_name_H-M",
            "symmetry.space_group_name_h-m",
        ]

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            nlist = blk.getObjNameList()

            cn = CifName()
            for chk in check_list:
                cat = cn.categoryPart(chk)
                attr = cn.attributePart(chk)

                if cat in nlist:
                    cObj = blk.getObj(cat)
                    if attr in cObj.getAttributeList():
                        self.__logger.pinfo(f"Warning: Block {blkname} has unwanted CIF item ({chk})", 0)

    def __getUniqueTuples(self, cObj, attL):
        """Returns unique tuples of attributes"""

        tempD = None
        for att in attL:
            idx = cObj.getAttributeIndex(att)
            if idx < 0:
                self.__logger.info(f"Missing attribute {att}", 0)
                return None
            newD = cObj.getColumn(idx)
            if tempD is None:
                tempD = newD
            else:
                tempD = tuple(zip(tempD, newD))

        # Unique values
        rD = []
        for tup in tempD:
            if tup not in rD:
                rD.append(tup)

        return rD

    def __ensure_pdbx_r_free_flag_int(self, sffile):
        """If pdbx_r_free_flag is not an int, warn and truncate"""

        item = "pdbx_r_free_flag"

        for block_index in range(sffile.get_number_of_blocks()):
            warn = False
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            cObj = blk.getObj("refln")
            if not cObj:
                continue

            if item not in cObj.getAttributeList():
                continue

            # Faster to get data once - instead of dereferencing item name each time
            index = cObj.getIndex(item)
            data = cObj.getColumn(index)

            for idx in range(cObj.getRowCount()):
                val = data[idx]
                if val in [".", "?"]:
                    continue

                bad = False
                try:
                    _v = int(val)  # noqa: F841
                except ValueError:
                    bad = True

                if bad:
                    if not warn:
                        self.__logger.pinfo(f"Warning: In {blkname}, {item} value {val} is not integral -- truncating", 0)
                        warn = True
                    try:
                        newval = str(math.trunc(float(val)))
                    except ValueError:
                        newval = val
                    cObj.setValue(newval, item, idx)

    def __rename_diffrn_radiation(self, sffile):
        """If diffrn_radiation present and diffrn_radiation_wavelength, do a rename"""

        cat = "diffrn_radiation_wavelength"

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)

            cObj = blk.getObj("diffrn_radiation")
            if not cObj:
                continue

            if cat in blk.getObjNameList():
                # See if single row.
                cObj2 = blk.getObj(cat)
                if cObj2.getRowCount() != 1:
                    # Too complex
                    continue
                if cObj2.getValue("wavelength") not in [".", "?"]:
                    continue
                # Only copy if an option
                if "pdbx_wavelength" in cObj.getAttributeList():
                    val = cObj.getValue("pdbx_wavelength", 0)
                    cObj2.setValue(val, "wavelength", 0)
                blk.remove("diffrn_radiation")
                # next block
                continue

            # Rename block.
            blk.rename("diffrn_radiation", cat)

            # Rename attributes if needed
            cObj = blk.getObj(cat)

            renames = [["pdbx_wavelength", "wavelength"]]

            for r in renames:
                frm = r[0]
                dest = r[1]

                if frm in cObj.getAttributeList():
                    cObj.renameAttributes({frm: dest})

    def reassign_free(self, sffile, freer):
        """Reassign free R set"""

        cat = "refln"

        freer = str(freer)

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            cObj = blk.getObj(cat)
            if not cObj:
                continue

            alist = cObj.getAttributeList()
            if "pdbx_r_free_flag" not in alist:
                self.__logger.pinfo(f"Warning: pdbx_r_free_flag not in {cat} in block {blkname} no changes made", 0)
                continue

            if "status" not in alist:
                self.__logger.pinfo(f"Warning: status not in {cat} in block {blkname} no changes made", 0)
                continue

            setflag = False
            for idx in range(cObj.getRowCount()):
                curstat = cObj.getValue("status", idx)
                flag = cObj.getValue("pdbx_r_free_flag", idx)

                if curstat in ["h", "l", "x", "-", "<"]:
                    continue

                if curstat == "?":
                    newval = "x"
                if flag == freer:
                    newval = "f"
                    setflag = True
                else:
                    newval = "o"
                cObj.setValue(newval, "status", idx)

            if not setflag:
                self.__logger.pinfo(f"Warning: test set {freer} not in block {blkname} - nothing flagged as test set", 0)

    def set_cell_if_missing(self, sffile, pdbid, cell):
        """If cell is not present, then set"""

        cat = "cell"

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            if cat in blk.getObjNameList():
                continue

            # Instantiate cell
            alist = ["length_a", "length_b", "length_c", "angle_alpha", "angle_beta", "angle_gamma"]

            keys = ["entry_id"] + alist
            data = [pdbid]
            for k in cell:
                try:
                    val = str(f"{k:.3f}")
                except ValueError:
                    val = "?"
                data.append(val)

            newObj = DataCategory(cat, keys, [data])
            blk.append(newObj)

            self.__logger.pinfo(f"Note: Setting {cat} in block={blkname}", 0)

    def set_space_group_if_missing(self, sffile, pdbid, space_group):
        """If cell is not present, then set"""

        cat = "symmetry"

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            if cat in blk.getObjNameList():
                continue

            # Instantiate spacegroup
            alist = ["space_group_name_H-M"]

            keys = ["entry_id"] + alist
            data = [pdbid]
            data.append(space_group)

            newObj = DataCategory(cat, keys, [data])
            blk.append(newObj)

            self.__logger.pinfo(f"Note: Auto adding {cat} in block={blkname}", 0)

    def __filter_attributes(self, sffile):

        df = DictFilter()
        df.loadDataDictionary()

        for block_index in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(block_index)
            blkname = blk.getName()

            # We use list() to copy the contents - otherwise iterating through
            # a list that is changing is bad
            nlist = list(blk.getObjNameList())

            allowed = df.getAllowedCats()
            for cat in nlist:
                if cat not in allowed:
                    self.__logger.pinfo(f"Warning: Category '{cat}' not recognized in {blkname}.  Removing.", 0)
                    blk.remove(cat)
                    continue

                catAttrs = df.getAllowedAttrs(cat)
                if catAttrs is None:
                    # No restriction
                    continue

                cObj = blk.getObj(cat)
                attl = list(cObj.getAttributeList())

                for att in attl:
                    if att not in catAttrs:
                        self.__logger.pinfo(f"Warning: '{cat}.{att}' is unknown.  Removing.", 0)
                        cObj.removeAttribute(att)

                # Category no attributes. Remove
                if len(cObj.getAttributeList()) == 0:
                    blk.remove(cat)

    def __instantiate_refln_status(self, sffile):
        """Instantiate _refln.status if missing."""

        cat = "refln"
        for idx in range(sffile.get_number_of_blocks()):
            blk = sffile.get_block_by_index(idx)

            cObj = blk.getObj(cat)
            if cObj:
                if "status" not in cObj.getAttributeList():
                    cObj.appendAttributeExtendRows("status", "o")
                    self.__logger.pinfo(f"Adding status to {cat} in nblock={idx}", 0)
