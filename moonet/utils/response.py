from typing import Any


def build_response(success: bool, body: Any = None) -> dict:
  """Build a standardized response dictionary.
  Returns `{"ok": success, "data": body}` if success is True,
  otherwise returns `{"ok": success, "error": body}`.
  """
  response: dict[str, Any] = {"ok": success}
  if body is not None:
    key = "data" if success else "error"
    response[key] = body
  return response
