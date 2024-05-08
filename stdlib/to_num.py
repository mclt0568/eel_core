from cli_interface import basic_interface
from misc import read_to_eof
from type_def import EelTypeBase, decode_literal_or_repr


@basic_interface("to_num")
def to_num(val: EelTypeBase | None = None) -> EelTypeBase:
  if val is None:
    val = decode_literal_or_repr(read_to_eof())

  return val.eel_to_number()