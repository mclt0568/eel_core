from type_def import EelTypeArithmetic, EelTypeString, EelTypeBase
from cli_interface import basic_interface
from exceptions import EelExcInvalidOperation, EelExcTypeError


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
def arith(left: EelTypeArithmetic, operator: EelTypeString, right: EelTypeBase) -> EelTypeBase:
  get_type_name = lambda x: x.NAME if hasattr(x, "NAME") else x.__name__

  if not issubclass(type(right), EelTypeArithmetic):
    raise EelExcTypeError(
            f"arith on arg#2: expected Arithmetic, got {get_type_name(type(right))}")

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
