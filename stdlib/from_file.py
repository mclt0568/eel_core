from type_def import EelTypeBase, EelTypeString
from misc import read_to_eof
from cli_interface import basic_interface

@basic_interface("from_file")
def from_file(filename: EelTypeString = EelTypeString("")) -> EelTypeBase:
  if filename.value == "":
    return EelTypeString(read_to_eof())
  
  with open(filename.value, "r") as f:
    return EelTypeString(f.read())