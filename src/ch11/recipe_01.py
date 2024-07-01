# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Using pathlib to work with filenames






# Subsection: Getting ready


test_example_2_1 = """
>>> from pathlib import Path
"""

test_example_2_2 = """
>>> from argparse import Namespace
>>> options = Namespace(
...     input='/path/to/some/file.csv',
...     file1='data/ch11_file1.yaml',
...     file2='data/ch11_file2.yaml',
... )
"""

# Subsection: How to do it...
# Topic: Making the output filename by changing the input filename's suffix


test_example_3_1 = """
>>> from pathlib import Path
>>> from argparse import Namespace
>>> options = Namespace(input='/path/to/some/file.csv')

>>> input_path = Path(options.input)
>>> input_path
PosixPath('/path/to/some/file.csv')

>>> output_path = input_path.with_suffix('.out')
>>> output_path
PosixPath('/path/to/some/file.out')
"""

# Subsection: How to do it...
# Topic: Making a number of sibling output files with distinct names


test_example_4_1 = """
>>> from pathlib import Path
>>> from argparse import Namespace
>>> options = Namespace(input='/path/to/some/file.csv')

>>> input_path = Path(options.input)
>>> input_path
PosixPath('/path/to/some/file.csv')

>>> input_directory = input_path.parent
>>> input_stem = input_path.stem

>>> output_stem_pass = f"{input_stem}_pass"
>>> output_stem_pass
'file_pass'

>>> output_path = (
...     input_directory / output_stem_pass
... ).with_suffix('.csv')
>>> output_path
PosixPath('/path/to/some/file_pass.csv')
"""

# Subsection: How to do it...
# Topic: Creating a directory and a number of files in the directory


test_example_5_1 = """
>>> from pathlib import Path
>>> from argparse import Namespace
>>> options = Namespace(input='/path/to/some/file.csv')

>>> input_path = Path(options.input)
>>> input_path
PosixPath('/path/to/some/file.csv')

>>> output_parent = input_path.parent / "output"
>>> output_parent
PosixPath('/path/to/some/output')

>>> input_stem = input_path.stem
>>> output_path = (
...     output_parent / input_stem).with_suffix('.src')
>>> output_path
PosixPath('/path/to/some/output/file.src')
"""

# Subsection: How to do it...
# Topic: Comparing file dates to see which is newer

# assumes US/EST
test_example_6_1 = """
>>> from pathlib import Path
>>> from argparse import Namespace
>>> options = Namespace(
... file1='data/ch11_file1.yaml',
... file2='data/ch11_file2.yaml')

>>> file1_path = Path(options.file1)
>>> file2_path = Path(options.file2)

>>> file1_path.stat().st_mtime
1572806032.0
>>> file2_path.stat().st_mtime
1572806131.0

>>> import datetime
>>> mtime_1 = file1_path.stat().st_mtime
>>> datetime.datetime.fromtimestamp(mtime_1)
datetime.datetime(2019, 11, 3, 13, 33, 52)
"""

# Subsection: How to do it...
# Topic: Removing a file


test_example_7_1 = """
>>> from pathlib import Path
>>> from argparse import Namespace
>>> options = Namespace(input='/path/to/some/file.csv')

>>> input_path = Path(options.input)
>>> input_path
PosixPath('/path/to/some/file.csv')

>>> input_path.unlink(missing_ok=True)
"""

# Subsection: How to do it...
# Topic: Finding all files that match a given pattern


test_example_8_1 = """
>>> from pathlib import Path
>>> from argparse import Namespace
>>> options = Namespace(file1='data/ch11_file1.yaml')

>>> Path(options.file1)
PosixPath('data/ch11_file1.yaml')
>>> directory_path = Path(options.file1).parent
>>> directory_path
PosixPath('data')

>>> from pprint import pprint
>>> pprint(sorted(directory_path.glob("*.csv")))
[PosixPath('data/binned.csv'),
 PosixPath('data/ch14_r03.csv'),
 PosixPath('data/ch14_r04.csv'),
 PosixPath('data/craps.csv'),
 PosixPath('data/fuel.csv'),
 PosixPath('data/fuel2.csv'),
 PosixPath('data/output.csv'),
...

"""






# Subsection: There's more...


test_example_9_1 = """
>>> from pathlib import PureWindowsPath
>>> home_path = PureWindowsPath(r'C:\\Users\\slott')
>>> name_path = home_path / 'filename.ini'
>>> name_path
PureWindowsPath('C:/Users/slott/filename.ini')
>>> print(str(name_path))
C:\\Users\\slott\\filename.ini
"""


# End of Using pathlib to work with filenames

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
