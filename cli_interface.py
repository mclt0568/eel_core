from __future__ import annotations

from typing import get_args, get_origin, Callable, Iterable
from types import UnionType
from inspect import signature, _ParameterKind

from type_def import EelTypeBase, EelTypeString, decode_literal_or_repr
from exceptions import EelExcNotAnEelRepr, EelExcTypeError
from misc import read_to_eof


PIPE_IN_HOLDER = "@"

BASIC_INTERFACES: dict[str, Callable] = {}


def convert_arg(raw: str, pipe_in: bool = True) -> EelTypeBase:
  if pipe_in and raw == PIPE_IN_HOLDER:
    raw = read_to_eof()

  elif pipe_in and raw[:2] == (PIPE_IN_HOLDER * 2):
    raw = raw[1:]

  try:
    return decode_literal_or_repr(raw)
  
  except EelExcNotAnEelRepr:
    return EelTypeString(raw)


def get_types(func) -> dict[str, tuple[type, ...]]:
  result = {}
  for t in signature(func).parameters.values():
    if get_origin(t.annotation) is UnionType:
      result[t.name] = get_args(t.annotation)
      continue

    result[t.name] = (t.annotation, )

  return result


def get_arg_names_by_kind(func: Callable, kinds: Iterable[_ParameterKind]) -> list[str]:
  return list(map(lambda x: x.name, filter(
              lambda param: param.kind in kinds, 
              signature(func).parameters.values())))


def format_list_types(list_types: list[str]) -> str:
  if len(list_types) > 1:
    result = ", ".join(list_types[:-1]) + " or " + list_types[-1]
  else:
    result = list_types[0]
  
  return result


def basic_interface(name: str, pipe_in: bool = True):
  def runner_conv(func: Callable):
    arg_types = get_types(func)
    kind_positionals = (_ParameterKind.POSITIONAL_ONLY, _ParameterKind.POSITIONAL_OR_KEYWORD)
    positional = get_arg_names_by_kind(func, kind_positionals)

    def runner(*args: str):
      converted_args: list[EelTypeBase] = []
      
      for i, arg in enumerate(args):
        arg_type = arg_types[positional[i]]
        converted_arg = convert_arg(arg, pipe_in)
        
        if not issubclass(type(converted_arg), arg_type):
          get_name = lambda t: (t.NAME if hasattr(t, "NAME") else t.__name__)
          expected = format_list_types([get_name(t) for t in arg_type])
          got = get_name(type(converted_arg))
          raise EelExcTypeError(
            f"{name} on arg#{i}: expected {expected}, got {got}")
        
        converted_args.append(converted_arg)

      return func(*converted_args)

    BASIC_INTERFACES[name] = runner

    return runner
  return runner_conv