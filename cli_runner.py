from typing import Callable
from exceptions import EelExcBaseException, EelExcNotAnEelRepr, EelExcCommandNotFound
from type_def import decode_literal_or_repr, EelTypeBase, EelTypeString
from sys import stderr, argv, stdout
from misc import read_to_eof
from stdlib import BASIC_INTERFACE
from traceback import format_exc

PIPE_IN_HOLDER = "@"

def exec_basic_interface(interface_name: str, *args: str):
  try:
    if interface_name not in BASIC_INTERFACE:
      raise EelExcCommandNotFound(f"{interface_name} is not a valid command")

    lst_args = list(args)
    results_arg: list[EelTypeBase] = []
    interface = BASIC_INTERFACE[interface_name]

    for i, arg in enumerate(args):
      if arg and (arg[:2] == (PIPE_IN_HOLDER * 2)):
        lst_args[i] = arg[1:]
      
      elif arg == PIPE_IN_HOLDER:
        lst_args[i] = read_to_eof()

      try:
        results_arg.append(decode_literal_or_repr(arg))
      except EelExcNotAnEelRepr:
        results_arg.append(EelTypeString(arg))

    result: EelTypeBase = interface(*results_arg)
    stdout.write(result.eel_encode_repr())
    stdout.flush()
    exit(0)

  except EelExcBaseException as e:
    stderr.write(f"[EEL]{e.name}: {e}\n")
    stderr.write(format_exc())
    stderr.flush()
    exit(e.exit_code)

  except Exception as e:
    stderr.write(format_exc())
    stderr.flush()
    exit(126)

  except KeyboardInterrupt:
    exit(125)

if __name__ == "__main__":
  exec_basic_interface(argv[1], *argv[2:])