from sys import stdout, stderr, exit, argv, exc_info

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
    stderr.write(f"{e.name}: {e}")
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

  except Exception as e:
    ex_type, ex_value, ex_traceback = exc_info()

    stderr.write(f"python@{ex_type.__name__}: {e}\n")
    stderr.flush()
    stdout.write(f"err@120")
    stdout.flush()
    exit(120)