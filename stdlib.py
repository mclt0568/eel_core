from type_def import EelTypeArithmetic, EelTypeBase, EelTypeString, decode_literal_or_repr
from exceptions import EelExcInvalidOperation, EelExcTypeError
from typing import Callable
from misc import read_to_eof

BASIC_INTERFACE: dict[str, Callable] = {}

def basic_interface(name: str
                    ) -> Callable[[Callable], Callable]:
  def register(func: Callable) -> Callable:
    global BASIC_INTERFACE
    BASIC_INTERFACE[name] = func
    func.__name__ = name
    return func

  return register

OPERATOR_LOOKUP: dict[str, str] = {
  "==": "eq",
  "!=": "ne",
  ">": "gt",
  "<": "lt",
  ">=": "ge",
  "<=": "le",
  "+": "plus",
  "-": "minus",
  "*": "times",
  "/": "divideby",
  "%": "modulo",
  "**": "exponent",
  "//": "floordiv",
}

@basic_interface("arith")
def arithmetic(left: EelTypeArithmetic, operator: EelTypeString, right: EelTypeBase) -> EelTypeBase:
  if not issubclass(type(left), EelTypeArithmetic):
    raise EelExcTypeError(f"{arithmetic.__name__}: "+
                          f"{EelTypeArithmetic.NAME} operand expected, got {type(left).NAME}")

  if not issubclass(type(operator), EelTypeString):
    raise EelExcTypeError(f"{arithmetic.__name__}: "+
                          f"{EelTypeString.NAME} operand expected, got {type(left).NAME}")

  if not issubclass(type(right), EelTypeArithmetic):
    raise EelExcTypeError(f"{arithmetic.__name__}: "+
                          f"{EelTypeArithmetic.NAME} operand expected, got {type(right).NAME}")
  
  op_str = operator.value

  if op_str in OPERATOR_LOOKUP:
    op_str = OPERATOR_LOOKUP[op_str]


  match op_str:
    case "plus":
      return left.eel_arith_add(right)

    case "minus":
      return left.eel_arith_sub(right)

    case "times":
      return left.eel_arith_mul(right)

    case "divideby":
      return left.eel_arith_div(right)

    case "modulo":
      return left.eel_arith_mod(right)

    case "exponent":
      return left.eel_arith_exp(right)

    case "floordiv":
      return left.eel_arith_floordiv(right)
    
    case _:
      raise EelExcInvalidOperation(f"{op_str} is not a valid operator")

@basic_interface("from_file")
def from_file(filename: EelTypeString = EelTypeString("")) -> EelTypeBase:
  if filename.value == "":
    return EelTypeString(read_to_eof())
  
  with open(filename.value, "r") as f:
    return EelTypeString(f.read())
  
@basic_interface("to_num")
def to_num(val: EelTypeBase | None = None) -> EelTypeBase:
  if val is None:
    val = decode_literal_or_repr(read_to_eof())

  return val.eel_to_number()