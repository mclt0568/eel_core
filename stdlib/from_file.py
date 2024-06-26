from type_def import EelTypeBase, EelTypeString
from misc import read_to_eof
from cli_interface import basic_interface
from os.path import isfile
from exceptions import EelExcFileError

@basic_interface("from_file")
def from_file(filename: EelTypeString = EelTypeString("")) -> EelTypeBase:
  if filename.value == "":
    return EelTypeString(read_to_eof())

  if not isfile(filename.value):
    raise EelExcFileError(f"{filename.value} does not exist")
  
  with open(filename.value, "r") as f:
    return EelTypeString(f.read())