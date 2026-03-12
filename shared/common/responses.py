from typing import Any


def success_response(data: Any, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    response: dict[str, Any] = {"data": data}
    if meta:
        response["meta"] = meta
    return response


def error_response(code: str, message: str, details: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"code": code, "message": message}
    if details:
        payload["details"] = details
    return {"error": payload}
