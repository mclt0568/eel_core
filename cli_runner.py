from sys import stdout, stderr, exit, argv

from traceback import format_exc

from exceptions import EelExcBaseException, EelExcSystemException
from exceptions import EelExcCommandNotFound, EelExcArgumentError


def try_import_command(name: str):
  try:
    return getattr(__import__(f"stdlib.{name}"), name)

  except ModuleNotFoundError:
    raise EelExcCommandNotFound(f"{name} is not defined in Eel")


def main():
  if len(argv) == 1:
    raise EelExcArgumentError(f"Command name not provided")
  
  command_name = argv[1]
  command_args = argv[2:]

  command = try_import_command(command_name)
  
  result = getattr(command, command_name)(*command_args)
  stdout.write(result.eel_encode_repr())
  stdout.flush()

if __name__ == "__main__":
  try:
    main()
    exit(0)

  except EelExcSystemException as e:
    stderr.write(format_exc())
    stderr.write("\n")
    stderr.flush()
    stdout.write(f"err@{e.exit_code}")
    stdout.flush()
    exit(e.exit_code)

  except EelExcBaseException as e:
    stderr.write(f"{e.name}: {e}\n")
    stderr.flush()
    stdout.write(f"err@{e.exit_code}")
    stdout.flush()
    exit(e.exit_code)