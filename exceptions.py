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

    super().__init__(message, f"InternalError{name}")

class EelExcSysTypeError(EelExcSystemException):
  def __init__(self, message: str | None = None):
    super().__init__(message, "TypeError")

# Generic Exception

class EelExcCommandNotFound(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "CommandNotFound", 127)

class EelExcInvalidOperation(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "InvalidOperationError")

class EelExcNotAnEelRepr(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "NotAnEelRepr")

class EelExcTypeError(EelExcBaseException):
  def __init__(self, message: str):
    super().__init__(message, "TypeError")