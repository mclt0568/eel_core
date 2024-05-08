from inspect import signature
from inspect import _ParameterKind
from typing import get_args, get_origin
from types import UnionType

def func(x: int, y: int | str, /, *, z: str = "1") -> int:
  return 1

def get_types(func) -> dict[str, tuple[type, ...]]:
  result = {}
  for t in signature(func).parameters.values():
    if get_origin(t.annotation) is UnionType:
      result[t.name] = get_args(t.annotation)
      continue

    result[t.name] = (t.annotation, )

  return result

positional = map(lambda x: x.name, filter(
                     lambda param: param.kind == _ParameterKind.POSITIONAL_ONLY, 
                     signature(func).parameters.values()))

print(list(positional))