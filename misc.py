from sys import stdin

LINE_BREAK = "\n"

def read_to_eof() -> str:
  return "".join(l for l in stdin)

def is_int(string: str) -> bool:
  try:
    int(string)
    return True
  except ValueError:
    return False

def is_float_strict(string: str) -> bool:
  try:
    float(string)
    return not is_int(string)
  except ValueError:
    return False