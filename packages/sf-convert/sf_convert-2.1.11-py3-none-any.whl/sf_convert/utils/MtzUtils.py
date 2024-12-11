import gemmi

import numpy as np


class GetMtzInfo:
    """Class to extract information for an MTZ file"""

    def __init__(self):
        self.__mtz = None

    def readmtz(self, fpath):
        self.__mtz = gemmi.read_mtz_file(fpath)

    def get_column_data(self):
        """Returns column info for the datasets.  Not H, K, L are daataset_id 1 and not 0"""
        ret = []

        for c in self.__mtz.columns:
            cD = {}
            cD["label"] = c.label
            cD["dataset_id"] = c.dataset_id
            cD["type"] = c.type
            cD["min"] = c.min_value
            cD["max"] = c.max_value
            cD["is_int"] = c.is_integer()

            ret.append(cD)

            # 'array', 'dataset', 'dataset_id', 'idx', 'is_integer', 'label', 'max_value', 'min_value', 'source', 'type']

        return ret

    def write_fake_mtzdump(self, fpath):
        """Outputs a mtzdump equivalent file"""

        with open(fpath, "w") as fout:
            fout.write("* Title:\n\n")
            fout.write("    %s\n\n" % self.__mtz.title)

            cell = self.__mtz.cell

            numds = len(self.__mtz.datasets)
            fout.write("* Number of datasets: %s\n\n" % numds)

            fout.write("* Dataset ID, project/crystal/dataset names, cell dimensions, wavelength:\n\n")

            for ds in self.__mtz.datasets:
                cname = ds.crystal_name
                if cname == "":
                    cname = "unknown"
                fout.write(f"       {ds.id} {ds.project_name}\n         {cname}\n         {ds.dataset_name}\n")

                icell = ds.cell if ds.cell.is_crystal() else cell

                fout.write(f"            {icell.a:.4f}     {icell.b:.4f}     {icell.c:.4f}     {icell.alpha:.4f}     {icell.beta:.4f}     {icell.gamma:.4f}\n")
                fout.write(f"            {ds.wavelength:.4f}\n\n")

            ncols = len(self.__mtz.columns)

            fout.write(f"* Number of Columns = {ncols}\n\n")

            fout.write(f"* Number of Reflections = {self.__mtz.nreflections}\n\n")

            fout.write("* HISTORY for current MTZ file :\n")
            for h in self.__mtz.history:
                fout.write(f"    {h}\n")

            fout.write("\n")

            fout.write("* Column Labels :\n\n")
            fout.write(" ".join(self.__mtz.column_labels()) + "\n\n")

            fout.write("* Column Types :\n\n")

            tlist = [col.type for col in self.__mtz.columns]
            fout.write(" ".join(tlist) + "\n\n")

            fout.write("* Associated datasets :\n\n")

            dlist = [str(col.dataset_id) for col in self.__mtz.columns]
            fout.write(" ".join(dlist) + "\n\n")

            fout.write("# * Cell Dimensions : (obsolete - refer to dataset cell dimensions above)\n\n")
            fout.write(f" {cell.a:.4f}     {cell.b:.4f}     {cell.c:.4f}     {cell.alpha:.4f}     {cell.beta:.4f}     {cell.gamma:.4f}\n")

            fout.write("*  Resolution Range :\n\n")
            fout.write(f"  {self.__mtz.resolution_low():.4f} - {self.__mtz.resolution_high():.4f} A\n\n")

            fout.write("* Sort Order :\n\n")
            so = " ".join([str(x) for x in self.__mtz.sort_order])
            fout.write(f"   {so}\n\n")

            fout.write(f"* Space group = '{self.__mtz.spacegroup_name}' (number  {self.__mtz.spacegroup_number})\n\n\n")

            fout.write("OVERALL FILE STATISTICS\n=======================\n\n")

            fout.write("Col     Min        Max      Num       %        Mean  Type Column\n")
            fout.write("                          Missing  complete               label\n\n")

            for idx, col in enumerate(self.__mtz.columns):
                cmin = col.min_value
                cmax = col.max_value
                nonzero = np.count_nonzero(~np.isnan(col.array))
                mean = np.nanmean(col.array)
                clen = col.array.size
                nummis = clen - nonzero
                if clen > 0:
                    complper = (nonzero / clen) * 100
                else:
                    complper = 0

                if col.is_integer():
                    fout.write(f"{idx + 1:2}  {cmin:7n}  {cmax:9n}   {nummis:5n}     {complper:6.2f}   {mean:6.2f}    {col.type}    {col.label}\n")
                else:
                    fout.write(f"{idx + 1:2}  {cmin:7.2f}  {cmax:9.2f}   {nummis:5n}     {complper:6.2f}   {mean:6.2f}    {col.type}    {col.label}\n")
