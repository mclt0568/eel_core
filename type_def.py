from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, cast
from exceptions import *
from misc import is_float_strict, is_int
from base64 import b64decode as b_dec, b64encode as b_enc
from binascii import Error as BinError

TYPE_PREFIX: dict[str, type[EelTypeBase]] = {}


T = TypeVar("T")


def eel_type(prefix: str, name: str) -> Callable[[type], type]:
  def register_type(t: type[EelTypeBase]) -> type:
    TYPE_PREFIX[prefix] = t
    t.PREFIX = prefix
    t.NAME = name

    return t

  return register_type


def eel_operation(func: Callable) -> Callable:
  def check_call(self, other) -> EelTypeBase:
    if issubclass(type(other), EelTypeBase):
      return func(self, other)

    raise EelExcSysTypeError()

  return check_call


class EelTypeBase(ABC, Generic[T]):
  PREFIX: str = ""
  NAME: str = ""
  REPR_PREFIX_MARKER = "!"
  LITERAL_PREFIX_MARKER = "@"

  value: T

  def __init__(self, value: T) -> None:
    self.value = value

  @staticmethod
  @abstractmethod
  def eel_from_repr(repr: str) -> EelTypeBase: ...

  @classmethod
  def eel_from_literal(cls: type[EelTypeBase], literal: str) -> EelTypeBase:
    return cls.eel_from_repr(literal)

  @abstractmethod
  def eel_to_repr(self) -> str: ...

  def eel_encode_repr(self) -> str:
    return f"{self.PREFIX}{self.REPR_PREFIX_MARKER}{self.eel_to_repr()}"

  def eel_to_file(self) -> str:
    return str(self.value)

  @abstractmethod
  def eel_to_string(self) -> EelTypeString: ...

  @abstractmethod
  def eel_to_number(self) -> EelTypeNumber: ...

  @abstractmethod
  def eel_to_list(self) -> EelTypeList: ...

  @abstractmethod
  def eel_to_dict(self) -> EelTypeDict: ...

  @abstractmethod
  def eel_to_bool(self) -> EelTypeBool: ...

  @eel_operation
  def eel_op_comp(self, other: EelTypeBase) -> EelTypeBool:
    return EelTypeBool(self.value == other.value)

  @eel_operation
  def eel_op_and(self, other: EelTypeBase) -> EelTypeBase:
    if self.eel_to_bool().value:
      return other
    
    return self

  @eel_operation
  def eel_op_or(self, other: EelTypeBase) -> EelTypeBase:
    if self.eel_to_bool().value:
      return self
    
    return other

  @eel_operation
  def eel_op_not(self) -> EelTypeBool:
    return EelTypeBool(not self.value)


class EelTypeArithmetic:
  value: object
  NAME: str

  @eel_operation
  def eel_arith_basic(self, other: EelTypeBase, computation: Callable) -> EelTypeBase:
    if issubclass(type(other), type(self)):
      raise EelExcInvalidOperation(f"Cannot evaluate {self.NAME} + {type(other.NAME)}")
    
    return computation(self, other)

  def eel_arith_add(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value + y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)

  def eel_arith_sub(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value - y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)

  def eel_arith_mul(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value * y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)

  def eel_arith_div(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value / y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)

  def eel_arith_mod(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value % y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)

  def eel_arith_exp(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value ** y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)

  def eel_arith_floordiv(self, other: EelTypeBase) -> EelTypeBase:
    comp = lambda x, y: type(self)(x.value // y.value) # type: ignore
    return self.eel_arith_basic(other, type(self), comp)


class EelTypeSequence:
  value: object

  @abstractmethod
  def eel_iterate(self) -> str: ...

  @abstractmethod
  def eel_op_contains(self) -> EelTypeBool: ...

  @abstractmethod
  def eel_op_len(self) -> EelTypeNumber: ...


class EelTypeComparable:
  value: object
  eel_op_comp: Callable[[EelTypeBase], EelTypeBase]

  @eel_operation
  def eel_op_greater(self, other: EelTypeBase) -> EelTypeBool:
    return EelTypeBool(self.value > other.value)
  
  @eel_operation
  def eel_op_less(self, other: EelTypeBase) -> EelTypeBool:
    return EelTypeBool(self.value < other.value)

  @eel_operation
  def eel_op_greater_or_eq(self, other: EelTypeBase) -> EelTypeBool:
    comp = self.eel_op_greater(other)
    if not comp.value:
      return self.eel_op_comp(other)
    
    return comp
  
  @eel_operation
  def eel_op_less_or_eq(self, other: EelTypeBase) -> EelTypeBool:
    comp = self.eel_op_less(other)
    if not comp.value:
      return self.eel_op_comp(other)
    
    return comp



###############################################################################
"""
Type Implementations

The following class implement the actual types used in eel scripts.
"""
###############################################################################



@eel_type("num", "Number")
class EelTypeNumber(EelTypeBase[int | float], 
                    EelTypeArithmetic, 
                    EelTypeComparable):

  @staticmethod
  def eel_from_repr(repr: str) -> EelTypeNumber:
    if is_int(repr):
      return EelTypeNumber(int(repr))
    
    if is_float_strict(repr):
      return EelTypeNumber(float(repr))
    
    raise EelExcSysTypeError()

  def eel_to_repr(self) -> str:
    return str(self.value)

  def eel_to_string(self) -> EelTypeString:
    return EelTypeString(str(self.value))

  def eel_to_number(self) -> EelTypeNumber:
    return EelTypeNumber(self.value)

  def eel_to_list(self) -> EelTypeList:
    raise EelExcInvalidOperation(f"Cannot convert type {self.NAME} to {EelTypeList.NAME}")

  def eel_to_dict(self) -> EelTypeDict:
    raise EelExcInvalidOperation(f"Cannot convert type {self.NAME} to {EelTypeDict.NAME}")

  def eel_to_bool(self) -> EelTypeBool:
    return EelTypeBool(bool(self.value))


@eel_type("str", "String")
class EelTypeString(EelTypeBase[str]):
  @staticmethod
  def eel_from_repr(repr: str) -> EelTypeString:
    try:
      return EelTypeString(b_dec(repr).decode())
    
    except BinError:
      raise EelExcSysTypeError()

  @staticmethod
  def eel_from_literal(literal: str) -> EelTypeString:
    return EelTypeString(literal)

  def eel_to_repr(self) -> str:
    return b_enc(self.value.encode()).decode()

  def eel_to_string(self) -> EelTypeString:
    return EelTypeString(str(self.value))

  def eel_to_number(self) -> EelTypeNumber:
    return EelTypeNumber.eel_from_repr(self.value)

  def eel_to_list(self) -> EelTypeList:
    return EelTypeList(list(self.value))

  def eel_to_dict(self) -> EelTypeDict:
    raise EelExcInvalidOperation(f"Cannot convert type {self.NAME} to {EelTypeDict.NAME}")

  def eel_to_bool(self) -> EelTypeBool:
    return EelTypeBool(bool(self.value))


@eel_type("lst", "List")
class EelTypeList(EelTypeBase[list], EelTypeSequence): ...


@eel_type("dic", "Dictionary")
class EelTypeDict(EelTypeBase[dict], EelTypeSequence): ...


@eel_type("bol", "Boolean")
class EelTypeBool(EelTypeBase[bool]): ...



###############################################################################
"""
Type Reading / Manipulation Utilities
"""
###############################################################################



def from_file(raw: str) -> EelTypeString:
  return EelTypeString(raw)


def to_file(obj: EelTypeBase) -> str:
  return obj.eel_to_file()


def decode_repr(raw: str) -> EelTypeBase:
  marker = EelTypeBase.REPR_PREFIX_MARKER
  
  if marker not in raw:
    raise EelExcNotAnEelRepr(f"{raw} is not a valid Eel Representation")
  
  type_prefix = raw.split(marker)[0]

  if not type_prefix:
    raise EelExcNotAnEelRepr(f"{raw} is not a valid Eel Representation")

  if type_prefix not in TYPE_PREFIX:
    raise EelExcTypeError(f"{type_prefix} is not a valid Eel Type or user defined type")

  return TYPE_PREFIX[type_prefix].eel_from_repr(raw[raw.index(marker) + 1:])


def decode_literal(raw: str) -> EelTypeBase:
  marker = EelTypeBase.LITERAL_PREFIX_MARKER
  
  if marker not in raw:
    raise EelExcNotAnEelRepr(f"{raw} is not a valid Eel Literal")
  
  type_prefix = raw.split(marker)[0]

  if not type_prefix:
    raise EelExcNotAnEelRepr(f"{raw} is not a valid Eel Literal")

  if type_prefix not in TYPE_PREFIX:
    raise EelExcTypeError(f"{type_prefix} is not a valid Eel Type or user defined type")

  return TYPE_PREFIX[type_prefix].eel_from_literal(raw[raw.index(marker) + 1:])


def decode_literal_or_repr(raw: str) -> EelTypeBase:
  marker_literal = EelTypeBase.LITERAL_PREFIX_MARKER
  marker_repr = EelTypeBase.REPR_PREFIX_MARKER
  
  if marker_literal in raw and marker_repr in raw:
    determ = raw.index(marker_literal) < raw.index(marker_repr)
    return decode_literal(raw) if determ else decode_repr(raw)
  
  if marker_literal in raw:
    return decode_literal(raw)
  
  return decode_repr(raw)
