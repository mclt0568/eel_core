__all__ = [
  "EelExcSysTypeError",
  "EelExcInvalidOperation",
  "EelExcNotAnEelRepr",
  "EelExcTypeError",
  "EelExcCommandNotFound"
]


class EelExcBaseException(Exception):
  def __init__(self, message: str, name: str, exit_code: int = 1) -> None:
    self.name = name
    self.exit_code = exit_code
    super().__init__(message)

# System Exception

class EelExcSystemException(EelExcBaseException):
  def __init__(self, message: str | None = None, name: str | None = None):
    if name is None:
      name = ""
    else:
      name = f"<{name}>"

    if message is None:
      message = "Unknown error has occurred"

    super().__init__(message, f"InternalError{name}", 120)

class EelExcSysTypeError(EelExcSystemException):
  def __init__(self, message: str | None = None):
    super().__init__(message, "TypeError")

# Generic Exception

class EelWhenEvaluating(EelExcBaseException):
  def __init__(self, message: str, exit_code: int):
    super().__init__(message, "  when evaluating", exit_code)

class EelExcCommandNotFound(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "CommandNotFound", 127)

class EelExcFileError(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "FileError", 1)

class EelExcArgumentError(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "ArgumentError", 2)

class EelExcInvalidOperation(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "InvalidOperationError", 3)

class EelExcNotAnEelRepr(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "NotAnEelRepr", 4)

class EelExcTypeError(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "TypeError", 5)