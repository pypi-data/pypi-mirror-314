import os
import traceback
import re

from mmcif.io.IoAdapterCore import IoAdapterCore
from mmcif.api.PdbxContainers import DataContainer
from mmcif.api.DataCategory import DataCategory
from sf_convert.utils.CifUtils import reorderCategoryAttr


class StructureFactorFile:
    def __init__(self):
        """
        Initializes a new instance of the StructureFactorFile class.
        """
        self.__data_blocks = []  # Contains the data blocks in the file
        self.__file_io = IoAdapterCore()  # Handles file input/output
        self.__default_block_index = 0  # The index of the default data block

    def read_file(self, filename):
        """
        Reads a structure factor file.

        Args:
            filename (str): The path to the file to be read.

        Raises:
            RuntimeError: If the file fails to be read.
        """
        try:
            self.__data_blocks = self.__file_io.readFile(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to read file {filename}") from e

    def get_block_by_index(self, block_index):
        """
        Retrieves a data block by its index.

        Args:
            block_index (int): The index of the data block.

        Returns:
            DataContainer: The data block at the specified index, or None if the index is invalid.
        """
        if 0 <= block_index < len(self.__data_blocks):
            return self.__data_blocks[block_index]
        else:
            print(f"Block index {block_index} is not valid. It should be between 0 and {len(self.__data_blocks) - 1}.")
            return None

    def get_number_of_blocks(self):
        """
        Gets the number of data blocks in the file.

        Returns:
            int: The number of data blocks.
        """
        return len(self.__data_blocks)

    def write_file(self, filename, endcomments=False):
        """
        Writes the structure factor file to disk.

        Args:
            filename (str): The path to the output file.
            endcomments (bool): Whether to include #END and #END_OF_DATA
        """
        if endcomments:
            tempfile = filename + ".tmp." + str(os.getpid())
            self.__file_io.writeFile(tempfile, self.__data_blocks)
            if os.path.exists(tempfile):
                self.__insertComments(tempfile, filename)
                os.remove(tempfile)
        else:
            self.__file_io.writeFile(filename, self.__data_blocks)

    def get_all_block_names(self):
        """
        Gets the names of all data blocks.

        Returns:
            list: A list of block names.
        """
        return [block.getName() for block in self.__data_blocks]

    def get_block_by_name(self, name):
        """
        Retrieves a data block by its name.

        Args:
            name (str): The name of the data block.

        Returns:
            tuple: A tuple containing the index and the data block with the specified name, or (None, None) if the block does not exist.
        """
        for idx, block in enumerate(self.__data_blocks):
            if block.getName() == name:
                return idx, block
        return None, None

    def get_default_block_index(self):
        """
        Gets the index of the default data block.

        Returns:
            int: The index of the default data block.
        """
        return self.__default_block_index

    def get_category_object(self, category, block_name=None):
        """
        Retrieves a category object from a data block.

        Args:
            category (str): The name of the category.
            block_name (str, optional): The name of the data block. Defaults to None.

        Returns:
            DataCategory: The category object, or None if the category or data block does not exist.
        """
        if block_name is None:
            block_index = self.__default_block_index
            return self.__data_blocks[block_index].getObj(category)
        else:
            block_index, block_res = self.get_block_by_name(block_name)
            if block_res is None:
                return None
            return block_res.getObj(category)

    def set_default_block(self, block_name):
        """
        Sets the default data block.

        Args:
            block_name (str): The name of the data block to set as default.
        """
        block_index, _ = self.get_block_by_name(block_name)
        if block_index is not None:
            self.__default_block_index = block_index

    def get_category_names(self, block_name=None):
        """
        Gets the names of all categories in a data block.

        Args:
            block_name (str, optional): The name of the data block. Defaults to None.

        Returns:
            list: A list of category names.
        """
        if block_name == "Default" or block_name is None:
            block_index = self.__default_block_index
            return self.__data_blocks[block_index].getObjNameList()
        else:
            block_index, block_res = self.get_block_by_name(block_name)
            if block_res is None:
                return None
            return block_res.getObjNameList()

    def append_category_to_block(self, category, block_name=None):
        """
        Appends a category to a data block.

        Args:
            category (DataCategory): The category to append.
            block_name (str, optional): The name of the data block. Defaults to None.
        """
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return
        block.append(category)

    def remove_category_by_name(self, category_name, block_name=None):
        """
        Removes a category from a data block by its name.

        Args:
            category_name (str): The name of the category to remove.
            block_name (str, optional): The name of the data block. Defaults to None.

        Returns:
            bool: True if the category was successfully removed, False otherwise.
        """
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return False
        removed_category = block.remove(category_name)
        return removed_category

    def add_data_to_block(self, category_name, data_dict, block_name=None):
        """
        Adds a category with its data to a specific block.

        Args:
            category_name (str): The name of the category to be added.
            data_dict (dict): A dictionary where the keys are the attribute names and the values are their respective values.
            block_name (str, optional): The name of the block to which the category should be added. Defaults to None.
        """
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return
        new_category = DataCategory(category_name)
        for attribute in data_dict.keys():
            new_category.appendAttribute(attribute)
        new_category.append(list(data_dict.values()))
        block.append(new_category)

    def remove_duplicates_in_category(self, category_name, block_name=None):
        """
        Removes duplicate rows in a category.

        Args:
            category_name (str): The name of the category.
            block_name (str, optional): The name of the data block. Defaults to None.

        Returns:
            bool: True if any duplicates were removed, False otherwise.
        """
        if block_name is None:
            block = self.get_block_by_index(self.__default_block_index)
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return False

        category = block.getObj(category_name)
        if category is None:
            print(f"Category {category_name} does not exist in block {block.getName()}.")
            return False

        initial_row_count = category.getRowCount()
        seen = set()
        new_data = []
        for row in category.data:
            row_tuple = tuple(row)
            if row_tuple in seen:
                print(f"Warning: Duplicated row {row} (data block={block.getName()}).")
            else:
                seen.add(row_tuple)
                new_data.append(row)
        category.data = new_data
        final_row_count = category.getRowCount()

        return initial_row_count != final_row_count

    def replace_value_in_category(self, category_name, attribute_name, new_value, old_value=None, block_name=None):
        """
        Replaces a value in a category.

        Args:
            category_name (str): The name of the category.
            attribute_name (str): The name of the attribute.
            new_value (str): The new value to replace with.
            old_value (str, optional): The old value to replace. Defaults to None.
            block_name (str, optional): The name of the data block. Defaults to None.

        Returns:
            int: The number of values replaced.
        """
        if block_name is None:
            block = self.get_block_by_index(self.__default_block_index)
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return 0

        category = block.getObj(category_name)
        if category is None:
            print(f"Category {category_name} does not exist in block {block.getName()}.")
            return 0

        num_replaced = 0
        for row in category.data:
            index = category.getAttributeIndex(attribute_name)
            if index is None:
                print(f"Attribute {attribute_name} does not exist in category {category_name}.")
                return 0
            if old_value is None or row[index] == old_value:
                row[index] = new_value
                num_replaced += 1

        return num_replaced

    def reorder_category_attributes(self, category_name, new_order, block_name=None):
        """
        Reorders the attributes of a category.

        Args:
            category_name (str): The name of the category.
            new_order (list): The new order of attribute names.
            block_name (str, optional): The name of the data block. Defaults to None.
        """
        # Get the category object
        category = self.get_category_object(category_name, block_name)

        # Reorder the category's attributes
        reordered_category = reorderCategoryAttr(category, new_order)

        # Replace the existing category with the reordered one
        _, block = self.get_block_by_name(block_name)
        block.replace(reordered_category)

    def reorder_categories_in_block(self, new_order, block_name=None):
        """
        Reorders the categories in a data block.

        Args:
            new_order (list): The new order of category names.
            block_name (str, optional): The name of the data block. Defaults to None.
        """
        # Get the block
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            block_index, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return

        # Create a new block with the same name and type
        new_block = DataContainer(block.getName())
        new_block.setType(block.getType())

        # Copy properties from the old block to the new one
        for prop_name in block.getPropCatalog():
            new_block.setProp(prop_name, block.getProp(prop_name))

        # Add categories to the new block in the desired order
        for category_name in new_order:
            category = block.getObj(category_name)
            if category is not None:
                new_block.append(category)

        # Add any remaining categories that were not in new_order
        for category_name in block.getObjNameList():
            if category_name not in new_order:
                category = block.getObj(category_name)
                new_block.append(category)

        # Replace the original block with the new one
        if block_name is None:
            self.__data_blocks[self.__default_block_index] = new_block
        else:
            self.__data_blocks[block_index] = new_block

    def generate_expected_block_name(self, pdbid, block):
        """
        Generates the expected name for a data block.

        Args:
            pdbid (str): The PDB ID.
            block (int): The block index. 0...n

        Returns:
            str: The expected block name.
        """
        # Set bid
        bid = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        bname = ""

        if block > 0:
            cont = True
        else:
            cont = False

        while cont:
            block = block - 1
            # we are numbering 1...26, 27...52, 53...
            mod = block % 26
            block = int((block) / 26.0)
            if block == 0:
                cont = False

            bname = bname + bid[mod]

        return f"r{pdbid}{bname}sf"

    def correct_block_names(self, pdbid):
        """
        Corrects the names of all data blocks.

        Args:
            pdbid (str): The PDB ID.
        """
        for index, block in enumerate(self.__data_blocks):
            expected_name = self.generate_expected_block_name(pdbid, index)  # Assuming pdbid is the 4 characters after "r"
            if block.getName() != expected_name:
                block.setName(expected_name)

    def add_block(self, block):
        """
        Adds a new data block to existing file

        Args:
            pdbid (DataContainer): Data container to add
        """
        self.__data_blocks.append(block)

    def extract_pdbid_from_block(self):
        """
        Retrieves pdb id from first block name

        Returns PDB id or "xxxx"
        """
        if self.__data_blocks is None or len(self.__data_blocks) == 0:
            return "xxxx"

        b0name = self.__data_blocks[0].getName()

        if len(b0name) > 1 and "#" not in b0name and " " not in b0name:
            pdbid = b0name[1:5]
        else:
            pdbid = "xxxx"

        return pdbid

    def __insertComments(self, inpFn, outFn):
        """Insert end of block/file comments in the input file --"""
        #
        try:
            pattern = r"[\r\n]+data_"
            replacement = r"\n#END\ndata_"
            reObj = re.compile(pattern, re.MULTILINE | re.DOTALL | re.VERBOSE)
            # Flush changes made to the in-memory copy of the file back to disk
            with open(outFn, "w") as ofh:
                with open(inpFn, "r") as ifh:
                    ofh.write(reObj.sub(replacement, ifh.read()) + "\n#END OF REFLECTIONS\n")
            return True
        except:  # noqa: E722 pylint: disable=bare-except
            # What to do?
            print("Failure to add END blocks")
            traceback.print_exc()
            return False

    def merge_sf(self, sfnew):
        """Merge new StructureFactorFile into existing definition.
        Care is made to ensure unique data block names

        Args:
          sfnew (StructureFactorFile): Object to merge
        """
        for idx in range(sfnew.get_number_of_blocks()):
            blk = sfnew.get_block_by_index(idx)

            # Check if block name in use
            blkname = blk.getName()
            origname = blkname
            cnt = 1
            while blkname in self.get_all_block_names():
                blkname = origname + str(cnt)
                cnt += 1

            if blkname != origname:
                blk.setName(blkname)

            # Add
            self.add_block(blk)

    def remove_block(self, blkid):
        """Removes block blkid from indices"""
        del self.__data_blocks[blkid]
