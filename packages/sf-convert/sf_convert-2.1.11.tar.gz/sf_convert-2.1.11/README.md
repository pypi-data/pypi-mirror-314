# mmCIF File Script

This Python script provides command line interface to read, write, and manipulate mmCIF files using the `py-mmcif` library. 

## Installation

You need Python 3.6 or later to run this script. The `py-mmcif` library can be installed via pip:

```bash
pip install py-mmcif
```

## Usage

Run the script with the `-h` or `--help` option to view the help message:

```bash
python sffile.py --help
```

Here are the available command line arguments:

- `-r` or `--read`: Read from an mmCIF file. Provide the filename as an argument. 
    Example: `python sffile.py --read myfile.cif`
- `-w` or `--write`: Write to an mmCIF file. Provide the filename as an argument. 
    Example: `python sffile.py --write myfile.cif`
- `-b` or `--block`: Get a block by its name. Provide the block name as an argument.
    Example: `python sffile.py --read myfile.cif --block myblock`
- `-o` or `--object`: Get an object from a block by its category. Provide the block name and category as arguments.
    Example: `python sffile.py --read myfile.cif --object myblock mycategory`
- `-d` or `--default`: Set a block as the default block. Provide the block name as an argument.
    Example: `python sffile.py --read myfile.cif --default myblock`
- `-g` or `--get`: Get an object from the default block by its category. Provide the category as an argument.
    Example: `python sffile.py --read myfile.cif --default myblock --get mycategory`
- `-ob` or `--objblock`: Get an object from a block. This is similar to the `--object` argument. Provide the block name and category as arguments.
    Example: `python sffile.py --read myfile.cif --objblock myblock mycategory`
- `-l` or `--list`: List the names of all blocks in the file.
    Example: `python sffile.py --read myfile.cif --list`
- `-c` or `--categories`: List all categories in a block. Provide the block name as an argument.
    Example: `python sffile.py --read myfile.cif --categories myblock`

You can also combine these arguments. For example, you can read from a file, list the blocks, get an object from a block, and then write to a file:

```bash
python sffile.py --read myfile.cif --list --object myblock mycategory --write myfile.cif
```
