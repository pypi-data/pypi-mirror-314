from typing import Any

from .types import HeadersType


def compose_response(headers: HeadersType, body: str) -> str:
    formatted_headers = "\n".join([f"{k}: {v}" for k, v in headers.items()])
    return f"{formatted_headers}\n\n{body}"
